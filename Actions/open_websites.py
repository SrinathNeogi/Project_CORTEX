# actions/open_websites.py

import subprocess
import time
import urllib.parse


class OpenWebsites:

    def get_response(self, command: str):

        command = command.lower()

        # Fix common speech mistakes
        corrections = {
            "lead code": "leetcode",
            "leet code": "leetcode",
            "chatgpt": "chat gpt",
            "you tube": "youtube"
        }

        for wrong, correct in corrections.items():
            command = command.replace(wrong, correct)

        # Removing noise of the command
        noise_words = {"jarvis","please","can","you","for","me","the","a","an","to","in","on"}

        command = " ".join([w for w in command.split() if w not in noise_words])

        websites = {
            "youtube": {
                "url": "https://www.youtube.com",
                "speech": "Opening YouTube..."
            },
            "google": {
                "url": "https://www.google.com",
                "speech": "Opening Google..."
            },
            "pw": {
                "url": "https://pwskills.com/dashboard/mycourse/",
                "speech": "Opening PW Skills..."
            },
            "github": {
                "url": "https://github.com/SrinathNeogi",
                "speech": "Opening your Github profile..."
            },
            "linkedin": {
                "url": "https://www.linkedin.com/in/srinath-neogi-7b3a06255/",
                "speech": "Opening your LinkedIn profile..."
            },
            "drive": {
                "url": "https://drive.google.com/drive/my-drive",
                "speech": "Opening Google Drive..."
            },
            "gmail": {
                "url": "https://mail.google.com/mail/u/0/?ogbl#inbox",
                "speech": "Opening your Gmail..."
            },
            "chat gpt": {
                "url": "https://chatgpt.com",
                "speech": "Opening Chat GPT..."
            },
            "leetcode": {
                "url": "https://leetcode.com/problemset/",
                "speech": "Opening your Leetcode..."
            },
            "hackerrank": {
                "url": "https://www.hackerrank.com/dashboard",
                "speech": "Opening your Hackerrank..."
            },
            "overleaf": {
                "url": "https://www.overleaf.com/project",
                "speech": "Opening your Overleaf..."
            }
        }

        # -------- OPEN WEBSITE --------
        if command.startswith("open"):

            query = command.replace("open", "").strip()

            for site in websites:
                if site in query:

                    url = websites[site]["url"]
                    response = websites[site]["speech"]

                    def action():
                        time.sleep(1)
                        subprocess.Popen(
                            r'C:\Program Files\Google\Chrome\Application\chrome.exe "%s"' % url
                        )

                    return response, action

        # -------- SEARCH command to do deeper browsing --------
        if command.startswith("search"):

            query = command.replace("search", "").strip()

            # YouTube Search
            if "youtube" in query:

                search_term = query.replace("youtube", "")

                connectors = ["on", "in", "at", "inside", "into"]

                words = search_term.split()

                filtered_words = []

                for word in words:
                    if word not in connectors:
                        filtered_words.append(word)

                search_term = " ".join(filtered_words)

                encoded = urllib.parse.quote(search_term)

                url = f"https://www.youtube.com/results?search_query={encoded}"

                def action():
                    subprocess.Popen(
                        r'C:\Program Files\Google\Chrome\Application\chrome.exe "%s"' % url
                    )

                return f"Searching YouTube for {search_term}", action
            
            # Google Search

            if "google" in query:

                search_term = query.replace("google", "")

                connectors = ["on", "in", "at", "inside", "into"]

                words = search_term.split()

                filtered_words = []

                for word in words:
                    if word not in connectors:
                        filtered_words.append(word)

                search_term = " ".join(filtered_words)

                encoded = urllib.parse.quote(search_term)

                url = f"https://www.google.com/search?q={encoded}"

                def action():
                    subprocess.Popen(
                        r'C:\Program Files\Google\Chrome\Application\chrome.exe "%s"' % url
                    )

                return f"Searching Google for {search_term}", action
            
        return None, None
