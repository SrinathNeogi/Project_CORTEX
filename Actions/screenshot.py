# Actions/screenshot.py

import pyautogui
import time
import os


class Screenshot:

    SCREENSHOT_PATH = r"C:\Users\KIIT\Pictures\Screenshots"

    def get_response(self, command: str):

        command = command.lower()

        if "screenshot" in command or "capture screen" in command:

            def action():

                filename = f"Jarvis_screenshot_{int(time.time())}.png"
                full_path = os.path.join(self.SCREENSHOT_PATH, filename)

                screenshot = pyautogui.screenshot()
                screenshot.save(full_path)

            return "Taking a screenshot", action

        return None, None