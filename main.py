import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject
import socket
from main_tray_icon import TrayApplication
import sys
import os

from notification_windows import NotificationWindow  # birrar solo para debug
HEADLESS_PARAMS = ["headless", "-headless", "--headless"]

MSJ = "show_main_window"


class SignalHolder(QObject):
    message_received = pyqtSignal()

# solo se puede ejecutar una vez
# sen encarga de ver si se puedo enviar un mensaje a otro instancia de la app y si no
# eso quiere decir q es la única instancia por lo tanto se queda en escucha de un mensaje de otra instancia
# cuando recibe el mensaje envía una la señal para abrir la ventana principal


class SocketListener:
    def __init__(self, handler_callback, signals: pyqtSignal, host='localhost', port=50000):
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

        self.handler_callback = handler_callback
        self.msj = MSJ
        self.msj_is_send = False
        self.signals = signals

    def _create_recv_socket(self):
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_socket.bind((self.host, self.port))
        self.recv_socket.listen(1)

    def listen_socket(self):
        self._create_recv_socket()
        while True:
            self.client_socket, self.address = self.recv_socket.accept()
            data = self.client_socket.recv(1024).decode('utf-8')

            if data and data == MSJ:
                self.signals.message_received.emit()

    def send_msj(self):
        self.send_socket.settimeout(5.0)
        try:
            self.send_socket.connect((self.host, self.port))
            message = self.msj.encode('utf-8')
            self.send_socket.send(message)
            self.msj_is_send = True
        except TimeoutError:
            self.msj_is_send = False
        except ConnectionRefusedError:
            pass  # si no se puedo establecer la conexion es porque no se esta ejecutando
        except Exception as e:
            print(f"[{type(e).__name__}]: {e}")
        self.send_socket.close()


class Main_app:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.tray_app = TrayApplication()
        self.signals = SignalHolder()
        self.signals.message_received.connect(self.handle_message)

    def check_single_instance(self):
        self.listener = SocketListener(self.handle_message, self.signals)
        sender_thread = threading.Thread(
            target=self.listener.send_msj, daemon=True)
        sender_thread.start()
        sender_thread.join()
        if not self.listener.msj_is_send:
            threading.Thread(
                target=self.listener.listen_socket, daemon=True).start()
        else:
            sys.exit(0)

    def handle_message(self):
        self.tray_app.open_main_window(0)

    def run(self):

        self.check_single_instance()
        # si esta el parametro HEADLESS no se abre la interfaz
        try:
            if sys.argv[1] in HEADLESS_PARAMS:
                pass
        except IndexError:  # por si no se le pasa parametros
            self.tray_app.main_window.show()
        except Exception as e:
            print(f"Error: parameter exception {e}")
            raise Exception(f"Unexpected error: parameter exception {e}")
        self.tray_app.show_notifications()
        os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '0'
        self.app.setQuitOnLastWindowClosed(False)
        sys.exit(self.app.exec_())


def main():
    runner = Main_app()
    runner.run()


if __name__ == '__main__':
    main()
