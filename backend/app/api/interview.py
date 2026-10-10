from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.candidate_profile import CandidateProfile
from app.schemas.interview import (
    InterviewCreate,
    InterviewResponse,
)
from app.services.interview_service import InterviewService


router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"]
)


service = InterviewService()


@router.post(
    "/start",
    response_model=InterviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_interview(
    data: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    candidate = (
        db.query(CandidateProfile)
        .filter(
            CandidateProfile.user_id == current_user.id
        )
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    return service.start_interview(
        db,
        candidate.id,
        data,
    )


@router.get(
    "",
    response_model=list[InterviewResponse],
)
def get_my_interviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    candidate = (
        db.query(CandidateProfile)
        .filter(
            CandidateProfile.user_id == current_user.id
        )
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    return service.get_candidate_interviews(
        db,
        candidate.id,
    )


@router.get(
    "/{interview_id}",
    response_model=InterviewResponse,
)
def get_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    interview = service.get_interview(
        db,
        interview_id,
    )

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    return interview


@router.put(
    "/{interview_id}/complete",
    response_model=InterviewResponse,
)
def complete_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    interview = service.get_interview(
        db,
        interview_id,
    )

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    return service.complete_interview(
        db,
        interview,
    )