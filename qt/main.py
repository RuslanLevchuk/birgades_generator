# РОБОЧА!!!!


from PyQt5 import QtCore, QtGui, QtWidgets
from add_assortment_dialog import Ui_Dialog
from  add_brigade_dialog import  Ui_Dialog as UI

class Ui_MainWindow(object):
    def open_dialog(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def open_dialog_2(self):
        self.window = QtWidgets.QDialog()
        self.ui = UI()
        self.ui.setupUi(self.window)
        self.window.show()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Списки")
        MainWindow.setFixedSize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.q_add_asortment_button = QtWidgets.QPushButton(self.centralwidget)
        self.q_add_asortment_button.setGeometry(QtCore.QRect(775, 725, 200, 30))
        self.q_add_asortment_button.setText('Додати Асортимент')
        self.q_add_asortment_button.clicked.connect(self.open_dialog)

        self.q_add_asortment_button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.q_add_asortment_button_2.setGeometry(QtCore.QRect(600, 725, 200, 30))
        self.q_add_asortment_button_2.setText('Додати Асортимент')
        self.q_add_asortment_button_2.clicked.connect(self.open_dialog_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)





        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())