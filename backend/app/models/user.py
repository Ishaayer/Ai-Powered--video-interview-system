from enum import Enum
from uuid import uuid4

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserRole(str, Enum):
    CANDIDATE = "candidate"
    ADMIN = "admin"



class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    full_name: Mapped[str] = mapped_column(String(100), nullable=False)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole),
        default=UserRole.CANDIDATE,
        nullable=False,
    )

    candidate_profile: Mapped["CandidateProfile"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete",
    )