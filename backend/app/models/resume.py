from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey(
            "candidate_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    file_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    raw_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    parsed_skills: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    parsed_languages: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    parsed_projects: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    parsed_experience: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    candidate: Mapped["CandidateProfile"] = relationship(
        back_populates="resume",
    )