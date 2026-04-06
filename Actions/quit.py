# Actions/quit.py

class Quit:

    def get_response(self, command: str):
        command = command.lower()

        exit_words = ['quit', 'exit', 'stop']

        if any(word in command for word in exit_words):
            response = "Exiting System Controls. Jarvis Signing off!"
            return response, None

        return None, None