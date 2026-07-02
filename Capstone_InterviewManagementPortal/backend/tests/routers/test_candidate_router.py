"""Router tests for candidate management APIs."""

from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.enums.app_enums import UserRole
from src.main import app
from src.routers.candidate_router import get_candidate_service
from src.services.candidate_service import CandidateService
from src.utils.security import get_current_user


@pytest.fixture
def mock_candidate_service():
    """Provide a mocked candidate service for router tests."""
    return AsyncMock(spec=CandidateService)


@pytest.fixture
def client(mock_candidate_service):
    """Provide a test client with the candidate service dependency overridden."""
    app.dependency_overrides[get_candidate_service] = lambda: mock_candidate_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def override_get_current_user_hr():
    """Return an HR user for dependency override tests."""
    return {"email": "hr@nucleusteq.com", "role": UserRole.HR.value}


def override_get_current_user_admin():
    """Return an admin user for dependency override tests."""
    return {"email": "admin@nucleusteq.com", "role": UserRole.ADMIN.value}


def override_get_current_user_interviewer():
    """Return an interviewer user for dependency override tests."""
    return {"email": "int@nucleusteq.com", "role": UserRole.INTERVIEWER.value}


class TestCandidateRouter:
    def test_create_candidate_endpoint_success(self, client, mock_candidate_service):
        """Allow HR users to create candidates successfully."""
        app.dependency_overrides[get_current_user] = override_get_current_user_hr
        mock_candidate_service.create_candidate.return_value = {
            "_id": "123",
            "name": "Ashutosh Khadse",
        }

        response = client.post(
            "/api/v1/candidates/",
            json={
                "name": "Ashutosh Khadse",
                "email": "ashutosh.khadse@nucleusteq.com",
                "mobile": "9876543210",
            },
        )

        assert response.status_code == 201
        assert response.json()["message"] == "Candidate created successfully"
        mock_candidate_service.create_candidate.assert_called_once()

    def test_create_candidate_validation_error(self, client, mock_candidate_service):
        """Return HTTP 422 when the email or mobile validation fails."""
        app.dependency_overrides[get_current_user] = override_get_current_user_hr

        response = client.post(
            "/api/v1/candidates/",
            json={
                "name": "Ashutosh Khadse",
                "email": "ashu_khadse@nucleusteq.com",
                "mobile": "98A6543210",
            },
        )

        assert response.status_code == 422
        assert "nucleusteq.com" in response.text
        mock_candidate_service.create_candidate.assert_not_called()

    def test_list_candidates_endpoint_supports_search(self, client, mock_candidate_service):
        """Allow list access and pass the optional search term to the service."""
        app.dependency_overrides[get_current_user] = override_get_current_user_interviewer
        mock_candidate_service.get_all_candidates.return_value = [{"_id": "123"}]

        response = client.get("/api/v1/candidates/?search=ashutosh")

        assert response.status_code == 200
        assert response.json()["message"] == "Candidates retrieved successfully"
        mock_candidate_service.get_all_candidates.assert_called_once_with(search="ashutosh")

    def test_get_candidate_by_id_endpoint_success(self, client, mock_candidate_service):
        """Allow authorized users to retrieve a candidate by id."""
        app.dependency_overrides[get_current_user] = override_get_current_user_admin
        mock_candidate_service.get_candidate_by_id.return_value = {"_id": "123", "name": "Ashutosh"}

        response = client.get("/api/v1/candidates/123")

        assert response.status_code == 200
        assert response.json()["data"]["_id"] == "123"
        mock_candidate_service.get_candidate_by_id.assert_called_once_with("123")

    def test_update_candidate_endpoint_success(self, client, mock_candidate_service):
        """Allow HR users to update candidate profiles successfully."""
        app.dependency_overrides[get_current_user] = override_get_current_user_hr
        mock_candidate_service.update_candidate.return_value = {"_id": "123", "status": "SELECTED"}

        response = client.patch(
            "/api/v1/candidates/123",
            json={"status": "SELECTED"},
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Candidate updated successfully"
        mock_candidate_service.update_candidate.assert_called_once()

    def test_admin_cannot_create_candidate(self, client, mock_candidate_service):
        """Reject candidate creation attempts from admin users."""
        app.dependency_overrides[get_current_user] = override_get_current_user_admin

        response = client.post(
            "/api/v1/candidates/",
            json={
                "name": "Ashutosh Khadse",
                "email": "ashutosh.khadse@nucleusteq.com",
                "mobile": "9876543210",
            },
        )

        assert response.status_code == 403
        mock_candidate_service.create_candidate.assert_not_called()

    def test_interviewer_cannot_update_candidate(self, client, mock_candidate_service):
        """Reject candidate update attempts from interviewer users."""
        app.dependency_overrides[get_current_user] = override_get_current_user_interviewer

        response = client.patch("/api/v1/candidates/123", json={"status": "REJECTED"})

        assert response.status_code == 403
        mock_candidate_service.update_candidate.assert_not_called()
