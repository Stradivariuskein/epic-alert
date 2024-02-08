# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_app_daialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(747, 367)
        Dialog.setFixedSize(746, 366)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Dialog.setStyleSheet("* {\n"
"    font: 87 8pt \"Segoe UI Black\";\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
".nav-btn { \n"
"    max-width: 40px;\n"
"    font-size: 28px;\n"
"}\n"
"\n"
"QLabel {\n"
"    font-size: 28px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QLabel#background_img {\n"
"    padding: 0px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"QLabel#title_game {\n"
"    background-color: rgba(0, 0, 0, 100);\n"
"}\n"
"\n"
"QPushButton#exit_btn {\n"
"    font-size: 36px;\n"
"    margin: 0;\n"
"}\n"
"\n"
"QPushButton#previus_button {\n"
"\n"
"        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 100), stop:1 rgba(0, 0, 0, 0));\n"
"\n"
"}\n"
"\n"
"QPushButton#next_button {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 100));\n"
"}\n"
"\n"
"QLabel#date {\n"
"    background-color: rgba(0, 0, 0, 100);\n"
"    font-size: 18px;\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.background_layout = QtWidgets.QGridLayout()
        self.background_layout.setSpacing(0)
        self.background_layout.setObjectName("background_layout")
        self.header = QtWidgets.QWidget(Dialog)
        self.header.setObjectName("header")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.header)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.exit_btn = QtWidgets.QPushButton(self.header)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit_btn.sizePolicy().hasHeightForWidth())
        self.exit_btn.setSizePolicy(sizePolicy)
        self.exit_btn.setMaximumSize(QtCore.QSize(40, 47))
        self.exit_btn.setSizeIncrement(QtCore.QSize(0, 0))
        self.exit_btn.setObjectName("exit_btn")
        #self.gridLayout_2.addWidget(self.exit_btn, 0, 0, 1, 1)
        self.title_game = QtWidgets.QLabel(self.header)
        self.title_game.setLineWidth(1)
        self.title_game.setMidLineWidth(0)
        self.title_game.setAlignment(QtCore.Qt.AlignCenter)
        self.title_game.setWordWrap(False)
        self.title_game.setIndent(1)
        self.title_game.setObjectName("title_game")
        #self.gridLayout_2.addWidget(self.title_game, 0, 1, 1, 1)
        #self.background_layout.addWidget(self.header, 1, 0, 1, 1)
        self.body = QtWidgets.QWidget(Dialog)
        self.body.setObjectName("body")
        self.gridLayout = QtWidgets.QGridLayout(self.body)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.buy_button = QtWidgets.QPushButton(self.body)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buy_button.sizePolicy().hasHeightForWidth())
        self.buy_button.setSizePolicy(sizePolicy)
        self.buy_button.setObjectName("buy_button")
        self.gridLayout.addWidget(self.buy_button, 0, 1, 1, 1)
        self.previus_button = QtWidgets.QPushButton(self.body)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previus_button.sizePolicy().hasHeightForWidth())
        self.previus_button.setSizePolicy(sizePolicy)
        self.previus_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.previus_button.setObjectName("previus_button")
        self.gridLayout.addWidget(self.previus_button, 0, 0, 1, 1)
        self.next_button = QtWidgets.QPushButton(self.body)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next_button.sizePolicy().hasHeightForWidth())
        self.next_button.setSizePolicy(sizePolicy)
        self.next_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.next_button.setObjectName("next_button")
        self.gridLayout.addWidget(self.next_button, 0, 2, 1, 1)
        self.date = QtWidgets.QLabel(self.body)
        self.date.setAlignment(QtCore.Qt.AlignCenter)
        self.date.setObjectName("date")
        self.gridLayout.addWidget(self.date, 1, 0, 1, 3)
        #self.background_layout.addWidget(self.body, 2, 0, 1, 1)
        self.background_img = QtWidgets.QLabel(Dialog)
        self.background_img.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.background_img.sizePolicy().hasHeightForWidth())
        self.background_img.setSizePolicy(sizePolicy)
        self.background_img.setSizeIncrement(QtCore.QSize(0, 0))
        self.background_img.setTabletTracking(True)
        self.background_img.setStatusTip("")
        self.background_img.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.background_img.setLineWidth(0)
        self.background_img.setMidLineWidth(0)
        self.background_img.setText("")
        self.background_img.setWordWrap(False)
        self.background_img.setObjectName("background_img")
        #self.background_layout.addWidget(self.background_img, 0, 0, 1, 1)
        self.horizontalLayout.addLayout(self.background_layout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.exit_btn.setText(_translate("Dialog", "X"))
        self.title_game.setText(_translate("Dialog", "title"))
        self.buy_button.setText(_translate("Dialog", "buy game"))
        self.previus_button.setText(_translate("Dialog", "<"))
        self.previus_button.setProperty("class", _translate("Dialog", "nav-btn"))
        self.next_button.setText(_translate("Dialog", ">"))
        self.next_button.setProperty("class", _translate("Dialog", "nav-btn"))
        self.date.setText(_translate("Dialog", "date"))
