"""Unit tests for authentication service and security helpers.

The tests isolate authentication business rules from MongoDB by replacing the
user repository with asynchronous mocks. Security helper tests validate password
encoding and protected-route credential checks without external services.
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.security import HTTPBasicCredentials

from src.enums.app_enums import UserRole
from src.exceptions.custom_exceptions import (
    AppBaseException,
    ForbiddenException,
    UnauthorizedException,
)
from src.schemas.request.auth_request import LoginRequest, ResetPasswordRequest
from src.services.auth_service import AuthService
from src.utils.security import encode_password, get_current_user


@pytest.fixture
def auth_service():
    """Provide an AuthService wired to a mocked user repository.

    Yields:
        AuthService: Service instance whose repository methods are async mocks.
    """
    with patch("src.services.auth_service.UserRepository") as mock_repo_class:
        mock_repo = mock_repo_class.return_value
        mock_repo.get_user_by_email = AsyncMock()
        mock_repo.update_user = AsyncMock()

        service = AuthService()
        service.user_repo = mock_repo

        yield service


@pytest.fixture
def active_hr_user():
    """Provide a reusable active HR user document.

    Returns:
        dict: Mock user document matching the repository contract.
    """
    return {
        "_id": "user-123",
        "email": "hr@nucleusteq.com",
        "password_base64": encode_password("Password@1"),
        "role": UserRole.HR.value,
        "is_active": True,
        "requires_password_reset": False,
    }


class TestAuthServiceLogin:
    """Validate login business rules in the authentication service."""

    async def test_login_returns_user_metadata_for_valid_credentials(
        self,
        auth_service,
        active_hr_user,
    ):
        """Return email, role, and reset flag for a valid login."""
        auth_service.user_repo.get_user_by_email.return_value = active_hr_user

        request = LoginRequest(email="hr@nucleusteq.com", password="Password@1")
        response = await auth_service.login(request)

        assert response == {
            "email": "hr@nucleusteq.com",
            "role": "HR",
            "requires_password_reset": False,
        }
        auth_service.user_repo.get_user_by_email.assert_awaited_once_with(
            "hr@nucleusteq.com"
        )

    async def test_login_preserves_password_reset_flag(
        self,
        auth_service,
        active_hr_user,
    ):
        """Return first-login reset state when stored on the user document."""
        active_hr_user["requires_password_reset"] = True
        auth_service.user_repo.get_user_by_email.return_value = active_hr_user

        request = LoginRequest(email="hr@nucleusteq.com", password="Password@1")
        response = await auth_service.login(request)

        assert response["requires_password_reset"] is True

    async def test_login_preserves_user_role_from_repository(
        self,
        auth_service,
        active_hr_user,
    ):
        """Return the role stored on the authenticated user document."""
        active_hr_user["role"] = UserRole.INTERVIEWER.value
        auth_service.user_repo.get_user_by_email.return_value = active_hr_user

        request = LoginRequest(email="hr@nucleusteq.com", password="Password@1")
        response = await auth_service.login(request)

        assert response["role"] == "INTERVIEWER"

    async def test_login_raises_unauthorized_for_unknown_user(self, auth_service):
        """Raise UnauthorizedException when repository lookup returns no user."""
        auth_service.user_repo.get_user_by_email.return_value = None

        request = LoginRequest(email="missing@nucleusteq.com", password="Password@1")

        with pytest.raises(UnauthorizedException) as excinfo:
            await auth_service.login(request)

        assert excinfo.value.message == "Invalid email or password"

    async def test_login_raises_unauthorized_for_invalid_password(
        self,
        auth_service,
        active_hr_user,
    ):
        """Raise UnauthorizedException when password verification fails."""
        auth_service.user_repo.get_user_by_email.return_value = active_hr_user

        request = LoginRequest(email="hr@nucleusteq.com", password="WrongPass")

        with pytest.raises(UnauthorizedException) as excinfo:
            await auth_service.login(request)

        assert excinfo.value.message == "Invalid email or password"

    async def test_login_raises_unauthorized_for_disabled_account(
        self,
        auth_service,
        active_hr_user,
    ):
        """Raise UnauthorizedException when account status is inactive."""
        active_hr_user["is_active"] = False
        auth_service.user_repo.get_user_by_email.return_value = active_hr_user

        request = LoginRequest(email="hr@nucleusteq.com", password="Password@1")

        with pytest.raises(UnauthorizedException) as excinfo:
            await auth_service.login(request)

        assert excinfo.value.message == "Account is disabled"


class TestAuthServiceResetPassword:
    """Validate password reset business rules in the authentication service."""

    async def test_reset_password_updates_encoded_password_and_reset_flag(
        self,
        auth_service,
        active_hr_user,
    ):
        """Update stored password and clear the reset-required flag."""
        auth_service.user_repo.get_user_by_email.return_value = active_hr_user
        request = ResetPasswordRequest(
            email="hr@nucleusteq.com",
            old_password="Password@1",
            new_password="NewPass@1",
        )

        await auth_service.reset_password(request)

        auth_service.user_repo.update_user.assert_awaited_once_with(
            email="hr@nucleusteq.com",
            update_data={
                "password_base64": encode_password("NewPass@1"),
                "requires_password_reset": False,
            },
        )

    async def test_reset_password_raises_unauthorized_for_unknown_user(
        self,
        auth_service,
    ):
        """Raise UnauthorizedException when password reset user is missing."""
        auth_service.user_repo.get_user_by_email.return_value = None
        request = ResetPasswordRequest(
            email="missing@nucleusteq.com",
            old_password="Password@1",
            new_password="NewPass@1",
        )

        with pytest.raises(UnauthorizedException) as excinfo:
            await auth_service.reset_password(request)

        assert excinfo.value.message == "Invalid email or old password"
        auth_service.user_repo.update_user.assert_not_awaited()

    async def test_reset_password_raises_unauthorized_for_wrong_old_password(
        self,
        auth_service,
        active_hr_user,
    ):
        """Raise UnauthorizedException when the current password is wrong."""
        auth_service.user_repo.get_user_by_email.return_value = active_hr_user
        request = ResetPasswordRequest(
            email="hr@nucleusteq.com",
            old_password="WrongPass",
            new_password="NewPass@1",
        )

        with pytest.raises(UnauthorizedException) as excinfo:
            await auth_service.reset_password(request)

        assert excinfo.value.message == "Invalid email or old password"
        auth_service.user_repo.update_user.assert_not_awaited()


class TestSecurityHelpers:
    """Validate password encoding and Basic Auth user resolution."""

    def test_encode_password_returns_base64_encoded_value(self):
        """Encode plaintext passwords using the configured Base64 contract."""
        assert encode_password("Password@1") == "UGFzc3dvcmRAMQ=="

    async def test_get_current_user_returns_active_user_for_valid_credentials(
        self,
        active_hr_user,
    ):
        """Return the user document for valid Basic Auth credentials."""
        with patch("src.utils.security.UserRepository") as mock_repo_class:
            mock_repo = mock_repo_class.return_value
            mock_repo.get_user_by_email = AsyncMock(return_value=active_hr_user)
            credentials = HTTPBasicCredentials(
                username="hr@nucleusteq.com",
                password="Password@1",
            )

            user = await get_current_user(credentials)

        assert user == active_hr_user
        mock_repo.get_user_by_email.assert_awaited_once_with("hr@nucleusteq.com")

    async def test_get_current_user_raises_unauthorized_for_bad_password(
        self,
        active_hr_user,
    ):
        """Raise UnauthorizedException when Basic Auth password is invalid."""
        with patch("src.utils.security.UserRepository") as mock_repo_class:
            mock_repo = mock_repo_class.return_value
            mock_repo.get_user_by_email = AsyncMock(return_value=active_hr_user)
            credentials = HTTPBasicCredentials(
                username="hr@nucleusteq.com",
                password="WrongPass",
            )

            with pytest.raises(UnauthorizedException) as excinfo:
                await get_current_user(credentials)

        assert excinfo.value.message == "Invalid email or password"

    async def test_get_current_user_raises_for_disabled_account(
        self,
        active_hr_user,
    ):
        """Raise ForbiddenException when Basic Auth user is disabled."""
        active_hr_user["is_active"] = False

        with patch("src.utils.security.UserRepository") as mock_repo_class:
            mock_repo = mock_repo_class.return_value
            mock_repo.get_user_by_email = AsyncMock(return_value=active_hr_user)
            credentials = HTTPBasicCredentials(
                username="hr@nucleusteq.com",
                password="Password@1",
            )

            with pytest.raises(ForbiddenException) as excinfo:
                await get_current_user(credentials)

        assert excinfo.value.message == "User account is disabled"

    async def test_get_current_user_raises_when_password_reset_is_required(
        self,
        active_hr_user,
    ):
        """Raise AppBaseException when first-login password reset is pending."""
        active_hr_user["requires_password_reset"] = True

        with patch("src.utils.security.UserRepository") as mock_repo_class:
            mock_repo = mock_repo_class.return_value
            mock_repo.get_user_by_email = AsyncMock(return_value=active_hr_user)
            credentials = HTTPBasicCredentials(
                username="hr@nucleusteq.com",
                password="Password@1",
            )

            with pytest.raises(AppBaseException) as excinfo:
                await get_current_user(credentials)

        assert excinfo.value.error_code == "PASSWORD_RESET_REQUIRED"
        assert excinfo.value.status_code == 403
