from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Interview(Base):

    __tablename__ = "interviews"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )


    candidate_id: Mapped[int] = mapped_column(
        ForeignKey(
            "candidate_profiles.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    topic: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


    difficulty: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )


    status: Mapped[str] = mapped_column(
        String(50),
        default="CREATED"
    )


    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )


    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    # Relationships

    candidate: Mapped["CandidateProfile"] = relationship(
        back_populates="interviews"
    )


    questions: Mapped[list["Question"]] = relationship(
        back_populates="interview",
        cascade="all, delete"
    )


    answers: Mapped[list["CandidateAnswer"]] = relationship(
        back_populates="interview",
        cascade="all, delete"
    )


    score: Mapped["Score"] = relationship(
        back_populates="interview",
        uselist=False,
        cascade="all, delete"
    )


    report: Mapped["Report"] = relationship(
        back_populates="interview",
        uselist=False,
        cascade="all, delete"
    )