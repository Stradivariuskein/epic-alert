from PyQt5.QtWidgets import QApplication, QDialog, QWidget
from PyQt5.QtCore import QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QIcon, QPixmap
from ui_app_dialog import Ui
import sys
import requests
from auto_buy_game import ApiFreeGame

WINDOWS_HEIGHT = 366
WINDOWS_WIDTH = 746


class App(QDialog):
    def __init__(self, games=None):
        super().__init__()
        self.ui = Ui()
        self.ui.setupUi(self)
        self.icon = QIcon("icon.png")
        self.setWindowIcon(self.icon)
        self.games = games
        self.download_images()

        self.index_game = 0
        self.animations = {
            'next': [],
            'back': []
        }
        self.show_game()
        self.set_background_img()
        self.ui.exit_btn.clicked.connect(self.close_windows)
        self.ui.next_button.clicked.connect(self.view_next_game)
        self.ui.previous_button.clicked.connect(self.view_previous_game)

        # self.put_elements_body()
        self.put_elements_windows()
        self.put_elements_header()
        self.resize_grid()

    def download_images(self):
        if self.games is not None:
            self.img_games = []
            for i in range(len(self.games)):
                # Cargar la imagen desde una URL y establecerla en el QLabel
                pixmap = QPixmap()
                pixmap.loadFromData(
                    requests.get(
                        self.games[i].img_src
                        ).content
                        )
                # Escalar la imagen al alto deseado (300px)746, 366
                scaled_pixmap = pixmap.scaledToHeight(
                    WINDOWS_HEIGHT,
                    Qt.SmoothTransformation
                    )
                # si la imagen no ocupa toda la ventana
                # ajusta el tamaño de la imagen
                if scaled_pixmap.width() < WINDOWS_WIDTH:
                    scaled_value = (
                        (1 - scaled_pixmap.width() / WINDOWS_WIDTH) + 1
                        )
                    img_width = int(scaled_value * WINDOWS_WIDTH)
                    scaled_pixmap = pixmap.scaledToWidth(
                        img_width,
                        Qt.SmoothTransformation
                        )
                self.img_games.append(scaled_pixmap)
            return len(self.img_games) == len(self.games)

    def show_game(self):

        self.ui.title_game.setText(
            self.games[self.index_game]
            .title_game.upper()
            )
        self.ui.expiration.setText(
            self.games[self.index_game]
            .expiration.upper()
            )
        # en la primera iteración no hay una función asignada
        if (
            self.ui.buy_button.receivers(self.ui.buy_button.clicked) == 1
        ):
            self.ui.buy_button.clicked.disconnect(self.buy_game)

        self.ui.buy_button.clicked.connect(self.buy_game)

    def buy_game(self):
        self.games[self.index_game].open_in_store()

    def set_background_img(self, element=None, index_game=None):
        if element is None:
            element = self.ui.background_img

        if index_game is None:
            index_game = self.index_game
        elif not (index_game >= 0 and index_game <= len(self.games)):
            raise IndexError("out of range index")

        # pone la imagen
        try:
            element.setPixmap(self.img_games[index_game])
        except IndexError:
            print("Error: IndexError, missing images")
            element.setPixmap(QPixmap())

    def put_elements_windows(self):
        self.ui.background_layout.addWidget(self.ui.header, 0, 0, 1, 1)
        self.ui.background_layout.addWidget(self.ui.background_img, 0, 0, 2, 1)
        self.ui.background_img.lower()  # mando la imagen al fondo
        self.ui.background_layout.addWidget(
            self.ui.next_background_img,
            0, 0, 2, 1)
        self.ui.next_background_img.lower()  # mando la imagen al fondo
        self.ui.background_layout.addWidget(self.ui.body, 1, 0, 1, 1)

    def put_elements_header(self):
        self.ui.gridLayout_2.addWidget(self.ui.exit_btn, 0, 1, 1, 1)
        self.ui.exit_btn.raise_()
        self.ui.gridLayout_2.addWidget(self.ui.title_game, 0, 0, 1, 2)

    def put_elements_body(self):
        self.ui.gridLayout.addWidget(self.ui.previous_button, 0, 0, 2, 1)
        self.ui.gridLayout.addWidget(self.ui.buy_button, 0, 1, 1, 1)
        self.ui.gridLayout.addWidget(self.ui.next_button, 0, 2, 2, 1)
        self.ui.gridLayout.addWidget(self.ui.date, 1, 1, 1, 1)

    def resize_grid(self):
        # Configurar el grid predefinido
        self.ui.gridLayout.setColumnStretch(0, 30)
        self.ui.gridLayout.setColumnStretch(1, 200)
        self.ui.gridLayout.setColumnStretch(2, 30)

        self.ui.gridLayout.setRowStretch(0, 500)
        self.ui.gridLayout.setRowStretch(1, 50)

        self.ui.gridLayout.setSpacing(0)

    def set_games(self, games: dict[str]) -> None:
        self.games = games

    # cambiara la imagen el titulo, link y fecha con una animación de delis
    def view_next_game(self):
        len_games = len(self.games) - 1
        if self.index_game < len_games:
            self.index_game += 1
            self.set_animation_next()
            self.start_animation_next()
            self.show_game()

    def view_previous_game(self):
        if self.index_game > 0:
            self.index_game -= 1
            self.set_animation_back()
            self.start_animation_back()
            self.show_game()

    def _set_animation_slide_next(
            self, current: QWidget,
            next: QWidget,
            next_start_position: int
            ):
        current_move_animation = QPropertyAnimation(current, b'geometry')
        current_move_animation.setDuration(750)
        rect = QRect(0, 0, WINDOWS_WIDTH, WINDOWS_HEIGHT)
        current_move_animation.setStartValue(rect)
        rect = QRect(
            int(- (WINDOWS_WIDTH * .2)),
            0,
            WINDOWS_WIDTH,
            WINDOWS_HEIGHT
            )
        current_move_animation.setKeyValueAt(0.4, rect)
        rect = QRect(
            int(- (WINDOWS_WIDTH * .8)),
            0,
            WINDOWS_WIDTH,
            WINDOWS_HEIGHT
            )
        current_move_animation.setKeyValueAt(0.8, rect)
        rect = QRect(-WINDOWS_WIDTH, 0, WINDOWS_WIDTH, WINDOWS_HEIGHT)
        current_move_animation.setKeyValueAt(1, rect)
        next_move_animation = QPropertyAnimation(next, b'geometry')
        next_move_animation.setDuration(750)
        rect = QRect(next_start_position, 0, WINDOWS_WIDTH, WINDOWS_HEIGHT)
        next_move_animation.setStartValue(rect)
        rect = QRect(
            int((WINDOWS_WIDTH * .8)),
            0,
            WINDOWS_WIDTH,
            WINDOWS_HEIGHT
            )
        next_move_animation.setKeyValueAt(0.4, rect)
        rect = QRect(
            int((WINDOWS_WIDTH * .2)),
            0,
            WINDOWS_WIDTH,
            WINDOWS_HEIGHT
            )
        next_move_animation.setKeyValueAt(0.8, rect)
        rect = QRect(0, 0, WINDOWS_WIDTH, WINDOWS_HEIGHT)
        next_move_animation.setKeyValueAt(1, rect)
        self.animations['next'] = [current_move_animation, next_move_animation]

    def _set_animation_slide_back(
            self,
            current: QWidget,
            next: QWidget,
            next_start_position: int
            ):
        current_move_animation = QPropertyAnimation(current, b'geometry')
        current_move_animation.setDuration(750)
        rect = QRect(0, 0, WINDOWS_WIDTH, WINDOWS_HEIGHT)
        # current_move_animation.setStartValue(current.geometry())
        current_move_animation.setStartValue(rect)
        rect = QRect(
            int((WINDOWS_WIDTH * 0.2)),
            0,
            WINDOWS_WIDTH,
            WINDOWS_HEIGHT
            )
        current_move_animation.setKeyValueAt(0.4, rect)
        rect = QRect(
            int((WINDOWS_WIDTH * .8)),
            0,
            WINDOWS_WIDTH,
            WINDOWS_HEIGHT
            )
        current_move_animation.setKeyValueAt(0.8, rect)
        rect = QRect(WINDOWS_WIDTH, 0, WINDOWS_WIDTH, WINDOWS_HEIGHT)
        current_move_animation.setKeyValueAt(1, rect)
        next_move_animation = QPropertyAnimation(next, b'geometry')
        next_move_animation.setDuration(750)
        rect = QRect(next_start_position, 0, WINDOWS_WIDTH, WINDOWS_HEIGHT)
        # next_move_animation.setStartValue(next.geometry())
        next_move_animation.setStartValue(rect)
        rect = QRect(
            int(next_start_position+(WINDOWS_WIDTH * .2)),
            0,
            WINDOWS_WIDTH,
            WINDOWS_HEIGHT
            )
        next_move_animation.setKeyValueAt(0.4, rect)
        rect = QRect(
            int(next_start_position+(WINDOWS_WIDTH * .8)),
            0,
            WINDOWS_WIDTH,
            WINDOWS_HEIGHT
            )
        next_move_animation.setKeyValueAt(0.8, rect)
        rect = QRect(0, 0, WINDOWS_WIDTH, WINDOWS_HEIGHT)
        next_move_animation.setKeyValueAt(1, rect)

        self.animations['back'] = [current_move_animation, next_move_animation]

    def set_animation_next(self):
        start_next_position = WINDOWS_WIDTH
        self.set_background_img(element=self.ui.next_background_img)
        self.set_background_img(index_game=self.index_game - 1)
        self._set_animation_slide_next(
            self.ui.background_img,
            self.ui.next_background_img,
            start_next_position
            )

    def set_animation_back(self):
        start_next_position = -WINDOWS_WIDTH
        self.set_background_img(element=self.ui.next_background_img)
        self.set_background_img(index_game=self.index_game + 1)
        self._set_animation_slide_back(
            self.ui.background_img,
            self.ui.next_background_img,
            start_next_position
            )

    def start_animation_next(self):

        for animation in self.animations['next']:
            animation.start()

    def start_animation_back(self):

        for animation in self.animations['back']:
            animation.start()

    def close_windows(self):
        self.close()


if __name__ == '__main__':

    api_epic = ApiFreeGame()
    games = api_epic.get_free_games()

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icono.png"))

    my_app = App(games)
    my_app.show()
    sys.exit(app.exec_())
