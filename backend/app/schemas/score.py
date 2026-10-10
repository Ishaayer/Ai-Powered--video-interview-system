from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ScoreResponse(BaseModel):
    id: int
    interview_id: int
    technical_score: float | None
    communication_score: float | None
    confidence_score: float | None
    overall_score: float | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )