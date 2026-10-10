from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CandidateAnswerCreate(BaseModel):
    interview_id: int
    question_id: int
    answer_text: str | None = None
    video_url: str | None = None


class CandidateAnswerResponse(BaseModel):
    id: int
    interview_id: int
    question_id: int
    answer_text: str | None
    video_url: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )