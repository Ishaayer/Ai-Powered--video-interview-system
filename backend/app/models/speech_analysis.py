from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class SpeechAnalysis(Base):

    __tablename__ = "speech_analysis"


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


    speaking_rate: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )


    pause_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )


    confidence_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    answer: Mapped["CandidateAnswer"] = relationship(
        back_populates="speech_analysis"
    )