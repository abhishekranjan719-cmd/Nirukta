"""
External API clients for third-party service integrations.

This package contains client wrappers for:
- LiteLLM proxy (litellm_client.py)
- Azure OpenAI direct API (azure_openai_client.py)
- Langfuse observability (langfuse_client.py)
"""

from app.clients.azure_openai_client import AzureOpenAIClient, get_azure_openai_client
from app.clients.langfuse_client import LangfuseClient, get_langfuse_client
from app.clients.litellm_client import LiteLLMClient, get_litellm_client


__all__ = [
    "AzureOpenAIClient",
    "LangfuseClient",
    "LiteLLMClient",
    "get_azure_openai_client",
    "get_langfuse_client",
    "get_litellm_client",
]
