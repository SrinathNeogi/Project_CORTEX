# Actions/image_finder.py

import os
from rapidfuzz import fuzz, process


class ImageFinder:

    SEARCH_PATHS = [
        r"C:\Users\KIIT\OneDrive\Desktop",
        r"C:\Users\KIIT\Pictures",
        r"C:\Users\KIIT\Downloads"
    ]

    # Words to ignore
    STOPWORDS = ["find", "search", "open", "locate", "image", "photo", "picture", "pic"]

    # Supported image formats
    IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

    def extract_query(self, command: str):

        command = command.lower()

        words = command.split()
        filtered_words = [word for word in words if word not in self.STOPWORDS]

        query = " ".join(filtered_words).strip()

        return query


    def get_response(self, command: str):

        command = command.lower()

        # Trigger only if image-related keywords present
        if not any(word in command for word in ["image", "photo", "picture", "pic"]):
            return None, None

        query = self.extract_query(command)

        if not query:
            return "Please tell me the name of the image.", None

        all_files = []

        # Collect all image files
        for path in self.SEARCH_PATHS:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.lower().endswith(self.IMAGE_EXTENSIONS):
                        full_path = os.path.join(root, file)

                        filename = file.lower()
                        for ext in self.IMAGE_EXTENSIONS:
                            filename = filename.replace(ext, "")

                        all_files.append((filename, full_path, file))

        if not all_files:
            return "No images found in search locations.", None

        filenames = [item[0] for item in all_files]

        # Best match using RapidFuzz
        match, score, index = process.extractOne(
            query,
            filenames,
            scorer=fuzz.token_set_ratio
        )

        if score > 65:   # slightly stricter for images
            best_file = all_files[index]

            def action():
                os.startfile(best_file[1])

            return f"I found the image {best_file[2]}. Opening it.", action

        return "Sorry, I could not find that image.", None