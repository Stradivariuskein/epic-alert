from auto_buy_game import ApiFreeGame
from main_window import App
from notification_windows import NotificationWindow
from PyQt5.QtWidgets import QApplication, QDialog, QMenu, QSystemTrayIcon
from PyQt5.QtCore import QTimer
import sys
from datetime import datetime, timedelta

HEADLESS_PARAMS = ["headless", "-headless", "--headless"]
CHECK_GAMES_DELY = 43200000  # 12hs
NOTIFICATION_DELAY = 3600000  # 1hs


class TrayApplication(QDialog):
    def __init__(self):
        super().__init__()
        self.epic_api = ApiFreeGame()
        games = self.epic_api.get_free_games()

        self.notifications = []
        self.olds_games = {}
        self.main_window = App(games)

        self.timer_check_game = QTimer()
        self.timer_check_game.timeout.connect(self.cron_update)
        self.timer_check_game.start(CHECK_GAMES_DELY)

        self.timer_notification = QTimer()
        self.timer_notification.timeout.connect(self.show_notifications)
        self.timer_notification.timeout.connect(self.timer_notification.stop)

        try:
            if sys.argv[1] in HEADLESS_PARAMS:
                pass
        except IndexError:
            self.main_window.show()
        except Exception as e:
            print(f"Error: parameter exception {e}")
            raise Exception(f"Unexpected error: parameter exception {e}")

        for i in range(len(games)):
            new_notification = NotificationWindow(
                games[i].title_game,
                games[i].expiration,
                self.remember_notification,
                position=i)
            new_notification.show()
            self.notifications.append(new_notification)

        self.init_ui()
        self.create_tray_icon()

    def show_notification(self, position):
        self.notifications = []
        new_notification = NotificationWindow(
                    self.main_window.games[position].title_game,
                    self.main_window.games[position].expiration,
                    self.remember_notification,
                    position=position
                    )
        self.notifications.append(new_notification)
        new_notification.show()

    def show_notifications(self):
        for i in range(len(self.epic_api.games)):
            self.show_notification(i)

    def cron_update(self):
        self.olds_games = self.epic_api.get_olds_games()
        diff_time = datetime.now() - datetime.strptime(
            self.olds_games['last_update'],
            "%Y-%m-%d %H:%M:%S"
            )

        if diff_time >= timedelta(minutes=1):  # timedelta(hours=12):
            if self.see_changes():
                self.show_notifications()

    def init_ui(self):
        self.setWindowTitle("Free Games")

    def create_tray_icon(self):
        tray_icon = QSystemTrayIcon(self.main_window.icon, self)
        tray_icon.setToolTip("Free Games")

        # Crear un menú contextual
        menu = QMenu()
        action_open = menu.addAction("Open")
        action_exit = menu.addAction("Exit")

        # Conectar las acciones a los eventos
        action_open.triggered.connect(self.open_main_window)
        action_exit.triggered.connect(self.exit_application)

        # Establecer el menú contextual
        tray_icon.setContextMenu(menu)

        # Mostrar el icono en la bandeja del sistema
        tray_icon.show()

    def open_main_window(self):
        self.main_window.show()

    def exit_application(self):
        QApplication.quit()

    def see_changes(self):
        games = self.epic_api.get_free_games()
        changes = False
        for i in range(len(self.epic_api.games)):
            for old_game in self.olds_games['olds_games']:
                # si existe pasamos al siguiente juego. nada para hacer
                if old_game['link'] == games[i].link:
                    break
            else:
                changes = True

        return changes

    def remember_notification(self):
        self.timer_notification.start(NOTIFICATION_DELAY)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    tray_app = TrayApplication()
    sys.exit(app.exec_())
