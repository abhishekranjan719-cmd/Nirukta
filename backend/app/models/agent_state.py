from typing import Annotated, Any, Dict, List, Optional
from typing_extensions import TypedDict

class AgentState(TypedDict):
    """Single source of truth flowing through every node in the orchestration graph."""

    # Core state
    input: str                          # Original user question
    question: str                       # Current question being processed
    messages: List[Dict[str, Any]]      # Conversation history

    # Planner state
    overall_plan: str                   # Strategic plan created by planner
    plan_steps: List[Dict[str, Any]]    # List of planned steps with status
    current_step: int                   # Current step number

    # Tool management
    next_tool: Optional[str]            # Which tool to execute next
    next_question: str                  # Specific question for the tool
    planner_reasoning: str              # Why this tool was selected

    # Tool execution tracking
    tool_outcome: List[str]             # Human-readable outcomes
    tool_execution_history: List[Dict[str, Any]]  # Detailed execution log
    tool_results: List[Dict[str, Any]]  # Structured results from tools

    # Evaluator state
    is_complete: bool                   # Whether question is fully answered
    completeness_score: float           # 0.0 to 1.0
    missing_information: str            # What is still needed
    evaluation_reasoning: str          # Evaluator's reasoning

    # Iteration control
    iteration_count: int                # Current iteration
    max_iterations: int                 # Hard cap (default 5)

    # Final output
    final_answer: str                   # Synthesized final response
    sources: List[str]                  # Data sources used
    confidence: float                   # Confidence score
