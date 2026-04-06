# Actions/ip_address.py

import requests

class IPAddress:

    def get_response(self, command: str):

        command = command.lower()

        if "ip address" in command or "my ip" in command:

            try:
                ip = requests.get("https://api.ipify.org").text
                return f"Your public IP address is {ip}", None
            except:
                return "Unable to retrieve IP address", None

        return None, None
