from sqlalchemy.orm import Session

from app.models.question import Question


class QuestionRepository:

    def create(
        self,
        db: Session,
        question: Question
    ):
        db.add(question)
        db.commit()
        db.refresh(question)

        return question


    def get_by_interview_id(
        self,
        db: Session,
        interview_id: int
    ):
        return (
            db.query(Question)
            .filter(
                Question.interview_id == interview_id
            )
            .all()
        )


    def get_by_id(
        self,
        db: Session,
        question_id: int
    ):
        return (
            db.query(Question)
            .filter(
                Question.id == question_id
            )
            .first()
        )


    def delete(
        self,
        db: Session,
        question: Question
    ):
        db.delete(question)
        db.commit()