#UI/main_window.py

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import subprocess
import time
import sys

from Voice.listener import Google_Listener
from Actions.action_router2 import ActionRouter


class ListenThread(QThread):
    result_signal = pyqtSignal(str)

    def __init__(self, listen_duration=3, parent=None):
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
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Jarvis")
        self.setFixedSize(400, 300)

        self.status_label = QLabel("Status: Idle")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.output_label = QLabel("")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setWordWrap(True)

        self.mic_button = QPushButton("🎤 Speak (Right Ctrl)")
        self.mic_button.clicked.connect(self.start_listening)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.output_label)
        layout.addWidget(self.mic_button)

        self.setLayout(layout)

    def start_listening(self):
        self.status_label.setText("Status: Listening...")
        self.mic_button.setEnabled(False)

        self.thread = ListenThread(listen_duration=5, parent=self)
        self.thread.result_signal.connect(self.process_result)
        self.thread.start()


    def keyPressEvent(self, event):

        # detect ONLY Right Ctrl using scan code
        if event.nativeScanCode() == 285 and not event.isAutoRepeat():
            self.start_listening()

    def process_result(self, text):
        self.status_label.setText("Status: Idle")
        self.mic_button.setEnabled(True)

        display_text = f"Command: {text}\n"

        response, action = self.action_router.action_handler(text)

        if response:
            display_text += f"Jarvis: {response}"
            self.output_label.setText(display_text)

            process = subprocess.Popen(
                ["python", "voice/speaker.py", response]
            )

            if action:
                action()

            if "signing off" in response.lower():
                sys.exit()

        else:
            display_text += "Jarvis: I don't understand that yet."
            self.output_label.setText(display_text)
