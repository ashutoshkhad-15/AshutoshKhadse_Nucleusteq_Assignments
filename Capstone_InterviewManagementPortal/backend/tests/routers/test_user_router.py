"""Tests for the user management router."""

from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.enums.app_enums import UserRole
from src.main import app
from src.routers.user_router import get_user_service
from src.utils.security import get_current_user


@pytest.fixture
def mock_user_service():
    """Provide a mocked user service instance."""
    service = AsyncMock()
    service.create_user = AsyncMock()
    service.get_all_users = AsyncMock()
    service.get_user_by_id = AsyncMock()
    service.update_user = AsyncMock()
    service.disable_user = AsyncMock()
    return service


@pytest.fixture
def client(mock_user_service):
    """Return a test client with the user service dependency overridden."""
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def override_get_current_user_admin():
    """Return an admin user for dependency override in router tests."""
    return {"email": "admin@nucleusteq.com", "role": UserRole.ADMIN.value}


def override_get_current_user_hr():
    """Return an HR user for dependency override in router tests."""
    return {"email": "hr@nucleusteq.com", "role": UserRole.HR.value}

class TestUserRouter:
    def test_unauthorized_access_rejected(self, client):
        """Reject access when no authenticated user is available."""
        response = client.get("/api/v1/users/")
        assert response.status_code == 401

    def test_hr_role_rejected(self, client):
        """Reject access for roles that are not allowed to manage users."""
        app.dependency_overrides[get_current_user] = override_get_current_user_hr

        response = client.get("/api/v1/users/")
        assert response.status_code == 403
        assert response.json()["message"] == "You do not have permission to perform this action"

        app.dependency_overrides.clear()

    def test_create_user_endpoint_success(self, client, mock_user_service):
        """Create a user successfully through the router."""
        app.dependency_overrides[get_current_user] = override_get_current_user_admin

        mock_user_service.create_user.return_value = {"name": "New User", "email": "new@nucleusteq.com", "role": "HR"}

        payload = {"name": "New User", "email": "new@nucleusteq.com", "role": "HR"}

        response = client.post("/api/v1/users/", json=payload)

        assert response.status_code == 200
        assert response.json()["data"]["email"] == "new@nucleusteq.com"
        assert response.json()["message"] == "User created successfully"

        app.dependency_overrides.clear()

    def test_create_user_pydantic_validation_fails(self, client):
        """Surface validation errors before the request reaches the service."""
        app.dependency_overrides[get_current_user] = override_get_current_user_admin

        payload = {"name": "Bad Actor", "email": "bad_actor@gmail.com", "role": "HR"}

        response = client.post("/api/v1/users/", json=payload)

        assert response.status_code == 422
        assert "Email must belong to nucleusteq.com domain" in response.text

        app.dependency_overrides.clear()

    def test_create_user_pydantic_validation_rejects_invalid_format(self, client):
        """Reject emails that violate the NucleusTeq corporate format rules."""
        app.dependency_overrides[get_current_user] = override_get_current_user_admin

        payload = {"name": "Bad Actor", "email": "bad_actor@nucleusteq.com", "role": "HR"}

        response = client.post("/api/v1/users/", json=payload)

        assert response.status_code == 422
        assert "valid NucleusTeq" in response.text

        app.dependency_overrides.clear()

    def test_disable_user_endpoint_success(self, client, mock_user_service):
        """Disable a user successfully through the router."""
        app.dependency_overrides[get_current_user] = override_get_current_user_admin

        mock_user_service.disable_user.return_value = None

        response = client.patch("/api/v1/users/123/disable")

        assert response.status_code == 200
        assert response.json()["message"] == "User disabled successfully"

        app.dependency_overrides.clear()
