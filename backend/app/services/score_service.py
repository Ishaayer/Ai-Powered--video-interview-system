from sqlalchemy.orm import Session

from app.repositories.score_repository import (
    ScoreRepository
)


class ScoreService:

    def __init__(self):
        self.repository = ScoreRepository()


    def get_score(
        self,
        db: Session,
        interview_id: int
    ):

        return self.repository.get_by_interview_id(
            db,
            interview_id
        )