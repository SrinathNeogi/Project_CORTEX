# Actions/system_status.py

import psutil

class SystemStatus:

    def get_response(self, command: str):

        command = command.lower()

        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent

        if "cpu" in command:
            return f"CPU usage is at {cpu} percent", None

        if "ram" in command or "memory" in command:
            return f"RAM usage is at {ram} percent", None

        if "system status" in command:
            return f"CPU is at {cpu} percent and RAM is at {ram} percent", None

        return None, None