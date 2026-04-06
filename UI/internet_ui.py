# UI/internet_ui.py

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QPen
import math


class Internet_UI(QWidget):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(200, 200)

        # POSITION (TOP CENTER)
        self.set_top_center(5)

        # Orb properties
        self.base_radius = 12
        self.amplitude = 4
        self.radius = self.base_radius

        self.color = QColor(0, 180, 255, 90)  # default internet tone
        self.state = "idle"

        # Animation
        self.phase = 0
        self.rotation = 0  # globe rotation

        # Ripple
        self.ripple_radius = 0
        self.ripple_alpha = 60

        # Timer (~60 FPS)
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

    # ===== POSITION HELPER =====
    def set_top_center(self, y_offset=5):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        self.move(x, y_offset)

    # ---------------- STATE ----------------
    def set_state(self, state):
        self.state = state
        self.phase = 0

        if state == "idle":
            self.color = QColor(0, 180, 255, 70)
            self.base_radius = 12
            self.amplitude = 3

        elif state == "listening":
            self.color = QColor(0, 255, 180, 100)
            self.base_radius = 14
            self.amplitude = 5

            self.ripple_radius = self.base_radius
            self.ripple_alpha = 60

        elif state == "speaking":
            self.color = QColor(255, 30, 30, 200)  # bright glowing red
            self.base_radius = 16
            self.amplitude = 6

    # ---------------- ANIMATION ----------------
    def animate(self):
        # Smooth breathing
        self.phase += 0.08
        self.radius = self.base_radius + self.amplitude * math.sin(self.phase)

        # Globe rotation
        self.rotation += 1.2

        # Ripple
        if self.state == "listening":
            self.ripple_radius += 0.8
            self.ripple_alpha -= 1.2

            if self.ripple_alpha <= 0:
                self.ripple_radius = self.base_radius
                self.ripple_alpha = 60

        if self.state == "speaking":
            self.ripple_radius += 0.5
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

        # -------- GLOW --------
        for i in range(2):
            glow_radius = self.radius + (i * 6)
            glow_color = QColor(self.color)

            # stronger glow for speaking
            if self.state == "speaking":
                glow_color.setAlpha(50 - i * 12)
            else:
                glow_color.setAlpha(25 - i * 8)

            painter.setBrush(glow_color)
            painter.setPen(Qt.NoPen)

            painter.drawEllipse(
                int(center_x - glow_radius),
                int(center_y - glow_radius),
                int(glow_radius * 2),
                int(glow_radius * 2),
            )

        # -------- GLOBE RINGS --------
        pen_color = QColor(self.color)
        pen_color.setAlpha(80)
        pen = QPen(pen_color)
        pen.setWidth(1)

        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        for angle in [0, 45, 90]:
            painter.save()
            painter.translate(center_x, center_y)
            painter.rotate(self.rotation + angle)

            painter.drawEllipse(
                int(-self.radius * 1.6),
                int(-self.radius * 0.6),
                int(self.radius * 3.2),
                int(self.radius * 1.2),
            )

            painter.restore()

        # -------- RIPPLE --------
        if self.state in ["listening", "speaking"]:
            ripple_color = QColor(self.color)
            ripple_color.setAlpha(int(self.ripple_alpha))

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