# Action/lock_screen.py

import ctypes

class LockScreen:

    def get_response(self, command: str):

        command = command.lower()

        TRIGGER = ["lock" , "screen off"]
        
        if any(word in command for word in TRIGGER):

            def action():
                ctypes.windll.user32.LockWorkStation()

            return "Locking the system", action

        return None, None