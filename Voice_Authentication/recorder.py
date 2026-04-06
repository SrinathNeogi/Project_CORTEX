# Voice_Authentication/recorder.py

import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename="temp.wav", duration=3, fs=16000):
    print(f"Recording for {duration}s... Speak now!")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)
    print(f"Saved: {filename}")
    return filename