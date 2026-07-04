"""Router tests for the Job Description API."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from src.enums.app_enums import UserRole
from src.main import app
from src.routers.job_router import get_job_service
from src.services.job_service import JobService
from src.utils.security import get_current_user


@pytest.fixture
def mock_job_service():
    service = AsyncMock(spec=JobService)
    return service


@pytest.fixture
def client(mock_job_service):
    app.dependency_overrides[get_job_service] = lambda: mock_job_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def override_get_current_user_hr():
    return {"email": "hr@nucleusteq.com", "role": UserRole.HR.value}


def override_get_current_user_interviewer():
    return {"email": "int@nucleusteq.com", "role": UserRole.INTERVIEWER.value}


class TestJobRouter:
    def test_create_job_endpoint(self, client, mock_job_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_hr
        mock_job_service.create_job.return_value = {"_id": "123", "jobTitle": "Data Engineer"}

        payload = {
            "jobTitle": "Data Engineer",
            "jobDetails": "Build pipelines and data services.",
            "jobRole": "Data Engineering",
            "requiredSkills": ["Hadoop", "Python", "SQL"],
            "experienceRequired": "2 years",
            "employmentType": "Full Time",
            "location": "Remote",
        }

        response = client.post("/api/v1/jobs/", json=payload)

        assert response.status_code == 201
        assert response.json()["message"] == "Job created successfully"
        assert response.json()["data"]["jobTitle"] == "Data Engineer"
        mock_job_service.create_job.assert_called_once()

    def test_create_job_validation_error(self, client, mock_job_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_hr
        payload = {
            "jobTitle": "  ",
            "jobDetails": "Build pipelines and data services.",
            "jobRole": "Data Engineering",
            "requiredSkills": ["Python"],
            "experienceRequired": "2 years",
            "employmentType": "Full Time",
            "location": "Remote",
        }

        response = client.post("/api/v1/jobs/", json=payload)

        assert response.status_code == 422
        mock_job_service.create_job.assert_not_called()

    def test_get_all_jobs_endpoint(self, client, mock_job_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_interviewer
        mock_job_service.get_all_jobs.return_value = ([{"_id": "1"}, {"_id": "2"}], {"page": 1, "limit": 10, "total_items": 2, "total_pages": 1})

        response = client.get("/api/v1/jobs/")

        assert response.status_code == 200
        assert len(response.json()["data"]) == 2
        mock_job_service.get_all_jobs.assert_called_once()

    def test_get_job_by_id_endpoint(self, client, mock_job_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_interviewer
        mock_job_service.get_job_by_id.return_value = {"_id": "123", "jobTitle": "Data Engineer"}

        response = client.get("/api/v1/jobs/123")

        assert response.status_code == 200
        assert response.json()["data"]["jobTitle"] == "Data Engineer"
        mock_job_service.get_job_by_id.assert_called_once_with("123")

    def test_update_job_endpoint(self, client, mock_job_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_hr
        mock_job_service.update_job.return_value = {"_id": "123", "jobTitle": "Data Engineer"}

        payload = {"jobTitle": "Platform Engineer"}

        response = client.patch("/api/v1/jobs/123", json=payload)

        assert response.status_code == 200
        assert response.json()["message"] == "Job updated successfully"
        assert response.json()["data"]["jobTitle"] == "Data Engineer"
        mock_job_service.update_job.assert_called_once()

    def test_interviewer_cannot_create_job(self, client, mock_job_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_interviewer

        payload = {
            "jobTitle": "Data Engineer",
            "jobDetails": "Build pipelines and data services.",
            "jobRole": "Data Engineering",
            "requiredSkills": ["Python"],
            "experienceRequired": "2 years",
            "employmentType": "Full Time",
            "location": "Remote",
        }

        response = client.post("/api/v1/jobs/", json=payload)

        assert response.status_code == 403
        mock_job_service.create_job.assert_not_called()

    def test_interviewer_cannot_update_job(self, client, mock_job_service):
        app.dependency_overrides[get_current_user] = override_get_current_user_interviewer

        response = client.patch("/api/v1/jobs/123", json={"jobTitle": "Platform Engineer"})

        assert response.status_code == 403
        mock_job_service.update_job.assert_not_called()
