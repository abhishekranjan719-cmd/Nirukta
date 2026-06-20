from unittest.mock import AsyncMock, MagicMock, patch


def test_health_endpoint(backend_client):
    """Test the health check endpoint"""
    response = backend_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "backend"
    assert "timestamp" in data


def test_list_conversations_empty(backend_client):
    """Test listing conversations when none exist"""
    response = backend_client.get("/api/conversations")
    assert response.status_code == 200
    data = response.json()
    assert "conversations" in data
    assert len(data["conversations"]) == 0


def test_chat_endpoint(backend_client):
    """Test sending a chat message"""
    # Mock the engine response at the async context manager level
    with patch("httpx.AsyncClient") as mock_client_class:
        # Create mock client instance
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client

        # Setup mock response (use MagicMock, not AsyncMock for the response object)
        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value={"response": "Echo: Hello", "metadata": {}})
        mock_response.raise_for_status = MagicMock()
        mock_response.status_code = 200

        # Make the post method return the mock response (wrapped in awaitable)
        async def mock_post(*args, **kwargs):
            return mock_response

        mock_client.post = mock_post

        # Send chat request
        response = backend_client.post("/api/chat", json={"message": "Hello", "conversation_id": None})

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "conversation_id" in data
        assert "timestamp" in data


def test_chat_endpoint_invalid_request(backend_client):
    """Test chat endpoint with invalid request"""
    response = backend_client.post("/api/chat", json={})
    assert response.status_code == 422  # Validation error


def test_get_conversation_not_found(backend_client):
    """Test getting a conversation that doesn't exist"""
    response = backend_client.get("/api/conversations/non-existent-id")
    assert response.status_code == 404
