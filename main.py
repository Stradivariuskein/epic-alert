from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from ui_app_dialog import *
import sys
import requests
from auto_buy_game import ApiFreeGame
from playwright.sync_api import sync_playwright
#image_url = 'https://cdn1.epicgames.com/spt-assets/27da8c9da5774ade943fb2d5490bfc99/doors--paradox-1yr08.jpg?h=480&quality=medium&resize=1&w=854'
WINDOWS_HEIGHT = 366
WINDOWS_WIDTH = 746

class App(QDialog):
    def __init__(self, games=None):
        super().__init__()
        self.ui = Ui()
        self.ui.setupUi(self)
        self.games = games
        self.index_game = 0
        self.show_game()

        self.ui.exit_btn.clicked.connect(self.close_windows)
        self.ui.next_button.clicked.connect(self.view_next_game)        
        self.ui.previous_button.clicked.connect(self.view_previous_game)
        
        self.set_background_img()

        # self.put_elements_body()
        self.put_elements_windows()
        self.put_elements_header()
        
        self.resize_grid()

        self.show()
        
    def show_game(self):
        self.ui.title_game.setText(self.games[self.index_game].title_game)
        self.ui.expiration.setText(self.games[self.index_game].expiration)
        self.set_background_img()
        
    def set_background_img(self):
         # Cargar la imagen desde una URL y establecerla en el QLabel
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(requests.get(self.games[self.index_game].img_src).content)
        
        # Escalar la imagen al alto deseado (300px)746, 366
        scaled_pixmap = pixmap.scaledToHeight(WINDOWS_HEIGHT, QtCore.Qt.SmoothTransformation)
        # si la imagen no ocupa toda la ventana ajusta el tamaño de la imagen 
        if scaled_pixmap.width() < WINDOWS_WIDTH:
            scaled_value = (1 - scaled_pixmap.width() / WINDOWS_WIDTH) + 1
            img_width = int(scaled_value * WINDOWS_WIDTH)
            scaled_pixmap = pixmap.scaledToWidth(img_width, QtCore.Qt.SmoothTransformation)
        # pone la imagen
        self.ui.background_img.setPixmap(scaled_pixmap)
        self.ui.background_img.lower() # mando la imagen al fondo
        

    def put_elements_windows(self):
        self.ui.background_layout.addWidget(self.ui.header, 0, 0, 1, 1)
        self.ui.background_layout.addWidget(self.ui.background_img, 0, 0, 2, 1)
        self.ui.background_layout.addWidget(self.ui.body, 1, 0, 1, 1)

    def put_elements_header(self):
        self.ui.gridLayout_2.addWidget(self.ui.exit_btn, 0, 0, 1, 1)
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
            self.show_game()
            
    def view_previous_game(self):
        if self.index_game > 0:
            self.index_game -= 1
            self.show_game()

    def close_windows(self):
        self.close()



if __name__ == '__main__':
    with sync_playwright() as playwright:
        api_epic = ApiFreeGame(playwright)
        games = api_epic.get_free_games()
        app = QApplication(sys.argv)
        my_app = App(games)

        my_app.show()
        sys.exit(app.exec_())