# UI/password_dialog.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette


class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.correct_password = "superSrinath"
        self.authenticated = False

        self.setWindowTitle("Jarvis — Security Verification")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setFixedSize(400, 220)
        self.setModal(True)

        # Dark background style
        self.setStyleSheet("""
            QDialog {
                background-color: #0a0a0f;
                border: 1px solid #00aaff;
            }
            QLabel#title {
                color: #00aaff;
                font-size: 16px;
                font-weight: bold;
            }
            QLabel#subtitle {
                color: #888888;
                font-size: 11px;
            }
            QLabel#error {
                color: #ff4444;
                font-size: 11px;
            }
            QLineEdit {
                background-color: #111122;
                color: #ffffff;
                border: 1px solid #00aaff;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #00ccff;
            }
            QPushButton#confirm {
                background-color: #00aaff;
                color: #000000;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton#confirm:hover {
                background-color: #00ccff;
            }
            QPushButton#cancel {
                background-color: transparent;
                color: #888888;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 13px;
            }
            QPushButton#cancel:hover {
                color: #ffffff;
                border: 1px solid #888888;
            }
        """)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(30, 25, 30, 25)

        # Title
        title = QLabel("🔒  Voice Authentication Failed")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Enter master password to unlock Jarvis")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password...")
        self.password_input.setEchoMode(QLineEdit.Password)  # hides with *
        self.password_input.returnPressed.connect(self._check_password)
        layout.addWidget(self.password_input)

        # Error label (hidden initially)
        self.error_label = QLabel("")
        self.error_label.setObjectName("error")
        self.error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_label)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.confirm_btn = QPushButton("Unlock")
        self.confirm_btn.setObjectName("confirm")
        self.confirm_btn.clicked.connect(self._check_password)

        self.cancel_btn = QPushButton("Lock System")
        self.cancel_btn.setObjectName("cancel")
        self.cancel_btn.clicked.connect(self._lock_system)

        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.confirm_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Focus on input
        self.password_input.setFocus()

    def _check_password(self):
        entered = self.password_input.text()

        if entered == self.correct_password:
            self.authenticated = True
            self.hide()
        else:
            # Wrong password — close immediately, no retry
            self.authenticated = False
            self.hide()

    def _lock_system(self):
        self.authenticated = False
        self.hide()  # just hide, don't reject

def show_password_dialog():
    dialog = PasswordDialog()
    dialog.exec_()
    return dialog.authenticated

