# Actions/media_control.py

import pyautogui

class MediaControl:

    def get_response(self, command: str):

        command = command.lower()

        response = None

        if "pause" in command or "play" in command:

            def action():
                action = pyautogui.press("playpause")

            if "pause" in command:
                response = "Music paused."
        
            elif "play" in command:
                response = "Music played."

            return response, action

        if "next song" in command:

            def action():
                pyautogui.press("nexttrack")

            return "Playing next song", action

        if "previous song" in command:

            def action():
                pyautogui.press("prevtrack")

            return "Playing previous song", action

        return None, None