from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.question import (
    QuestionCreate,
    QuestionResponse,
)

from app.services.question_service import (
    QuestionService
)


router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)


service = QuestionService()


@router.post(
    "",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_question(
    data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return service.create_question(
        db,
        data
    )


@router.get(
    "/interview/{interview_id}",
    response_model=list[QuestionResponse],
)
def get_questions(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return service.get_questions(
        db,
        interview_id
    )


@router.get(
    "/{question_id}",
    response_model=QuestionResponse,
)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    question = service.get_question(
        db,
        question_id
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    return question