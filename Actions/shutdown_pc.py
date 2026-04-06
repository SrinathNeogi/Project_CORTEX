# Actions/shutdown_pc.py

import os

class ShutdownPC:

    def get_response(self, command: str):

        command = command.lower()

        TRIGGER = ["shutdown" , "shut down"]

        if any(word in command for word in TRIGGER) :

            def action():
                os.system("shutdown /s /t 5")

            return "Shutting down the computer", action

        return None, None