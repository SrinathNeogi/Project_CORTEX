# Actions/clipboard_reader.py

import pyperclip

class ClipboardReader:

    def get_response(self, command: str):

        command = command.lower()

        TRIGGER = ["clipboard" , "copied"]

        if any(word in command for word in TRIGGER):

            text = pyperclip.paste()

            if not text or text.strip() == "":
                return "Clipboard is empty", None

            words = text.split()

            # take first 8 words as preview
            preview_words = words[:8]
            preview_text = " ".join(preview_words)

            if len(words) > 8:
                return f"Clipboard contains: {preview_text} ... and more text.", None
            else:
                return f"Clipboard contains: {preview_text}", None

        return None, None