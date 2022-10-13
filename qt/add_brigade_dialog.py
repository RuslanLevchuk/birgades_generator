# РОБОЧА!!!!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):

    def __init__(self):
        self.lst = []
        self.some_str = ''
        self.vertical_position = 10
        self.vertical_position_shift = 30


        self.buttons = []


    def setupUi(self, Dialog):

        self.Dialog = Dialog

        Dialog.setObjectName("Dialog")
        Dialog.resize(710, 450)


        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(510, 90, 150, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add_update_position_comboboxes)

        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(10, 80, 481, 48))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setVisible(False)






        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 477, 297))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)




        self.button_layout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.button_layout.setGeometry(QtCore.QRect(0, 0, 481, 42))
        self.button_layout.setColumnStretch(0, 5)
        self.button_layout.setColumnStretch(1, 10)
        self.button_layout.setColumnStretch(2, 1)








        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(10, 40, 481, 26))
        self.lineEdit.setObjectName("lineEdit")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(520, 380, 166, 27))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.ok_button_pressed)


        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 200, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "< Додати позицію"))
        self.label.setText(_translate("Dialog", "Коментар про бригаду"))



    def add_update_position_comboboxes(self, Dialog):


        but, combobox, label = self.add_position_button_combobox()
        self.lst.append((label, combobox, but))
        self.update()



    def add_position_button_combobox(self):

        self.pisition_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pisition_label.setFont(font)

        self.position_combobox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.position_combobox.addItems(['a', 'b', 'c', 'd'])

        self.delete_position_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.delete_position_button.clicked.connect(self.del_worker)
        self.delete_position_button.setToolTip('Видалити')

        return self.delete_position_button, self.position_combobox, self.pisition_label


    def update(self):

        for index, element in enumerate(self.lst):
            # оновлення лейблів
            element[0].setText(f"Працівник #{index + 1}")
            element[0].setObjectName(f"position_label_{index}")

            # оновлення комбобоксів
            element[1].setObjectName(f"position_combobox_{index}")

            # оновлення кнопок видалення
            element[2].setText("X")
            element[2].setObjectName(f"{index}")


        if len(self.lst) > 0:
            self.scrollArea.setVisible(True)
        else:
            self.scrollArea.setVisible(False)

        for index, element in enumerate(self.lst):
            if index == 0:
                self.scrollArea.setGeometry(QtCore.QRect(10, 80, 481, 48))
            if index < 9 and index != 0:
                self.scrollArea.setGeometry(QtCore.QRect(10, 80, 481, 10+35*(index+1)))

            self.button_layout.addWidget(element[0], index, 0)
            self.button_layout.addWidget(element[1], index, 1)
            self.button_layout.addWidget(element[2], index, 2)

            element[0].show()
            element[1].show()
            element[2].show()




    def del_worker(self):

        index = int(self.Dialog.sender().objectName())
        print(index)
        for element in self.lst[index]:
            element.hide()
        self.lst.pop(int(self.Dialog.sender().objectName()))
        self.update()



    def ok_button_pressed(self, Dialog):
        for element in self.lst:
            self.some_str += element[1].currentText()
            #self.some_str += str(i[0])
        self.lineEdit.setText(self.some_str)







if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    MainWindow = QtWidgets.QWidget()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
