from kokoro_onnx import Kokoro
import soundfile as sf


class TTSService:

    def __init__(self):

        self.model = Kokoro(
            "models/kokoro-v1.0.onnx",
            "models/voices-v1.0.bin"
        )


    def generate_voice(self, text: str):

        output_path = "generated_audio.wav"

        samples, sample_rate = self.model.create(
            text,
            voice="af_bella",
            speed=1.0
        )

        sf.write(
            output_path,
            samples,
            sample_rate
        )

        return output_path