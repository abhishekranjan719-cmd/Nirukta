"""
Utility for loading and managing prompts.
"""

from pathlib import Path

from loguru import logger


class PromptLoader:
    """
    Loads prompts from the prompts directory.

    This utility handles loading system prompts from files, with proper
    error handling and fallbacks.
    """

    def __init__(self, prompts_dir: Path | None = None):
        """
        Initialize prompt loader.

        Args:
            prompts_dir: Path to prompts directory. If None, uses default location.
        """
        if prompts_dir is None:
            # Default location: engine/prompts/
            self.prompts_dir = Path(__file__).parent.parent.parent / "prompts"
        else:
            self.prompts_dir = prompts_dir

        logger.info(f"PromptLoader initialized | Prompts dir: {self.prompts_dir}")

    def load_prompt(
        self,
        prompt_name: str,
        fallback: str = "You are a helpful AI assistant. Provide clear, concise, and accurate responses.",
    ) -> str:
        """
        Load a prompt from file.

        Args:
            prompt_name: Name of the prompt file (with or without .md extension)
            fallback: Fallback prompt if file not found

        Returns:
            Prompt content as string
        """
        # Add .md extension if not present
        if not prompt_name.endswith(".md"):
            prompt_name = f"{prompt_name}.md"

        prompt_path = self.prompts_dir / prompt_name

        try:
            content = prompt_path.read_text(encoding="utf-8")
            logger.info(f"Loaded prompt: {prompt_name} | " f"Length: {len(content)} chars | " f"Path: {prompt_path}")
            return content
        except FileNotFoundError:
            logger.warning(
                f"Prompt file not found: {prompt_path} | "
                f"Using fallback | "
                f"Fallback length: {len(fallback)} chars"
            )
            return fallback
        except Exception as e:
            logger.error(f"Failed to load prompt: {prompt_name} | " f"Error: {e!s} | " f"Using fallback")
            return fallback

    def load_formatter_prompt(self) -> str:
        """
        Load the formatter prompt specifically.

        Returns:
            Formatter prompt content
        """
        return self.load_prompt("formatter_prompt")


# Singleton instance
_prompt_loader: PromptLoader | None = None


def get_prompt_loader() -> PromptLoader:
    """
    Get singleton prompt loader instance.

    Returns:
        PromptLoader instance
    """
    global _prompt_loader
    if _prompt_loader is None:
        _prompt_loader = PromptLoader()
    return _prompt_loader
