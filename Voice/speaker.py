# voice/speaker.py

import pyttsx3
import sys


def speak(text):
    engine = pyttsx3.init()

    rate = engine.getProperty("rate")
    engine.setProperty("rate", 185)

    volume = engine.getProperty("volume")
    engine.setProperty("volume", 1.0)

    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)

    engine.say(text)
    engine.runAndWait()
    engine.stop()


if __name__ == "__main__":
    text = sys.argv[1]
    speak(text)

