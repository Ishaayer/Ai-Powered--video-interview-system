from faster_whisper import WhisperModel
import tempfile
import os


# Load the model once when the application starts.
# Do NOT load the model every time a request arrives.
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


def speech_to_text(audio_data: bytes, suffix: str = ".wav") -> str:
    """
    Convert uploaded audio bytes into text using Faster-Whisper.
    """

    temp_file_path = None

    try:
        # Create a temporary audio file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(audio_data)
            temp_file_path = temp_file.name

        # Transcribe the temporary audio file
        segments, info = model.transcribe(
            temp_file_path,
            beam_size=5
        )

        # Combine all segments
        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        return text.strip()

    finally:
        # Delete temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)