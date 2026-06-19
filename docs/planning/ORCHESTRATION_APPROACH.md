# Agentic Orchestration Copilot - Implementation Approach

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Core Components](#core-components)
4. [Implementation Guide](#implementation-guide)
5. [Tool Integration](#tool-integration)
6. [State Management](#state-management)
7. [Testing Strategy](#testing-strategy)
8. [Offline Evaluation Framework](#offline-evaluation-framework)
9. [Best Practices](#best-practices)
10. [Common Pitfalls](#common-pitfalls)

---

## Executive Summary

This document provides a comprehensive guide for building an agentic orchestration system using the **Planner-Evaluator pattern**. The system intelligently answers complex questions by:

1. **Planning** - Breaking down user questions into actionable steps
2. **Executing** - Using specialized tools (NL2SQL, Doc QA, Python REPL, Function Calling)
3. **Evaluating** - Assessing completeness and re-planning if needed
4. **Iterating** - Refining the approach until the question is fully answered

### Key Design Principles
- **Simplicity First**: Start with core functionality, avoid premature optimization
- **Iterative Refinement**: Use feedback loops to improve responses
- **Human in the Loop**: Allow interrupts for clarification
- **Observability**: Track execution for debugging and evaluation

---

## Architecture Overview

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER QUESTION                                 │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│              MEMORY RETRIEVAL (Optional)                         │
│  - Fetch relevant conversation history                           │
│  - Augment question with user context                            │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│                     PLANNER NODE                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Responsibilities:                                         │   │
│  │ 1. Analyze user question and conversation history        │   │
│  │ 2. Create an overall plan with steps                     │   │
│  │ 3. Select the most appropriate tool                      │   │
│  │ 4. Formulate a specific question for that tool           │   │
│  │ 5. Provide reasoning for the selection                   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  Output: {                                                        │
│    overall_plan: "Step 1: ... Step 2: ...",                      │
│    next_tool: "sql_tool",                                        │
│    next_question: "Get sales data for Q1 2024",                  │
│    reasoning: "Need data before analysis"                        │
│  }                                                                │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│                   ROUTER FROM PLANNER                            │
│  Routes to appropriate tool based on next_tool field             │
└─────────────────┬───────────────────────────────────────────────┘
                  │
         ┌────────┼────────┬───────────┬──────────┐
         │        │        │           │          │
         ↓        ↓        ↓           ↓          ↓
    ┌────────┐ ┌──────┐ ┌────────┐ ┌──────┐  ┌──────┐
    │  SQL   │ │ Doc  │ │Analysis│ │Python│  │Human │
    │  Tool  │ │  QA  │ │  Tool  │ │ REPL │  │ HIL  │
    └────┬───┘ └───┬──┘ └───┬────┘ └───┬──┘  └───┬──┘
         │         │        │           │         │
         └─────────┴────────┴───────────┴─────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│                    EVALUATOR NODE                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Responsibilities:                                         │   │
│  │ 1. Review all tool execution outcomes                    │   │
│  │ 2. Compare results against original question             │   │
│  │ 3. Determine if question is fully answered               │   │
│  │ 4. Identify missing information if incomplete            │   │
│  │ 5. Decide: continue planning OR generate final answer    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  Output: {                                                        │
│    decision: "complete" | "incomplete",                          │
│    reasoning: "All required data gathered and analyzed",         │
│    missing_information: "" | "Need trend analysis"               │
│  }                                                                │
└─────────────────┬───────────────────────────────────────────────┘
                  │
         ┌────────┴────────┐
         │                 │
         ↓                 ↓
  [INCOMPLETE]      [COMPLETE]
  Loop back to      Generate
  Planner Node      Final Answer
         │                 │
         │                 ↓
         │          ┌──────────────┐
         │          │ FINAL ANSWER │
         │          │    TOOL      │
         │          └──────┬───────┘
         │                 │
         └─────────────────┴──────────→ Response to User
```

### Iteration Control Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ Iteration 1: Planner → SQL Tool → Evaluator (Incomplete)        │
│              "Need to analyze the data"                          │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│ Iteration 2: Planner → Python Tool → Evaluator (Incomplete)     │
│              "Need to create visualization"                      │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│ Iteration 3: Planner → Python Tool → Evaluator (Complete)       │
│              "All requirements met"                              │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│ Final Answer Generation → Response to User                       │
└─────────────────────────────────────────────────────────────────┘

Max Iterations: 5 (configurable)
```

---

## Core Components

### 1. State Definition

The state is the **single source of truth** that flows through all nodes in the graph.

```python
from typing import Annotated, List, Dict, Any, Optional
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """State that flows through the orchestration graph"""

    # ========== CORE STATE ==========
    messages: Annotated[List[BaseMessage], add_messages]
    input: str                    # Original user question
    question: str                 # Current question being processed

    # ========== PLANNER STATE ==========
    overall_plan: str             # The strategic plan created by planner
    plan_steps: List[Dict[str, Any]]  # List of planned steps with status
    current_step: int             # Current step number

    # ========== TOOL MANAGEMENT ==========
    next_tool: Optional[str]      # Which tool to execute next
    next_question: str            # Specific question for the tool
    planner_reasoning: str        # Why this tool was selected

    # ========== TOOL EXECUTION TRACKING ==========
    tool_outcome: List[str]       # Human-readable outcomes
    tool_execution_history: List[Dict[str, Any]]  # Detailed execution log
    tool_results: List[Dict[str, Any]]  # Structured results from tools

    # ========== EVALUATOR STATE ==========
    evaluator_decision: Optional[str]  # "complete" or "incomplete"
    evaluator_reasoning: str      # Reasoning for the decision
    missing_information: str      # What's still needed (if incomplete)

    # ========== ITERATION CONTROL ==========
    iteration_count: int          # Number of planner-evaluator cycles
    max_iterations: int           # Maximum allowed iterations (default: 5)

    # ========== INTERMEDIATE DATA ==========
    intermediate_data: Dict[str, Any]  # Data passed between tools
    datasets_used: Optional[List[str]]  # List of tools used

    # ========== CONTEXT & METADATA ==========
    context: Dict[str, Any]       # Additional context
    conversation_history: List[Dict[str, Any]]  # Past Q&A pairs
    request_id: str               # Unique request identifier
    user_id: str                  # User identifier

    # ========== FINAL OUTPUT ==========
    final_answer: Optional[str]   # Final response to user
    response: str                 # Formatted response

    # ========== CONTROL FLAGS ==========
    requires_human_input: bool    # Whether human interrupt is needed
    execution_metadata: Dict[str, Any]  # Performance tracking
```

**Key Design Decisions:**

1. **Use `Annotated[List[BaseMessage], add_messages]`** for messages field
   - This enables automatic message deduplication
   - LangGraph handles message appending correctly

2. **Separate tracking fields** for different purposes:
   - `tool_outcome`: Simple strings for display
   - `tool_execution_history`: Detailed logs with timestamps
   - `tool_results`: Structured data for downstream processing

3. **Iteration control** prevents infinite loops:
   - Default max_iterations: 5
   - Force final answer at max iterations

---

### 2. Planner Node

The planner is responsible for **strategic thinking** and **tool selection**.

```python
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

class PlannerOutput(BaseModel):
    """Structured output from the planner"""
    overall_plan: str = Field(
        description="Complete strategic plan with numbered steps"
    )
    next_tool: str = Field(
        description="Name of the tool to execute next (e.g., 'sql_tool', 'python_tool')"
    )
    next_question: str = Field(
        description="Specific question to ask the selected tool"
    )
    reasoning: str = Field(
        description="Justification for why this tool and question were chosen"
    )

def create_planner_node(llm, available_tools: List[str], tool_descriptions: Dict[str, str]):
    """
    Create the planner node with structured output

    Args:
        llm: Language model (e.g., GPT-4)
        available_tools: List of available tool names
        tool_descriptions: Dictionary mapping tool names to descriptions
    """

    # Format tool descriptions for the prompt
    tools_description = "\n".join([
        f"- **{tool}**: {tool_descriptions[tool]}"
        for tool in available_tools
    ])

    planner_prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are an expert planning agent for a business intelligence copilot.

Available Tools:
{tools_description}

Your job is to:
1. Analyze the user's question and conversation history
2. Create a strategic plan to answer the question completely
3. Select the most appropriate tool for the NEXT step
4. Formulate a specific question for that tool

Guidelines:
- Start with data retrieval (sql_tool, analysis_tool) before analysis
- Use python_tool for analysis, visualization, or ML after data is retrieved
- Use doc_qa_tool for document-based questions
- Use metadata_tool when user asks "what data do you have?"
- Break complex questions into simple, sequential steps
- Consider what data/context is already available from previous tool executions

Important:
- Only select ONE tool at a time
- Formulate a clear, specific question for that tool
- Explain your reasoning clearly"""),

        ("human", """Original Question: {question}

Conversation History:
{conversation_history}

Previous Tool Executions:
{tool_execution_history}

Current Iteration: {iteration_count} / {max_iterations}

Based on the above, create a plan and select the next tool to use.""")
    ])

    # Bind structured output to LLM
    structured_llm = llm.with_structured_output(PlannerOutput)
    planner_chain = planner_prompt | structured_llm

    def planner_node(state: AgentState) -> Dict[str, Any]:
        """Execute planner logic"""

        # Format conversation history
        conv_history = "\n".join([
            f"Q: {item['question']}\nA: {item['final_answer']}"
            for item in state.get("conversation_history", [])
        ])

        # Format tool execution history
        tool_history = "\n".join([
            f"- {item['tool']}: {item['outcome']}"
            for item in state.get("tool_execution_history", [])
        ])

        # Invoke planner
        result = planner_chain.invoke({
            "question": state["input"],
            "conversation_history": conv_history or "No previous conversation",
            "tool_execution_history": tool_history or "No tools executed yet",
            "iteration_count": state.get("iteration_count", 0),
            "max_iterations": state.get("max_iterations", 5)
        })

        # Update state
        return {
            "overall_plan": result.overall_plan,
            "next_tool": result.next_tool,
            "next_question": result.next_question,
            "planner_reasoning": result.reasoning,
            "current_step": state.get("current_step", 0) + 1
        }

    return planner_node
```

**Key Implementation Notes:**

1. **Use structured output** (`with_structured_output()`) for reliable parsing
2. **Provide rich context** to the planner:
   - Original question
   - Conversation history
   - Previous tool executions
   - Current iteration count
3. **Clear guidelines** on when to use each tool
4. **One tool at a time** - avoid confusion

---

### 3. Evaluator Node

The evaluator determines if the question has been fully answered.

```python
class EvaluatorOutput(BaseModel):
    """Structured output from the evaluator"""
    decision: str = Field(
        description="Either 'complete' or 'incomplete' - whether the question is fully answered"
    )
    reasoning: str = Field(
        description="Explanation of why the question is complete or incomplete"
    )
    missing_information: str = Field(
        description="What information is still needed (empty string if complete)"
    )

def create_evaluator_node(llm):
    """Create the evaluator node with structured output"""

    evaluator_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert evaluation agent for a business intelligence copilot.

Your job is to:
1. Review the original user question
2. Review all tool execution outcomes
3. Determine if the question has been FULLY answered
4. Identify any missing information

Decision Criteria for "complete":
- All parts of the question have been addressed
- Sufficient data has been retrieved and analyzed
- Visualizations have been created if requested
- The user would be satisfied with the current information

Decision Criteria for "incomplete":
- Some parts of the question remain unanswered
- Data was retrieved but not analyzed
- Analysis was done but visualization is missing
- User requested multiple things and only some were completed

Be thorough but reasonable - don't aim for perfection, aim for answering the question."""),

        ("human", """Original Question: {question}

Overall Plan: {overall_plan}

Tool Execution History:
{tool_execution_history}

Current Iteration: {iteration_count} / {max_iterations}

Based on the above, determine if the question is fully answered.""")
    ])

    structured_llm = llm.with_structured_output(EvaluatorOutput)
    evaluator_chain = evaluator_prompt | structured_llm

    def evaluator_node(state: AgentState) -> Dict[str, Any]:
        """Execute evaluator logic"""

        # Format tool execution history
        tool_history = "\n".join([
            f"- Tool: {item['tool']}\n  Question: {item['question']}\n  Outcome: {item['outcome']}"
            for item in state.get("tool_execution_history", [])
        ])

        # Force completion at max iterations
        if state.get("iteration_count", 0) >= state.get("max_iterations", 5):
            return {
                "evaluator_decision": "complete",
                "evaluator_reasoning": "Max iterations reached - generating final answer with available information",
                "missing_information": ""
            }

        # Invoke evaluator
        result = evaluator_chain.invoke({
            "question": state["input"],
            "overall_plan": state.get("overall_plan", "No plan yet"),
            "tool_execution_history": tool_history or "No tools executed yet",
            "iteration_count": state.get("iteration_count", 0),
            "max_iterations": state.get("max_iterations", 5)
        })

        return {
            "evaluator_decision": result.decision,
            "evaluator_reasoning": result.reasoning,
            "missing_information": result.missing_information
        }

    return evaluator_node
```

**Key Implementation Notes:**

1. **Force completion at max iterations** - prevent infinite loops
2. **Clear decision criteria** in the prompt
3. **Provide full context** - original question, plan, and execution history
4. **Balance thoroughness with reasonableness** - don't over-optimize

---

### 4. Tool Nodes

Each tool has a dedicated node wrapper.

```python
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
import httpx

# ========== SQL Tool ==========
@tool
async def sql_tool(query: str, config: RunnableConfig) -> str:
    """
    Execute SQL queries against the database.

    Args:
        query: Natural language question to convert to SQL

    Returns:
        SQL results formatted as JSON
    """
    try:
        # Get use case from config
        use_case = config.get("configurable", {}).get("use_case", "default")

        # Call SQL service (NL2SQL)
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                f"http://sql-service/query?use_case={use_case}",
                json={"question": query}
            )

            if response.status_code >= 400:
                return f"Error executing SQL: {response.text}"

            result = response.json()
            return json.dumps(result, indent=2)

    except Exception as e:
        return f"Error executing SQL: {str(e)}"


def create_sql_tool_node(sql_tool_func):
    """Wrap sql_tool in a node function"""

    async def sql_node(state: AgentState, config: RunnableConfig) -> Dict[str, Any]:
        """Execute SQL tool and update state"""

        # Get the question from planner
        question = state.get("next_question", state["input"])

        # Execute tool
        result = await sql_tool_func.ainvoke(
            {"query": question},
            config=config
        )

        # Parse result to extract data
        try:
            parsed_result = json.loads(result)
            sql_data = parsed_result.get("result", [])
        except:
            sql_data = result

        # Save dataset to file for downstream use
        dataset_name = f"sql_data_{state.get('iteration_count', 0)}"
        save_dataset(sql_data, dataset_name, config)

        # Update state
        return {
            "tool_outcome": state.get("tool_outcome", []) + [
                f"SQL Tool: Retrieved {len(sql_data)} rows of data"
            ],
            "tool_execution_history": state.get("tool_execution_history", []) + [{
                "tool": "sql_tool",
                "question": question,
                "outcome": f"Retrieved {len(sql_data)} rows",
                "timestamp": datetime.now().isoformat()
            }],
            "tool_results": state.get("tool_results", []) + [{
                "tool": "sql_tool",
                "result": parsed_result,
                "metadata": {"row_count": len(sql_data)}
            }],
            "intermediate_data": {
                **state.get("intermediate_data", {}),
                "sql_data": sql_data
            },
            "datasets_used": list(set(state.get("datasets_used", []) + ["sql_tool"]))
        }

    return sql_node


# ========== Document QA Tool ==========
@tool
async def doc_qa_tool(query: str, config: RunnableConfig) -> str:
    """
    Search document vector database for relevant information.

    Args:
        query: Question to search for

    Returns:
        Relevant document context
    """
    try:
        use_case = config.get("configurable", {}).get("use_case", "default")

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"http://doc-qa-service/search?use_case={use_case}",
                json={"question": query}
            )

            if response.status_code >= 400:
                return f"Error searching documents: {response.text}"

            result = response.json()
            return json.dumps(result, indent=2)

    except Exception as e:
        return f"Error searching documents: {str(e)}"


def create_doc_qa_node(doc_qa_tool_func):
    """Wrap doc_qa_tool in a node function"""

    async def doc_qa_node(state: AgentState, config: RunnableConfig) -> Dict[str, Any]:
        """Execute Document QA tool and update state"""

        question = state.get("next_question", state["input"])
        result = await doc_qa_tool_func.ainvoke({"query": question}, config=config)

        return {
            "tool_outcome": state.get("tool_outcome", []) + [
                f"Doc QA Tool: Found relevant documentation"
            ],
            "tool_execution_history": state.get("tool_execution_history", []) + [{
                "tool": "doc_qa_tool",
                "question": question,
                "outcome": "Retrieved relevant documents",
                "timestamp": datetime.now().isoformat()
            }],
            "tool_results": state.get("tool_results", []) + [{
                "tool": "doc_qa_tool",
                "result": result
            }],
            "datasets_used": list(set(state.get("datasets_used", []) + ["doc_qa_tool"]))
        }

    return doc_qa_node


# ========== Python REPL Tool ==========
from langchain_experimental.utilities import PythonREPL

repl = PythonREPL()

@tool
def python_repl_tool(code: str, config: RunnableConfig) -> str:
    """
    Execute Python code for analysis and visualization.

    Args:
        code: Python code to execute

    Returns:
        Execution output
    """
    try:
        # Load datasets from previous tools
        datasets = load_datasets_from_session(config)

        # Inject datasets into REPL
        repl.globals["datasets"] = datasets
        repl.globals["pd"] = pd
        repl.globals["plt"] = plt
        repl.globals["px"] = px

        # Execute code
        result = repl.run(code)
        return f"Successfully executed.\n\nOutput:\n{result}"

    except Exception as e:
        return f"Error executing Python code: {str(e)}"


def create_python_node(python_tool_func):
    """Wrap python_repl_tool in a node function"""

    async def python_node(state: AgentState, config: RunnableConfig) -> Dict[str, Any]:
        """Execute Python tool and update state"""

        # For Python tool, use a ReAct agent that can iteratively write code
        question = state.get("next_question", state["input"])

        # Create a Python agent with the REPL tool
        python_agent = create_react_agent(
            llm,
            tools=[python_tool_func],
            prompt=PYTHON_AGENT_PROMPT
        )

        # Execute agent
        result = await python_agent.ainvoke({
            "messages": [("user", question)]
        }, config=config)

        return {
            "tool_outcome": state.get("tool_outcome", []) + [
                f"Python Tool: Executed analysis and generated outputs"
            ],
            "tool_execution_history": state.get("tool_execution_history", []) + [{
                "tool": "python_tool",
                "question": question,
                "outcome": "Code executed successfully",
                "timestamp": datetime.now().isoformat()
            }],
            "datasets_used": list(set(state.get("datasets_used", []) + ["python_tool"]))
        }

    return python_node


# ========== Analysis Tool (Domain-Specific Functions) ==========
@tool
async def analysis_tool(query: str, config: RunnableConfig) -> str:
    """
    Execute pre-curated analysis templates for complex business questions.

    Args:
        query: Business question

    Returns:
        Detailed analysis results
    """
    try:
        use_case = config.get("configurable", {}).get("use_case", "default")

        async with httpx.AsyncClient(timeout=180) as client:
            response = await client.post(
                f"http://analysis-service/analyze?use_case={use_case}",
                json={"question": query}
            )

            if response.status_code >= 400:
                return f"Error executing analysis: {response.text}"

            result = response.json()
            return json.dumps(result, indent=2)

    except Exception as e:
        return f"Error executing analysis: {str(e)}"


# ========== Human in the Loop Tool ==========
from langgraph.types import interrupt

@tool
def human_assistance(query: str, context: str = "") -> str:
    """
    Request human assistance for clarification.

    Args:
        query: Question for the human
        context: Additional context

    Returns:
        Human response
    """
    try:
        human_response = interrupt({
            "query": query,
            "context": context
        })

        if isinstance(human_response, dict):
            return human_response.get("response", "Continue with available tools")
        return str(human_response)

    except Exception as e:
        return "Continue with available tools"


# ========== Final Answer Tool ==========
@tool
def final_answer_tool(
    question: str,
    plan: str,
    tool_execution_history: str,
    conversation_history: str = ""
) -> str:
    """
    Generate comprehensive final answer.

    Args:
        question: Original user question
        plan: Overall plan
        tool_execution_history: Complete execution history
        conversation_history: Past conversations

    Returns:
        Final answer
    """
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful AI assistant that generates comprehensive final answers.

Based on the plan and tool execution history, provide a clear, concise answer that:
- Directly addresses the user's question
- References specific data and findings
- Is formatted in clear markdown
- Acknowledges any limitations

Be thorough but concise."""),

        ("human", """Question: {question}

Plan: {plan}

Tool Execution History:
{tool_execution_history}

Conversation History:
{conversation_history}

Generate a comprehensive final answer.""")
    ])

    chain = final_prompt | llm
    result = chain.invoke({
        "question": question,
        "plan": plan,
        "tool_execution_history": tool_execution_history,
        "conversation_history": conversation_history
    })

    return result.content


def create_final_answer_node(final_answer_tool_func):
    """Wrap final_answer_tool in a node function"""

    async def final_answer_node(state: AgentState, config: RunnableConfig) -> Dict[str, Any]:
        """Generate final answer"""

        # Format tool execution history
        tool_history = "\n".join([
            f"- Tool: {item['tool']}\n  Question: {item['question']}\n  Outcome: {item['outcome']}"
            for item in state.get("tool_execution_history", [])
        ])

        # Format conversation history
        conv_history = "\n".join([
            f"Q: {item['question']}\nA: {item['final_answer']}"
            for item in state.get("conversation_history", [])
        ])

        # Generate final answer
        final_answer = await final_answer_tool_func.ainvoke({
            "question": state["input"],
            "plan": state.get("overall_plan", "No plan created"),
            "tool_execution_history": tool_history,
            "conversation_history": conv_history
        }, config=config)

        return {
            "final_answer": final_answer,
            "response": final_answer
        }

    return final_answer_node
```

**Key Implementation Notes:**

1. **Tool wrapper pattern**: Each tool is wrapped in a node function
2. **State updates**: Each node updates relevant state fields
3. **Dataset persistence**: Save data to files for downstream use
4. **Error handling**: Graceful error handling with fallback responses
5. **Python agent**: Use ReAct agent for iterative code execution

---

## Implementation Guide

### Step 1: Set Up Project Structure

```
agentic_orchestration/
│
├── src/
│   ├── __init__.py
│   ├── state.py              # State definition
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── planner.py        # Planner node
│   │   ├── evaluator.py      # Evaluator node
│   │   ├── tools.py          # Tool definitions and nodes
│   │   └── final_answer.py   # Final answer node
│   ├── graph/
│   │   ├── __init__.py
│   │   └── workflow.py       # Graph construction
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py       # Configuration
│   └── utils/
│       ├── __init__.py
│       ├── dataset_utils.py  # Dataset loading/saving
│       └── llm_utils.py      # LLM initialization
│
├── tests/
│   ├── __init__.py
│   ├── test_nodes.py
│   ├── test_integration.py
│   └── test_scenarios.py
│
├── evaluation/
│   ├── __init__.py
│   ├── eval_dataset.json     # Evaluation questions
│   ├── run_evaluation.py     # Evaluation runner
│   └── metrics.py            # Evaluation metrics
│
├── .env                       # Environment variables
├── requirements.txt
└── README.md
```

### Step 2: Install Dependencies

```bash
# requirements.txt
langgraph>=0.2.0
langchain>=0.1.0
langchain-openai>=0.1.0
langchain-experimental>=0.0.50
python-dotenv>=1.0.0
pydantic>=2.0.0
httpx>=0.25.0
pandas>=2.0.0
plotly>=5.0.0
loguru>=0.7.0
redis>=5.0.0
```

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# .env
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4

# Service URLs (if using microservices)
SQL_SERVICE_URL=http://localhost:8001
DOC_QA_SERVICE_URL=http://localhost:8002
ANALYSIS_SERVICE_URL=http://localhost:8003

# Redis for checkpointing
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
```

### Step 4: Build the Graph

```python
# src/graph/workflow.py
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.redis import AsyncRedisSaver
import redis.asyncio as redis

from src.state import AgentState
from src.nodes.planner import create_planner_node
from src.nodes.evaluator import create_evaluator_node
from src.nodes.tools import (
    create_sql_tool_node,
    create_doc_qa_node,
    create_python_node,
    create_analysis_node,
    create_human_assistance_node,
    sql_tool,
    doc_qa_tool,
    python_repl_tool,
    analysis_tool,
    human_assistance
)
from src.nodes.final_answer import create_final_answer_node, final_answer_tool
from src.utils.llm_utils import get_llm


def create_orchestration_graph(
    available_tools: List[str],
    use_checkpointing: bool = True
):
    """
    Create the orchestration graph

    Args:
        available_tools: List of available tool names
        use_checkpointing: Whether to use Redis checkpointing for memory
    """

    # Initialize LLM
    llm = get_llm()

    # Define tool descriptions
    TOOL_DESCRIPTIONS = {
        "sql_tool": "Retrieve structured data from SQL database using natural language queries",
        "doc_qa_tool": "Search internal documents and knowledge base for relevant information",
        "python_tool": "Execute Python code for analysis, visualization, and machine learning",
        "analysis_tool": "Run pre-curated business analysis templates for complex questions",
        "human_assistance": "Request clarification from the user when needed"
    }

    # Create nodes
    planner_node = create_planner_node(llm, available_tools, TOOL_DESCRIPTIONS)
    evaluator_node = create_evaluator_node(llm)
    sql_node = create_sql_tool_node(sql_tool)
    doc_qa_node = create_doc_qa_node(doc_qa_tool)
    python_node = create_python_node(python_repl_tool)
    analysis_node = create_analysis_node(analysis_tool)
    human_node = create_human_assistance_node(human_assistance)
    final_answer_node = create_final_answer_node(final_answer_tool)

    # Create graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("evaluator", evaluator_node)
    workflow.add_node("final_answer", final_answer_node)

    # Add tool nodes
    if "sql_tool" in available_tools:
        workflow.add_node("sql_tool", sql_node)
    if "doc_qa_tool" in available_tools:
        workflow.add_node("doc_qa_tool", doc_qa_node)
    if "python_tool" in available_tools:
        workflow.add_node("python_tool", python_node)
    if "analysis_tool" in available_tools:
        workflow.add_node("analysis_tool", analysis_node)
    if "human_assistance" in available_tools:
        workflow.add_node("human_assistance", human_node)

    # Set entry point
    workflow.set_entry_point("planner")

    # Add routing from planner to tools
    def route_from_planner(state: AgentState) -> str:
        """Route from planner to appropriate tool"""
        next_tool = state.get("next_tool", "")

        # Map tool names to node names
        if next_tool in available_tools:
            return next_tool

        # Default to final answer if no valid tool
        return "final_answer"

    workflow.add_conditional_edges(
        "planner",
        route_from_planner,
        {tool: tool for tool in available_tools} | {"final_answer": "final_answer"}
    )

    # Add edges from tools to evaluator
    for tool in available_tools:
        if tool != "human_assistance":  # human_assistance might interrupt
            workflow.add_edge(tool, "evaluator")

    # Add routing from evaluator
    def route_from_evaluator(state: AgentState) -> str:
        """Route from evaluator based on decision"""
        decision = state.get("evaluator_decision", "incomplete")

        # Update iteration count
        state["iteration_count"] = state.get("iteration_count", 0) + 1

        if decision == "complete":
            return "final_answer"
        else:
            return "planner"

    workflow.add_conditional_edges(
        "evaluator",
        route_from_evaluator,
        {
            "planner": "planner",
            "final_answer": "final_answer"
        }
    )

    # Final answer ends the graph
    workflow.add_edge("final_answer", END)

    # Set up checkpointing if enabled
    if use_checkpointing:
        redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            password=os.getenv("REDIS_PASSWORD", None),
            decode_responses=False
        )
        checkpointer = AsyncRedisSaver(redis_client)
    else:
        checkpointer = None

    # Compile graph
    app = workflow.compile(checkpointer=checkpointer)

    return app
```

### Step 5: Create Initial State Helper

```python
# src/utils/state_utils.py
import uuid
from datetime import datetime
from src.state import AgentState

def create_initial_state(
    question: str,
    user_id: str = "default_user",
    conversation_history: List[Dict[str, Any]] = None,
    max_iterations: int = 5,
    context: Dict[str, Any] = None
) -> AgentState:
    """
    Create initial state for a new question

    Args:
        question: User's question
        user_id: User identifier
        conversation_history: Previous conversation history
        max_iterations: Maximum planner-evaluator iterations
        context: Additional context
    """

    return {
        # Core
        "messages": [],
        "input": question,
        "question": question,

        # Planner
        "overall_plan": "",
        "plan_steps": [],
        "current_step": 0,

        # Tool management
        "next_tool": None,
        "next_question": "",
        "planner_reasoning": "",

        # Tool execution
        "tool_outcome": [],
        "tool_execution_history": [],
        "tool_results": [],

        # Evaluator
        "evaluator_decision": None,
        "evaluator_reasoning": "",
        "missing_information": "",

        # Iteration control
        "iteration_count": 0,
        "max_iterations": max_iterations,

        # Data
        "intermediate_data": {},
        "datasets_used": [],

        # Context
        "context": context or {},
        "conversation_history": conversation_history or [],
        "request_id": str(uuid.uuid4()),
        "user_id": user_id,

        # Output
        "final_answer": None,
        "response": "",

        # Control
        "requires_human_input": False,
        "execution_metadata": {
            "start_time": datetime.now().isoformat()
        }
    }
```

### Step 6: Run the Orchestration

```python
# example_usage.py
import asyncio
from src.graph.workflow import create_orchestration_graph
from src.utils.state_utils import create_initial_state

async def main():
    # Create graph
    app = create_orchestration_graph(
        available_tools=[
            "sql_tool",
            "doc_qa_tool",
            "python_tool",
            "human_assistance"
        ],
        use_checkpointing=True
    )

    # Create initial state
    initial_state = create_initial_state(
        question="What were our top 5 products by sales in Q1 2024?",
        user_id="user123",
        max_iterations=5
    )

    # Run with config for checkpointing
    config = {
        "configurable": {
            "thread_id": "session_123",  # For checkpointing
            "use_case": "sales_analysis"
        }
    }

    # Execute graph
    result = await app.ainvoke(initial_state, config=config)

    # Print final answer
    print("Final Answer:")
    print(result["final_answer"])

    print("\nTools Used:")
    print(result["datasets_used"])

    print("\nIteration Count:")
    print(result["iteration_count"])

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Tool Integration

### NL2SQL Tool Integration

```python
# Example: Integrate with existing NL2SQL service

@tool
async def sql_tool(query: str, config: RunnableConfig) -> str:
    """Execute SQL queries via NL2SQL service"""

    use_case = config.get("configurable", {}).get("use_case")
    request_id = config.get("configurable", {}).get("request_id", str(uuid.uuid4()))

    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(
            f"{SQL_SERVICE_URL}/query",
            json={
                "question": query,
                "use_case": use_case,
                "request_id": request_id
            }
        )

        if response.status_code != 200:
            return f"Error: {response.text}"

        result = response.json()

        # Expected response format:
        # {
        #   "sql_query": "SELECT ...",
        #   "result": [...],
        #   "row_count": 100
        # }

        return json.dumps(result, indent=2)
```

### Document QA Tool Integration

```python
@tool
async def doc_qa_tool(query: str, config: RunnableConfig) -> str:
    """Search documents via vector database"""

    use_case = config.get("configurable", {}).get("use_case")

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{DOC_QA_SERVICE_URL}/search",
            json={
                "question": query,
                "use_case": use_case,
                "top_k": 5
            }
        )

        if response.status_code != 200:
            return f"Error: {response.text}"

        result = response.json()

        # Expected response format:
        # {
        #   "response": "Based on the documents...",
        #   "sources": [...]
        # }

        return json.dumps(result, indent=2)
```

### Python REPL with Dataset Loading

```python
def load_datasets_from_session(config: RunnableConfig) -> Dict[str, pd.DataFrame]:
    """Load all datasets created in this session"""

    thread_id = config.get("configurable", {}).get("thread_id", "default")
    datasets_folder = f"./datasets/{thread_id}"

    datasets = {}

    if os.path.exists(datasets_folder):
        for filename in os.listdir(datasets_folder):
            if filename.endswith(".json"):
                dataset_name = filename.replace(".json", "")
                file_path = os.path.join(datasets_folder, filename)

                with open(file_path, 'r') as f:
                    data = json.load(f)

                # Convert to DataFrame if it's a list
                if isinstance(data, list) and data:
                    datasets[dataset_name] = pd.DataFrame(data)
                else:
                    datasets[dataset_name] = data

    return datasets
```

### Function Calling Tool (Domain-Specific)

```python
# Example: Brand performance analysis function

@tool
async def analysis_tool(query: str, config: RunnableConfig) -> str:
    """Execute domain-specific analysis functions"""

    use_case = config.get("configurable", {}).get("use_case")

    async with httpx.AsyncClient(timeout=180) as client:
        response = await client.post(
            f"{ANALYSIS_SERVICE_URL}/analyze",
            json={
                "question": query,
                "use_case": use_case,
                "functions": [
                    "get_brand_performance",
                    "get_regional_highlights",
                    "get_trend_analysis"
                ]
            }
        )

        if response.status_code != 200:
            return f"Error: {response.text}"

        result = response.json()

        # Expected response format:
        # {
        #   "function_called": "get_brand_performance",
        #   "result": {...},
        #   "metadata": {...}
        # }

        return json.dumps(result, indent=2)
```

---

## State Management

### Dataset Persistence

```python
# src/utils/dataset_utils.py
import os
import json
import pandas as pd
from pathlib import Path

def save_dataset(data: Any, dataset_name: str, config: RunnableConfig) -> str:
    """
    Save dataset to session folder

    Args:
        data: Data to save (list, dict, or DataFrame)
        dataset_name: Name for the dataset
        config: RunnableConfig with thread_id

    Returns:
        Path to saved file
    """
    thread_id = config.get("configurable", {}).get("thread_id", "default")
    datasets_folder = Path(f"./datasets/{thread_id}")
    datasets_folder.mkdir(parents=True, exist_ok=True)

    file_path = datasets_folder / f"{dataset_name}.json"

    # Convert to serializable format
    if hasattr(data, 'to_dict'):  # pandas DataFrame
        data_to_save = data.to_dict(orient='records')
    elif isinstance(data, (list, dict)):
        data_to_save = data
    else:
        data_to_save = str(data)

    with open(file_path, 'w') as f:
        json.dump(data_to_save, f, indent=2)

    return str(file_path)


def load_dataset(dataset_name: str, config: RunnableConfig) -> Optional[Any]:
    """Load dataset from session folder"""

    thread_id = config.get("configurable", {}).get("thread_id", "default")
    file_path = Path(f"./datasets/{thread_id}/{dataset_name}.json")

    if not file_path.exists():
        return None

    with open(file_path, 'r') as f:
        data = json.load(f)

    return data


def get_available_datasets(config: RunnableConfig) -> List[Dict[str, Any]]:
    """Get list of all available datasets in session"""

    thread_id = config.get("configurable", {}).get("thread_id", "default")
    datasets_folder = Path(f"./datasets/{thread_id}")

    if not datasets_folder.exists():
        return []

    datasets_info = []

    for file_path in datasets_folder.glob("*.json"):
        dataset_name = file_path.stem

        with open(file_path, 'r') as f:
            data = json.load(f)

        row_count = len(data) if isinstance(data, list) else 1

        datasets_info.append({
            "name": dataset_name,
            "file_path": str(file_path),
            "row_count": row_count,
            "preview": data[:2] if isinstance(data, list) else str(data)[:200]
        })

    return datasets_info
```

### Conversation History Management

```python
def add_to_conversation_history(
    state: AgentState,
    question: str,
    final_answer: str,
    datasets_used: List[str]
) -> List[Dict[str, Any]]:
    """Add completed Q&A to conversation history"""

    conversation_history = state.get("conversation_history", [])

    conversation_history.append({
        "question": question,
        "final_answer": final_answer,
        "datasets": datasets_used,
        "timestamp": datetime.now().isoformat()
    })

    # Keep only last 10 conversations to avoid context overflow
    return conversation_history[-10:]
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_nodes.py
import pytest
from src.nodes.planner import create_planner_node
from src.nodes.evaluator import create_evaluator_node
from src.state import AgentState
from src.utils.llm_utils import get_llm

@pytest.mark.asyncio
async def test_planner_node():
    """Test planner node selects appropriate tool"""

    llm = get_llm()
    planner = create_planner_node(
        llm,
        available_tools=["sql_tool", "python_tool"],
        tool_descriptions={
            "sql_tool": "Get data from database",
            "python_tool": "Analyze data with Python"
        }
    )

    state = {
        "input": "Show me sales data for Q1 2024",
        "conversation_history": [],
        "tool_execution_history": [],
        "iteration_count": 0,
        "max_iterations": 5
    }

    result = await planner(state)

    assert "overall_plan" in result
    assert result["next_tool"] == "sql_tool"  # Should select SQL for data retrieval
    assert "next_question" in result
    assert "planner_reasoning" in result


@pytest.mark.asyncio
async def test_evaluator_node_incomplete():
    """Test evaluator correctly identifies incomplete answer"""

    llm = get_llm()
    evaluator = create_evaluator_node(llm)

    state = {
        "input": "Analyze sales trends and create visualization",
        "overall_plan": "1. Get data 2. Analyze 3. Visualize",
        "tool_execution_history": [
            {
                "tool": "sql_tool",
                "question": "Get sales data",
                "outcome": "Retrieved 100 rows"
            }
        ],
        "iteration_count": 1,
        "max_iterations": 5
    }

    result = await evaluator(state)

    assert result["evaluator_decision"] == "incomplete"
    assert "missing_information" in result


@pytest.mark.asyncio
async def test_evaluator_node_complete():
    """Test evaluator correctly identifies complete answer"""

    llm = get_llm()
    evaluator = create_evaluator_node(llm)

    state = {
        "input": "Analyze sales trends and create visualization",
        "overall_plan": "1. Get data 2. Analyze 3. Visualize",
        "tool_execution_history": [
            {
                "tool": "sql_tool",
                "question": "Get sales data",
                "outcome": "Retrieved 100 rows"
            },
            {
                "tool": "python_tool",
                "question": "Analyze trends",
                "outcome": "Identified 20% growth trend"
            },
            {
                "tool": "python_tool",
                "question": "Create visualization",
                "outcome": "Created line chart showing trends"
            }
        ],
        "iteration_count": 3,
        "max_iterations": 5
    }

    result = await evaluator(state)

    assert result["evaluator_decision"] == "complete"
```

### Integration Tests

```python
# tests/test_integration.py
import pytest
from src.graph.workflow import create_orchestration_graph
from src.utils.state_utils import create_initial_state

@pytest.mark.asyncio
async def test_full_workflow():
    """Test complete orchestration workflow"""

    app = create_orchestration_graph(
        available_tools=["sql_tool", "python_tool"],
        use_checkpointing=False
    )

    initial_state = create_initial_state(
        question="What were the top 5 products by sales in Q1 2024?",
        max_iterations=5
    )

    config = {
        "configurable": {
            "thread_id": "test_session",
            "use_case": "test"
        }
    }

    result = await app.ainvoke(initial_state, config=config)

    # Assertions
    assert "final_answer" in result
    assert result["final_answer"] is not None
    assert len(result["tool_execution_history"]) > 0
    assert "sql_tool" in result["datasets_used"]
    assert result["iteration_count"] <= 5
```

### Scenario Tests

```python
# tests/test_scenarios.py
import pytest

SCENARIOS = [
    {
        "name": "Simple data retrieval",
        "question": "Show me sales for Q1 2024",
        "expected_tools": ["sql_tool"],
        "expected_iterations": 1
    },
    {
        "name": "Data retrieval + analysis",
        "question": "Analyze sales trends for Q1 2024",
        "expected_tools": ["sql_tool", "python_tool"],
        "expected_iterations": 2
    },
    {
        "name": "Data + analysis + visualization",
        "question": "Show sales trends for Q1 2024 with a chart",
        "expected_tools": ["sql_tool", "python_tool"],
        "expected_iterations": 2-3
    },
    {
        "name": "Document search",
        "question": "What is our return policy?",
        "expected_tools": ["doc_qa_tool"],
        "expected_iterations": 1
    }
]

@pytest.mark.parametrize("scenario", SCENARIOS)
@pytest.mark.asyncio
async def test_scenario(scenario):
    """Test different question scenarios"""

    app = create_orchestration_graph(
        available_tools=["sql_tool", "python_tool", "doc_qa_tool"],
        use_checkpointing=False
    )

    initial_state = create_initial_state(
        question=scenario["question"],
        max_iterations=5
    )

    config = {
        "configurable": {
            "thread_id": f"test_{scenario['name']}",
            "use_case": "test"
        }
    }

    result = await app.ainvoke(initial_state, config=config)

    # Check tools used
    for expected_tool in scenario["expected_tools"]:
        assert expected_tool in result["datasets_used"]

    # Check iteration count is reasonable
    if isinstance(scenario["expected_iterations"], int):
        assert result["iteration_count"] == scenario["expected_iterations"]
    else:
        # Range provided (e.g., 2-3)
        min_iter, max_iter = scenario["expected_iterations"]
        assert min_iter <= result["iteration_count"] <= max_iter
```

---

## Offline Evaluation Framework

### Evaluation Dataset Structure

```json
{
  "eval_dataset": [
    {
      "id": "eval_001",
      "category": "data_retrieval",
      "question": "What were the top 5 products by sales in Q1 2024?",
      "expected_tools": ["sql_tool"],
      "expected_answer_contains": ["top 5", "sales", "Q1 2024"],
      "ground_truth": "The top 5 products by sales in Q1 2024 were...",
      "metadata": {
        "difficulty": "easy",
        "requires_visualization": false
      }
    },
    {
      "id": "eval_002",
      "category": "analysis",
      "question": "Analyze sales trends for our top 3 brands and identify patterns",
      "expected_tools": ["sql_tool", "python_tool"],
      "expected_answer_contains": ["trends", "patterns", "brands"],
      "ground_truth": null,
      "metadata": {
        "difficulty": "medium",
        "requires_visualization": true
      }
    },
    {
      "id": "eval_003",
      "category": "multi_step",
      "question": "Compare Q1 2024 sales to Q1 2023, identify growth drivers, and forecast Q2 2024",
      "expected_tools": ["sql_tool", "python_tool"],
      "expected_answer_contains": ["comparison", "growth", "forecast"],
      "ground_truth": null,
      "metadata": {
        "difficulty": "hard",
        "requires_visualization": true
      }
    }
  ]
}
```

### Evaluation Metrics

```python
# evaluation/metrics.py
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class EvaluationMetrics:
    """Metrics for evaluating orchestration performance"""

    # Correctness metrics
    tool_accuracy: float           # % of correct tool selections
    answer_relevance: float        # LLM-as-judge score for relevance
    answer_completeness: float     # LLM-as-judge score for completeness

    # Efficiency metrics
    avg_iterations: float          # Average number of iterations
    avg_execution_time: float      # Average time in seconds
    tool_efficiency: float         # % of useful tool calls (no wasted calls)

    # Quality metrics
    final_answer_quality: float    # LLM-as-judge overall quality score
    hallucination_rate: float      # % of answers with hallucinations

    # User experience metrics
    clarity_score: float           # How clear is the answer?
    actionability_score: float     # Can user act on the answer?


def calculate_tool_accuracy(
    predicted_tools: List[str],
    expected_tools: List[str]
) -> float:
    """Calculate tool selection accuracy"""

    if not expected_tools:
        return 1.0  # No expectation

    correct = sum(1 for tool in expected_tools if tool in predicted_tools)
    return correct / len(expected_tools)


def calculate_answer_relevance(
    question: str,
    answer: str,
    llm
) -> float:
    """Use LLM as judge to evaluate answer relevance"""

    prompt = f"""Evaluate the relevance of the answer to the question on a scale of 0-10.

Question: {question}

Answer: {answer}

Score (0-10): Provide only a number."""

    response = llm.invoke(prompt)
    score = float(response.content.strip())
    return score / 10.0


def calculate_answer_completeness(
    question: str,
    answer: str,
    expected_answer_contains: List[str],
    llm
) -> float:
    """Evaluate answer completeness"""

    # Check if expected keywords are present
    keyword_score = sum(
        1 for keyword in expected_answer_contains
        if keyword.lower() in answer.lower()
    ) / len(expected_answer_contains) if expected_answer_contains else 1.0

    # LLM-as-judge for overall completeness
    prompt = f"""Evaluate if the answer completely addresses all aspects of the question on a scale of 0-10.

Question: {question}

Answer: {answer}

Score (0-10): Provide only a number."""

    response = llm.invoke(prompt)
    llm_score = float(response.content.strip()) / 10.0

    # Weighted average
    return 0.4 * keyword_score + 0.6 * llm_score


def detect_hallucinations(
    question: str,
    answer: str,
    tool_results: List[Dict[str, Any]],
    llm
) -> bool:
    """Detect if answer contains hallucinations"""

    # Extract data from tool results
    available_data = "\n".join([
        f"Tool: {result['tool']}\nResult: {result['result']}"
        for result in tool_results
    ])

    prompt = f"""Determine if the answer contains any hallucinations (made-up facts not supported by the data).

Question: {question}

Available Data:
{available_data}

Answer: {answer}

Does the answer contain hallucinations? Respond with only YES or NO."""

    response = llm.invoke(prompt)
    return response.content.strip().upper() == "YES"
```

### Evaluation Runner

```python
# evaluation/run_evaluation.py
import json
import asyncio
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd

from src.graph.workflow import create_orchestration_graph
from src.utils.state_utils import create_initial_state
from evaluation.metrics import (
    EvaluationMetrics,
    calculate_tool_accuracy,
    calculate_answer_relevance,
    calculate_answer_completeness,
    detect_hallucinations
)


class EvaluationRunner:
    """Run offline evaluation on test dataset"""

    def __init__(
        self,
        eval_dataset_path: str,
        available_tools: List[str],
        output_dir: str = "./evaluation/results"
    ):
        self.eval_dataset_path = eval_dataset_path
        self.available_tools = available_tools
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load evaluation dataset
        with open(eval_dataset_path, 'r') as f:
            self.eval_dataset = json.load(f)["eval_dataset"]

        # Create orchestration graph
        self.app = create_orchestration_graph(
            available_tools=available_tools,
            use_checkpointing=False
        )

        # For LLM-as-judge
        from src.utils.llm_utils import get_llm
        self.judge_llm = get_llm()

    async def evaluate_single_question(
        self,
        eval_item: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate a single question"""

        question_id = eval_item["id"]
        question = eval_item["question"]
        expected_tools = eval_item.get("expected_tools", [])
        expected_answer_contains = eval_item.get("expected_answer_contains", [])

        print(f"Evaluating {question_id}: {question}")

        # Run orchestration
        initial_state = create_initial_state(
            question=question,
            max_iterations=5
        )

        config = {
            "configurable": {
                "thread_id": f"eval_{question_id}",
                "use_case": "evaluation"
            }
        }

        start_time = datetime.now()

        try:
            result = await self.app.ainvoke(initial_state, config=config)

            execution_time = (datetime.now() - start_time).total_seconds()

            # Extract results
            final_answer = result.get("final_answer", "")
            tools_used = result.get("datasets_used", [])
            iteration_count = result.get("iteration_count", 0)
            tool_results = result.get("tool_results", [])

            # Calculate metrics
            tool_accuracy = calculate_tool_accuracy(tools_used, expected_tools)

            answer_relevance = calculate_answer_relevance(
                question, final_answer, self.judge_llm
            )

            answer_completeness = calculate_answer_completeness(
                question, final_answer, expected_answer_contains, self.judge_llm
            )

            has_hallucinations = detect_hallucinations(
                question, final_answer, tool_results, self.judge_llm
            )

            # Calculate tool efficiency (no redundant tool calls)
            unique_tools = len(set(tools_used))
            tool_efficiency = unique_tools / len(tools_used) if tools_used else 0

            return {
                "question_id": question_id,
                "question": question,
                "category": eval_item.get("category", "unknown"),
                "final_answer": final_answer,
                "tools_used": tools_used,
                "iteration_count": iteration_count,
                "execution_time": execution_time,
                "metrics": {
                    "tool_accuracy": tool_accuracy,
                    "answer_relevance": answer_relevance,
                    "answer_completeness": answer_completeness,
                    "has_hallucinations": has_hallucinations,
                    "tool_efficiency": tool_efficiency
                },
                "success": True,
                "error": None
            }

        except Exception as e:
            return {
                "question_id": question_id,
                "question": question,
                "category": eval_item.get("category", "unknown"),
                "final_answer": None,
                "tools_used": [],
                "iteration_count": 0,
                "execution_time": 0,
                "metrics": None,
                "success": False,
                "error": str(e)
            }

    async def run_evaluation(self) -> Dict[str, Any]:
        """Run evaluation on entire dataset"""

        print(f"Starting evaluation on {len(self.eval_dataset)} questions...")

        results = []

        for eval_item in self.eval_dataset:
            result = await self.evaluate_single_question(eval_item)
            results.append(result)

            # Small delay to avoid rate limits
            await asyncio.sleep(1)

        # Calculate aggregate metrics
        successful_results = [r for r in results if r["success"]]

        if not successful_results:
            print("No successful evaluations!")
            return {"error": "All evaluations failed"}

        aggregate_metrics = {
            "total_questions": len(self.eval_dataset),
            "successful": len(successful_results),
            "failed": len(results) - len(successful_results),
            "avg_tool_accuracy": sum(r["metrics"]["tool_accuracy"] for r in successful_results) / len(successful_results),
            "avg_answer_relevance": sum(r["metrics"]["answer_relevance"] for r in successful_results) / len(successful_results),
            "avg_answer_completeness": sum(r["metrics"]["answer_completeness"] for r in successful_results) / len(successful_results),
            "hallucination_rate": sum(1 for r in successful_results if r["metrics"]["has_hallucinations"]) / len(successful_results),
            "avg_iterations": sum(r["iteration_count"] for r in successful_results) / len(successful_results),
            "avg_execution_time": sum(r["execution_time"] for r in successful_results) / len(successful_results),
            "avg_tool_efficiency": sum(r["metrics"]["tool_efficiency"] for r in successful_results) / len(successful_results)
        }

        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "eval_dataset": self.eval_dataset_path,
            "available_tools": self.available_tools,
            "aggregate_metrics": aggregate_metrics,
            "detailed_results": results
        }

        # Save report
        report_path = self.output_dir / f"eval_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\nEvaluation complete! Report saved to {report_path}")

        # Print summary
        print("\n" + "="*80)
        print("EVALUATION SUMMARY")
        print("="*80)
        print(f"Total Questions: {aggregate_metrics['total_questions']}")
        print(f"Successful: {aggregate_metrics['successful']}")
        print(f"Failed: {aggregate_metrics['failed']}")
        print(f"\nMetrics:")
        print(f"  Tool Accuracy: {aggregate_metrics['avg_tool_accuracy']:.2%}")
        print(f"  Answer Relevance: {aggregate_metrics['avg_answer_relevance']:.2%}")
        print(f"  Answer Completeness: {aggregate_metrics['avg_answer_completeness']:.2%}")
        print(f"  Hallucination Rate: {aggregate_metrics['hallucination_rate']:.2%}")
        print(f"  Avg Iterations: {aggregate_metrics['avg_iterations']:.1f}")
        print(f"  Avg Execution Time: {aggregate_metrics['avg_execution_time']:.1f}s")
        print(f"  Tool Efficiency: {aggregate_metrics['avg_tool_efficiency']:.2%}")
        print("="*80)

        # Generate CSV for analysis
        df = pd.DataFrame([
            {
                "question_id": r["question_id"],
                "category": r["category"],
                "success": r["success"],
                "tool_accuracy": r["metrics"]["tool_accuracy"] if r["success"] else None,
                "answer_relevance": r["metrics"]["answer_relevance"] if r["success"] else None,
                "answer_completeness": r["metrics"]["answer_completeness"] if r["success"] else None,
                "has_hallucinations": r["metrics"]["has_hallucinations"] if r["success"] else None,
                "iterations": r["iteration_count"],
                "execution_time": r["execution_time"]
            }
            for r in results
        ])

        csv_path = self.output_dir / f"eval_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(csv_path, index=False)
        print(f"Detailed CSV saved to {csv_path}\n")

        return report


# Usage
async def main():
    runner = EvaluationRunner(
        eval_dataset_path="./evaluation/eval_dataset.json",
        available_tools=["sql_tool", "python_tool", "doc_qa_tool"],
        output_dir="./evaluation/results"
    )

    await runner.run_evaluation()


if __name__ == "__main__":
    asyncio.run(main())
```

### Evaluation Best Practices

1. **Diverse Test Cases**: Cover different categories
   - Simple data retrieval
   - Analysis questions
   - Multi-step reasoning
   - Visualization requests
   - Document searches

2. **Regular Evaluation**: Run evaluations
   - After major changes
   - Before deployments
   - Weekly for monitoring

3. **Track Metrics Over Time**:
   - Create a metrics dashboard
   - Compare evaluation runs
   - Identify regressions

4. **A/B Testing**:
   - Test different prompts
   - Test different tool orderings
   - Test different LLM models

5. **User Feedback Integration**:
   - Collect real user feedback
   - Add failed cases to eval dataset
   - Continuously improve

---

## Best Practices

### 1. Prompt Engineering

**Planner Prompt**:
- Be specific about when to use each tool
- Provide examples of good tool selection
- Emphasize sequential thinking (data → analysis → visualization)

**Evaluator Prompt**:
- Clear criteria for "complete" vs "incomplete"
- Balance thoroughness with reasonableness
- Consider iteration limits

**Final Answer Prompt**:
- Reference specific data points
- Format in markdown
- Acknowledge limitations

### 2. Error Handling

```python
def safe_tool_execution(tool_func):
    """Decorator for safe tool execution"""

    async def wrapper(*args, **kwargs):
        try:
            return await tool_func(*args, **kwargs)
        except httpx.TimeoutException:
            return "Error: Tool execution timed out. Please try again."
        except httpx.HTTPStatusError as e:
            return f"Error: Tool returned status {e.response.status_code}"
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return f"Error executing tool: {str(e)}"

    return wrapper
```

### 3. Observability

```python
from loguru import logger
import time

def log_node_execution(node_name: str):
    """Decorator to log node execution"""

    def decorator(func):
        async def wrapper(state, *args, **kwargs):
            logger.info(f"[{node_name}] Starting execution")
            start_time = time.time()

            try:
                result = await func(state, *args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(f"[{node_name}] Completed in {execution_time:.2f}s")
                return result
            except Exception as e:
                logger.error(f"[{node_name}] Failed: {e}")
                raise

        return wrapper
    return decorator
```

### 4. Cost Optimization

- Use cheaper models for evaluation (GPT-3.5)
- Cache LLM responses when possible
- Limit max iterations
- Implement token counting

```python
def count_tokens(text: str) -> int:
    """Estimate token count"""
    return len(text) // 4  # Rough estimate

def truncate_context(text: str, max_tokens: int = 4000) -> str:
    """Truncate context to fit token limit"""
    estimated_tokens = count_tokens(text)

    if estimated_tokens <= max_tokens:
        return text

    # Truncate to fit
    ratio = max_tokens / estimated_tokens
    target_chars = int(len(text) * ratio)
    return text[:target_chars] + "... [truncated]"
```

### 5. Human in the Loop Best Practices

```python
# Only interrupt when necessary
def should_trigger_hil(state: AgentState) -> bool:
    """Determine if human input is needed"""

    # Trigger HIL if:
    # 1. Tool selection is ambiguous
    # 2. Entity recognition is uncertain
    # 3. Question is ambiguous
    # 4. User explicitly requested clarification

    if state.get("planner_reasoning", "").lower().find("ambiguous") != -1:
        return True

    if state.get("iteration_count", 0) > 3:
        # Too many iterations, might need clarification
        return True

    return False
```

---

## Common Pitfalls

### 1. Infinite Loops

**Problem**: Planner-evaluator loop doesn't converge

**Solution**:
- Set max_iterations (default 5)
- Force completion at max iterations
- Monitor iteration count in evaluator

### 2. Tool Selection Errors

**Problem**: Planner selects wrong tools

**Solution**:
- Improve tool descriptions
- Add examples to planner prompt
- Use few-shot learning with successful examples
- Add similar plan retrieval tool

### 3. Context Overflow

**Problem**: State becomes too large, exceeds LLM context window

**Solution**:
- Truncate conversation history (keep last 10)
- Summarize tool results instead of including raw data
- Use references to datasets instead of inline data

### 4. Hallucinations

**Problem**: Final answer contains made-up facts

**Solution**:
- Explicitly instruct to only use tool results
- Add hallucination detection in evaluation
- Reference specific tool results in final answer

### 5. Poor Evaluation Scores

**Problem**: System performs poorly on eval dataset

**Solution**:
- Analyze failure cases
- Improve prompts based on patterns
- Add failed cases to few-shot examples
- Consider different LLM models

---

## Next Steps

### Phase 1: Core Implementation (Week 1-2)
- [ ] Implement state definition
- [ ] Create planner node
- [ ] Create evaluator node
- [ ] Build graph structure
- [ ] Add basic tools (SQL, Python)
- [ ] Test end-to-end flow

### Phase 2: Tool Integration (Week 3-4)
- [ ] Integrate NL2SQL service
- [ ] Integrate Doc QA service
- [ ] Integrate Analysis service
- [ ] Add dataset persistence
- [ ] Test with real services

### Phase 3: Enhancement (Week 5-6)
- [ ] Add human in the loop
- [ ] Implement conversation history
- [ ] Add memory retrieval
- [ ] Optimize prompts
- [ ] Add observability

### Phase 4: Evaluation (Week 7-8)
- [ ] Create evaluation dataset
- [ ] Implement evaluation metrics
- [ ] Run offline evaluation
- [ ] Analyze results
- [ ] Iterate on improvements

### Phase 5: Production Ready (Week 9-10)
- [ ] Add error handling
- [ ] Implement cost tracking
- [ ] Add monitoring/logging
- [ ] Create API endpoints
- [ ] Write documentation
- [ ] Deploy to staging

---

## Conclusion

This approach document provides a complete blueprint for building an agentic orchestration copilot using the **Planner-Evaluator pattern**. Key takeaways:

1. **Start Simple**: Begin with core planner-evaluator-tools flow
2. **Iterate**: Add features incrementally based on needs
3. **Evaluate**: Use offline evaluation to measure progress
4. **Monitor**: Track metrics in production
5. **Improve**: Continuously refine based on feedback

The architecture is flexible and extensible - you can add new tools, change LLM models, or modify the orchestration logic without major rewrites.

**Remember**: The goal is to build a system that reliably answers user questions, not to create perfect AI. Focus on user value, iterate quickly, and measure what matters.

Good luck with your implementation!
