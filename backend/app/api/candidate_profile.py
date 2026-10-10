from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.candidate_profile import (
    CandidateProfileCreate,
    CandidateProfileUpdate,
    CandidateProfileResponse,
)
from app.services.candidate_profile_service import (
    CandidateProfileService,
)


router = APIRouter(
    prefix="/candidate-profile",
    tags=["Candidate Profile"]
)


service = CandidateProfileService()


@router.post(
    "",
    response_model=CandidateProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate_profile(
    data: CandidateProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    existing = service.get_profile(
        db,
        current_user.id
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Candidate profile already exists"
        )
    return service.create_profile(
        db,
        current_user.id,
        data,
        current_user
    )


@router.get(
    "",
    response_model=CandidateProfileResponse,
)
def get_candidate_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    profile = service.get_profile(
        db,
        current_user.id
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    return profile


@router.put(
    "",
    response_model=CandidateProfileResponse,
)
def update_candidate_profile(
    data: CandidateProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    profile = service.update_profile(
        db,
        current_user.id,
        data
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    return profile


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_candidate_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    deleted = service.delete_profile(
        db,
        current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )