from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.services.tts_service import TTSService


router = APIRouter(
    prefix="/tts",
    tags=["TTS"]
)


tts_service = TTSService()


@router.post("/")
def text_to_speech(text: str):

    audio_path = tts_service.generate_voice(
        text
    )

    return FileResponse(
        audio_path,
        media_type="audio/wav"
    )