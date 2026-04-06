# Voice/listener.py

import speech_recognition as sr


class Google_Listener:
    """
    Lightweight Google-based speech recognizer.
    """

    def __init__(self, listen_duration=8):
        self.recognizer = sr.Recognizer()
        
        # Tuning parameters
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8  # pause allowed inside phrase
        
        self.microphone = sr.Microphone()
        self.listen_duration = listen_duration

    def listen(self):
        with self.microphone as source:
            #print("Speak now...")

            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=3,  # max wait for speech to start
                    phrase_time_limit=self.listen_duration  # max speech length
                )

                text = self.recognizer.recognize_google(
                    audio,
                    language="en-IN"
                )

                return text

            except sr.WaitTimeoutError:
                return "No speech detected. Please try again."
            except sr.UnknownValueError:
                return "Sorry, I could not understand."
            except sr.RequestError as e:
                return f"Speech service error: {e}"