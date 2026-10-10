from sqlalchemy.orm import Session

from app.models.score import Score


class ScoreRepository:

    def get_by_interview_id(
        self,
        db: Session,
        interview_id: int
    ):

        return (
            db.query(Score)
            .filter(
                Score.interview_id == interview_id
            )
            .first()
        )


    def create(
        self,
        db: Session,
        score: Score
    ):

        db.add(score)
        db.commit()
        db.refresh(score)

        return score