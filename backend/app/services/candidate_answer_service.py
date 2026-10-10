from sqlalchemy.orm import Session

from app.models.candidate_answer import CandidateAnswer
from app.repositories.candidate_answer_repository import (
    CandidateAnswerRepository
)


class CandidateAnswerService:

    def __init__(self):
        self.repository = CandidateAnswerRepository()


    def create_answer(
        self,
        db: Session,
        data
    ):

        answer = CandidateAnswer(
            **data.model_dump()
        )

        return self.repository.create(
            db,
            answer
        )


    def get_answer(
        self,
        db: Session,
        answer_id: int
    ):

        return self.repository.get_by_id(
            db,
            answer_id
        )


    def get_interview_answers(
        self,
        db: Session,
        interview_id: int
    ):

        return self.repository.get_by_interview_id(
            db,
            interview_id
        )