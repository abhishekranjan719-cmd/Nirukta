"""
LiteLLM Proxy Client

This module provides a client for interacting with the LiteLLM proxy service.
LiteLLM is a unified LLM gateway that provides OpenAI-compatible API.
"""

from typing import Any

import httpx
from loguru import logger

from app.config import settings


class LiteLLMClient:
    """
    Client for LiteLLM proxy service.

    Features:
    - SSL verification disabled for local development
    - Automatic authentication with master key
    - Support for chat completions API
    - Error handling and retry logic
    """

    def __init__(self):
        """Initialize LiteLLM client with configuration from settings."""
        self.base_url = settings.litellm.litellm_base_url
        self.master_key = settings.litellm.litellm_master_key
        self.timeout = settings.engine_llm_timeout
        self.ssl_verify = settings.engine_http_ssl_verify

        # Create httpx client with configurable SSL verification
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            verify=self.ssl_verify,
            headers={
                "Authorization": f"Bearer {self.master_key}",
                "Content-Type": "application/json",
            },
        )

        logger.info(
            f"LiteLLM client initialized | "
            f"Base URL: {self.base_url} | "
            f"Timeout: {self.timeout}s | "
            f"SSL Verify: {self.ssl_verify}"
        )

    async def chat_completion(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Call LiteLLM chat completions API.

        Args:
            model: Model name (e.g., 'gpt-4.1', 'gpt-4')
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the API

        Returns:
            API response dictionary

        Raises:
            httpx.HTTPError: If the request fails
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            **kwargs,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        logger.debug(
            f"LiteLLM chat completion request | "
            f"Model: {model} | "
            f"Messages: {len(messages)} | "
            f"Temperature: {temperature}"
        )

        try:
            response = await self.client.post(
                "/v1/chat/completions",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()

            logger.info(
                f"LiteLLM chat completion success | "
                f"Model: {model} | "
                f"Tokens: {result.get('usage', {}).get('total_tokens', 'unknown')}"
            )

            return result

        except httpx.HTTPStatusError as e:
            logger.error(f"LiteLLM HTTP error | " f"Status: {e.response.status_code} | " f"Response: {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"LiteLLM request error | Error: {e!s}")
            raise

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
        logger.debug("LiteLLM client closed")

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


# Singleton instance
_litellm_client: LiteLLMClient | None = None


def get_litellm_client() -> LiteLLMClient:
    """
    Get or create singleton LiteLLM client instance.

    Returns:
        LiteLLMClient instance
    """
    global _litellm_client
    if _litellm_client is None:
        _litellm_client = LiteLLMClient()
    return _litellm_client
