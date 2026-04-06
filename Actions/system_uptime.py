# Actions/system_uptime.py

import psutil
import time

class SystemUptime:

    def get_response(self, command: str):

        command = command.lower()

        TRIGGER = ["uptime" , "running", "up time"]

        if any(word in command for word in TRIGGER):

            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time

            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)

            return f"System has been running for {hours} hours and {minutes} minutes", None

        return None, None
