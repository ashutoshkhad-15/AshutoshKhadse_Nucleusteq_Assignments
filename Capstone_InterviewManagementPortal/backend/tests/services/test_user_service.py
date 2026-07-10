"""Tests for the user service layer."""

import pytest
from unittest.mock import AsyncMock, patch
from src.services.user_service import UserService
from src.schemas.request.user_request import CreateUserRequest, UpdateUserRequest
from src.exceptions.custom_exceptions import AppBaseException
from src.enums.app_enums import UserRole

@pytest.fixture
def user_service():
    """Provide a service instance backed by a mocked repository."""
    with patch('src.services.user_service.UserRepository') as mock_repo_class, \
         patch('src.services.user_service.InterviewRepository') as mock_interview_repo_class, \
         patch('os.getenv', return_value="TestPassword@123"):
             
        mock_repo_instance = mock_repo_class.return_value
        mock_repo_instance.get_user_by_email = AsyncMock()
        mock_repo_instance.create_user = AsyncMock()
        mock_repo_instance.get_all_users = AsyncMock()
        mock_repo_instance.search_users = AsyncMock()
        mock_repo_instance.get_user_by_id = AsyncMock()
        mock_repo_instance.update_user_by_id = AsyncMock()
        mock_interview_repo_instance = mock_interview_repo_class.return_value
        mock_interview_repo_instance.has_scheduled_interviews_for_interviewer = AsyncMock(return_value=False)
        
        service = UserService()
        service.user_repo = mock_repo_instance
        service.interview_repo = mock_interview_repo_instance
        yield service

class TestUserService:
    async def test_create_user_success(self, user_service):
        """Create a user and strip sensitive credentials from the response."""
        user_service.user_repo.get_user_by_email.return_value = None
        user_service.user_repo.create_user.return_value = {"_id": "123", "email": "interviewer@nucleusteq.com", "password_base64": "hash"}

        request = CreateUserRequest(name="Interviewer User", email="interviewer@nucleusteq.com", role=UserRole.INTERVIEWER)
        result = await user_service.create_user(request)

        assert result["email"] == "interviewer@nucleusteq.com"
        assert "password_base64" not in result

    async def test_create_user_duplicate(self, user_service):
        """Reject duplicate user creation requests."""
        user_service.user_repo.get_user_by_email.return_value = {"email": "hr@nucleusteq.com"}
        request = CreateUserRequest(name="HR User", email="hr@nucleusteq.com", role=UserRole.HR)

        with pytest.raises(AppBaseException) as excinfo:
            await user_service.create_user(request)
        assert excinfo.value.error_code == "USER_EXISTS"

    async def test_get_all_users(self, user_service):
        """Return the full user list from the repository."""
        user_service.user_repo.get_all_users.return_value = [{"email": "test@nucleusteq.com"}]
        result = await user_service.get_all_users()
        assert len(result[0]) == 1

    async def test_search_users_returns_matching_results(self, user_service):
        """Return repository results for a sanitized search term."""
        user_service.user_repo.search_users.return_value = [{"email": "ashutosh@nucleusteq.com"}]

        result = await user_service.get_all_users(search="  Ashutosh  ")

        assert len(result[0]) == 1
        user_service.user_repo.search_users.assert_awaited_once_with("ashutosh", page=1, limit=10)

    async def test_get_user_by_id_not_found(self, user_service):
        """Raise a not-found error when the user does not exist."""
        user_service.user_repo.get_user_by_id.return_value = None
        with pytest.raises(AppBaseException) as excinfo:
            await user_service.get_user_by_id("fake_id")
        assert excinfo.value.error_code == "USER_NOT_FOUND"

    async def test_update_user_success(self, user_service):
        """Apply a partial user update and persist only populated fields."""
        user_service.user_repo.get_user_by_id.return_value = {"_id": "123", "email": "test@nucleusteq.com"}
        user_service.user_repo.update_user_by_id.return_value = None

        request = UpdateUserRequest(role=UserRole.ADMIN)
        await user_service.update_user("123", request)
        user_service.user_repo.update_user_by_id.assert_called_once_with("123", {"role": "ADMIN"})

    async def test_update_user_invalid_fields(self, user_service):
        """Reject update requests that do not contain any mutable fields."""
        user_service.user_repo.get_user_by_id.return_value = {"_id": "123"}
        request = UpdateUserRequest()

        with pytest.raises(AppBaseException) as excinfo:
            await user_service.update_user("123", request)
        assert excinfo.value.error_code == "INVALID_UPDATE"

    async def test_disable_user_success(self, user_service):
        """Disable a non-admin user account."""
        user_service.user_repo.get_user_by_id.return_value = {"_id": "123", "email": "interviewer@nucleusteq.com"}
        await user_service.disable_user("123")
        user_service.user_repo.update_user_by_id.assert_called_once_with("123", {"is_active": False})

    async def test_disable_primary_admin_fails(self, user_service):
        """Prevent the primary administrator account from being disabled."""
        user_service.user_repo.get_user_by_id.return_value = {"_id": "123", "email": "admin@nucleusteq.com"}
        with pytest.raises(AppBaseException) as excinfo:
            await user_service.disable_user("123")
        assert excinfo.value.error_code == "ACTION_DENIED"

    async def test_update_interviewer_with_scheduled_interviews_fails(self, user_service):
        user_service.user_repo.get_user_by_id.return_value = {"_id": "123", "email": "interviewer@nucleusteq.com", "role": UserRole.INTERVIEWER.value}
        user_service.interview_repo.has_scheduled_interviews_for_interviewer.return_value = True

        with pytest.raises(AppBaseException) as excinfo:
            await user_service.update_user("123", UpdateUserRequest(name="New Name"))

        assert excinfo.value.error_code == "VALIDATION_ERROR"

    async def test_update_default_admin_fails(self, user_service):
        user_service.user_repo.get_user_by_id.return_value = {"_id": "123", "email": "admin@nucleusteq.com", "role": UserRole.ADMIN.value}

        with pytest.raises(AppBaseException) as excinfo:
            await user_service.update_user("123", UpdateUserRequest(name="New Name"))

        assert excinfo.value.error_code == "ACTION_DENIED"

    async def test_create_user_missing_default_password_fails(self, user_service, monkeypatch):
        monkeypatch.setattr("src.services.user_service.settings.DEFAULT_USER_PASSWORD", "")
        user_service.user_repo.get_user_by_email.return_value = None

        with pytest.raises(AppBaseException) as excinfo:
            await user_service.create_user(CreateUserRequest(name="User One", email="user1@nucleusteq.com", role=UserRole.HR))

        assert excinfo.value.error_code == "SERVER_ERROR"
