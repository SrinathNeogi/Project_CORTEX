# UI/jarvis_ui2.py

import math
from PyQt5 import QtWidgets, QtGui, QtCore


SIZE = 120   # widget size — change this one value to resize everything


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

        self.resize(SIZE, SIZE)

        # TOP CENTER — same as original
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.move((screen.width() - SIZE) // 2, 20)

        self.state       = "idle"
        self.core_r      = SIZE * 0.20
        self.growing     = True
        self.wave_phase  = 0.0
        self.ring_angle  = 0.0   # outer ring rotates forward
        self.ring2_angle = 0.0   # inner ring rotates backward
        self.old_pos     = None

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._tick)
        self.timer.start(28)

    # ── state colours ─────────────────────────────────────────────────────────
    def _colours(self):
        if self.state == "listening":
            return QtGui.QColor(0, 220, 110), QtGui.QColor(0, 255, 140), "LISTENING"
        if self.state == "speaking":
            return QtGui.QColor(0, 190, 255), QtGui.QColor(50, 220, 255), "SPEAKING"
        return QtGui.QColor(0, 160, 210), QtGui.QColor(0, 190, 240), "IDLE"

    # ── animation tick ────────────────────────────────────────────────────────
    def _tick(self):
        speed = 0.12 if self.state == "speaking" else 0.06
        if self.growing:
            self.core_r += speed
            if self.core_r >= SIZE * 0.225:
                self.growing = False
        else:
            self.core_r -= speed
            if self.core_r <= SIZE * 0.175:
                self.growing = True

        self.wave_phase  = (self.wave_phase + (0.10 if self.state == "speaking" else 0.05)) % (2 * math.pi)
        self.ring_angle  = (self.ring_angle  + 0.35) % 360
        self.ring2_angle = (self.ring2_angle - 0.18) % 360
        self.update()

    def set_state(self, state):
        self.state = state
        self.update()

    # ── paint ─────────────────────────────────────────────────────────────────
    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)

        cx, cy = SIZE / 2, SIZE / 2
        core_col, ring_col, label = self._colours()
        r = self.core_r

        # 1. Soft outer aura
        aura = QtGui.QRadialGradient(cx, cy, SIZE * 0.46)
        aura_c = QtGui.QColor(core_col); aura_c.setAlpha(28)
        aura.setColorAt(0, aura_c)
        aura.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
        p.setPen(QtCore.Qt.NoPen)
        p.setBrush(aura)
        p.drawEllipse(0, 0, SIZE, SIZE)

        # 2. Outer dashed rotating ring
        p.save()
        p.translate(cx, cy)
        p.rotate(self.ring_angle)
        ring_r = SIZE * 0.46
        pen = QtGui.QPen(QtGui.QColor(ring_col.red(), ring_col.green(), ring_col.blue(), 100), 1.0)
        pen.setStyle(QtCore.Qt.DotLine)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        p.setPen(pen)
        p.setBrush(QtCore.Qt.NoBrush)
        p.drawEllipse(int(-ring_r), int(-ring_r), int(ring_r * 2), int(ring_r * 2))
        p.restore()

        # 3. Inner dashed counter-rotating ring
        p.save()
        p.translate(cx, cy)
        p.rotate(self.ring2_angle)
        ring2_r = SIZE * 0.36
        pen2 = QtGui.QPen(QtGui.QColor(ring_col.red(), ring_col.green(), ring_col.blue(), 55), 0.8)
        pen2.setStyle(QtCore.Qt.DashLine)
        pen2.setCapStyle(QtCore.Qt.RoundCap)
        p.setPen(pen2)
        p.setBrush(QtCore.Qt.NoBrush)
        p.drawEllipse(int(-ring2_r), int(-ring2_r), int(ring2_r * 2), int(ring2_r * 2))
        p.restore()

        # 4. Listening — frequency bars around orb edge
        if self.state == "listening":
            bar_base = r + 4
            for i in range(24):
                angle = (i / 24) * 2 * math.pi
                h = 3 + abs(math.sin(self.wave_phase * 5 + i * 0.9)) * 7
                x0 = cx + math.cos(angle) * bar_base
                y0 = cy + math.sin(angle) * bar_base
                x1 = cx + math.cos(angle) * (bar_base + h)
                y1 = cy + math.sin(angle) * (bar_base + h)
                bar_pen = QtGui.QPen(QtGui.QColor(ring_col.red(), ring_col.green(), ring_col.blue(), 180), 1.4)
                bar_pen.setCapStyle(QtCore.Qt.RoundCap)
                p.setPen(bar_pen)
                p.drawLine(QtCore.QPointF(x0, y0), QtCore.QPointF(x1, y1))

        # 5. Speaking — wobbly wave ring around orb
        if self.state == "speaking":
            path = QtGui.QPainterPath()
            for i in range(361):
                angle = math.radians(i)
                wr = r + 8 + 3 * math.sin(self.wave_phase * 4 + angle * 6)
                x = cx + math.cos(angle) * wr
                y = cy + math.sin(angle) * wr
                if i == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
            path.closeSubpath()
            wave_pen = QtGui.QPen(QtGui.QColor(ring_col.red(), ring_col.green(), ring_col.blue(), 90), 1.0)
            p.setPen(wave_pen)
            p.setBrush(QtCore.Qt.NoBrush)
            p.drawPath(path)

        # 6. Main orb with off-centre specular highlight
        orb = QtGui.QRadialGradient(cx - r * 0.28, cy - r * 0.28, r * 1.1)
        orb.setColorAt(0.0,  QtGui.QColor(255, 255, 255, 130))
        orb.setColorAt(0.3,  QtGui.QColor(core_col.red(), core_col.green(), core_col.blue(), 210))
        orb.setColorAt(0.75, QtGui.QColor(core_col.red() // 2, core_col.green() // 2, core_col.blue() // 2, 180))
        orb.setColorAt(1.0,  QtGui.QColor(0, 0, 0, 0))
        p.setPen(QtCore.Qt.NoPen)
        p.setBrush(orb)
        p.drawEllipse(QtCore.QPointF(cx, cy), r, r)

        # 7. State label below orb
        label_col = QtGui.QColor(ring_col.red(), ring_col.green(), ring_col.blue(), 160)
        p.setPen(label_col)
        font = QtGui.QFont("Courier New", 6, QtGui.QFont.Bold)
        font.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, 2.5)
        p.setFont(font)
        label_rect = QtCore.QRectF(0, cy + r + 4, SIZE, 16)
        p.drawText(label_rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop, label)

    # ── drag support ──────────────────────────────────────────────────────────
    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            d = event.globalPos() - self.old_pos
            self.move(self.x() + d.x(), self.y() + d.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None