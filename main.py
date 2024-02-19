from PyQt5.QtWidgets import QApplication
from main_tray_icon import TrayApplication
import sys
import os

if __name__ == "__main__":
    os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '0'
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    tray_app = TrayApplication()
    sys.exit(app.exec_())
