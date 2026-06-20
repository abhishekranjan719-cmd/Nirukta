import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def backend_client():
    """Create a test client for the backend API"""
    import sys
    from pathlib import Path

    # Add backend directory to path
    backend_path = Path(__file__).parent.parent / "backend"
    sys.path.insert(0, str(backend_path))

    from app.main import app

    return TestClient(app)


@pytest.fixture
def engine_client():
    """Create a test client for the engine API"""
    import sys
    from pathlib import Path

    # Add engine directory to path
    engine_path = Path(__file__).parent.parent / "engine"
    sys.path.insert(0, str(engine_path))

    from app.main import app

    return TestClient(app)
