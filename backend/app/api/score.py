from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.score import ScoreResponse

from app.services.score_service import (
    ScoreService
)


router = APIRouter(
    prefix="/scores",
    tags=["Scores"]
)


service = ScoreService()


@router.get(
    "/{interview_id}",
    response_model=ScoreResponse
)
def get_score(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    score = service.get_score(
        db,
        interview_id
    )

    if not score:
        raise HTTPException(
            status_code=404,
            detail="Score not found"
        )

    return score