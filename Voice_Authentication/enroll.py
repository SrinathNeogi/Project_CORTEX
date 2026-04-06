# Voice_Authentication/enroll.py

import os
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from resemblyzer import VoiceEncoder, preprocess_wav

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMBEDDINGS_DIR = os.path.join(BASE_DIR, "embeddings")
EMBEDDINGS_PATH = os.path.join(EMBEDDINGS_DIR, "user_voice.npy")
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

encoder = VoiceEncoder()

PASSPHRASE = "its me srinath"
NUM_SAMPLES = 5
DURATION = 4
FS = 16000


def record_audio(filepath):
    print(f'Say: "{PASSPHRASE}"')
    print(f"Recording for {DURATION}s... Speak now!")
    audio = sd.rec(int(DURATION * FS), samplerate=FS, channels=1, dtype="int16")
    sd.wait()
    write(filepath, FS, audio)
    print("Saved!\n")
    return filepath


def get_embedding(wav_path):
    wav = preprocess_wav(wav_path)
    embedding = encoder.embed_utterance(wav)
    embedding = embedding / np.linalg.norm(embedding)
    return embedding


print(f"Enrolling — {NUM_SAMPLES} samples")
print(f'Passphrase: "{PASSPHRASE}"\n')

embeddings = []

for i in range(NUM_SAMPLES):
    input(f"Sample {i+1}/{NUM_SAMPLES} — Press Enter when ready...")
    wav_path = os.path.join(BASE_DIR, f"enroll_{i}.wav")
    record_audio(wav_path)
    embedding = get_embedding(wav_path)
    embeddings.append(embedding)
    print(f"✅ Sample {i+1} done.\n")

embeddings_array = np.stack(embeddings)
np.save(EMBEDDINGS_PATH, embeddings_array)

# Show inter-sample similarities
print("Inter-sample similarities (should be > 0.75):")
for i in range(NUM_SAMPLES):
    for j in range(i+1, NUM_SAMPLES):
        sim = float(np.dot(embeddings[i], embeddings[j]))
        print(f"  Sample {i+1} vs Sample {j+1}: {sim:.4f}")

print(f"\n✅ Enrolled! Shape: {embeddings_array.shape}")