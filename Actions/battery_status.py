# Action/battery_status

import psutil

class BatteryStatus:

    def get_response(self, command: str):

        command = command.lower()

        if "battery" in command:

            battery = psutil.sensors_battery()

            if battery is None:
                return "Battery information not available", None

            percent = battery.percent
            plugged = battery.power_plugged

            if plugged:
                status = "charging"
            else:
                status = "not charging"

            response = f"Battery is at {percent} percent and it is {status}."

            if percent < 30 and not plugged:
                response += " Please connect the charger immediately."

            return response, None

        return None, None