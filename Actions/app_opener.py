# Actions/app_opener.py

import os
import subprocess

class AppOpener:

    def get_response(self, command: str):
        command = command.lower()

        if "launch" not in command:
            return None, None

        apps = {
            "chrome": {
                "method": "os",
                "path": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk",
                "speech": "Launching Google Chrome..."
            },

            "calculator": {
                "method": "os",
                "path": "calc.exe",
                "speech": "Launching Calculator..."
            },

            "notepad": {
                "method": "os",
                "path": "notepad.exe",
                "speech": "Launching Notepad..."
            },

            "cmd": {
                "method": "subprocess",
                "path": "cmd.exe",
                "speech": "Launching Command Prompt..."
            },

            "powershell": {
                "method": "subprocess",
                "path": "powershell.exe",
                "speech": "Launching PowerShell..."
            },

            "camera": {
                "method": "os",
                "path": "microsoft.windows.camera:",
                "speech": "Launching Camera..."
            },

            "settings": {
                "method": "os",
                "path": "ms-settings:",
                "speech": "Launching Settings..."
            },

            "task manager": {
                "method": "os",
                "path": r"C:\Windows\System32\Taskmgr.exe",
                "speech": "Launching Task Manager..."
            },

            "gmail": {
                "method": "os",
                "path": r"C:\Users\KIIT\OneDrive\Desktop\Gmail.lnk",
                "speech": "Launching Gmail..."
            },

            "valorant": {
                "method": "os",
                "path": r"C:\Users\Public\Desktop\VALORANT.lnk",
                "speech": "Launching Valorant..."
            },

            "brave": {
                "method": "os",
                "path": r"C:\Users\Public\Desktop\Brave.lnk",
                "speech": "Launching Brave Browser..."
            }
        }

        for app in apps:
            if app in command:

                def action():
                    method = apps[app]["method"]
                    path = apps[app]["path"]

                    if method == "os":
                        os.startfile(path)

                    else:
                        subprocess.Popen(
                            path,
                            creationflags=subprocess.CREATE_NEW_CONSOLE
                        )

                return apps[app]["speech"], action

        return "Application not recognized.", None