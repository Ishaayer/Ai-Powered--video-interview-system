from datetime import datetime

from sqlalchemy import Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Report(Base):

    __tablename__ = "reports"


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


    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    strengths: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    weaknesses: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    recommendations: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    interview: Mapped["Interview"] = relationship(
        back_populates="report"
    )