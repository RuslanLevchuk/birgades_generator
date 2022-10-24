# РОБОЧА!!!


from PyQt5 import QtCore, QtGui, QtWidgets
from add_assortment_dialog import Ui_Dialog as UI_add_assortment_dialog
from add_brigade_dialog import Ui_Dialog as UI_add_brigade_dialog
from edit_brigade_dialog import Ui_Dialog as UI_edit_brigade_dialog
from main_generator import generate as generate_xlsx


class Ui_MainWindow(object):
    def open_dialog_add_assortment(self):
        self.window = QtWidgets.QDialog()
        self.ui = UI_add_assortment_dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def open_dialog_add_brigade(self):
        self.window = QtWidgets.QDialog()
        self.ui = UI_add_brigade_dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def open_dialog_edit_brigade(self):
        self.window = QtWidgets.QDialog()
        self.ui = UI_edit_brigade_dialog()
        self.ui.setupUi(self.window)
        self.window.show()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Списки")
        MainWindow.setFixedSize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.open_xlsx_file_label = QtWidgets.QLabel(self.centralwidget)
        self.open_xlsx_file_label.setGeometry(QtCore.QRect(20, 10, 200, 16))
        self.open_xlsx_file_label.setText('Відкрити файл із завданням:')


        self.open_xlsx_file_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.open_xlsx_file_lineedit.setGeometry(QtCore.QRect(20, 35, 600, 32))


        self.open_xlsx_file_button = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.open_xlsx_file_button.setStandardButtons(QtWidgets.QDialogButtonBox.Open)
        self.open_xlsx_file_button.setGeometry(QtCore.QRect(20, 35, 710, 32))
        self.open_xlsx_file_button.button(QtWidgets.QDialogButtonBox.Open).setText('Огляд')
        self.open_xlsx_file_button.clicked.connect(self.open_xlsx_button_action)

        self.make_brigades_button = QtWidgets.QPushButton(self.centralwidget)
        self.make_brigades_button.setGeometry(QtCore.QRect(760, 35, 200, 30))
        self.make_brigades_button.setText('Сформувати завдання')
        self.make_brigades_button.setEnabled(False)

        self.make_brigades_button.clicked.connect(self.generate_button_action)




        self.q_add_asortment_button = QtWidgets.QPushButton(self.centralwidget)
        self.q_add_asortment_button.setGeometry(QtCore.QRect(775, 725, 180, 30))
        self.q_add_asortment_button.setText('Додати Асортимент')
        self.q_add_asortment_button.clicked.connect(self.open_dialog_add_assortment)

        self.q_add_brigade_button = QtWidgets.QPushButton(self.centralwidget)
        self.q_add_brigade_button.setGeometry(QtCore.QRect(415, 725, 150, 30))
        self.q_add_brigade_button.setText('Додати Бригаду')
        self.q_add_brigade_button.clicked.connect(self.open_dialog_add_brigade)

        self.q_edit_brigade_button = QtWidgets.QPushButton(self.centralwidget)
        self.q_edit_brigade_button.setGeometry(QtCore.QRect(590, 725, 160, 30))
        self.q_edit_brigade_button.setText('Редагувати Бригаду')
        self.q_edit_brigade_button.clicked.connect(self.open_dialog_edit_brigade)

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



    def open_xlsx_button_action(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Відкрити файл EXCEL", "",
                                                  'Excel Files (*.xlsx)', options=options)
        self.open_xlsx_file_lineedit.setText(fileName)
        if self.open_xlsx_file_lineedit.text() != '':
            self.make_brigades_button.setEnabled(True)



    def generate_button_action(self):
        generate_xlsx(self.open_xlsx_file_lineedit.text())
        self.open_xlsx_file_lineedit.clear()
        self.make_brigades_button.setEnabled(False)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())