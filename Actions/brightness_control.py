# Actions/brightness_control.py

import screen_brightness_control as sbc


class Brightness:

    def get_response(self, command: str):

        command = command.lower()

        if "brightness" in command:

            for word in command.split():

                if word.isdigit():

                    level = int(word)

                    if 0 <= level <= 100:

                        def action():
                            try:
                                sbc.set_brightness(level)
                            except Exception as e:
                                print("Brightness error:", e)

                        response = f"Setting brightness to {level} percent"
                        return response, action

            return "Please specify brightness between 0 and 100", None

        return None, None