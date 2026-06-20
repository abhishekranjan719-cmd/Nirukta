"""
Agent Graph - LangGraph ReAct Agent Implementation

This module implements the core ReAct (Reasoning-Action-Observation) pattern
using LangGraph. The agent autonomously decides which tools to use based on
the question and iteratively reasons through the problem.

Architecture:
    START → agent (reasoning) → conditional_router
                                      ↓
                                      ├─ tool_calls? → tools → agent
                                      ├─ >10 messages? → summarize → agent
                                      └─ otherwise → END
"""

from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode
from loguru import logger

from app.config import settings
from app.routers.qna_agent.state import AgentState
from app.routers.qna_agent.tools import tools


def create_agent_graph(model, formatter_prompt: str, checkpointer=None):
    """
    Create the LangGraph ReAct agent workflow.

    Args:
        model: The LLM model (ChatOpenAI) with tools bound
        formatter_prompt: System prompt for formatting rich content responses
        checkpointer: Optional AsyncPostgresSaver for conversation memory

    Returns:
        Compiled StateGraph ready for execution
    """
    # Bind tools to model
    model_with_tools = model.bind_tools(tools)

    # Create async wrapper for invoke_agent_model with bound model and formatter_prompt
    async def agent_node(state: AgentState, config: RunnableConfig) -> AgentState:
        return await invoke_agent_model(state, config, model_with_tools, formatter_prompt)

    # Create workflow
    workflow = StateGraph(AgentState)

    # Define nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))
    workflow.add_node("summarize", summarize_conversation)

    # Define edges
    workflow.set_entry_point("agent")

    # Conditional routing from agent
    workflow.add_conditional_edges(
        "agent",
        route_next_action,
        {
            "tools": "tools",
            "summarize": "summarize",
            "end": END,
        },
    )

    # After tools, go back to agent for next reasoning step
    workflow.add_edge("tools", "agent")

    # After summarize, go back to agent with reduced context
    workflow.add_edge("summarize", "agent")

    # Compile the graph with checkpointer (if provided)
    graph = workflow.compile(checkpointer=checkpointer)

    logger.info(
        "[Agent Graph] Compiled successfully | "
        f"max_messages_before_summary={settings.agent_max_messages_before_summary} | "
        f"memory_enabled={checkpointer is not None}"
    )
    return graph


async def invoke_agent_model(state: AgentState, config: RunnableConfig, model, formatter_prompt: str) -> AgentState:
    """
    Agent reasoning node - the core LLM invocation.

    This node:
    1. Constructs the system prompt with formatter instructions
    2. Adds conversation summary if available
    3. Invokes the LLM with tools
    4. Returns updated state with LLM response

    The LLM autonomously decides:
    - Which tool to call (if any)
    - What arguments to pass
    - When to provide final answer

    Args:
        state: Current agent state
        config: Runtime configuration
        model: LLM model with tools bound
        formatter_prompt: System prompt for rich content formatting

    Returns:
        Updated state with LLM response
    """
    try:
        logger.debug("[invoke_agent_model] Invoking LLM | question={}", state.get("question", "")[:50])

        # Build system prompt with formatter instructions and tool guidance
        system_prompt = f"""{formatter_prompt}

## Agent Capabilities

You are an AI assistant with access to the following tools:
- **web_search**: Search the web for current information
- **calculate**: Perform mathematical calculations
- **format_response**: Format responses with rich content (tables, code, etc.)

## Instructions

1. Think step-by-step about what information you need
2. Use available tools when necessary to provide accurate answers
3. Provide clear, well-formatted responses using the rich content features described above
4. If you don't know something, say so honestly
5. For multi-turn conversations, maintain context from previous messages"""

        # Add summary if available (for long conversations)
        summary = state.get("summary")
        if summary:
            system_prompt += f"\n\n## Conversation Summary (from earlier messages)\n{summary}"

        # Construct messages starting with system prompt
        messages = [SystemMessage(content=system_prompt)]

        # Add conversation messages (these already include conversation history from service)
        if state.get("messages"):
            messages.extend(state["messages"])
        else:
            # First message - add the question
            question = state.get("question", "")
            if question:
                messages.append(HumanMessage(content=question))

        # Invoke model
        response = await model.ainvoke(messages, config=config)

        logger.info("[invoke_agent_model] LLM invoked | has_tool_calls={}", bool(response.tool_calls))

        return {"messages": [response]}

    except Exception as e:
        logger.error("[invoke_agent_model] ERROR | error={}", str(e), exc_info=True)
        # Return error message
        from langchain_core.messages import AIMessage

        error_msg = AIMessage(content=f"I encountered an error: {e!s}")
        return {"messages": [error_msg]}


