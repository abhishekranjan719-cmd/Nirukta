"""
Chain definitions for workflow-based orchestration.

This module defines various chains that can be composed for different workflows:
- Simple QnA chain
- Multi-step reasoning chain
- RAG (Retrieval Augmented Generation) chain
- etc.

Currently implements a simple single-step chain.
Future: Can be extended with LangChain or custom chain implementations.
"""

from collections.abc import Callable
from typing import Any

from loguru import logger


class Chain:
    """
    Base class for defining processing chains.

    A chain is a sequence of processing steps that can be composed together.
    """

    def __init__(self, name: str, steps: list[Callable]):
        """
        Initialize a chain.

        Args:
            name: Chain name
            steps: List of callable steps
        """
        self.name = name
        self.steps = steps

    async def execute(self, input_data: Any) -> Any:
        """
        Execute the chain by running all steps sequentially.

        Args:
            input_data: Initial input

        Returns:
            Final output after all steps
        """
        logger.debug(f"Chain '{self.name}' started | Steps: {len(self.steps)}")

        result = input_data
        for i, step in enumerate(self.steps, 1):
            logger.debug(f"Chain '{self.name}' | Step {i}/{len(self.steps)}")
            result = await step(result) if callable(step) else result

        logger.debug(f"Chain '{self.name}' completed")
        return result


# Example chain definitions (can be extended)
def create_simple_qna_chain() -> Chain:
    """
    Create a simple QnA chain.

    Steps:
    1. Input validation
    2. LLM call
    3. Response formatting
    """
    return Chain(
        name="simple_qna",
        steps=[
            # Steps would be defined here
            # For now, this is handled in the service layer
        ],
    )
