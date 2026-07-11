"""Shared dependency providers for FastAPI routes."""


def get_auth_service() -> "AuthService":
    """Resolve the authentication service dependency."""
    from src.services.auth_service import AuthService

    return AuthService()


def get_dashboard_service() -> "DashboardService":
    """Resolve the dashboard service dependency."""
    from src.services.dashboard_service import DashboardService

    return DashboardService()


def get_feedback_service() -> "FeedbackService":
    """Resolve the feedback service dependency."""
    from src.services.feedback_service import FeedbackService

    return FeedbackService()


def get_interview_service() -> "InterviewService":
    """Resolve the interview service dependency."""
    from src.services.interview_service import InterviewService

    return InterviewService()


def get_job_service() -> "JobService":
    """Resolve the job service dependency."""
    from src.services.job_service import JobService

    return JobService()


def get_user_service() -> "UserService":
    """Resolve the user service dependency."""
    from src.services.user_service import UserService

    return UserService()
