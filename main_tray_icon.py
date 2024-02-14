from auto_buy_game import ApiFreeGame
from playwright.sync_api import sync_playwright
from main_window import App
from PyQt5.QtWidgets import QApplication, QDialog, QMenu, QSystemTrayIcon
import sys

headless_params = ["headless", "-headless", "--headless"]


class TrayApplication(QDialog):
    def __init__(self):
        super().__init__()
        with sync_playwright() as playwright:
            api_epic = ApiFreeGame(playwright)
            games = api_epic.get_free_games()
            self.main_window = App(games)
            try:
                if sys.argv[1] in headless_params:
                    pass
            except IndexError:
                self.main_window.show()
            except Exception as e:
                print(f"Error: parameter exception {e}")
                raise Exception(f"Unexpected error: parameter exception {e}")

        self.init_ui()
        self.create_tray_icon()

    def init_ui(self):
        self.setWindowTitle("Free Games")
        # self.setGeometry(100, 100, 400, 300)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    tray_app = TrayApplication()
    sys.exit(app.exec_())
