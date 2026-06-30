"""Shared pytest fixtures for backend router and service tests."""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """Provide a FastAPI TestClient for router tests.

    Returns:
        TestClient: Synchronous test client bound to the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def mock_admin_user():
    """Provide a standard active administrator user document.

    Returns:
        dict: Mock user document matching the authentication service contract.
    """
    from src.utils.security import encode_password
    from src.enums.app_enums import UserRole
    
    return {
        "_id": "mock_id_123",
        "email": "admin@nucleusteq.com",
        "password_base64": encode_password("Admin@123"),
        "role": UserRole.ADMIN.value,
        "is_active": True,
        "requires_password_reset": False
    }
