# Actions/internet_speed_test.py

import speedtest

class InternetSpeed:

    def get_response(self, command: str):

        command = command.lower()

        TRIGGER = ["speed test", "internet speed"]

        if any(word in command for word in TRIGGER):

            st = speedtest.Speedtest()

            download = round(st.download() / 1_000_000, 2)
            upload = round(st.upload() / 1_000_000, 2)

            response = f"Download speed is {download} Mbps and upload speed is {upload} Mbps"

            return response, None

        return None, None