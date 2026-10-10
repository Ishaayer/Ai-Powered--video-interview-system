from datetime import datetime

from sqlalchemy import Text, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class CandidateAnswer(Base):

    __tablename__ = "candidate_answers"


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


    question_id: Mapped[int] = mapped_column(
        ForeignKey(
            "questions.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    answer_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    video_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    # Relationships

    interview: Mapped["Interview"] = relationship(
        back_populates="answers"
    )


    question: Mapped["Question"] = relationship(
        back_populates="answers"
    )


    video_recording: Mapped["VideoRecording"] = relationship(
        back_populates="answer",
        uselist=False,
        cascade="all, delete"
    )


    transcript: Mapped["Transcript"] = relationship(
        back_populates="answer",
        uselist=False,
        cascade="all, delete"
    )


    emotion_analysis: Mapped["EmotionAnalysis"] = relationship(
        back_populates="answer",
        uselist=False,
        cascade="all, delete"
    )


    speech_analysis: Mapped["SpeechAnalysis"] = relationship(
        back_populates="answer",
        uselist=False,
        cascade="all, delete"
    )


    face_analysis: Mapped["FaceAnalysis"] = relationship(
        back_populates="answer",
        uselist=False,
        cascade="all, delete"
    )


    llm_evaluation: Mapped["LLMEvaluation"] = relationship(
        back_populates="answer",
        uselist=False,
        cascade="all, delete"
    )