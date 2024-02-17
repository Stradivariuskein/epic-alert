from PyQt5.QtWidgets import QApplication
from main_tray_icon import TrayApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    tray_app = TrayApplication()
    sys.exit(app.exec_())
