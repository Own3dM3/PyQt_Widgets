import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGraphicsBlurEffect
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QTime, QPoint


class TransparentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Time")
        self.setGeometry(100, 100, 400, 250)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.mouse_position = None
        self.screen_geometry = QApplication.primaryScreen().geometry()

        self.grid_rows = 4
        self.grid_cols = 4
        self.margin = 15

        self.background_widget = QWidget(self)
        self.background_widget.setGeometry(self.rect())
        self.background_widget.setStyleSheet(
            """
            background-color: rgba(30, 30, 30, 130);
            border-radius: 20px;
            border: 2px solid white; /* Добавление обводки */
            """
        )
        self.background_widget.setGraphicsEffect(self.create_blur_effect())

        self.time_label = QLabel(self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet(
            """
            color: white;
            font-size: 40px;
            font-family: 'Segoe UI', Arial, sans-serif;
            background: transparent;
            """
        )
        self.time_label.setFont(QFont("Segoe UI", 32, QFont.Bold))
        self.time_label.setGeometry(self.rect())

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def create_blur_effect(self):
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(20)
        return blur_effect

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.time_label.setText(current_time)

    def snap_to_grid(self):
        screen_width = self.screen_geometry.width()
        screen_height = self.screen_geometry.height()

        cell_width = (screen_width - 2 * self.margin) // self.grid_cols
        cell_height = (screen_height - 2 * self.margin) // self.grid_rows

        current_x = self.x()
        current_y = self.y()

        nearest_x = round((current_x - self.margin) / cell_width) * cell_width + self.margin
        nearest_y = round((current_y - self.margin) / cell_height) * cell_height + self.margin

        nearest_x = max(self.margin, min(nearest_x, screen_width - self.width() - self.margin))
        nearest_y = max(self.margin, min(nearest_y, screen_height - self.height() - self.margin))

        self.move(nearest_x, nearest_y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.mouse_position is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.mouse_position)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.snap_to_grid()
            self.mouse_position = None

    def resizeEvent(self, event):
        self.background_widget.setGeometry(self.rect())
        self.time_label.setGeometry(self.rect())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TransparentWidget()
    window.show()
    sys.exit(app.exec_())
