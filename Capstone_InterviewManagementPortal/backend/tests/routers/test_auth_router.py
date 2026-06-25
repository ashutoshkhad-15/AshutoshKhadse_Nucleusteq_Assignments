"""Unit tests for authentication API endpoints.

The tests validate request validation, HTTP status codes, response envelopes,
and service exception handling for login and password reset routes. Service
dependencies are mocked so router tests never access MongoDB.
"""

from unittest.mock import AsyncMock, patch

import pytest

from src.exceptions.custom_exceptions import UnauthorizedException


class TestLoginApi:
    """Verify login endpoint request and response behavior."""

    @patch("src.routers.auth_router.AuthService")
    def test_login_returns_success_response_for_valid_credentials(
        self,
        mock_auth_service_class,
        client,
    ):
        """Return HTTP 200 and user metadata for valid credentials."""
        expected_data = {
            "email": "hr@nucleusteq.com",
            "role": "HR",
            "requires_password_reset": False,
        }
        mock_service = mock_auth_service_class.return_value
        mock_service.login = AsyncMock(return_value=expected_data)

        response = client.post(
            "/api/v1/auth/login",
            json={"email": "hr@nucleusteq.com", "password": "Password@1"},
        )

        assert response.status_code == 200
        assert response.json() == {
            "success": True,
            "message": "Login successful",
            "data": expected_data,
            "meta": None,
        }
        mock_service.login.assert_awaited_once()

    @pytest.mark.parametrize(
        "payload",
        [
            {"email": "invalid-email", "password": "Password@1"},
            {"email": "hr@nucleusteq.com"},
            {"password": "Password@1"},
            {},
        ],
    )
    def test_login_returns_validation_error_for_invalid_payload(self, client, payload):
        """Return HTTP 422 when required login fields are missing or invalid."""
        response = client.post("/api/v1/auth/login", json=payload)

        assert response.status_code == 422
        body = response.json()
        assert body["success"] is False
        assert body["error_code"] == "VALIDATION_ERROR"
        assert body["message"] == "Invalid request parameters"
        assert body["details"]

    @patch("src.routers.auth_router.AuthService")
    def test_login_returns_unauthorized_for_incorrect_password(
        self,
        mock_auth_service_class,
        client,
    ):
        """Return HTTP 401 when the submitted password is incorrect."""
        mock_service = mock_auth_service_class.return_value
        mock_service.login = AsyncMock(
            side_effect=UnauthorizedException("Invalid email or password")
        )

        response = client.post(
            "/api/v1/auth/login",
            json={"email": "hr@nucleusteq.com", "password": "WrongPass"},
        )

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "error_code": "UNAUTHORIZED",
            "message": "Invalid email or password",
            "details": None,
        }

    @patch("src.routers.auth_router.AuthService")
    def test_login_returns_unauthorized_for_nonexistent_user(
        self,
        mock_auth_service_class,
        client,
    ):
        """Return HTTP 401 when no user exists for the submitted email."""
        mock_service = mock_auth_service_class.return_value
        mock_service.login = AsyncMock(
            side_effect=UnauthorizedException("Invalid email or password")
        )

        response = client.post(
            "/api/v1/auth/login",
            json={"email": "missing@nucleusteq.com", "password": "Password@1"},
        )

        assert response.status_code == 401
        assert response.json()["error_code"] == "UNAUTHORIZED"
        assert response.json()["message"] == "Invalid email or password"

    @patch("src.routers.auth_router.AuthService")
    def test_login_returns_unauthorized_for_disabled_account(
        self,
        mock_auth_service_class,
        client,
    ):
        """Return HTTP 401 when the account is disabled."""
        mock_service = mock_auth_service_class.return_value
        mock_service.login = AsyncMock(
            side_effect=UnauthorizedException("Account is disabled")
        )

        response = client.post(
            "/api/v1/auth/login",
            json={"email": "disabled@nucleusteq.com", "password": "Password@1"},
        )

        assert response.status_code == 401
        assert response.json()["message"] == "Account is disabled"

    @patch("src.routers.auth_router.AuthService")
    def test_login_response_preserves_authorized_role_from_service(
        self,
        mock_auth_service_class,
        client,
    ):
        """Return the role supplied by the authentication service."""
        mock_service = mock_auth_service_class.return_value
        mock_service.login = AsyncMock(
            return_value={
                "email": "interviewer@nucleusteq.com",
                "role": "INTERVIEWER",
                "requires_password_reset": False,
            }
        )

        response = client.post(
            "/api/v1/auth/login",
            json={"email": "interviewer@nucleusteq.com", "password": "Password@1"},
        )

        assert response.status_code == 200
        assert response.json()["data"]["role"] == "INTERVIEWER"


