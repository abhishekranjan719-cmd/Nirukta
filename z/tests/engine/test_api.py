def test_health_endpoint(engine_client):
    """Test the health check endpoint"""
    response = engine_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "engine"
    assert "timestamp" in data


def test_root_endpoint(engine_client):
    """Test the root endpoint"""
    response = engine_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Zuna Engine"
    assert "endpoints" in data


def test_process_endpoint(engine_client):
    """Test message processing"""
    response = engine_client.post("/process", json={"message": "Hello", "context": None})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "metadata" in data
    assert data["response"] == "Echo: Hello"


def test_process_endpoint_with_context(engine_client):
    """Test processing with context"""
    response = engine_client.post("/process", json={"message": "Test", "context": {"user": "test"}})
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Echo: Test"


def test_process_endpoint_invalid_request(engine_client):
    """Test process endpoint with invalid request"""
    response = engine_client.post("/process", json={})
    assert response.status_code == 422  # Validation error
