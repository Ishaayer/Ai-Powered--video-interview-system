import os
import uuid

from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.models.candidate_answer import CandidateAnswer


class UploadService:


    def __init__(self):
        self.upload_directory = "uploads/videos"


    async def save_video(
        self,
        db: Session,
        answer_id: int,
        file: UploadFile,
    ):

        os.makedirs(
            self.upload_directory,
            exist_ok=True
        )


        extension = (
            file.filename.split(".")[-1]
            if "." in file.filename
            else "mp4"
        )


        filename = f"{uuid.uuid4()}.{extension}"


        file_path = os.path.join(
            self.upload_directory,
            filename
        )


        content = await file.read()


        with open(
            file_path,
            "wb"
        ) as buffer:
            buffer.write(content)


        answer = (
            db.query(CandidateAnswer)
            .filter(
                CandidateAnswer.id == answer_id
            )
            .first()
        )


        if not answer:
            raise Exception(
                "Answer not found"
            )


        answer.video_url = file_path

        db.commit()

        db.refresh(answer)


        return file_path