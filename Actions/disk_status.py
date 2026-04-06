# Actions/disk_status.py

import psutil

class DiskStatus:

    def get_response(self, command: str):

        command = command.lower()

        TRIGGER = ["disk" , "storage"]

        if any(word in command for word in TRIGGER):

            usage = psutil.disk_usage("C:")

            percent = usage.percent

            free_storage = round((((100-percent) * 474) / 100) , 2) 

            response = f"Disk C is {percent} percent full and {free_storage} GB storage is free."

            return response, None

        return None, None