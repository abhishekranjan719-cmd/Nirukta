import httpx
import pytest


@pytest.mark.asyncio
async def test_full_chat_flow():
    """
    Integration test: React → Backend → Engine → Response

    This test validates the complete flow from frontend to backend to engine and back.
    Run this test with docker-compose services running.
    """
    # Send message to backend
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                "http://localhost:8000/api/chat",
                json={"message": "Hello, world!", "conversation_id": None},
            )

            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert data["response"].startswith("Echo:")
            assert "conversation_id" in data
            assert "timestamp" in data

            print("\nFull flow test passed!")
            print("Request: Hello, world!")
            print(f"Response: {data['response']}")
            print(f"Conversation ID: {data['conversation_id']}")

        except httpx.ConnectError:
            pytest.skip("Services not running. Start with 'docker-compose up' before running integration tests.")


@pytest.mark.asyncio
async def test_engine_directly():
    """Test engine processing directly"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                "http://localhost:8001/process",
                json={"message": "Test message", "context": None},
            )

            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert data["response"] == "Echo: Test message"
            assert "metadata" in data

            print("\nEngine test passed!")
            print("Request: Test message")
            print(f"Response: {data['response']}")

        except httpx.ConnectError:
            pytest.skip("Engine service not running.")


@pytest.mark.asyncio
async def test_health_checks():
    """Test health endpoints for all services"""
    services = [
        ("Backend", "http://localhost:8000/health"),
        ("Engine", "http://localhost:8001/health"),
    ]

    async with httpx.AsyncClient(timeout=10.0) as client:
        for service_name, url in services:
            try:
                response = await client.get(url)
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "ok"
                print(f"{service_name} health check: OK")
            except httpx.ConnectError:
                pytest.skip(f"{service_name} service not running.")


@pytest.mark.asyncio
async def test_conversation_persistence():
    """Test that conversations are persisted in memory"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Send first message
            response1 = await client.post(
                "http://localhost:8000/api/chat",
                json={"message": "First message", "conversation_id": None},
            )
            assert response1.status_code == 200
            conversation_id = response1.json()["conversation_id"]

            # Send second message to same conversation
            response2 = await client.post(
                "http://localhost:8000/api/chat",
                json={
                    "message": "Second message",
                    "conversation_id": conversation_id,
                },
            )
            assert response2.status_code == 200

            # Get conversation history
            response3 = await client.get(f"http://localhost:8000/api/conversations/{conversation_id}")
            assert response3.status_code == 200
            conversation = response3.json()

            # Should have 4 messages (2 user + 2 assistant)
            assert len(conversation["messages"]) == 4

            print("\nConversation persistence test passed!")
            print(f"Conversation ID: {conversation_id}")
            print(f"Message count: {len(conversation['messages'])}")

        except httpx.ConnectError:
            pytest.skip("Services not running.")
