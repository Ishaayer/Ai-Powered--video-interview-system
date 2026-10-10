from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CandidateProfileCreate(BaseModel):

    phone: str | None = None
    location: str | None = None

    education: str | None = None
    experience: str | None = None
    skills: str | None = None

    linkedin_url: str | None = None
    github_url: str | None = None

    profile_image: str | None = None



class CandidateProfileUpdate(BaseModel):

    phone: str | None = None
    location: str | None = None

    education: str | None = None
    experience: str | None = None
    skills: str | None = None

    linkedin_url: str | None = None
    github_url: str | None = None

    profile_image: str | None = None



class CandidateProfileResponse(BaseModel):

    id: int
    user_id: str

    full_name: str

    phone: str | None
    location: str | None

    education: str | None
    experience: str | None
    skills: str | None

    linkedin_url: str | None
    github_url: str | None

    profile_image: str | None

    created_at: datetime
    updated_at: datetime


    model_config = ConfigDict(
        from_attributes=True
    )