import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 150
MARGIN_RIGHT = 5
MARGIN_BOTTOM = 10
DEFAULT_DELAY = 500


class NotificationWindow(QWidget):
    def __init__(self, title, message,
                 func_remembered, timeout=3000, position=1):
        super().__init__()
        self.timeout = timeout
        self.position = position + 1
        self.func_remembered = func_remembered

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

                            QLabel {
                                max-width: 300px;
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
        message_label.setWordWrap(True)
        close_button = QPushButton("X")
        close_button.setObjectName("close_button")
        close_button.setMaximumWidth(20)
        dont_remember_button = QPushButton("Recordar mastarde")
        dont_remember_button.setObjectName("dont_remember_button")

        gridLayout.addWidget(title_label, 0, 0, 1, 2)
        gridLayout.addWidget(close_button, 0, 1, 1, 1)
        gridLayout.addWidget(message_label, 1, 0, 1, 2)
        gridLayout.addWidget(dont_remember_button, 2, 0, 1, 2)
        close_button.clicked.connect(self.close_notification)
        dont_remember_button.clicked.connect(self.func_remembered)
        self.setLayout(gridLayout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.close_notification)
        self.timer.start(timeout + (DEFAULT_DELAY * self.position))

        # Conectar eventos del mouse
        self.enterEvent = self.reset_timer
        self.leaveEvent = self.start_timer

        self.move_to_bottom_right()
        self.start_animation()

    def reset_timer(self, event):
        # Reiniciar el temporizador
        self.timer.stop()

    def start_timer(self, event):
        # Comenzar el temporizador
        self.timer.start(self.timeout + DEFAULT_DELAY)

    def start_animation(self, delay=DEFAULT_DELAY):
        QTimer.singleShot(delay * self.position, self.animation.start)

    def move_to_bottom_right(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(1000)
        # Curva de aceleración para un movimiento más natural
        self.animation.setEasingCurve(QEasingCurve.OutQuad)

        # Establecer la geometría inicial para la animación
        desktop_rect = QApplication.desktop().availableGeometry()
        new_x = desktop_rect.right()  # Iniciar desde la derecha de la pantalla
        position_pixels = (WINDOW_HEIGHT - MARGIN_BOTTOM) * self.position
        new_y = desktop_rect.bottom() - position_pixels
        self.setGeometry(new_x, new_y, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Establecer la geometría final para la animación
        final_x = desktop_rect.right() - WINDOW_WIDTH - MARGIN_RIGHT
        final_y = new_y
        final_geometry = QRect(final_x, final_y, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.animation.setEndValue(final_geometry)

    def close_notification(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    notifications = []
    for i in range(5):
        print(f"animacion: {i}")
        new_notification = NotificationWindow(
            "Notification Title",
            "This is a notification message.",
            position=i
            )
        notifications.append(new_notification)
        new_notification.show()

    sys.exit(app.exec_())
