from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class CandidateProfile(Base):

    __tablename__ = "candidate_profiles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    location: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    education: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    experience: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    skills: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    linkedin_url: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    github_url: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )


    profile_image: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user: Mapped["User"] = relationship(
        back_populates="candidate_profile"
    )

    interviews: Mapped[list["Interview"]] = relationship(
        back_populates="candidate",
        cascade="all, delete"
    )

    resume: Mapped["Resume"] = relationship(
        back_populates="candidate",
        uselist=False,
        cascade="all, delete-orphan",
    )