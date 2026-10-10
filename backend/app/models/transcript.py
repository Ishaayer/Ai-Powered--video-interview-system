from datetime import datetime

from sqlalchemy import Text, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Transcript(Base):

    __tablename__ = "transcripts"


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


    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    language: Mapped[str | None] = mapped_column(
        String(50),
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
        back_populates="transcript"
    )