from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReportResponse(BaseModel):
    id: int
    interview_id: int
    summary: str | None
    strengths: str | None
    weaknesses: str | None
    recommendations: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )