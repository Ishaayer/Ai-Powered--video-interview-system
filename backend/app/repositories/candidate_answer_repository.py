from sqlalchemy.orm import Session

from app.models.candidate_answer import CandidateAnswer


class CandidateAnswerRepository:

    def create(
        self,
        db: Session,
        answer: CandidateAnswer
    ):
        db.add(answer)
        db.commit()
        db.refresh(answer)

        return answer


    def get_by_id(
        self,
        db: Session,
        answer_id: int
    ):
        return (
            db.query(CandidateAnswer)
            .filter(
                CandidateAnswer.id == answer_id
            )
            .first()
        )


    def get_by_interview_id(
        self,
        db: Session,
        interview_id: int
    ):
        return (
            db.query(CandidateAnswer)
            .filter(
                CandidateAnswer.interview_id == interview_id
            )
            .all()
        )