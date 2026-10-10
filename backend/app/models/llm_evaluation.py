from datetime import datetime

from sqlalchemy import Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class LLMEvaluation(Base):

    __tablename__ = "llm_evaluations"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )


    answer_id: Mapped[int] = mapped_column(
        ForeignKey(
            "candidate_answers.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    technical_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )


    explanation_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )


    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    answer: Mapped["CandidateAnswer"] = relationship(
        back_populates="llm_evaluation"
    )