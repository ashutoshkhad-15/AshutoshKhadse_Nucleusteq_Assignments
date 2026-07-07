"""Router tests for interview feedback APIs."""

from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.enums.app_enums import UserRole
from src.main import app
from src.routers.feedback_router import get_feedback_service
from src.services.feedback_service import FeedbackService
from src.utils.security import get_current_user


@pytest.fixture
def mock_feedback_service():
    return AsyncMock(spec=FeedbackService)


@pytest.fixture
def client(mock_feedback_service):
    app.dependency_overrides[get_feedback_service] = lambda: mock_feedback_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def override_interviewer():
    return {"_id": "int1", "email": "int@nucleusteq.com", "role": UserRole.INTERVIEWER.value}


class TestFeedbackRouter:
    def test_submit_feedback_success(self, client, mock_feedback_service):
        app.dependency_overrides[get_current_user] = override_interviewer
        mock_feedback_service.submit_feedback.return_value = {
            "_id": "int1",
            "feedback": {
                "technical_rating": 5,
                "communication_rating": 4,
                "problem_solving": 5,
                "tech_areas_covered": ["Python"],
                "comments": "Good",
                "recommendation": "SELECT",
            },
            "feedback_by": "int1",
        }
        response = client.post("/api/v1/interviews/int1/feedback", json={
            "technicalRating": 5,
            "communicationRating": 4,
            "problemSolving": 5,
            "techAreasCovered": ["Python"],
            "comments": "Good",
            "recommendation": "SELECT",
        })
        assert response.status_code == 200
        assert response.json()["message"] == "Feedback submitted successfully"

    def test_view_feedback_success(self, client, mock_feedback_service):
        app.dependency_overrides[get_current_user] = override_interviewer
        mock_feedback_service.view_feedback.return_value = {
            "_id": "int1",
            "feedback": {
                "technical_rating": 5,
                "communication_rating": 4,
                "problem_solving": 5,
                "tech_areas_covered": ["Python"],
                "comments": "Good",
                "recommendation": "SELECT",
            },
            "feedback_by": "int1",
        }
        response = client.get("/api/v1/interviews/int1/feedback")
        assert response.status_code == 200
        assert response.json()["data"]["feedback"]["recommendation"] == "SELECT"
