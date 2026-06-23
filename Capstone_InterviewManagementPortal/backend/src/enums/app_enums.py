from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    HR = "HR"
    INTERVIEWER = "INTERVIEWER"

class CandidateStatus(str, Enum):
    PROFILE_CREATED = "PROFILE_CREATED"
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED"
    INTERVIEW_COMPLETED = "INTERVIEW_COMPLETED"
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"

class Recommendation(str, Enum):
    NEXT_ROUND = "NEXT_ROUND"
    SELECT = "SELECT"
    REJECT = "REJECT"