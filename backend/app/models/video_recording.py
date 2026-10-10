from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class VideoRecording(Base):

    __tablename__ = "video_recordings"


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


    video_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )


    duration: Mapped[int | None] = mapped_column(
        nullable=True
    )


    file_size: Mapped[int | None] = mapped_column(
        nullable=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    answer: Mapped["CandidateAnswer"] = relationship(
        back_populates="video_recording"
    )