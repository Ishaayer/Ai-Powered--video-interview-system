from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Question(Base):

    __tablename__ = "questions"


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


    question_text: Mapped[str] = mapped_column(
        Text,
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


    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )


    interview: Mapped["Interview"] = relationship(
        back_populates="questions"
    )


    answers: Mapped[list["CandidateAnswer"]] = relationship(
        back_populates="question",
        cascade="all, delete"
    )