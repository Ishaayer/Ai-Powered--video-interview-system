from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.report import ReportResponse

from app.services.report_service import (
    ReportService
)


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


service = ReportService()


@router.get(
    "/{interview_id}",
    response_model=ReportResponse
)
def get_report(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    report = service.get_report(
        db,
        interview_id
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return report