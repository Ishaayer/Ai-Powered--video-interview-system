from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.speech_to_text_service import speech_to_text


router = APIRouter(
    prefix="/api/speech-to-text",
    tags=["Speech to Text"]
)


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...)
):
    """
    Receive an audio file and convert it to text.
    """

    try:
        # Read uploaded audio
        audio_data = await file.read()

        if not audio_data:
            raise HTTPException(
                status_code=400,
                detail="Audio file is empty."
            )

        # Get file extension
        filename = file.filename or "audio.wav"

        if "." in filename:
            suffix = "." + filename.split(".")[-1]
        else:
            suffix = ".wav"

        # Convert speech to text
        text = speech_to_text(
            audio_data,
            suffix=suffix
        )

        return {
            "success": True,
            "filename": filename,
            "text": text
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Speech-to-text failed: {str(e)}"
        )