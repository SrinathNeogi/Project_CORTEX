# Voice_Authentication/verify.py

import os
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from resemblyzer import VoiceEncoder, preprocess_wav
import whisper

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "embeddings", "user_voice.npy")
TEST_WAV_PATH = os.path.join(BASE_DIR, "test.wav")

# Load models
print("[AUTH] Loading models...")
encoder = VoiceEncoder()
whisper_model = whisper.load_model("base")  # small/base/medium — base is fast and accurate enough
print("[AUTH] Models loaded.")

# Load enrolled embeddings
saved_embeddings = np.load(EMBEDDINGS_PATH)
saved_embeddings = saved_embeddings / np.linalg.norm(
    saved_embeddings, axis=1, keepdims=True
)

# Auto threshold from enrolled samples
inter_sims = []
for i in range(len(saved_embeddings)):
    for j in range(i+1, len(saved_embeddings)):
        inter_sims.append(float(np.dot(saved_embeddings[i], saved_embeddings[j])))

VOICE_THRESHOLD = float(np.mean(inter_sims)) - 0.10
print(f"[AUTH] Voice threshold: {VOICE_THRESHOLD:.4f}")

PASSPHRASE = "its me srinath"  # lowercase for comparison
FS = 16000
DURATION = 4


def record_audio(filepath):
    print(f'\nSay: "Its me Srinath"')
    print(f"Recording for {DURATION}s... Speak now!")
    audio = sd.rec(int(DURATION * FS), samplerate=FS, channels=1, dtype="int16")
    sd.wait()
    write(filepath, FS, audio)
    return filepath


def get_embedding(wav_path):
    wav = preprocess_wav(wav_path)
    embedding = encoder.embed_utterance(wav)
    embedding = embedding / np.linalg.norm(embedding)
    return embedding


def check_passphrase(wav_path):
    """Use Whisper to transcribe and check if correct passphrase was spoken."""
    result = whisper_model.transcribe(wav_path, language="en", fp16=False)
    spoken = result["text"].strip().lower()
    print(f"  Heard    : \"{spoken}\"")
    print(f"  Expected : \"{PASSPHRASE}\"")

    # Flexible match — checks if key words are present
    # This handles slight transcription variations like "it's me srinath"
    
    key_words = ["srinath"]  # must contain your name at minimum
    name_variants = ["srinath", "shrinath", "sri nath", "shri nath", "shinnah"]
    passphrase_match = any(variant in spoken for variant in name_variants)
    return passphrase_match, spoken


def verify_voice():
    print("\n[AUTH] Speak to verify...")
    record_audio(TEST_WAV_PATH)

    # LAYER 1 — Passphrase check (Whisper)
    print("\n[CHECK 1] Passphrase...")
    passphrase_ok, spoken = check_passphrase(TEST_WAV_PATH)

    if not passphrase_ok:
        print("❌ Access Denied — Wrong passphrase")
        print(f"   You said: \"{spoken}\"")
        return False

    print("✅ Passphrase correct!")

    # LAYER 2 — Voice biometrics (Resemblyzer)
    print("\n[CHECK 2] Voice biometrics...")
    new_embedding = get_embedding(TEST_WAV_PATH)
    similarities = saved_embeddings @ new_embedding

    avg_sim = float(np.mean(similarities))
    max_sim = float(np.max(similarities))
    min_sim = float(np.min(similarities))

    print(f"  Average   : {avg_sim:.4f}")
    print(f"  Max       : {max_sim:.4f}")
    print(f"  Min       : {min_sim:.4f}")
    print(f"  Threshold : {VOICE_THRESHOLD:.4f}")

    if avg_sim >= VOICE_THRESHOLD:
        print("\n✅ Access Granted — Voice verified!")
        return True
    else:
        print("\n❌ Access Denied — Voice mismatch")
        print(f"   avg {avg_sim:.4f} < threshold {VOICE_THRESHOLD:.4f}")
        return False


if __name__ == "__main__":
    verify_voice()