def route_next_action(state: AgentState) -> Literal["tools", "summarize", "end"]:
    """
    Conditional router that decides the next step in the agent workflow.

    Routing Logic:
    1. If LLM made tool calls → go to "tools" node
    2. If conversation is too long (>10 messages) → go to "summarize" node
    3. Otherwise → END (LLM provided final answer)

    Args:
        state: Current agent state

    Returns:
        Next node name: "tools", "summarize", or "end"
    """
    messages = state.get("messages", [])

    if not messages:
        logger.debug("[route_next_action] No messages, ending")
        return "end"

    last_message = messages[-1]

    # Check if LLM wants to use tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        logger.info("[route_next_action] Tool calls detected | count={}", len(last_message.tool_calls))
        return "tools"

    # Check if conversation needs summarization
    if len(messages) > settings.agent_max_messages_before_summary:
        logger.info(
            "[route_next_action] Conversation too long | "
            f"messages={len(messages)}, max={settings.agent_max_messages_before_summary}, "
            "triggering summarization"
        )
        return "summarize"

    # No tools needed and conversation is short - we're done
    logger.debug("[route_next_action] Ending conversation | messages={}", len(messages))
    return "end"


async def summarize_conversation(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Summarize long conversations to manage context window.

    This node is triggered when the conversation exceeds agent_max_messages_before_summary.
    It:
    1. Creates or extends the conversation summary
    2. Keeps only the last agent_messages_to_keep_after_summary messages
    3. Reduces context window significantly

    Args:
        state: Current agent state
        config: Runtime configuration

    Returns:
        Updated state with summary and pruned messages
    """
    try:
        messages = state.get("messages", [])
        existing_summary = state.get("summary", "")

        logger.info("[summarize_conversation] Summarizing conversation | messages={}", len(messages))

        # Create summary prompt
        summary_prompt = "Provide a concise summary of the conversation so far, focusing on key points and decisions."

        if existing_summary:
            summary_prompt = (
                f"Extend this summary with new information:\n\n{existing_summary}\n\nNew messages to summarize:"
            )

        # For now, create a simple summary
        # In production, use an LLM to generate the summary
        summary_content = f"[Summary of {len(messages)} messages]"

        if messages:
            # Get content from recent messages
            summary_msg_count = settings.agent_summary_message_count
            summary_max_length = settings.agent_summary_max_length

            recent_content = " ".join(
                [getattr(msg, "content", "") for msg in messages[-summary_msg_count:] if hasattr(msg, "content")]
            )
            summary_content = (
                f"{existing_summary}\n\n{recent_content[:summary_max_length]}..."
                if existing_summary
                else f"{recent_content[:summary_max_length]}..."
            )

        # Keep only recent messages
        messages_to_keep = messages[-settings.agent_messages_to_keep_after_summary :]

        logger.info("[summarize_conversation] Summary created | kept_messages={}", len(messages_to_keep))

        return {
            "summary": summary_content,
            "messages": messages_to_keep,
        }

    except Exception as e:
        logger.error("[summarize_conversation] ERROR | error={}", str(e), exc_info=True)
        # Return state unchanged on error
        return {}
