# Actions/groq_internet_access.py

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)


class Groq:

    def get_response(self, command: str):

        command = command.lower()

        try:
            # Smart prompt engineering
            system_prompt = """
            You are a smart assistant with internet-like knowledge.

            Rules:
            - Give short, clear answers
            - If user asks for weather, give a realistic estimate
            - If user asks for news, give recent general headlines
            - Keep answers concise and human-like
            """

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": command}
                ],
            )

            answer = completion.choices[0].message.content

            return answer, None

        except Exception as e:
            return f"Error: {e}", None