import api from "./api";

let currentAudio: HTMLAudioElement | null = null;

export const ttsService = {

  stop() {
    console.log("🛑 TTS: Stopping audio");
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
      currentAudio = null;
    }
  },

  async speak(text: string) {
    try {
      // Stop previous audio
      this.stop();

      console.log("🎤 TTS: Calling API with text:", text);

      const response = await api.post(
        "/tts/",
        null,
        {
          params: { text },
          responseType: "blob",
        }
      );

      console.log("✅ TTS: Response received, blob size:", response.data.size);

      if (response.data.size === 0) {
        console.error("❌ TTS: Empty blob received");
        throw new Error("Empty audio blob");
      }

      const url = URL.createObjectURL(response.data);
      console.log("✅ TTS: Audio URL created:", url);

      currentAudio = new Audio(url);
      currentAudio.volume = 1.0;

      console.log("🎵 TTS: Attempting to play audio...");

      return new Promise<void>((resolve, reject) => {
        if (!currentAudio) {
          console.error("❌ TTS: currentAudio is null");
          reject(new Error("currentAudio is null"));
          return;
        }

        let isResolved = false;

        const cleanup = () => {
          console.log("🧹 TTS: Cleaning up resources");
          URL.revokeObjectURL(url);
          currentAudio = null;
        };

        currentAudio.onended = () => {
          if (!isResolved) {
            isResolved = true;
            console.log("✅ TTS: Audio finished playing");
            cleanup();
            resolve();
          }
        };

        currentAudio.onerror = (error) => {
          if (!isResolved) {
            isResolved = true;
            console.error("❌ TTS: Audio playback error:", error);
            cleanup();
            reject(error);
          }
        };

        // Timeout fallback - if audio doesn't play, resolve after 10 seconds
        const timeout = setTimeout(() => {
          if (!isResolved) {
            isResolved = true;
            console.warn("⚠️ TTS: Audio timeout - resolving");
            cleanup();
            resolve();
          }
        }, 10000);

        currentAudio.play()
          .then(() => {
            console.log("✅ TTS: Play started successfully");
            clearTimeout(timeout);
          })
          .catch((err) => {
            if (!isResolved) {
              isResolved = true;
              console.error("❌ TTS: Play error:", err);
              clearTimeout(timeout);
              cleanup();
              reject(err);
            }
          });
      });

    } catch (error) {
      console.error("❌ TTS: Service error:", error);
      throw error;
    }
  },

};