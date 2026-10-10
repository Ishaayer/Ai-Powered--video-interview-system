from sqlalchemy.orm import Session

from app.models.interview import Interview


class InterviewRepository:

    def create(
        self,
        db: Session,
        interview: Interview
    ):
        db.add(interview)
        db.commit()
        db.refresh(interview)

        return interview


    def get_by_id(
        self,
        db: Session,
        interview_id: int
    ):
        return (
            db.query(Interview)
            .filter(
                Interview.id == interview_id
            )
            .first()
        )


    def get_by_candidate_id(
        self,
        db: Session,
        candidate_id: int
    ):
        return (
            db.query(Interview)
            .filter(
                Interview.candidate_id == candidate_id
            )
            .all()
        )


    def update(
        self,
        db: Session,
        interview: Interview,
        data: dict
    ):
        for key, value in data.items():
            setattr(
                interview,
                key,
                value
            )

        db.commit()
        db.refresh(interview)

        return interview