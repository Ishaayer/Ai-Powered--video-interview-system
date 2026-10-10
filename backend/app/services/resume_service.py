import os
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.repositories.resume_repository import ResumeRepository

from app.services.resume_parser import (
    extract_text,
    extract_skills,
    extract_languages,
    extract_projects,
    extract_experience,
)

class ResumeService:

    def __init__(self):
        self.repository = ResumeRepository()
        self.upload_directory = "uploads/resumes"


    async def upload_resume(
        self,
        db: Session,
        candidate_id: int,
        file: UploadFile,
    ):

        os.makedirs(
            self.upload_directory,
            exist_ok=True,
        )

        extension = (
            file.filename.split(".")[-1]
            if "." in file.filename
            else "pdf"
        )

        filename = f"{uuid.uuid4()}.{extension}"

        filepath = os.path.join(
            self.upload_directory,
            filename,
        )

        content = await file.read()

        with open(filepath, "wb") as buffer:
            buffer.write(content)

            resume_text = extract_text(
                filepath,
                file.content_type,
            )


            skills = extract_skills(resume_text)

            languages = extract_languages(resume_text)

            projects = extract_projects(resume_text)

            experience = extract_experience(resume_text)            



        existing = self.repository.get_by_candidate_id(
            db,
            candidate_id,
        )

        if existing:

            existing.file_name = file.filename
            existing.file_url = filepath
            existing.file_type = file.content_type
            existing.file_size = len(content)
            existing.raw_text = resume_text
            existing.parsed_skills = skills
            existing.parsed_languages = languages
            existing.parsed_projects = projects
            existing.parsed_experience = experience            

            db.commit()
            db.refresh(existing)

            return existing

        resume = Resume(
            candidate_id=candidate_id,
            file_name=file.filename,
            file_url=filepath,
            file_type=file.content_type,
            file_size=len(content),
            raw_text=resume_text,
            parsed_skills=skills,
            parsed_languages=languages,
            parsed_projects=projects,
            parsed_experience=experience,
        )

        return self.repository.create(
            db,
            resume,
        )


    def get_resume(
        self,
        db: Session,
        candidate_id: int,
    ):
        return self.repository.get_by_candidate_id(
            db,
            candidate_id,
        )


    def delete_resume(
        self,
        db: Session,
        candidate_id: int,
    ):

        resume = self.repository.get_by_candidate_id(
            db,
            candidate_id,
        )

        if not resume:
            return False

        if os.path.exists(resume.file_url):
            os.remove(resume.file_url)

        self.repository.delete(
            db,
            resume,
        )

        return True