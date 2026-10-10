from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
)

from sqlalchemy.orm import Session


from app.core.database import get_db

from app.dependencies.auth import get_current_user

from app.models.user import User


from app.schemas.upload import (
    VideoUploadResponse,
)


from app.models.candidate_profile import CandidateProfile

import os
import shutil


from app.services.upload_service import (
    UploadService,
)



router = APIRouter(
    prefix="/upload",
    tags=["File Upload"]
)


service = UploadService()



@router.post(
    "/video/{answer_id}",
    response_model=VideoUploadResponse,
)
async def upload_video(
    answer_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if not file.content_type.startswith(
        "video/"
    ):
        raise HTTPException(
            status_code=400,
            detail="Only video files are allowed"
        )


    video_path = await service.save_video(
        db,
        answer_id,
        file,
    )


    return VideoUploadResponse(
        answer_id=answer_id,
        video_url=video_path,
        message="Video uploaded successfully"
    )

@router.post(
    "/profile-image"
)
async def upload_profile_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if not file.content_type.startswith(
        "image/"
    ):
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed"
        )


    upload_dir = "uploads/profile_images"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )


    file_path = (
        f"{upload_dir}/{current_user.id}_{file.filename}"
    )


    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    profile = (
        db.query(CandidateProfile)
        .filter(
            CandidateProfile.user_id == current_user.id
        )
        .first()
    )


    if not profile:

        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )


    profile.profile_image = file_path


    db.commit()

    db.refresh(profile)


    return {
        "profile_image": file_path
    }