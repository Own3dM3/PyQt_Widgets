import sys
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGraphicsBlurEffect, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QRect


class PCInfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PC Info")

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

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.cpu_label = QLabel("CPU Usage: 0%", self)
        self.ram_label = QLabel("RAM Usage: 0%", self)
        self.disk_label = QLabel("Disk Usage: 0%", self)
        for label in [self.cpu_label, self.ram_label, self.disk_label]:
            label.setStyleSheet(
                """
                color: white;
                font-size: 20px;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent;
                """
            )
            label.setFont(QFont("Segoe UI", 14, QFont.Bold))
            label.setAlignment(Qt.AlignLeft)
            self.layout.addWidget(label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)

        self.update_info()

    def create_blur_effect(self):
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(20)
        return blur_effect

    def update_info(self):
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        dist_usage = psutil.disk_usage("/").percent

        self.cpu_label.setText(f"CPU Usage: {cpu_usage}%")
        self.ram_label.setText(f"RAM Usage: {ram_usage}%")
        self.disk_label.setText(f"Disk Usage: {dist_usage}%")

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


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = PCInfoWidget()
    window.show()

    sys.exit(app.exec_())
