import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPen, QFont, QColor
from PyQt5.QtCore import Qt, QPoint

class RulerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window setup
        self.setWindowTitle("20cm Transparent Ruler")
        self.PIXELS_PER_CM = 37.8  # Initial guess, adjust after calibration
        self.RULER_LENGTH_CM = 20  # Increased to 20 cm (change this for other lengths)
        self.RULER_WIDTH = int(self.RULER_LENGTH_CM * self.PIXELS_PER_CM)
        self.RULER_HEIGHT = 50  # Increased height for larger appearance
        self.setGeometry(100, 100, self.RULER_WIDTH, self.RULER_HEIGHT)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Dragging variables
        self.dragging = False
        self.drag_position = QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw ruler markings
        pen = QPen()
        pen.setColor(QColor(255, 255, 255, 200))  # Semi-transparent white
        pen.setWidth(2)  # Thicker lines
        painter.setPen(pen)
        
        for i in range(0, self.RULER_WIDTH + 1, int(self.PIXELS_PER_CM / 10)):  # 1 mm
            if i % (self.PIXELS_PER_CM * 5) < 1:  # Every 5 cm
                height = 35
                cm = int(i / self.PIXELS_PER_CM)
                painter.setFont(QFont("Arial", 14))  # Larger font
                painter.drawText(i - 12, 5, 24, 15, Qt.AlignCenter, f"{cm}cm")
            elif i % self.PIXELS_PER_CM < 1:  # Every 1 cm
                height = 25
                mm = int(i / (self.PIXELS_PER_CM / 10)) % 10
                if mm == 0:
                    cm = int(i / self.PIXELS_PER_CM)
                    painter.setFont(QFont("Arial", 10))
                    painter.drawText(i - 10, 20, 20, 10, Qt.AlignCenter, f"{cm}")
            else:  # Every 1 mm
                height = 15
            painter.drawLine(i, self.RULER_HEIGHT - height, i, self.RULER_HEIGHT)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_W:  # Move up
            self.move(self.pos() + QPoint(0, -1))
        elif event.key() == Qt.Key_S:  # Move down
            self.move(self.pos() + QPoint(0, 1))
        elif event.key() == Qt.Key_A:  # Move left
            self.move(self.pos() + QPoint(-1, 0))
        elif event.key() == Qt.Key_D:  # Move right
            self.move(self.pos() + QPoint(1, 0))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ruler = RulerWindow()
    ruler.show()
    sys.exit(app.exec_())