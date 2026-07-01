"""Tests for the user management router."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import base64

from src.main import app
from src.enums.app_enums import UserRole
from src.utils.security import get_current_user

client = TestClient(app)

def override_get_current_user_admin():
    """Return an admin user for dependency override in router tests."""
    return {"email": "admin@nucleusteq.com", "role": UserRole.ADMIN.value}

def override_get_current_user_hr():
    """Return an HR user for dependency override in router tests."""
    return {"email": "hr@nucleusteq.com", "role": UserRole.HR.value}

class TestUserRouter:
    def test_unauthorized_access_rejected(self):
        """Reject access when no authenticated user is available."""
        response = client.get("/api/v1/users/")
        assert response.status_code == 401

    def test_hr_role_rejected(self):
        """Reject access for roles that are not allowed to manage users."""
        app.dependency_overrides[get_current_user] = override_get_current_user_hr

        response = client.get("/api/v1/users/")
        assert response.status_code == 403
        assert response.json()["message"] == "You do not have permission to perform this action"

        app.dependency_overrides.clear()

    @patch('src.routers.user_router.UserService')
    def test_create_user_endpoint_success(self, mock_user_service_class):
        """Create a user successfully through the router."""
        app.dependency_overrides[get_current_user] = override_get_current_user_admin

        mock_instance = mock_user_service_class.return_value
        mock_instance.create_user = AsyncMock(return_value={"email": "new@nucleusteq.com", "role": "HR"})

        payload = {"email": "new@nucleusteq.com", "role": "HR"}

        response = client.post("/api/v1/users/", json=payload)

        assert response.status_code == 200
        assert response.json()["data"]["email"] == "new@nucleusteq.com"
        assert response.json()["message"] == "User created successfully"

        app.dependency_overrides.clear()

    def test_create_user_pydantic_validation_fails(self):
        """Surface validation errors before the request reaches the service."""
        app.dependency_overrides[get_current_user] = override_get_current_user_admin

        payload = {"email": "bad_actor@gmail.com", "role": "HR"}

        response = client.post("/api/v1/users/", json=payload)

        assert response.status_code == 422
        assert "Email must belong to nucleusteq.com domain" in response.text

        app.dependency_overrides.clear()

    @patch('src.routers.user_router.UserService')
    def test_disable_user_endpoint_success(self, mock_user_service_class):
        """Disable a user successfully through the router."""
        app.dependency_overrides[get_current_user] = override_get_current_user_admin

        mock_instance = mock_user_service_class.return_value
        mock_instance.disable_user = AsyncMock(return_value=None)

        response = client.patch("/api/v1/users/123/disable")

        assert response.status_code == 200
        assert response.json()["message"] == "User disabled successfully"

        app.dependency_overrides.clear()
