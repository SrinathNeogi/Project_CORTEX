# Actions/folder_finder.py

import os
from rapidfuzz import fuzz, process


class FolderFinder:

    SEARCH_PATHS = [
        r"C:\Users\KIIT\OneDrive\Desktop",
        r"C:\Users\KIIT\Downloads",
        r"C:\Users\KIIT\Documents",
        r"C:" 
    ]

    # Words to ignore
    STOPWORDS = ["folder", "directory", "open", "find", "search", "my"]

    def extract_query(self, command: str):

        command = command.lower()

        words = command.split()
        filtered_words = [word for word in words if word not in self.STOPWORDS]

        query = " ".join(filtered_words).strip()

        return query


    def get_response(self, command: str):

        command = command.lower()

        # Trigger only if folder-related
        if not any(word in command for word in ["folder", "directory"]):
            return None, None

        query = self.extract_query(command)

        if not query:
            return "Please tell me the folder name.", None

        all_folders = []

        visited = 0
        MAX_VISIT = 20000   # prevent system hang

        for path in self.SEARCH_PATHS:

            for root, dirs, files in os.walk(path):

                # skip system-heavy folders
                if any(skip in root.lower() for skip in ["windows", "program files", "appdata"]):
                    continue

                for folder in dirs:

                    folder_name = folder.lower()
                    full_path = os.path.join(root, folder)

                    all_folders.append((folder_name, full_path, folder))

                    visited += 1
                    if visited > MAX_VISIT:
                        break

                if visited > MAX_VISIT:
                    break

            if visited > MAX_VISIT:
                break

        if not all_folders:
            return "No folders found in search locations.", None

        folder_names = [item[0] for item in all_folders]

        # Best match
        match, score, index = process.extractOne(
            query,
            folder_names,
            scorer=fuzz.token_set_ratio
        )

        if score > 65:
            best_folder = all_folders[index]

            def action():
                os.startfile(best_folder[1])

            return f"Opening the {best_folder[2]} folder.", action

        return "Sorry, I could not find that folder.", None