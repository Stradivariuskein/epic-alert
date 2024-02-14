import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt, QTimer
WINDOW_WITH = 300
WINDOW_HEIGHT = 150
MARGIN_RIGHT = 5
MARGIN_BOTTOM = 10


class NotificationWindow(QWidget):
    def __init__(self, title, message, timeout=5000):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowStaysOnTopHint |
                            Qt.FramelessWindowHint |
                            Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
                           * {
                            font: 30 12pt \"Segoe UI Black\";
                            background-color: rgba(0, 0, 0, 200);
                            border: 1px solid black;
                            color: white;
                            }

                            QPushButton#close_button {
                                color: rgba(236, 89, 89, 0.652);
                            }

                            QPushButton#dont_remember_button {
                                color: rgba(233, 207, 64, 0.712);
                            }
                           """)

        gridLayout = QGridLayout()
        gridLayout.setSpacing(0)

        title_label = QLabel(title)
        message_label = QLabel(message)
        close_button = QPushButton("X")
        close_button.setObjectName("close_button")
        close_button.setMaximumWidth(20)
        dont_remember_button = QPushButton("No recordar")
        dont_remember_button.setObjectName("dont_remember_button")

        gridLayout.addWidget(title_label, 0, 0, 1, 2)
        gridLayout.addWidget(close_button, 0, 1, 1, 1)
        gridLayout.addWidget(message_label, 1, 0, 1, 2)
        gridLayout.addWidget(dont_remember_button, 2, 0, 1, 2)
        close_button.clicked.connect(self.close_notification)
        dont_remember_button.clicked.connect(self.close_notification)
        self.setLayout(gridLayout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.close_notification)
        self.timer.start(timeout)

        self.move_to_bottom_right()

    def move_to_bottom_right(self):
        desktop_rect = QApplication.desktop().availableGeometry()
        new_x = desktop_rect.right() - WINDOW_WITH - MARGIN_RIGHT
        new_y = desktop_rect.bottom() - WINDOW_HEIGHT - MARGIN_BOTTOM
        self.setGeometry(new_x, new_y, WINDOW_WITH, WINDOW_HEIGHT)

    def close_notification(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NotificationWindow("Notification Title",
                                "This is a notification message.",
                                timeout=1000000)
    window.show()
    sys.exit(app.exec_())
