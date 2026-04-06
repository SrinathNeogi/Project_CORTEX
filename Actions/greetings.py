# Actions/greetings.py

import random

class Greetings:

    def get_response(self, text : str):
        text = text.lower()

        words = text.split()

        response = None

        if any(word in words for word in ['hey', 'hello', 'hi']):
            response = random.choice([
                "Hello Sir! how can I assist you ?",
                "Hi Sir! Jarvis at your service!",
                "Hello Sir! I am ready for your command."
            ])
        
        if "good morning" in text:
            response= "Good Morning Sir! I am ready to assist you for a productive day!"
        
        if "good afternoon" in text:
            response= "Good Afternoon Sir! whats your plan now?"
        
        if "good evening" in text:
            response= "Good Evening Sir! How was your day?"
        
        if "good night" in text:
            response= "Good Night Sir! Sound sleep!"
        
        if "are you up" in text or "wake up" in text:
            response= "Yes Sir! Jarvis at your Service!"
        
        if "ready" in text:
            response= "Always ready Sir!"
        
        if "thank you" in text:
            response= "My pleasure Sir! I am always ready to help you."
        
        # Identification

        if "what's your name" in text or "what is your name" in text:
            response = "My name is Jarvis. I am a smart desktop assistant."
        
        if "who are you" in text:
            response = "I am Jarvis! A smart virtual desktop assistant, made by Srinath Neogi."
        
        if "tell me about yourself" in text:
            response= (
                "Hello Sir! I am Jarvis, your smart desktop assistant. "
                "I can understand your commands and help you with tasks on your system. "
                "I am Designed, Derived and Developed by Srinath Neogi."
            )
        
        # Here Action is noting, so only response and None
        return response, None