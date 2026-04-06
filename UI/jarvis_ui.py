# UI/jarvis_ui.py

from PyQt5 import QtWidgets, QtGui, QtCore


class JarvisUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)

        # Smaller window
        self.resize(160, 160)

        # Move to top center (higher)
        self.set_top_center(5)

        # Smooth animation
        self.radius = 45.0
        self.direction = 0.5

        self.state = "idle"

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

        self.old_pos = None

    def animate(self):
        # Smooth breathing animation
        self.radius += self.direction

        if self.radius >= 52 or self.radius <= 42:
            self.direction *= -1

        self.update()

    def set_state(self, state):
        self.state = state
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        center = self.rect().center()
        center_f = QtCore.QPointF(center)

        gradient = QtGui.QRadialGradient(center_f, self.radius)

        # State colors
        if self.state == "listening":
            color = QtGui.QColor(0, 255, 0, 140)
            text = "LISTENING"
        elif self.state == "speaking":
            color = QtGui.QColor(0, 180, 255, 140)
            text = "SPEAKING"
        else:
            color = QtGui.QColor(255, 255, 255, 100)
            text = "IDLE"

        gradient.setColorAt(0, color)
        gradient.setColorAt(1, QtGui.QColor(0, 0, 0, 0))

        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtCore.Qt.NoPen)

        # Float-safe smooth circle
        painter.drawEllipse(center_f, self.radius, self.radius)

        # Smaller faded text
        painter.setPen(QtGui.QColor(color.red(), color.green(), color.blue(), 90))
        font = QtGui.QFont("Arial", 6, QtGui.QFont.Bold)
        painter.setFont(font)

        painter.drawText(self.rect(), QtCore.Qt.AlignCenter, text)

    # Drag support
    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def set_top_center(self, y_offset=5):
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        self.move(x, y_offset)