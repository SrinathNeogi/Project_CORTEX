# Actions/ppt_finder.py

import os
from rapidfuzz import fuzz, process


class PPTFinder:

    SEARCH_PATHS = [
        r"C:\Users\KIIT\OneDrive\Desktop",
        r"C:\Users\KIIT\Documents",
        r"C:\Users\KIIT\Downloads"
    ]

    # Words to ignore
    STOPWORDS = ["find", "search", "open", "locate", "ppt", "presentation", "file"]

    def extract_query(self, command: str):

        command = command.lower()

        words = command.split()
        filtered_words = [word for word in words if word not in self.STOPWORDS]

        query = " ".join(filtered_words).strip()

        return query


    def get_response(self, command: str):

        command = command.lower()

        # Trigger only if PPT-related
        if "ppt" not in command and "presentation" not in command:
            return None, None

        query = self.extract_query(command)

        if not query:
            return "Please tell me the name of the presentation file.", None

        all_files = []

        # Collect all PPT files
        for path in self.SEARCH_PATHS:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.lower().endswith((".ppt", ".pptx")):
                        full_path = os.path.join(root, file)
                        filename = file.lower().replace(".pptx", "").replace(".ppt", "")
                        all_files.append((filename, full_path, file))

        if not all_files:
            return "No presentation files found in search locations.", None

        filenames = [item[0] for item in all_files]

        # Best match using RapidFuzz
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

        return "Sorry, I could not find that presentation file.", None