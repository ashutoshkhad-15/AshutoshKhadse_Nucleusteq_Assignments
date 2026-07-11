"""Constants for interview scheduling, feedback, and dashboard workflows."""


class InterviewConstants:
    """Shared constants used by the interview-related modules."""

    INTERVIEW_START_TIME_PATTERN = r"^(?:[01]?\d|2[0-3]):[0-5]\d$"
    MIN_RATING = 1
    MAX_RATING = 5
    INTERVIEW_COLLECTION = "interviews"
    DASHBOARD_SELECTED_STATUS = "SELECTED"
    DASHBOARD_REJECTED_STATUS = "REJECTED"
    INTERVIEW_SCHEDULED_STATUS = "INTERVIEW_SCHEDULED"
