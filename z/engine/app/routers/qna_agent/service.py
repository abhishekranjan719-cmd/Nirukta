"""
QnA Agent Service - LangGraph ReAct Agent Implementation

This service implements a production-ready ReAct (Reasoning-Action-Observation) agent
using LangGraph. The agent autonomously:
1. Reasons about the question
2. Decides which tools to use (if any)
3. Observes tool outputs
4. Synthesizes the final answer

References:
- LangGraph Documentation: https://langchain-ai.github.io/langgraph/
- ReAct Pattern: https://langchain-ai.github.io/langgraph/how-tos/react-agent-from-scratch/
"""

from datetime import datetime

from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langfuse.langchain import CallbackHandler
from loguru import logger

from app.config import settings
from app.routers.qna_agent.graph import create_agent_graph
from app.routers.qna_agent.memory import get_memory_manager
from app.routers.qna_agent.state import AgentState
from app.schemas.common import TrackingMetadata
from app.utilities.prompt_loader import get_prompt_loader


class AgentService:
    """
    LangGraph-based ReAct agent service for QnA processing.

    Architecture:
    - Uses LangGraph for stateful agent workflow
    - ReAct pattern: Reasoning → Action → Observation loop
    - Tools are autonomously selected by the LLM
    - Langfuse observability integration
    """

    def __init__(self):
        """Initialize agent service with lazy initialization."""
        self.agent_graph = None
        self._model = None

        # Load formatter prompt
        prompt_loader = get_prompt_loader()
        self.formatter_prompt = prompt_loader.load_formatter_prompt()

        # Get memory manager
        self.memory_manager = get_memory_manager()

        logger.info(
            "[AgentService] Initialized | "
            "Mode: LangGraph ReAct Agent | "
            f"Formatter prompt loaded | "
            f"Memory enabled: {self.memory_manager.is_enabled}"
        )

    def _get_chat_model(self) -> ChatOpenAI:
        """
        Get or create ChatOpenAI model configured for LiteLLM proxy.

        Returns:
            ChatOpenAI instance configured to use LiteLLM proxy
        """
        if self._model is None:
            litellm_base_url = settings.litellm.litellm_base_url
            litellm_master_key = settings.litellm.litellm_master_key
            model_name = settings.litellm.litellm_chat_model

            self._model = ChatOpenAI(
                model=model_name,
                base_url=litellm_base_url,
                api_key=litellm_master_key,  # Use master key from settings
                temperature=settings.engine_llm_temperature,
                streaming=settings.engine_llm_streaming,
            )

            logger.info(
                f"[AgentService] ChatOpenAI initialized | "
                f"model={model_name} | base_url={litellm_base_url} | "
                f"temperature={settings.engine_llm_temperature} | "
                f"streaming={settings.engine_llm_streaming}"
            )

        return self._model

    async def _get_agent_graph(self):
        """
        Get or create the LangGraph agent workflow with checkpointer.

        Returns:
            Compiled StateGraph ready for execution
        """
        if self.agent_graph is None:
            model = self._get_chat_model()

            # Get checkpointer from memory manager (if enabled)
            checkpointer = self.memory_manager.get_checkpointer()

            self.agent_graph = create_agent_graph(model, self.formatter_prompt, checkpointer=checkpointer)

            if checkpointer:
                logger.info("[AgentService] Agent graph compiled with PostgreSQL checkpointer")
            else:
                logger.info("[AgentService] Agent graph compiled without memory (disabled)")

        return self.agent_graph

    async def process_question(
        self,
        message: str,
        context: dict | None = None,
        tracking: TrackingMetadata | None = None,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> tuple[str, dict]:
        """
        Process a question using the LangGraph ReAct agent.

        The agent will:
        1. Analyze the question
        2. Autonomously decide which tools to use (if any)
        3. Iterate through reasoning-action-observation cycles
        4. Provide a final answer

        Args:
            message: The question to process
            context: Optional context (currently unused but available for future)
            tracking: Tracking metadata for observability
            conversation_history: Previous messages in OpenAI format [{"role": "user/assistant", "content": "..."}]

        Returns:
            Tuple of (response_text, metadata)
        """
        start_time = datetime.now()

        logger.info(
            f"[AgentService] Processing started | "
            f"message_length={len(message)} | "
            f"conversation_history_length={len(conversation_history) if conversation_history else 0} | "
            f"chat_id={tracking.chat_id if tracking else 'none'}"
        )

        # Step 1: Validate input
        if not message or len(message.strip()) == 0:
            raise ValueError("Message cannot be empty")

        # Step 2: Convert conversation_history to LangChain messages
        history_messages = []
        if conversation_history:
            for msg in conversation_history:
                role = msg.get("role")
                content = msg.get("content", "")
                if role == "user":
                    history_messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    history_messages.append(AIMessage(content=content))

        # Step 3: Add current message and trim if enabled
        all_messages = history_messages + [HumanMessage(content=message)]

        # Trim messages to manage context window
        trimmed_messages = self.memory_manager.trim_messages_if_enabled(all_messages)

        logger.debug(
            f"[AgentService] Messages prepared | "
            f"Original: {len(all_messages)} | "
            f"After trim: {len(trimmed_messages)}"
        )

        initial_state: AgentState = {
            "messages": trimmed_messages,
            "question": message,
            "conversation_history": conversation_history or [],
            "summary": None,
            "final_response": None,
        }

        # Step 4: Prepare config with memory thread_id and Langfuse tracing
        langfuse_handler = CallbackHandler()

        # Get memory config with thread_id (maps to conversation_id)
        memory_config = self.memory_manager.get_config(
            conversation_id=tracking.conversation_id if tracking else None,
            user_id=tracking.user_id if tracking else None,
            chat_id=tracking.chat_id if tracking else None,
        )

        # Merge with Langfuse config
        config = {
            **memory_config,
            "callbacks": [langfuse_handler],
            "metadata": {
                "langfuse_user_id": tracking.user_id if tracking else "anonymous",
                "langfuse_session_id": tracking.conversation_id if tracking else "default",
                "langfuse_tags": ["qna_agent", "react", "langgraph"],
                "usecase": "qna",
                "question": message[:100],  # Truncate for metadata
            },
        }

        logger.debug(
            f"[AgentService] Config prepared | "
            f"langfuse_enabled=True | "
            f"thread_id={memory_config.get('configurable', {}).get('thread_id', 'none')}"
        )

        # Step 5: Get agent graph
        agent_graph = await self._get_agent_graph()

        # Step 6: Invoke agent
        try:
            logger.info("[AgentService] Invoking agent graph...")

            result = await agent_graph.ainvoke(initial_state, config=config)

            logger.info("[AgentService] Agent invocation complete")

        except Exception as e:
            logger.error(f"[AgentService] Agent invocation failed | error={e!s}", exc_info=True)
            raise

        # Step 7: Extract response
        messages = result.get("messages", [])
        if not messages:
            response_text = "I apologize, but I couldn't generate a response."
        else:
            last_message = messages[-1]
            response_text = getattr(last_message, "content", "No response generated")

        # Step 8: Build metadata
        processing_time = (datetime.now() - start_time).total_seconds()

        metadata = {
            "processed_at": datetime.now().isoformat(),
            "processing_time_seconds": processing_time,
            "processing_type": "langgraph_agent",
            "model": settings.litellm.litellm_chat_model,
            "temperature": settings.engine_llm_temperature,
            "streaming": settings.engine_llm_streaming,
            "original_message_length": len(message),
            "response_length": len(response_text),
            "orchestration": {
                "mode": "agent",
                "type": "react",
                "framework": "langgraph",
                "message_count": len(messages),
                "capabilities": [
                    "autonomous_reasoning",
                    "tool_selection",
                    "iterative_refinement",
                    "conversation_summarization",
                ],
            },
        }

        # Langfuse traces are automatically handled by the LangchainCallbackHandler
        # Traces are available in Langfuse UI after execution
        logger.debug("[AgentService] Langfuse traces handled by LangchainCallbackHandler")

        logger.info(
            f"[AgentService] Processing complete | "
            f"processing_time={processing_time:.2f}s | "
            f"response_length={len(response_text)} | "
            f"message_count={len(messages)}"
        )

        return response_text, metadata


# Singleton instance
_agent_service: AgentService | None = None


def get_agent_service() -> AgentService:
    """
    Get singleton agent service instance.

    Returns:
        AgentService instance
    """
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service
