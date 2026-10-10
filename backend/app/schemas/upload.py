from pydantic import BaseModel, ConfigDict


class VideoUploadResponse(BaseModel):
    answer_id: int
    video_url: str
    message: str

    model_config = ConfigDict(
        from_attributes=True
    )