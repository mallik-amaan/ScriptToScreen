# src/tts_generator.py
from gtts import gTTS
import time


def generate_narration(text, out_path):
    print("Generating single-shot TTS...")

    retries = 3
    while retries > 0:
        try:
            tts = gTTS(text=text, lang="en")
            tts.save(out_path)
            print(f"Audio saved to {out_path}")
            return out_path

        except Exception as e:
            print(f"TTS failed: {e}")
            retries -= 1
            time.sleep(1)

    raise RuntimeError("❌ Failed to generate narration after multiple retries.")
