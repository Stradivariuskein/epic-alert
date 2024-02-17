import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QPainter, QFontMetrics
from file_manager import FileManager

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 150
MARGIN_RIGHT = 5
MARGIN_BOTTOM = 10
DEFAULT_DELAY = 500


class Label(QLabel):

    def paintEvent(self, event):
        painter = QPainter(self)

        metrics = QFontMetrics(self.font())
        elided = metrics.elidedText(
            self.text(), Qt.ElideRight, self.width()-20
            )

        painter.drawText(self.rect(), self.alignment(), elided)


class NotificationWindow(QWidget):
    # position es para la posicion en pantalla
    def __init__(self, title, message,
                 on_click, timeout=5000, position=0, index_game=0): 
        super().__init__()
        self.timeout = timeout
        self.position = position
        self.index_game = index_game
        self.setWindowTitle(title.upper())
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
                                max-width: 277px;
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

        title_label = Label(title.upper())
        message_button = QPushButton(message.upper())
        message_button.clicked.connect(lambda: on_click(self.position))
        close_button = QPushButton("X")
        close_button.setObjectName("close_button")
        close_button.setMaximumWidth(20)
        dont_remember_button = QPushButton("No recordar..")
        dont_remember_button.setObjectName("dont_remember_button")

        gridLayout.addWidget(title_label, 0, 0, 1, 2)
        gridLayout.addWidget(close_button, 0, 1, 1, 1)
        gridLayout.addWidget(message_button, 1, 0, 1, 2)
        gridLayout.addWidget(dont_remember_button, 2, 0, 1, 2)
        close_button.clicked.connect(self.close_notification)
        dont_remember_button.clicked.connect(self.dont_remember_notification)
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
        self.animation.setEasingCurve(QEasingCurve.OutQuad)

        desktop_rect = QApplication.desktop().availableGeometry()
        new_x = desktop_rect.right()  # Iniciar desde la derecha de la pantalla
        position_pixels = ((WINDOW_HEIGHT - MARGIN_BOTTOM) * self.position) + 5
        new_y = desktop_rect.bottom() - position_pixels
        self.setGeometry(new_x, new_y, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Establecer la geometría final para la animación
        final_x = desktop_rect.right() - WINDOW_WIDTH - MARGIN_RIGHT
        final_y = new_y
        final_geometry = QRect(final_x, final_y, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.animation.setEndValue(final_geometry)

    def dont_remember_notification(self):
        data = FileManager.load()
        try:
            notifications_games = data["dont_notifications_games"]
        except KeyError:
            notifications_games = []
        notifications_games.append(int(self.index_game))
        FileManager.update_from_key(
            "dont_notifications_games",
            notifications_games
            )

    def close_notification(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    notifications = []

    def test():
        pass

    for i in range(5):
        print(f"animacion: {i}")
        new_notification = NotificationWindow(
            "Notification Titlasdasdasdasdasdasdasdasdasdasdadadsae",
            "This is a notification message.",
            position=i,
            func_remembered=test
            )
        notifications.append(new_notification)
        new_notification.show()

    sys.exit(app.exec_())
