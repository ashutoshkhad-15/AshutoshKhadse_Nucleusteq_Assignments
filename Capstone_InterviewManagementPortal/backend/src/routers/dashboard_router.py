"""API routes for dashboard statistics."""

import logging

from fastapi import APIRouter, Depends

from src.enums.app_enums import UserRole
from src.schemas.response.common_response import SuccessResponse
from src.schemas.response.dashboard_response import HrDashboardResponse, InterviewerDashboardResponse
from src.services.dashboard_service import DashboardService
from src.utils.common import build_success_response
from src.utils.dependencies import get_dashboard_service
from src.utils.security import require_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/interviews", tags=["Dashboard"])

@router.get("/dashboard/hr", response_model=SuccessResponse[HrDashboardResponse])
async def hr_dashboard(dashboard_service: DashboardService = Depends(get_dashboard_service), _current_user: dict = Depends(require_role([UserRole.HR, UserRole.ADMIN]))):
    """Return HR dashboard statistics."""
    logger.info("HR dashboard request received")
    data = await dashboard_service.get_hr_dashboard()
    logger.info("HR dashboard request completed successfully")
    return build_success_response("Dashboard retrieved successfully", data)


@router.get("/dashboard/admin", response_model=SuccessResponse[HrDashboardResponse])
async def admin_dashboard(dashboard_service: DashboardService = Depends(get_dashboard_service), _current_user: dict = Depends(require_role([UserRole.ADMIN]))):
    """Return admin dashboard statistics."""
    logger.info("Admin dashboard request received")
    data = await dashboard_service.get_admin_dashboard()
    logger.info("Admin dashboard request completed successfully")
    return build_success_response("Dashboard retrieved successfully", data)


@router.get("/dashboard/interviewer", response_model=SuccessResponse[InterviewerDashboardResponse])
async def interviewer_dashboard(dashboard_service: DashboardService = Depends(get_dashboard_service), current_user: dict = Depends(require_role([UserRole.INTERVIEWER]))):
    """Return interviewer dashboard statistics."""
    logger.info("Interviewer dashboard request received")
    data = await dashboard_service.get_interviewer_dashboard(current_user.get("_id") or current_user.get("id"))
    logger.info("Interviewer dashboard request completed successfully")
    return build_success_response("Dashboard retrieved successfully", data)
