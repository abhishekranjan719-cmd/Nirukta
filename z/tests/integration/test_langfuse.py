#!/usr/bin/env python3
"""
Langfuse Integration Tests
Tests Langfuse observability platform functionality independently
"""

import os
import sys
import time

import httpx


# Configuration
LANGFUSE_BASE_URL = os.getenv("LANGFUSE_HOST", "http://localhost:3000")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "lf_pk_a7b3c9d2e8f4a1b6c5d9e2f7a3b8c4d1")
LANGFUSE_SECRET_KEY = os.getenv(
    "LANGFUSE_SECRET_KEY", "lf_sk_f2a8b7c3d9e1f6a4b2c7d8e3f9a1b5c6d2e8f4a9b3c1d7e2f8a4b6c9d1e5f3a7"
)

# Create httpx client with SSL disabled
client = httpx.Client(verify=False, timeout=30.0)


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
    """Test Langfuse public health endpoint"""
    print_test("Testing Langfuse Public Health Endpoint")

    try:
        response = client.get(f"{LANGFUSE_BASE_URL}/api/public/health")
        if response.status_code == 200:
            data = response.json()
            print_success("Health check passed")
            print_info(f"Status: {data.get('status', 'unknown')}")
            print_info(f"Version: {data.get('version', 'unknown')}")
            return True
        print_error(f"Health check failed: {response.status_code}")
        return False
    except Exception as e:
        print_error(f"Health check error: {e!s}")
        return False


def test_web_ui():
    """Test Langfuse web UI accessibility"""
    print_test("Testing Langfuse Web UI")

    try:
        response = client.get(LANGFUSE_BASE_URL, timeout=10.0, follow_redirects=True)
        if response.status_code == 200 and "langfuse" in response.text.lower():
            print_success("Web UI accessible")
            return True
        print_error(f"Web UI check failed: {response.status_code}")
        return False
    except Exception as e:
        print_error(f"Web UI check error: {e!s}")
        return False


