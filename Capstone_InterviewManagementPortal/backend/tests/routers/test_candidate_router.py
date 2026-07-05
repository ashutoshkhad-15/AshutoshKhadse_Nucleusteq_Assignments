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
    return AsyncMock(spec=CandidateService)


@pytest.fixture
def client(mock_candidate_service):
    app.dependency_overrides[get_candidate_service] = lambda: mock_candidate_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def override_get_current_user_hr():
    return {"email": "hr@nucleusteq.com", "role": UserRole.HR.value}


def override_get_current_user_admin():
    return {"email": "admin@nucleusteq.com", "role": UserRole.ADMIN.value}


def override_get_current_user_interviewer():
    return {"email": "int@nucleusteq.com", "role": UserRole.INTERVIEWER.value}


class TestCandidateRouter:
    def test_create_candidate_endpoint_success(self, client, mock_candidate_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_hr
        mock_candidate_service.create_candidate.return_value = {"_id": "123"}
        response = client.post(
            "/api/v1/candidates/",
            json={
                "firstName": "Ashutosh",
                "lastName": "Khadse",
                "email": "ashutosh.khadse@gmail.com",
                "mobile": "9876543210",
                "currentCompany": "NucleusTeq",
                "totalExperience": "2 years",
                "appliedJobId": "job1",
            },
        )
        assert response.status_code == 201
        assert response.json()["message"] == "Candidate created successfully"

    def test_create_candidate_validation_error(self, client, mock_candidate_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_hr
        response = client.post(
            "/api/v1/candidates/",
            json={"firstName": "  ", "lastName": "", "email": "bad", "mobile": "98A", "currentCompany": "", "totalExperience": "fresher", "appliedJobId": ""},
        )
        assert response.status_code == 422
        mock_candidate_service.create_candidate.assert_not_called()

    def test_create_candidate_requires_current_company(self, client, mock_candidate_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_hr
        response = client.post(
            "/api/v1/candidates/",
            json={
                "firstName": "Ashutosh",
                "lastName": "Khadse",
                "email": "ashutosh.khadse@gmail.com",
                "mobile": "9876543210",
                "currentCompany": "   ",
                "totalExperience": "2 years",
                "appliedJobId": "job1",
            },
        )
        assert response.status_code == 422
        mock_candidate_service.create_candidate.assert_not_called()

    def test_list_candidates_endpoint_supports_search(self, client, mock_candidate_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_interviewer
        mock_candidate_service.get_all_candidates.return_value = ([{"_id": "123"}], {"page": 1, "limit": 10, "total_items": 1, "total_pages": 1})
        response = client.get("/api/v1/candidates/?search=ashutosh")
        assert response.status_code == 200
        assert response.json()["message"] == "Candidates retrieved successfully"
        mock_candidate_service.get_all_candidates.assert_called_once_with(search="ashutosh", page=1, limit=10)

    def test_get_candidate_by_id_endpoint_success(self, client, mock_candidate_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_admin
        mock_candidate_service.get_candidate_by_id.return_value = {"_id": "123", "first_name": "Ashutosh"}
        response = client.get("/api/v1/candidates/123")
        assert response.status_code == 200
        assert response.json()["data"]["_id"] == "123"

    def test_search_jobs_for_candidates_endpoint_success(self, client, mock_candidate_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_hr
        mock_candidate_service.get_jobs_for_dropdown.return_value = [{"_id": "job1", "jobTitle": "Backend Developer"}]
        response = client.get("/api/v1/candidates/jobs/search?search=backend")
        assert response.status_code == 200
        assert response.json()["data"][0]["jobTitle"] == "Backend Developer"

    def test_update_candidate_endpoint_success(self, client, mock_candidate_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_hr
        mock_candidate_service.update_candidate.return_value = {"_id": "123"}
        response = client.patch("/api/v1/candidates/123", json={"totalExperience": "3+ years"})
        assert response.status_code == 200
        assert response.json()["message"] == "Candidate updated successfully"

    def test_admin_cannot_create_candidate(self, client, mock_candidate_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_admin
        response = client.post("/api/v1/candidates/", json={"firstName": "A", "lastName": "B", "email": "a@gmail.com", "mobile": "9876543210", "currentCompany": "TestCorp", "totalExperience": "2 years", "appliedJobId": "job1"})
        assert response.status_code == 403
        mock_candidate_service.create_candidate.assert_not_called()

    def test_interviewer_cannot_update_candidate(self, client, mock_candidate_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_interviewer
        response = client.patch("/api/v1/candidates/123", json={"totalExperience": "3+ years"})
        assert response.status_code == 403
        mock_candidate_service.update_candidate.assert_not_called()
