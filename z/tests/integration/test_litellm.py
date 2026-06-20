#!/usr/bin/env python3
"""
LiteLLM Integration Tests
Tests LiteLLM proxy functionality independently
"""

import os
import sys

import httpx


# Configuration
LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL", "http://localhost:4000")
LITELLM_API_KEY = os.getenv("LITELLM_MASTER_KEY", "sk-1234")

# Create httpx client with SSL disabled
client = httpx.Client(verify=False)


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    END = "\033[0m"
    BOLD = "\033[1m"


def print_test(name: str):
    print(f"\n{Colors.BLUE}{Colors.BOLD}[TEST]{Colors.END} {name}")


def print_success(message: str):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")


def print_error(message: str):
    print(f"{Colors.RED}✗{Colors.END} {message}")


def print_info(message: str):
    print(f"{Colors.YELLOW}ℹ{Colors.END} {message}")


def test_health():
    """Test LiteLLM health endpoint"""
    print_test("Testing LiteLLM Health Endpoint")

    try:
        response = client.get(f"{LITELLM_BASE_URL}/health")
        if response.status_code == 200:
            print_success(f"Health check passed: {response.status_code}")
            return True
        print_error(f"Health check failed: {response.status_code}")
        return False
    except Exception as e:
        print_error(f"Health check error: {e!s}")
        return False


def test_liveliness():
    """Test LiteLLM liveliness endpoint"""
    print_test("Testing LiteLLM Liveliness Endpoint")

    try:
        response = client.get(f"{LITELLM_BASE_URL}/health/liveliness")
        if response.status_code == 200:
            print_success(f"Liveliness check passed: {response.status_code}")
            return True
        print_error(f"Liveliness check failed: {response.status_code}")
        return False
    except Exception as e:
        print_error(f"Liveliness check error: {e!s}")
        return False


def test_readiness():
    """Test LiteLLM readiness endpoint"""
    print_test("Testing LiteLLM Readiness Endpoint")

    try:
        response = client.get(f"{LITELLM_BASE_URL}/health/readiness")
        if response.status_code == 200:
            data = response.json()
            print_success("Readiness check passed")
            print_info(f"Database: {data.get('db', 'unknown')}")
            print_info(f"Cache: {data.get('cache', 'unknown')}")
            return True
        print_error(f"Readiness check failed: {response.status_code}")
        return False
    except Exception as e:
        print_error(f"Readiness check error: {e!s}")
        return False


def test_models_list():
    """Test LiteLLM models list endpoint"""
    print_test("Testing LiteLLM Models List")

    try:
        headers = {"Authorization": f"Bearer {LITELLM_API_KEY}", "Content-Type": "application/json"}
        response = client.get(f"{LITELLM_BASE_URL}/v1/models", headers=headers)

        if response.status_code == 200:
            data = response.json()
            models = data.get("data", [])
            print_success(f"Models list retrieved: {len(models)} models")
            for model in models:
                print_info(f"  - {model.get('id', 'unknown')}")
            return True
        print_error(f"Models list failed: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False
    except Exception as e:
        print_error(f"Models list error: {e!s}")
        return False


def test_chat_completion():
    """Test LiteLLM chat completion (requires Azure OpenAI configured)"""
    print_test("Testing LiteLLM Chat Completion")

    try:
        headers = {"Authorization": f"Bearer {LITELLM_API_KEY}", "Content-Type": "application/json"}

        payload = {
            "model": "gpt-4.1",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Respond in one short sentence."},
                {"role": "user", "content": "Say 'LiteLLM test successful' if you can read this."},
            ],
            "max_tokens": 50,
            "temperature": 0.1,
        }

        response = client.post(
            f"{LITELLM_BASE_URL}/v1/chat/completions",
            headers=headers,
            json=payload,
        )

        if response.status_code == 200:
            data = response.json()
            message = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            print_success("Chat completion successful")
            print_info(f"Response: {message}")
            print_info(f"Model: {data.get('model', 'unknown')}")
            print_info(f"Tokens: {data.get('usage', {})}")
            return True
        print_error(f"Chat completion failed: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False
    except Exception as e:
        print_error(f"Chat completion error: {e!s}")
        return False


def test_embedding():
    """Test LiteLLM embedding endpoint"""
    print_test("Testing LiteLLM Embeddings")

    try:
        headers = {"Authorization": f"Bearer {LITELLM_API_KEY}", "Content-Type": "application/json"}

        payload = {"model": "text-embedding-3-small", "input": "Test embedding generation from LiteLLM"}

        response = client.post(f"{LITELLM_BASE_URL}/v1/embeddings", headers=headers, json=payload, timeout=30.0)

        if response.status_code == 200:
            data = response.json()
            embedding = data.get("data", [{}])[0].get("embedding", [])
            print_success("Embedding generation successful")
            print_info(f"Embedding dimension: {len(embedding)}")
            print_info(f"Model: {data.get('model', 'unknown')}")
            return True
        print_error(f"Embedding generation failed: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False
    except Exception as e:
        print_error(f"Embedding generation error: {e!s}")
        return False


def test_cache():
    """Test LiteLLM cache functionality"""
    print_test("Testing LiteLLM Cache")

    try:
        headers = {"Authorization": f"Bearer {LITELLM_API_KEY}", "Content-Type": "application/json"}

        # Make the same request twice to test caching
        payload = {
            "model": "gpt-4.1",
            "messages": [{"role": "user", "content": "Cache test: What is 2+2?"}],
            "max_tokens": 20,
            "temperature": 0,
        }

        # First request (cache miss)
        print_info("Making first request (cache miss expected)...")
        response1 = httpx.post(
            f"{LITELLM_BASE_URL}/v1/chat/completions",
            headers=headers,
            json=payload,
        )

        if response1.status_code != 200:
            print_error(f"First request failed: {response1.status_code}")
            return False

        # Second request (cache hit expected)
        print_info("Making second request (cache hit expected)...")
        response2 = httpx.post(
            f"{LITELLM_BASE_URL}/v1/chat/completions",
            headers=headers,
            json=payload,
        )

        if response2.status_code == 200:
            print_success("Cache test completed")
            print_info("Both requests successful - check logs for cache behavior")
            return True
        print_error(f"Second request failed: {response2.status_code}")
        return False
    except Exception as e:
        print_error(f"Cache test error: {e!s}")
        return False


def main():
    """Run all LiteLLM tests"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}LiteLLM Integration Tests{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"Base URL: {LITELLM_BASE_URL}")

    tests = [
        ("Health Check", test_health),
        ("Liveliness Check", test_liveliness),
        ("Readiness Check", test_readiness),
        ("Models List", test_models_list),
        ("Chat Completion", test_chat_completion),
        ("Embeddings", test_embedding),
        ("Cache Functionality", test_cache),
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print_error(f"Test crashed: {e!s}")
            results[test_name] = False

    # Print summary
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}Test Summary{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")

    passed = sum(1 for r in results.values() if r)
    total = len(results)

    for test_name, result in results.items():
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"{status} - {test_name}")

    print(f"\n{Colors.BOLD}Total: {passed}/{total} tests passed{Colors.END}")

    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All tests passed!{Colors.END}\n")
        return 0
    print(f"{Colors.RED}{Colors.BOLD}✗ Some tests failed{Colors.END}\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
