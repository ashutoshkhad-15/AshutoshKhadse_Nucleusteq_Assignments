"""Application enumerations for users, candidates, and interview decisions."""

from enum import Enum


class UserRole(str, Enum):
    """Supported user roles for authorization decisions."""

    ADMIN = "ADMIN"
    HR = "HR"
    INTERVIEWER = "INTERVIEWER"


class CandidateStatus(str, Enum):
    """Candidate lifecycle states tracked by the interview workflow."""

    PROFILE_CREATED = "PROFILE_CREATED"
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED"
    INTERVIEW_COMPLETED = "INTERVIEW_COMPLETED"
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"


class Recommendation(str, Enum):
    """Interview recommendation outcomes recorded after evaluation."""

    NEXT_ROUND = "NEXT_ROUND"
    SELECT = "SELECT"
    REJECT = "REJECT"