class TestResetPasswordApi:
    """Verify reset-password endpoint request and response behavior."""

    @patch("src.routers.auth_router.AuthService")
    def test_reset_password_returns_success_response_for_valid_request(
        self,
        mock_auth_service_class,
        client,
    ):
        """Return HTTP 200 when password reset succeeds."""
        mock_service = mock_auth_service_class.return_value
        mock_service.reset_password = AsyncMock(return_value=None)

        response = client.post(
            "/api/v1/auth/reset-password",
            json={
                "email": "hr@nucleusteq.com",
                "old_password": "OldPass@1",
                "new_password": "NewPass@1",
            },
        )

        assert response.status_code == 200
        assert response.json() == {
            "success": True,
            "message": "Password reset successfully",
            "data": None,
            "meta": None,
        }
        mock_service.reset_password.assert_awaited_once()

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "email": "invalid-email",
                "old_password": "OldPass@1",
                "new_password": "NewPass@1",
            },
            {
                "email": "hr@gmail.com",
                "old_password": "OldPass@1",
                "new_password": "NewPass@1",
            },
            {
                "email": "hr@nucleusteq.com",
                "old_password": "OldPass@1",
                "new_password": "short",
            },
            {
                "email": "hr@nucleusteq.com",
                "old_password": "OldPass@1",
                "new_password": "PasswordWithMoreThan12Chars",
            },
            {
                "email": "hr@nucleusteq.com",
                "old_password": "OldPass@1",
                "new_password": "Bad Pass",
            },
            {"email": "hr@nucleusteq.com", "old_password": "OldPass@1"},
            {},
        ],
    )
    def test_reset_password_returns_validation_error_for_invalid_payload(
        self,
        client,
        payload,
    ):
        """Return HTTP 422 when reset-password validation fails."""
        response = client.post("/api/v1/auth/reset-password", json=payload)

        assert response.status_code == 422
        body = response.json()
        assert body["success"] is False
        assert body["error_code"] == "VALIDATION_ERROR"
        assert body["message"] == "Invalid request parameters"
        assert body["details"]

    @patch("src.routers.auth_router.AuthService")
    def test_reset_password_returns_unauthorized_for_unknown_user(
        self,
        mock_auth_service_class,
        client,
    ):
        """Return HTTP 401 when no user exists for the submitted email."""
        mock_service = mock_auth_service_class.return_value
        mock_service.reset_password = AsyncMock(
            side_effect=UnauthorizedException("Invalid email or old password")
        )

        response = client.post(
            "/api/v1/auth/reset-password",
            json={
                "email": "missing@nucleusteq.com",
                "old_password": "OldPass@1",
                "new_password": "NewPass@1",
            },
        )

        assert response.status_code == 401
        assert response.json()["error_code"] == "UNAUTHORIZED"
        assert response.json()["message"] == "Invalid email or old password"

    @patch("src.routers.auth_router.AuthService")
    def test_reset_password_returns_unauthorized_for_incorrect_old_password(
        self,
        mock_auth_service_class,
        client,
    ):
        """Return HTTP 401 when the current password is incorrect."""
        mock_service = mock_auth_service_class.return_value
        mock_service.reset_password = AsyncMock(
            side_effect=UnauthorizedException("Invalid email or old password")
        )

        response = client.post(
            "/api/v1/auth/reset-password",
            json={
                "email": "hr@nucleusteq.com",
                "old_password": "WrongPass",
                "new_password": "NewPass@1",
            },
        )

        assert response.status_code == 401
        assert response.json()["message"] == "Invalid email or old password"

    @patch("src.routers.auth_router.AuthService")
    def test_reset_password_returns_unauthorized_for_disabled_account(
        self,
        mock_auth_service_class,
        client,
    ):
        """Return HTTP 401 when service rejects a disabled account."""
        mock_service = mock_auth_service_class.return_value
        mock_service.reset_password = AsyncMock(
            side_effect=UnauthorizedException("Account is disabled")
        )

        response = client.post(
            "/api/v1/auth/reset-password",
            json={
                "email": "disabled@nucleusteq.com",
                "old_password": "OldPass@1",
                "new_password": "NewPass@1",
            },
        )

        assert response.status_code == 401
        assert response.json()["message"] == "Account is disabled"
