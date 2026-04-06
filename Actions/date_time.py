# actions/date_time.py

from datetime import datetime

class DateTimeAction:

    def get_response(self, text: str):
        text = text.lower()
        now = datetime.now()

        response = None

        # Time
        if "time" in text and "date" not in text:
            current_time = now.strftime("%I:%M %p")
            response = f"The current time is {current_time}."

        # Date
        if "date" in text and "time" not in text:
            current_date = now.strftime("%A, %d %B %Y")
            response = f"Today's date is {current_date}."
        
        # Date & Time together
        if "date" in text and "time" in text:
            current_time = now.strftime("%I:%M %p")
            current_date = now.strftime("%A, %d %B %Y")

            response = f"Current time is {current_time} and today's date is {current_date}"

        # Here too action is nothing
        return response, None