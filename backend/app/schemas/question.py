from pydantic import BaseModel, ConfigDict


class QuestionCreate(BaseModel):
    interview_id: int
    question_text: str
    topic: str
    difficulty: str
    category: str | None = None


class QuestionResponse(BaseModel):
    id: int
    interview_id: int
    question_text: str
    topic: str
    difficulty: str
    category: str | None

    model_config = ConfigDict(
        from_attributes=True
    )