# Action/volume_control.py

from pycaw.pycaw import AudioUtilities

class VolumeControl:

    def get_response(self, command: str):

        command = command.lower()

        if "volume" in command:

            for word in command.split():

                if word.isdigit():

                    level = int(word)

                    if 0 <= level <= 100:

                        def action():

                            device = AudioUtilities.GetSpeakers()
                            volume = device.EndpointVolume
                            volume.SetMasterVolumeLevelScalar(level / 100, None)

                        return f"Setting volume to {level} percent", action

            return "Please specify volume level between 0 and 100", None

        return None, None