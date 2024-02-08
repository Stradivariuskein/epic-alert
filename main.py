from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from ui_app_daialog import *
import sys
import requests
image_url = 'https://cdn1.epicgames.com/spt-assets/27da8c9da5774ade943fb2d5490bfc99/doors--paradox-1yr08.jpg?h=480&quality=medium&resize=1&w=854'
WINDWOS_HEIGHT = 366
WINDOWS_WIDTH = 746
class TestImg(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui()
        self.ui.setupUi(self)

        self.ui.exit_btn.clicked.connect(lambda: self.close_windows())
        # Cargar la imagen desde una URL y establecerla en el QLabel
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(requests.get(image_url).content)
        # Escalar la imagen al alto deseado (300px)746, 366
        scaled_pixmap = pixmap.scaledToHeight(WINDWOS_HEIGHT, QtCore.Qt.SmoothTransformation)
        if scaled_pixmap.width() < WINDOWS_WIDTH:
            scaled_value = (1 - scaled_pixmap.width() / WINDOWS_WIDTH) + 1
            img_width = int(scaled_value * WINDOWS_WIDTH)
            scaled_pixmap = pixmap.scaledToWidth(img_width, QtCore.Qt.SmoothTransformation)
        self.ui.background_img.setPixmap(scaled_pixmap)
        self.ui.background_img.lower() # mando la imagen al fondo

        # self.put_elements_body()
        self.put_elemntes_windwos()
        self.put_elements_header()
        
        self.resize_grid()

        self.show()

    def put_elemntes_windwos(self):
        self.ui.background_layout.addWidget(self.ui.header, 0, 0, 1, 1)
        self.ui.background_layout.addWidget(self.ui.background_img, 0, 0, 2, 1)
        self.ui.background_layout.addWidget(self.ui.body, 1, 0, 1, 1)

    def put_elements_header(self):
        self.ui.gridLayout_2.addWidget(self.ui.exit_btn, 0, 0, 1, 1)
        self.ui.exit_btn.raise_()
        self.ui.gridLayout_2.addWidget(self.ui.title_game, 0, 0, 1, 2)

    def put_elements_body(self):
        
        self.ui.gridLayout.addWidget(self.ui.previus_button, 0, 0, 2, 1)
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

    # cambiara la imagen el titulo, link y fehca con una animacion de delis
    def view_next_game(self):
        pass
    def view_previus_game(self):
        pass

    def close_windows(self):
        self.close()



if __name__ == '__main__':


    app = QApplication(sys.argv)
    my_app = TestImg()

    my_app.show()
    sys.exit(app.exec_())