"""Dashboard response DTOs."""

from pydantic import BaseModel


class HrDashboardResponse(BaseModel):
    """HR dashboard response model."""

    total_jobs: int
    total_candidates: int
    scheduled_interviews: int
    selected_candidates: int
    rejected_candidates: int


class InterviewerDashboardResponse(BaseModel):
    """Interviewer dashboard response model."""

    assigned_interviews: int
    pending_feedback: int
    completed_feedback: int

