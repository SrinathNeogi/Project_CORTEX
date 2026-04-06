# UI/before_authentication_ui.py

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QPen
import math


class BeforeAuthUI(QWidget):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setGeometry(800, 50, 300, 300)  # adjust position later

        # Animation variables
        self.angle = 0
        self.radius = 60

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)

    def update_animation(self):
        self.angle += 2
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center_x = self.width() // 2
        center_y = self.height() // 2

        # Base circle
        pen = QPen(QColor(0, 150, 255, 150), 2)
        painter.setPen(pen)
        painter.drawEllipse(center_x - self.radius, center_y - self.radius,
                            self.radius * 2, self.radius * 2)

        # Rotating scanning arc
        pen = QPen(QColor(0, 200, 255, 255), 4)
        painter.setPen(pen)

        start_angle = self.angle * 16
        span_angle = 60 * 16

        painter.drawArc(center_x - self.radius, center_y - self.radius,
                        self.radius * 2, self.radius * 2,
                        start_angle, span_angle)

        # Pulsing inner dot
        pulse = int(10 + 5 * math.sin(math.radians(self.angle * 4)))
        painter.setBrush(QColor(0, 200, 255, 180))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center_x - pulse, center_y - pulse,
                            pulse * 2, pulse * 2)