from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class FaceAnalysis(Base):

    __tablename__ = "face_analysis"


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


    eye_contact_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )


    posture_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )


    detected_expression: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    answer: Mapped["CandidateAnswer"] = relationship(
        back_populates="face_analysis"
    )