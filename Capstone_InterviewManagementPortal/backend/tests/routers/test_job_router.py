"""Router tests for the Job Description API.

Includes integration-style coverage for endpoint authorization and
request handling using FastAPI dependency overrides.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from src.main import app
from src.routers.job_router import get_job_service
from src.services.job_service import JobService
from src.utils.security import get_current_user
from src.enums.app_enums import UserRole

@pytest.fixture
def mock_job_service():
    service = AsyncMock(spec=JobService)
    return service

@pytest.fixture
def client(mock_job_service):
    app.dependency_overrides[get_job_service] = lambda: mock_job_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def override_get_current_user_admin():
    return {"email": "admin@nucleusteq.com", "role": UserRole.ADMIN.value}


def override_get_current_user_hr():
    return {"email": "hr@nucleusteq.com", "role": UserRole.HR.value}


def override_get_current_user_interviewer():
    return {"email": "int@nucleusteq.com", "role": UserRole.INTERVIEWER.value}

class TestJobRouter:
    
    def test_create_job_endpoint(self, client, mock_job_service):
        """Return HTTP 201 and created job metadata for valid HR requests."""
        app.dependency_overrides[get_current_user] = override_get_current_user_hr
        mock_job_service.create_job.return_value = {"_id": "123", "title": "Data Engineer"}
        
        payload = {
            "title": "Data Engineer",
            "department": "Data",
            "description": "Build pipelines.",
            "skills": ["Hadoop", "Python", "SQL"],
            "experience_required": "2 years",
            "location": "Remote"
        }
        
        response = client.post("/api/v1/jobs/", json=payload)
        
        assert response.status_code == 201
        assert response.json()["message"] == "Job created successfully"
        assert response.json()["data"]["title"] == "Data Engineer"
        mock_job_service.create_job.assert_called_once()

    def test_create_job_validation_error(self, client, mock_job_service):
        """Return HTTP 422 when required job fields are missing."""
        app.dependency_overrides[get_current_user] = override_get_current_user_hr
        payload = {
            "title": "Data Engineer",
            "department": "Data",
            "description": "Build pipelines.",
            "experience_required": "2 years",
            "location": "Remote"
        }

        response = client.post("/api/v1/jobs/", json=payload)

        assert response.status_code == 422
        mock_job_service.create_job.assert_not_called()

    def test_get_all_jobs_endpoint(self, client, mock_job_service):
        """Return HTTP 200 and a list of jobs for authorized users."""
        app.dependency_overrides[get_current_user] = override_get_current_user_interviewer
        mock_job_service.get_all_jobs.return_value = [{"_id": "1"}, {"_id": "2"}]
        
        response = client.get("/api/v1/jobs/")
        
        assert response.status_code == 200
        assert len(response.json()["data"]) == 2
        mock_job_service.get_all_jobs.assert_called_once()

    def test_get_job_by_id_endpoint(self, client, mock_job_service):
        """Return HTTP 200 and job details for a valid job ID."""
        app.dependency_overrides[get_current_user] = override_get_current_user_interviewer
        mock_job_service.get_job_by_id.return_value = {"_id": "123", "title": "Data Engineer"}
        
        response = client.get("/api/v1/jobs/123")
        
        assert response.status_code == 200
        assert response.json()["data"]["title"] == "Data Engineer"
        mock_job_service.get_job_by_id.assert_called_once_with("123")

    def test_update_job_endpoint(self, client, mock_job_service):
        """Return HTTP 200 and updated job data for authorized update requests."""
        app.dependency_overrides[get_current_user] = override_get_current_user_hr
        mock_job_service.update_job.return_value = {"_id": "123", "is_active": False}

        payload = {"is_active": False}

        response = client.patch("/api/v1/jobs/123", json=payload)

        assert response.status_code == 200
        assert response.json()["message"] == "Job updated successfully"
        assert response.json()["data"]["is_active"] is False
        mock_job_service.update_job.assert_called_once()
        
    def test_interviewer_cannot_create_job(self, client, mock_job_service):
        """Return HTTP 403 when an interviewer attempts to create a job."""
        app.dependency_overrides[get_current_user] = override_get_current_user_interviewer

        payload = {
            "title": "Data Engineer",
            "department": "Data",
            "description": "Build pipelines.",
            "skills": ["Hadoop"],
            "experience_required": "2 years",
            "location": "Remote"
        }

        response = client.post("/api/v1/jobs/", json=payload)

        assert response.status_code == 403
        mock_job_service.create_job.assert_not_called()

    def test_interviewer_cannot_update_job(self, client, mock_job_service):
        """Return HTTP 403 when an interviewer attempts to update a job."""
        app.dependency_overrides[get_current_user] = override_get_current_user_interviewer
        
        response = client.patch("/api/v1/jobs/123", json={"is_active": False})
        
        assert response.status_code == 403
        mock_job_service.update_job.assert_not_called()