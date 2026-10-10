from sqlalchemy.orm import Session

from app.models.candidate_profile import CandidateProfile
from app.repositories.candidate_profile_repository import (
    CandidateProfileRepository,
)


class CandidateProfileService:

    def __init__(self):
        self.repository = CandidateProfileRepository()

    def get_profile(
        self,
        db: Session,
        user_id: str,
    ):
        return self.repository.get_by_user_id(
            db,
            user_id,
        )

    def create_profile(
        self,
        db: Session,
        user_id: str,
        data,
        current_user,
    ):

        profile = CandidateProfile(
            user_id=user_id,
            full_name=current_user.full_name,
            phone=data.phone,
            location=data.location,
            education=data.education,
            experience=data.experience,
            skills=data.skills,
            linkedin_url=data.linkedin_url,
            github_url=data.github_url,
        )

        return self.repository.create(
            db,
            profile,
        )

    def update_profile(
        self,
        db: Session,
        user_id: str,
        data,
    ):

        profile = self.repository.get_by_user_id(
            db,
            user_id,
        )

        if not profile:
            return None

        update_data = data.model_dump(
            exclude_unset=True
        )

        return self.repository.update(
            db,
            profile,
            update_data,
        )

    def delete_profile(
        self,
        db: Session,
        user_id: str,
    ):

        profile = self.repository.get_by_user_id(
            db,
            user_id,
        )

        if not profile:
            return False

        self.repository.delete(
            db,
            profile,
        )

        return True