import pytest

from src.enums.app_enums import Recommendation, UserRole
from src.schemas.request.candidate_request import CandidateCreateRequest, CandidateUpdateRequest
from src.schemas.request.feedback_request import FeedbackRequest
from src.schemas.request.interview_request import InterviewCreateRequest, InterviewUpdateRequest
from src.schemas.request.job_request import CreateJobRequest, UpdateJobRequest
from src.schemas.request.user_request import CreateUserRequest, UpdateUserRequest


def test_job_request_validation():
    req = CreateJobRequest(
        jobTitle="Senior Backend Engineer",
        jobDetails="Build and maintain backend services for internal products.",
        jobRole="Engineer",
        requiredSkills=["Python", "FastAPI", "Python"],
        experienceRequired="3 years",
        employmentType="Full Time",
        location="Pune",
    )
    assert req.requiredSkills == ["Python", "FastAPI"]
    assert UpdateJobRequest(requiredSkills=["Python"], experienceRequired="2 years").requiredSkills == ["Python"]


def test_user_request_validation():
    assert CreateUserRequest(name="John Doe", email="john.doe@nucleusteq.com", role=UserRole.ADMIN).role == UserRole.ADMIN
    assert UpdateUserRequest(name="Jane Doe", email="jane.doe@nucleusteq.com").email == "jane.doe@nucleusteq.com"


def test_candidate_and_interview_request_validation():
    candidate = CandidateCreateRequest(
        firstName="John",
        lastName="Doe",
        email="john@gmail.com",
        mobile="9876543210",
        currentCompany="NucleusTeq",
        totalExperience="3 years",
        appliedJobId="job1",
    )
    assert candidate.first_name == "John"
    assert CandidateUpdateRequest(firstName="Jane", totalExperience="2 years").first_name == "Jane"

    interview = InterviewCreateRequest(
        candidateId="c1",
        jobId="j1",
        interviewDate="2026-07-10",
        interviewTime="10:30",
        interviewerId="u1",
        focusTechAreas=["Python", "FastAPI", "Python"],
    )
    assert interview.focus_tech_areas == ["Python", "FastAPI"]
    assert InterviewUpdateRequest(interviewTime="11:00").interview_time == "11:00"


def test_feedback_request_validation():
    feedback = FeedbackRequest(
        technicalRating=5,
        communicationRating=4,
        problemSolving=5,
        techAreasCovered=["Python", "APIs", "Python"],
        comments="Strong candidate",
        recommendation=Recommendation.SELECT,
    )
    assert feedback.tech_areas_covered == ["Python", "APIs"]


@pytest.mark.parametrize(
    "factory,payload",
    [
        (CreateJobRequest, {"jobTitle": "ab", "jobDetails": "short", "jobRole": "1", "requiredSkills": [], "experienceRequired": "bad", "employmentType": "Full Time", "location": "1"}),
        (CreateUserRequest, {"name": "1", "email": "bad", "role": "HR"}),
    ],
)
def test_request_models_reject_invalid_payloads(factory, payload):
    with pytest.raises(Exception):
        factory(**payload)
