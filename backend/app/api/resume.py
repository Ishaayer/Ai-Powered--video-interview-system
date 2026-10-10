from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user

from app.models.candidate_profile import CandidateProfile
from app.models.user import User

from app.schemas.resume import ResumeResponse

from app.services.resume_service import ResumeService


router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)

service = ResumeService()


@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if file.content_type not in (
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed.",
        )

    candidate = (
        db.query(CandidateProfile)
        .filter(
            CandidateProfile.user_id == current_user.id
        )
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found.",
        )

    return await service.upload_resume(
        db,
        candidate.id,
        file,
    )


@router.get(
    "",
    response_model=ResumeResponse,
)
def get_resume(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    candidate = (
        db.query(CandidateProfile)
        .filter(
            CandidateProfile.user_id == current_user.id
        )
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found.",
        )

    resume = service.get_resume(
        db,
        candidate.id,
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    return resume


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_resume(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    candidate = (
        db.query(CandidateProfile)
        .filter(
            CandidateProfile.user_id == current_user.id
        )
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found.",
        )

    deleted = service.delete_resume(
        db,
        candidate.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )