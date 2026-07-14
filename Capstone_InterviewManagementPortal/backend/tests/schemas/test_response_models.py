from src.enums.app_enums import UserRole
from src.schemas.request.job_request import EmploymentType
from src.schemas.response.job_response import JobResponse
from src.schemas.response.user_response import UserResponse


def test_response_models():
    user = UserResponse(id="1", email="john@nucleusteq.com", role=UserRole.ADMIN, is_active=True, requires_password_reset=False)
    job = JobResponse(
        id="j1",
        jobTitle="Backend",
        jobDetails="Build services",
        jobRole="Engineer",
        requiredSkills=["Python"],
        experienceRequired="3 years",
        employmentType=EmploymentType.FULL_TIME,
        location="Pune",
    )

    assert user.role == UserRole.ADMIN
    assert job.jobTitle == "Backend"
