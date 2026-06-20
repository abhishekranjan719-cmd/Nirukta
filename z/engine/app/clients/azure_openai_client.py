"""
Azure OpenAI Direct Client

This module provides a direct client for Azure OpenAI API.
Used as fallback when LiteLLM proxy is disabled.
"""

from typing import Any

import httpx
from loguru import logger

from app.config import settings


class AzureOpenAIClient:
    """
    Direct client for Azure OpenAI API (fallback when LiteLLM disabled).

    Features:
    - SSL verification disabled for local development
    - Direct Azure OpenAI REST API calls
    - Support for chat completions
    - Support for embeddings
    - Error handling and retry logic
    """

    def __init__(self):
        """Initialize Azure OpenAI client with configuration from settings."""
        self.endpoint = settings.azure_openai.azure_openai_endpoint
        self.api_key = settings.azure_openai.azure_openai_api_key
        self.api_version = settings.azure_openai.azure_openai_api_version

        # Model deployment names
        self.chat_deployment = settings.azure_openai.azure_openai_chat_deployment
        self.embedding_deployment = settings.azure_openai.azure_openai_embedding_deployment

        self.timeout = settings.engine_llm_timeout
        self.ssl_verify = settings.engine_http_ssl_verify

        # Create httpx client with configurable SSL verification
        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            verify=self.ssl_verify,
            headers={
                "api-key": self.api_key,
                "Content-Type": "application/json",
            },
        )

        logger.info(
            f"Azure OpenAI direct client initialized | "
            f"Endpoint: {self.endpoint} | "
            f"Chat deployment: {self.chat_deployment} | "
            f"Timeout: {self.timeout}s | "
            f"SSL Verify: {self.ssl_verify}"
        )

    async def chat_completion(
        self,
        model: str,  # Ignored, uses deployment from settings
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Call Azure OpenAI chat completions API.

        Args:
            model: Model name (ignored, uses deployment from settings)
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the API

        Returns:
            API response dictionary in OpenAI-compatible format

        Raises:
            httpx.HTTPError: If the request fails
        """
        # Build request URL
        url = (
            f"{self.endpoint}openai/deployments/{self.chat_deployment}"
            f"/chat/completions?api-version={self.api_version}"
        )

        # Build payload
        payload = {
            "messages": messages,
            "temperature": temperature,
            **kwargs,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        logger.debug(
            f"Azure OpenAI chat completion request | "
            f"Deployment: {self.chat_deployment} | "
            f"Messages: {len(messages)} | "
            f"Temperature: {temperature}"
        )

        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()

            logger.info(
                f"Azure OpenAI chat completion success | "
                f"Deployment: {self.chat_deployment} | "
                f"Tokens: {result.get('usage', {}).get('total_tokens', 'unknown')}"
            )

            return result

        except httpx.HTTPStatusError as e:
            logger.error(
                f"Azure OpenAI HTTP error | " f"Status: {e.response.status_code} | " f"Response: {e.response.text}"
            )
            raise
        except httpx.RequestError as e:
            logger.error(f"Azure OpenAI request error | Error: {e!s}")
            raise

    async def embedding(
        self,
        input: str | list[str],
        model: str | None = None,  # Ignored, uses deployment from settings
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Call Azure OpenAI embeddings API.

        Args:
            input: Text or list of texts to embed
            model: Model name (ignored, uses deployment from settings)
            **kwargs: Additional parameters for the API

        Returns:
            API response dictionary in OpenAI-compatible format

        Raises:
            httpx.HTTPError: If the request fails
        """
        # Build request URL
        url = (
            f"{self.endpoint}openai/deployments/{self.embedding_deployment}"
            f"/embeddings?api-version={self.api_version}"
        )

        # Build payload
        payload = {
            "input": input,
            **kwargs,
        }

        logger.debug(
            f"Azure OpenAI embedding request | "
            f"Deployment: {self.embedding_deployment} | "
            f"Input type: {type(input).__name__}"
        )

        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()

            logger.info(
                f"Azure OpenAI embedding success | "
                f"Deployment: {self.embedding_deployment} | "
                f"Tokens: {result.get('usage', {}).get('total_tokens', 'unknown')}"
            )

            return result

        except httpx.HTTPStatusError as e:
            logger.error(
                f"Azure OpenAI HTTP error | " f"Status: {e.response.status_code} | " f"Response: {e.response.text}"
            )
            raise
        except httpx.RequestError as e:
            logger.error(f"Azure OpenAI request error | Error: {e!s}")
            raise

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
        logger.debug("Azure OpenAI direct client closed")

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


# Singleton instance
_azure_openai_client: AzureOpenAIClient | None = None


def get_azure_openai_client() -> AzureOpenAIClient:
    """
    Get or create singleton Azure OpenAI client instance.

    Returns:
        AzureOpenAIClient instance
    """
    global _azure_openai_client
    if _azure_openai_client is None:
        _azure_openai_client = AzureOpenAIClient()
    return _azure_openai_client
