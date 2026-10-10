from sqlalchemy.orm import Session

from app.models.resume import Resume


class ResumeRepository:

    def create(
        self,
        db: Session,
        resume: Resume,
    ):
        db.add(resume)
        db.commit()
        db.refresh(resume)

        return resume


    def get_by_candidate_id(
        self,
        db: Session,
        candidate_id: int,
    ):
        return (
            db.query(Resume)
            .filter(
                Resume.candidate_id == candidate_id
            )
            .first()
        )


    def delete(
        self,
        db: Session,
        resume: Resume,
    ):
        db.delete(resume)
        db.commit()