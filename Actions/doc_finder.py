# Actions/doc_finder.py

import os
import re
from rapidfuzz import fuzz, process


class DOCFinder:

    SEARCH_PATHS = [
        r"C:\Users\KIIT\OneDrive\Desktop",
        r"C:\Users\KIIT\Documents",
        r"C:\Users\KIIT\Downloads",
    ]

    # Words to ignore in command
    STOPWORDS = ["find", "search", "open", "locate", "document", "docx", "doc"]

    def extract_query(self, command: str):

        command = command.lower()

        # Remove stopwords
        words = command.split()
        filtered_words = [word for word in words if word not in self.STOPWORDS]

        query = " ".join(filtered_words).strip()

        return query


    def get_response(self, command: str):

        command = command.lower()

        # Trigger only if document-related
        if not any(word in command for word in ["doc", "document"]):
            return None, None

        query = self.extract_query(command)

        if not query:
            return "Please tell me the name of the document.", None

        all_files = []

        # Collect all doc files first
        for path in self.SEARCH_PATHS:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.lower().endswith((".doc", ".docx")):
                        full_path = os.path.join(root, file)
                        filename = file.lower().replace(".docx", "").replace(".doc", "")
                        all_files.append((filename, full_path, file))

        if not all_files:
            return "No documents found in search locations.", None

        # Prepare list for matching
        filenames = [item[0] for item in all_files]

        # Get best match using rapidfuzz
        match, score, index = process.extractOne(
            query,
            filenames,
            scorer=fuzz.token_set_ratio
        )

        if score > 60:
            best_file = all_files[index]

            def action():
                os.startfile(best_file[1])

            return f"I found {best_file[2]}. Opening it.", action

        return "Sorry, I could not find that document.", None