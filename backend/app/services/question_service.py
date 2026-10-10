from sqlalchemy.orm import Session

from app.models.question import Question
from app.repositories.question_repository import (
    QuestionRepository
)


class QuestionService:

    def __init__(self):
        self.repository = QuestionRepository()


    def create_question(
        self,
        db: Session,
        data
    ):

        question = Question(
            **data.model_dump()
        )

        return self.repository.create(
            db,
            question
        )


    def get_questions(
        self,
        db: Session,
        interview_id: int
    ):

        return self.repository.get_by_interview_id(
            db,
            interview_id
        )


    def get_question(
        self,
        db: Session,
        question_id: int
    ):

        return self.repository.get_by_id(
            db,
            question_id
        )