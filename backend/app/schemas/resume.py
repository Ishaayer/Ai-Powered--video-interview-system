from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumeResponse(BaseModel):
    id: int
    candidate_id: int

    file_name: str
    file_url: str
    file_type: str
    file_size: int

    raw_text: str | None = None
    parsed_skills: str | None = None
    parsed_languages: str | None = None
    parsed_projects: str | None = None
    parsed_experience: str | None = None

    uploaded_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )