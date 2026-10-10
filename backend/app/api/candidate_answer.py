from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.candidate_answer import (
    CandidateAnswerCreate,
    CandidateAnswerResponse,
)

from app.services.candidate_answer_service import (
    CandidateAnswerService
)


router = APIRouter(
    prefix="/answers",
    tags=["Candidate Answers"]
)


service = CandidateAnswerService()


@router.post(
    "",
    response_model=CandidateAnswerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_answer(
    data: CandidateAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return service.create_answer(
        db,
        data
    )


@router.get(
    "/interview/{interview_id}",
    response_model=list[CandidateAnswerResponse],
)
def get_interview_answers(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return service.get_interview_answers(
        db,
        interview_id
    )


@router.get(
    "/{answer_id}",
    response_model=CandidateAnswerResponse,
)
def get_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    answer = service.get_answer(
        db,
        answer_id
    )

    if not answer:
        raise HTTPException(
            status_code=404,
            detail="Answer not found"
        )

    return answer