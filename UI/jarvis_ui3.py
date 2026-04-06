# UI//jarvis_ui3.py

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor
import math


class JarvisUI(QWidget):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(200, 200)

        # ---------- POSITION (MORE TOP) ----------
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = 5   # tighter to top
        self.move(x, y)

        # Orb properties
        self.base_radius = 10
        self.amplitude = 4   # smooth breathing size
        self.radius = self.base_radius

        self.color = QColor(255, 255, 255, 80)  # more transparent
        self.state = "idle"

        # Smooth animation control
        self.phase = 0

        # Ripple
        self.ripple_radius = 0
        self.ripple_alpha = 60

        # Timer (~60 FPS)
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

    # ---------------- STATE ----------------
    def set_state(self, state):
        self.state = state
        self.phase = 0  # reset smooth cycle

        if state == "idle":
            self.color = QColor(255, 255, 255, 70)
            self.base_radius = 10
            self.amplitude = 3

        elif state == "listening":
            self.color = QColor(0, 255, 120, 90)
            self.base_radius = 13
            self.amplitude = 5

            self.ripple_radius = self.base_radius
            self.ripple_alpha = 60

        elif state == "speaking":
            self.color = QColor(0, 160, 255, 100)
            self.base_radius = 15
            self.amplitude = 6

    # ---------------- ANIMATION ----------------
    def animate(self):
        # -------- SMOOTH BREATHING (NO SHAKING) --------
        self.phase += 0.08
        self.radius = self.base_radius + self.amplitude * math.sin(self.phase)

        # -------- SUBTLE RIPPLE --------
        if self.state == "listening":
            self.ripple_radius += 0.8   # slower + smaller
            self.ripple_alpha -= 1.2

            if self.ripple_alpha <= 0:
                self.ripple_radius = self.base_radius
                self.ripple_alpha = 60

        if self.state == "speaking":
            self.ripple_radius += 0.5   # very subtle
            self.ripple_alpha -= 0.8

            if self.ripple_alpha <= 0:
                self.ripple_radius = self.base_radius
                self.ripple_alpha = 50

        self.update()

    # ---------------- DRAW ----------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center_x = self.width() // 2
        center_y = self.height() // 2

        # -------- SOFT GLOW --------
        for i in range(2):  # reduced layers (cleaner)
            glow_radius = self.radius + (i * 5)
            glow_color = QColor(self.color)
            glow_color.setAlpha(25 - i * 8)

            painter.setBrush(glow_color)
            painter.setPen(Qt.NoPen)

            painter.drawEllipse(
                int(center_x - glow_radius),
                int(center_y - glow_radius),
                int(glow_radius * 2),
                int(glow_radius * 2),
            )

        # -------- RIPPLE (SUBTLE) --------
        if self.state in ["listening", "speaking"]:
            ripple_color = QColor(self.color)
            ripple_color.setAlpha(int(self.ripple_alpha))

            painter.setBrush(Qt.NoBrush)
            painter.setPen(ripple_color)

            painter.drawEllipse(
                int(center_x - self.ripple_radius),
                int(center_y - self.ripple_radius),
                int(self.ripple_radius * 2),
                int(self.ripple_radius * 2),
            )

        # -------- CORE ORB --------
        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)

        painter.drawEllipse(
            int(center_x - self.radius),
            int(center_y - self.radius),
            int(self.radius * 2),
            int(self.radius * 2),
        )