import src.services.auth_service as auth_module
import src.services.dashboard_service as dashboard_module
import src.services.feedback_service as feedback_module
import src.services.interview_service as interview_module
import src.services.job_service as job_module
import src.services.user_service as user_module
from src.utils.dependencies import (
    get_auth_service,
    get_dashboard_service,
    get_feedback_service,
    get_interview_service,
    get_job_service,
    get_user_service,
)


def test_dependency_factories_return_service_instances(monkeypatch):
    monkeypatch.setattr(auth_module, "AuthService", lambda: "auth")
    monkeypatch.setattr(dashboard_module, "DashboardService", lambda: "dashboard")
    monkeypatch.setattr(feedback_module, "FeedbackService", lambda: "feedback")
    monkeypatch.setattr(interview_module, "InterviewService", lambda: "interview")
    monkeypatch.setattr(job_module, "JobService", lambda: "job")
    monkeypatch.setattr(user_module, "UserService", lambda: "user")

    assert get_auth_service() == "auth"
    assert get_dashboard_service() == "dashboard"
    assert get_feedback_service() == "feedback"
    assert get_interview_service() == "interview"
    assert get_job_service() == "job"
    assert get_user_service() == "user"
