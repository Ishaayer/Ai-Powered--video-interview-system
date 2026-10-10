from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InterviewCreate(BaseModel):
    topic: str
    difficulty: str


class InterviewComplete(BaseModel):
    status: str = "completed"


class InterviewResponse(BaseModel):
    id: int
    candidate_id: int
    topic: str
    difficulty: str
    status: str
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )