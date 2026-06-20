"""
Agent State Definition

This module defines the state structure for the LangGraph ReAct agent.
The state tracks messages, input data, and intermediate results throughout
the agent's reasoning-action-observation loop.
"""

from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    State for the QnA ReAct agent.

    Uses add_messages reducer for automatic message list management,
    which is critical for LangGraph's message handling.

    Attributes:
        messages: Conversation messages (automatically merged via add_messages)
        question: The user's current question
        conversation_history: Previous conversation context in OpenAI format
        summary: Optional summary of long conversations
        final_response: The agent's final answer
    """

    # Messages with automatic merging via add_messages reducer
    # This is crucial for LangGraph - it handles message list updates correctly
    messages: Annotated[list[BaseMessage], add_messages]

    # Input data
    question: str
    conversation_history: list[dict]  # OpenAI format: [{"role": "user/assistant", "content": "..."}]

    # Summary for long conversations (>10 messages)
    summary: str | None

    # Final response
    final_response: dict | None
