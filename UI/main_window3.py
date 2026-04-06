# UI/main_window3.py

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5 import QtCore
import subprocess
import sys
import keyboard
import ctypes

from Voice.listener import Google_Listener
from Actions.action_router2 import ActionRouter
from Voice_Authentication.verify import verify_voice

from UI.jarvis_ui import JarvisUI
from UI.internet_ui import Internet_UI
from UI.password_dialog import show_password_dialog


def speak(text):
    """Non-blocking TTS."""
    subprocess.Popen(["python", "voice/speaker.py", text])


class ListenThread(QThread):
    result_signal = pyqtSignal(str)

    def __init__(self, listen_duration=5, parent=None):
        super().__init__(parent)
        self.listen_duration = listen_duration

    def run(self):
        listener = Google_Listener(listen_duration=self.listen_duration)
        text = listener.listen()
        self.result_signal.emit(text)


class WaitForEnterThread(QThread):
    """Waits for user to press Enter in terminal, then signals."""
    enter_pressed = pyqtSignal()

    def run(self):
        input()  # blocks here until Enter is pressed
        self.enter_pressed.emit()


class VerifyThread(QThread):
    result_signal = pyqtSignal(bool)

    def run(self):
        result = verify_voice()
        self.result_signal.emit(result)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.action_router = ActionRouter()
        self.is_listening = False
        self.is_ready = False

        # SECURITY
        self.is_authenticated = False
        self.failed_attempts = 0
        self.max_attempts = 3

        self.current_mode = "normal"

        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(0, 0)
        self.hide()

        self.jarvis_ui = JarvisUI()
        self.jarvis_ui.show()
        self.jarvis_ui.raise_()

        self.keep_on_top_timer = QTimer()
        self.keep_on_top_timer.timeout.connect(self.keep_ui_on_top)
        self.keep_on_top_timer.start(2000)

        keyboard.on_press(self.handle_key_press)

        QTimer.singleShot(0, self.hide)
        QTimer.singleShot(1500, self.activate_system)

    def activate_system(self):
        print("[DEBUG] System is now ready")
        self.is_ready = True
        speak("All systems operational! Jarvis at your service!")
        QTimer.singleShot(3000, self.start_verification)

    def start_verification(self):
        print("[SECURITY] Starting verification...")
        print("[SECURITY] Press Enter in terminal to begin voice recording...")
        self.jarvis_ui.set_state("listening")

        speak("Please do the voice authentication. Press Enter then say your password.")

        # Wait for Enter in a separate thread — does not block UI
        self.enter_thread = WaitForEnterThread()
        self.enter_thread.enter_pressed.connect(self._run_verify_thread)
        self.enter_thread.start()

    def _run_verify_thread(self):
        print("[SECURITY] Enter pressed — starting voice recording...")
        self.verify_thread = VerifyThread()
        self.verify_thread.result_signal.connect(self.handle_verification_result)
        self.verify_thread.start()

    def handle_verification_result(self, result):
        if result:
            print("[SECURITY] Access Granted")
            self.is_authenticated = True
            self.current_mode = "normal"
            self.jarvis_ui.set_state("idle")
            speak("Access granted. Welcome, Srinath Neogi!")

        else:
            self.failed_attempts += 1
            print(f"[SECURITY] Failed Attempts: {self.failed_attempts}")

            if self.failed_attempts >= self.max_attempts:
                print("[SECURITY] Max attempts reached. Showing password dialog...")
                speak("Voice authentication failed 3 times. Please enter your master password.")
                QTimer.singleShot(3000, self._show_password_dialog)

            else:
                remaining = self.max_attempts - self.failed_attempts
                print(f"[SECURITY] {remaining} attempts remaining")
                speak(f"Authentication failed. Please try again. {remaining} attempts remaining.")
                self.jarvis_ui.set_state("idle")
                QTimer.singleShot(3500, self.start_verification)

    def _show_password_dialog(self):
        print("[SECURITY] Showing password dialog...")
        self.jarvis_ui.set_state("idle")

        password_correct = show_password_dialog()

        if password_correct:
            print("[SECURITY] Password correct. Access granted.")
            self.is_authenticated = True
            self.failed_attempts = 0
            self.current_mode = "normal"
            self.jarvis_ui.set_state("idle")
            speak("Password accepted. Welcome, Srinath Neogi!")

        else:
            print("[SECURITY] Wrong password or cancelled. Locking system...")
            self.jarvis_ui.hide()
            speak("You are not Srinath Neogi. Locking system.")
            QTimer.singleShot(4000, self._lock_and_exit)

    def _lock_and_exit(self):
        print("[SECURITY] Locking workstation...")
        ctypes.windll.user32.LockWorkStation()
        QTimer.singleShot(1000, lambda: sys.exit())

    def keep_ui_on_top(self):
        if self.jarvis_ui:
            self.jarvis_ui.raise_()

    def handle_key_press(self, event):
        if event.scan_code in [285, 3612] or event.name == "right ctrl":
            self.start_listening()

    def start_listening(self):
        if not self.is_ready or not self.is_authenticated:
            return

        if self.is_listening:
            return

        self.is_listening = True
        self.jarvis_ui.set_state("listening")

        self.thread = ListenThread(parent=self)
        self.thread.result_signal.connect(self.process_result)
        self.thread.start()

    def process_result(self, text):
        self.is_listening = False

        response, action = self.action_router.action_handler(text)

        if response:
            self.jarvis_ui.set_state("speaking")

            speak(response)

            if action == "internet_on":
                self.switch_to_internet_ui()
            elif action == "internet_off":
                self.switch_to_normal_ui()
            elif callable(action):
                action()

            QTimer.singleShot(2000, lambda: self.jarvis_ui.set_state("idle"))

            if "signing off" in response.lower():
                sys.exit()
        else:
            self.jarvis_ui.set_state("idle")

    def switch_to_internet_ui(self):
        if self.current_mode == "internet":
            return

        self.jarvis_ui.hide()
        self.jarvis_ui = Internet_UI()
        self.jarvis_ui.show()
        self.jarvis_ui.raise_()

        self.current_mode = "internet"

    def switch_to_normal_ui(self):
        if self.current_mode == "normal":
            return

        self.jarvis_ui.hide()
        self.jarvis_ui = JarvisUI()
        self.jarvis_ui.show()
        self.jarvis_ui.raise_()

        self.current_mode = "normal"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())