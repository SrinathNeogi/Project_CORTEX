# UI/main_window2.py

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5 import QtCore
import subprocess
import sys
import keyboard

from Voice.listener import Google_Listener
from Actions.action_router2 import ActionRouter
from UI.jarvis_ui import JarvisUI # Normal mode ui
from UI.internet_ui import Internet_UI  # Internet mode ui


class ListenThread(QThread):
    result_signal = pyqtSignal(str)

    def __init__(self, listen_duration=5, parent=None):
        super().__init__(parent)
        self.listen_duration = listen_duration

    def run(self):
        listener = Google_Listener(listen_duration=self.listen_duration)
        text = listener.listen()
        self.result_signal.emit(text)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.action_router = ActionRouter()
        self.is_listening = False
        self.is_ready = False

        # Track current mode
        self.current_mode = "normal"

        # HIDE MAIN WINDOW
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(0, 0)
        self.hide()

        # Default UI
        self.jarvis_ui = JarvisUI()
        self.jarvis_ui.show()
        self.jarvis_ui.raise_()

        # Keep always on top
        self.keep_on_top_timer = QTimer()
        self.keep_on_top_timer.timeout.connect(self.keep_ui_on_top)
        self.keep_on_top_timer.start(2000)

        # GLOBAL KEY LISTENER
        keyboard.on_press(self.handle_key_press)

        QTimer.singleShot(0, self.hide)
        QTimer.singleShot(1500, self.activate_system)

    # ==== System activate function ====
    def activate_system(self):
        print("[DEBUG] System is now ready")

        self.is_ready = True

        # Optional startup speech
        subprocess.Popen(
            ["python", "voice/speaker.py", "All systems operational!Jarvis at your service!"]
        )
    # ===== KEEP UI ALWAYS ON TOP =====
    def keep_ui_on_top(self):
        if self.jarvis_ui:
            self.jarvis_ui.raise_()

    # ===== KEY DETECTION =====
    def handle_key_press(self, event):

        # Right Ctrl detection
        if event.scan_code in [285, 3612] or event.name == "right ctrl":
            self.start_listening()

    # ===== START LISTENING =====
    def start_listening(self):
        if not self.is_ready:
            print("[DEBUG] Ignored - system not ready")
            return
        if self.is_listening:
            return

        self.is_listening = True
        self.jarvis_ui.set_state("listening")

        self.thread = ListenThread(parent=self)
        self.thread.result_signal.connect(self.process_result)
        self.thread.start()

    # ===== PROCESS RESULT =====
    def process_result(self, text):
        self.is_listening = False

        print(f"[DEBUG INPUT]: {text}")

        response, action = self.action_router.action_handler(text)

        if response:
            self.jarvis_ui.set_state("speaking")

            # SPEAK
            subprocess.Popen(
                ["python", "voice/speaker.py", response]
            )

            # ===== INTERNET MODE UI SWITCH =====
            if action == "internet_on":
                self.switch_to_internet_ui()

            elif action == "internet_off":
                self.switch_to_normal_ui()

            # ===== NORMAL ACTION =====
            elif callable(action):
                action()

            # Back to idle
            QTimer.singleShot(2000, lambda: self.jarvis_ui.set_state("idle"))

            if "signing off" in response.lower():
                sys.exit()

        else:
            self.jarvis_ui.set_state("idle")

    # ===== SWITCH TO INTERNET UI =====
    def switch_to_internet_ui(self):
        if self.current_mode == "internet":
            return

        print("[MODE]: INTERNET MODE ON")

        self.jarvis_ui.hide()

        self.jarvis_ui = Internet_UI()
        self.jarvis_ui.show()
        self.jarvis_ui.raise_()

        self.current_mode = "internet"

    # ===== SWITCH TO NORMAL UI =====
    def switch_to_normal_ui(self):
        if self.current_mode == "normal":
            return

        print("[MODE]: NORMAL MODE ON")

        self.jarvis_ui.hide()

        self.jarvis_ui = JarvisUI()
        self.jarvis_ui.show()
        self.jarvis_ui.raise_()

        self.current_mode = "normal"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())