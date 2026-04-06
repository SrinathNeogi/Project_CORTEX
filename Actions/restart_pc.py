# Actions/restart_pc.py

import os

class RestartPC:

    def get_response(self, command: str):

        command = command.lower()

        if "restart" in command:

            def action():
                os.system("shutdown /r /t 5")

            return "Restarting the computer", action

        return None, None