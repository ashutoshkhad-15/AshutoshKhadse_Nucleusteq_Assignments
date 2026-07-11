"""Router tests for dashboard APIs."""

from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.enums.app_enums import UserRole
from src.main import app
from src.routers.dashboard_router import get_dashboard_service
from src.services.dashboard_service import DashboardService
from src.utils.security import get_current_user


@pytest.fixture
def mock_dashboard_service():
    return AsyncMock(spec=DashboardService)


@pytest.fixture
def client(mock_dashboard_service):
    app.dependency_overrides[get_dashboard_service] = lambda: mock_dashboard_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def override_hr():
    return {"_id": "hr1", "email": "hr@nucleusteq.com", "role": UserRole.HR.value}


def override_admin():
    return {"_id": "admin1", "email": "admin@nucleusteq.com", "role": UserRole.ADMIN.value}


def override_interviewer():
    return {"_id": "int1", "email": "int@nucleusteq.com", "role": UserRole.INTERVIEWER.value}


class TestDashboardRouter:
    def test_hr_dashboard_success(self, client, mock_dashboard_service):
        app.dependency_overrides[get_current_user] = override_hr
        mock_dashboard_service.get_hr_dashboard.return_value = {
            "total_jobs": 1,
            "total_candidates": 2,
            "scheduled_interviews": 3,
            "selected_candidates": 1,
            "rejected_candidates": 0,
        }
        response = client.get("/api/v1/interviews/dashboard/hr")
        assert response.status_code == 200
        assert response.json()["data"]["total_jobs"] == 1

    def test_admin_dashboard_success(self, client, mock_dashboard_service):
        app.dependency_overrides[get_current_user] = override_admin
        mock_dashboard_service.get_admin_dashboard.return_value = {
            "total_jobs": 1,
            "total_candidates": 2,
            "scheduled_interviews": 3,
            "selected_candidates": 1,
            "rejected_candidates": 0,
        }
        response = client.get("/api/v1/interviews/dashboard/admin")
        assert response.status_code == 200

    def test_interviewer_dashboard_success(self, client, mock_dashboard_service):
        app.dependency_overrides[get_current_user] = override_interviewer
        mock_dashboard_service.get_interviewer_dashboard.return_value = {
            "assigned_interviews": 2,
            "pending_feedback": 1,
            "completed_feedback": 1,
        }
        response = client.get("/api/v1/interviews/dashboard/interviewer")
        assert response.status_code == 200
        assert response.json()["data"]["assigned_interviews"] == 2
