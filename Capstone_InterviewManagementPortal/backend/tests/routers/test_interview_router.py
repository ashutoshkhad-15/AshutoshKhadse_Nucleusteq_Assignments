"""Router tests for interview scheduling APIs."""

from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.enums.app_enums import UserRole
from src.main import app
from src.routers.interview_router import get_interview_service
from src.services.interview_service import InterviewService
from src.utils.security import get_current_user


@pytest.fixture
def mock_interview_service():
    return AsyncMock(spec=InterviewService)


@pytest.fixture
def client(mock_interview_service):
    app.dependency_overrides[get_interview_service] = lambda: mock_interview_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def override_hr():
    return {"_id": "hr1", "email": "hr@nucleusteq.com", "role": UserRole.HR.value}


def override_admin():
    return {"_id": "admin1", "email": "admin@nucleusteq.com", "role": UserRole.ADMIN.value}


def override_interviewer():
    return {"_id": "int1", "email": "int@nucleusteq.com", "role": UserRole.INTERVIEWER.value}


class TestInterviewRouter:
    def test_create_interview_success(self, client, mock_interview_service):
        app.dependency_overrides[get_current_user] = override_hr
        mock_interview_service.create_interview.return_value = {
            "_id": "int1",
            "candidate_id": "cand1",
            "candidate_name": "Ashutosh Khadse",
            "job_id": "job1",
            "job_title": "Backend Developer",
            "interviewer_id": "int1",
            "interviewer_name": "Interviewer One",
            "interview_date": "2099-01-01",
            "interview_time": "10:30",
            "focus_tech_areas": ["Python"],
        }
        response = client.post("/api/v1/interviews/", json={
            "candidateId": "cand1",
            "jobId": "job1",
            "interviewDate": "2099-01-01",
            "interviewTime": "10:30",
            "interviewerId": "int1",
            "focusTechAreas": ["Python"],
        })
        assert response.status_code == 201
        assert response.json()["message"] == "Interview scheduled successfully"

    def test_create_interview_permission_denied(self, client, mock_interview_service):
        app.dependency_overrides[get_current_user] = override_admin
        response = client.post("/api/v1/interviews/", json={
            "candidateId": "cand1",
            "jobId": "job1",
            "interviewDate": "2099-01-01",
            "interviewTime": "10:30",
            "interviewerId": "int1",
            "focusTechAreas": ["Python"],
        })
        assert response.status_code == 403
        mock_interview_service.create_interview.assert_not_called()

    def test_list_interviews_success(self, client, mock_interview_service):
        app.dependency_overrides[get_current_user] = override_interviewer
        mock_interview_service.get_assigned_interviews.return_value = ([{
            "_id": "int1",
            "candidate_id": "cand1",
            "candidate_name": "Ashutosh Khadse",
            "job_id": "job1",
            "job_title": "Backend Developer",
            "interviewer_id": "int1",
            "interviewer_name": "Interviewer One",
            "interview_date": "2099-01-01",
            "interview_time": "10:30",
            "focus_tech_areas": ["Python"],
        }], {"page": 1, "limit": 10, "total_items": 1, "total_pages": 1})
        response = client.get("/api/v1/interviews/?search=python")
        assert response.status_code == 200
        assert response.json()["data"][0]["_id"] == "int1"

    def test_get_interview_success(self, client, mock_interview_service):
        app.dependency_overrides[get_current_user] = override_hr
        mock_interview_service.get_interview_for_user.return_value = {
            "_id": "int1",
            "candidate_id": "cand1",
            "candidate_name": "Ashutosh Khadse",
            "job_id": "job1",
            "job_title": "Backend Developer",
            "interviewer_id": "int1",
            "interviewer_name": "Interviewer One",
            "interview_date": "2099-01-01",
            "interview_time": "10:30",
            "focus_tech_areas": ["Python"],
        }
        response = client.get("/api/v1/interviews/int1")
        assert response.status_code == 200
        assert response.json()["data"]["_id"] == "int1"

    def test_get_interviews_for_hr_uses_all_interviews(self, client, mock_interview_service):
        app.dependency_overrides[get_current_user] = override_hr
        mock_interview_service.get_all_interviews.return_value = ([], {"page": 1, "limit": 10, "total_items": 0, "total_pages": 1})

        response = client.get("/api/v1/interviews/?search=python&page=2&limit=5")

        assert response.status_code == 200
        mock_interview_service.get_all_interviews.assert_awaited_once_with(search="python", page=2, limit=5)

    def test_get_interviewers_success(self, client, mock_interview_service):
        app.dependency_overrides[get_current_user] = override_admin
        mock_interview_service.get_interviewers.return_value = ([{"_id": "u1", "role": "INTERVIEWER"}], {"page": 1, "limit": 100, "total_items": 1, "total_pages": 1})

        response = client.get("/api/v1/interviews/interviewers?search=dev")

        assert response.status_code == 200
        assert response.json()["data"][0]["_id"] == "u1"
        mock_interview_service.get_interviewers.assert_awaited_once_with(search="dev", page=1, limit=100)

    def test_assigned_interviews_success(self, client, mock_interview_service):
        app.dependency_overrides[get_current_user] = override_interviewer
        mock_interview_service.get_assigned_interviews.return_value = ([{
            "_id": "int1",
            "candidate_id": "cand1",
            "candidate_name": "Ashutosh Khadse",
            "job_id": "job1",
            "job_title": "Backend Developer",
            "interviewer_id": "int1",
            "interviewer_name": "Interviewer One",
            "interview_date": "2099-01-01",
            "interview_time": "10:30",
            "focus_tech_areas": ["Python"],
        }], {"page": 1, "limit": 10, "total_items": 1, "total_pages": 1})

        response = client.get("/api/v1/interviews/assigned")

        assert response.status_code == 200
        assert response.json()["data"][0]["_id"] == "int1"
        mock_interview_service.get_assigned_interviews.assert_awaited_once()
