# Action/wifi_status.py

import os

class WifiStatus:

    def get_response(self, command: str):

        command = command.lower()

        TRIGGERS = ["wifi", "wi-fi", "internet status", "network status"]

        if any(word in command for word in TRIGGERS):

            try:

                output = os.popen("netsh wlan show interfaces").read()

                if "connected" in output.lower():
                    for line in output.split("\n"):
                        if "SSID" in line and "BSSID" not in line:
                            wifi = line.split(":")[1].strip()
                            return f"Wi-Fi is connected to {wifi} network.", None

                return "WiFi is disconnected", None

            except:
                return "Unable to check WiFi status", None

        return None, None