def test_project_list():
    """Test Langfuse API - List projects"""
    print_test("Testing Langfuse Projects API")

    try:
        auth = httpx.BasicAuth(LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY)
        response = client.get(f"{LANGFUSE_BASE_URL}/api/public/v2/projects", auth=auth, timeout=10.0)

        if response.status_code == 200:
            data = response.json()
            projects = data.get("data", [])
            print_success("Projects API accessible")
            print_info(f"Found {len(projects)} project(s)")
            for project in projects:
                print_info(f"  - {project.get('name', 'unknown')} (ID: {project.get('id', 'unknown')})")
            return True
        print_error(f"Projects API failed: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False
    except Exception as e:
        print_error(f"Projects API error: {e!s}")
        return False


def test_trace_ingestion():
    """Test Langfuse API - Ingest a trace"""
    print_test("Testing Langfuse Trace Ingestion")

    try:
        auth = httpx.BasicAuth(LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY)

        # Create a simple trace
        trace_id = f"test-trace-{int(time.time())}"
        payload = {
            "id": trace_id,
            "name": "test-trace",
            "userId": "test-user",
            "metadata": {"test": True, "source": "integration-test"},
            "tags": ["test", "integration"],
        }

        response = httpx.post(f"{LANGFUSE_BASE_URL}/api/public/traces", auth=auth, json=payload, timeout=10.0)

        if response.status_code in [200, 201]:
            print_success("Trace ingestion successful")
            print_info(f"Trace ID: {trace_id}")
            return True
        print_error(f"Trace ingestion failed: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False
    except Exception as e:
        print_error(f"Trace ingestion error: {e!s}")
        return False


def test_span_ingestion():
    """Test Langfuse API - Ingest a span"""
    print_test("Testing Langfuse Span Ingestion")

    try:
        auth = httpx.BasicAuth(LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY)

        # Create a simple span
        trace_id = f"test-trace-{int(time.time())}"
        span_id = f"test-span-{int(time.time())}"

        # First create the trace
        trace_payload = {"id": trace_id, "name": "test-trace-with-span"}
        client.post(f"{LANGFUSE_BASE_URL}/api/public/traces", auth=auth, json=trace_payload, timeout=10.0)

        # Then create a span
        span_payload = {
            "id": span_id,
            "traceId": trace_id,
            "name": "test-span",
            "startTime": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
            "endTime": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(time.time() + 1)),
            "metadata": {"test": True},
        }

        response = httpx.post(f"{LANGFUSE_BASE_URL}/api/public/spans", auth=auth, json=span_payload, timeout=10.0)

        if response.status_code in [200, 201]:
            print_success("Span ingestion successful")
            print_info(f"Span ID: {span_id}")
            return True
        print_error(f"Span ingestion failed: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False
    except Exception as e:
        print_error(f"Span ingestion error: {e!s}")
        return False


def test_generation_ingestion():
    """Test Langfuse API - Ingest a generation (LLM call)"""
    print_test("Testing Langfuse Generation Ingestion")

    try:
        auth = httpx.BasicAuth(LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY)

        # Create a generation
        trace_id = f"test-trace-{int(time.time())}"
        generation_id = f"test-gen-{int(time.time())}"

        # First create the trace
        trace_payload = {"id": trace_id, "name": "test-trace-with-generation"}
        client.post(f"{LANGFUSE_BASE_URL}/api/public/traces", auth=auth, json=trace_payload, timeout=10.0)

        # Create generation
        generation_payload = {
            "id": generation_id,
            "traceId": trace_id,
            "name": "test-generation",
            "startTime": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
            "endTime": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(time.time() + 2)),
            "model": "gpt-4.1",
            "modelParameters": {"temperature": 0.7, "max_tokens": 100},
            "input": [{"role": "user", "content": "Test message"}],
            "output": {"role": "assistant", "content": "Test response"},
            "usage": {"promptTokens": 10, "completionTokens": 5, "totalTokens": 15},
            "metadata": {"test": True},
        }

        response = httpx.post(
            f"{LANGFUSE_BASE_URL}/api/public/generations", auth=auth, json=generation_payload, timeout=10.0
        )

        if response.status_code in [200, 201]:
            print_success("Generation ingestion successful")
            print_info(f"Generation ID: {generation_id}")
            return True
        print_error(f"Generation ingestion failed: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False
    except Exception as e:
        print_error(f"Generation ingestion error: {e!s}")
        return False


def test_score_ingestion():
    """Test Langfuse API - Ingest a score"""
    print_test("Testing Langfuse Score Ingestion")

    try:
        auth = httpx.BasicAuth(LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY)

        # Create a score
        trace_id = f"test-trace-{int(time.time())}"
        score_id = f"test-score-{int(time.time())}"

        # First create the trace
        trace_payload = {"id": trace_id, "name": "test-trace-with-score"}
        client.post(f"{LANGFUSE_BASE_URL}/api/public/traces", auth=auth, json=trace_payload, timeout=10.0)

        # Create score
        score_payload = {
            "id": score_id,
            "traceId": trace_id,
            "name": "quality",
            "value": 0.95,
            "comment": "Test score from integration test",
        }

        response = httpx.post(f"{LANGFUSE_BASE_URL}/api/public/scores", auth=auth, json=score_payload, timeout=10.0)

        if response.status_code in [200, 201]:
            print_success("Score ingestion successful")
            print_info(f"Score ID: {score_id}")
            return True
        print_error(f"Score ingestion failed: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False
    except Exception as e:
        print_error(f"Score ingestion error: {e!s}")
        return False


def test_trace_retrieval():
    """Test Langfuse API - Retrieve traces"""
    print_test("Testing Langfuse Trace Retrieval")

    try:
        auth = httpx.BasicAuth(LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY)

        response = client.get(
            f"{LANGFUSE_BASE_URL}/api/public/traces", auth=auth, params={"page": 1, "limit": 10}, timeout=10.0
        )

        if response.status_code == 200:
            data = response.json()
            traces = data.get("data", [])
            print_success("Trace retrieval successful")
            print_info(f"Retrieved {len(traces)} trace(s)")
            return True
        print_error(f"Trace retrieval failed: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False
    except Exception as e:
        print_error(f"Trace retrieval error: {e!s}")
        return False


def main():
    """Run all Langfuse tests"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}Langfuse Integration Tests{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"Base URL: {LANGFUSE_BASE_URL}")
    print(f"Public Key: {LANGFUSE_PUBLIC_KEY[:20]}...")

    tests = [
        ("Public Health Check", test_health),
        ("Web UI Accessibility", test_web_ui),
        ("Projects API", test_project_list),
        ("Trace Ingestion", test_trace_ingestion),
        ("Span Ingestion", test_span_ingestion),
        ("Generation Ingestion", test_generation_ingestion),
        ("Score Ingestion", test_score_ingestion),
        ("Trace Retrieval", test_trace_retrieval),
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
