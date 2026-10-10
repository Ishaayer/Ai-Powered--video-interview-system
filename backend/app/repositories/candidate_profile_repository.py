from sqlalchemy.orm import Session

from app.models.candidate_profile import CandidateProfile


class CandidateProfileRepository:

    def get_by_user_id(
        self,
        db: Session,
        user_id: str
    ):
        return (
            db.query(CandidateProfile)
            .filter(
                CandidateProfile.user_id == user_id
            )
            .first()
        )


    def create(
        self,
        db: Session,
        profile: CandidateProfile
    ):
        db.add(profile)
        db.commit()
        db.refresh(profile)

        return profile


    def update(
        self,
        db: Session,
        profile: CandidateProfile,
        data: dict
    ):
        for key, value in data.items():
            setattr(profile, key, value)

        db.commit()
        db.refresh(profile)

        return profile


    def delete(
        self,
        db: Session,
        profile: CandidateProfile
    ):
        db.delete(profile)
        db.commit()