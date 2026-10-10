from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Score(Base):

    __tablename__ = "scores"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )


    interview_id: Mapped[int] = mapped_column(
        ForeignKey(
            "interviews.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    technical_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )


    communication_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )


    confidence_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )


    overall_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    interview: Mapped["Interview"] = relationship(
        back_populates="score"
    )