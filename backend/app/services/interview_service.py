from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.interview import Interview
from app.models.question import Question

from app.repositories.interview_repository import (
    InterviewRepository,
)
from app.repositories.question_repository import (
    QuestionRepository,
)

from app.services.ai_question_service import (
    AIQuestionService,
)


class InterviewService:

    def __init__(self):
        self.repository = InterviewRepository()
        self.question_repository = QuestionRepository()
        self.ai_question_service = AIQuestionService()

    def start_interview(
        self,
        db: Session,
        candidate_id: int,
        data,
    ):

        # Create Interview
        interview = Interview(
            candidate_id=candidate_id,
            topic=data.topic,
            difficulty=data.difficulty,
            status="in_progress",
            started_at=datetime.now(timezone.utc),
        )

        interview = self.repository.create(
            db,
            interview,
        )

        # Generate First Question
        question_text = self.ai_question_service.generate_question(
            topic=data.topic,
            difficulty=data.difficulty,
            question_number=0,
        )

        # Save Question
        question = Question(
            interview_id=interview.id,
            question_text=question_text,
            topic=data.topic,
            difficulty=data.difficulty,
            category="Introduction",
        )

        self.question_repository.create(
            db,
            question,
        )

        return interview

    def get_interview(
        self,
        db: Session,
        interview_id: int,
    ):

        return self.repository.get_by_id(
            db,
            interview_id,
        )

    def get_candidate_interviews(
        self,
        db: Session,
        candidate_id: int,
    ):

        return self.repository.get_by_candidate_id(
            db,
            candidate_id,
        )

    def complete_interview(
        self,
        db: Session,
        interview: Interview,
    ):

        return self.repository.update(
            db,
            interview,
            {
                "status": "completed",
                "completed_at": datetime.now(timezone.utc),
            },
        )