
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from sqlite_request import sqlite_positions_list, brigades_request_qt, sqlite_insert_brigade_composition


class Ui_Dialog(object):

    def __init__(self):
        # ініціалізація списка, у якому будуть зберігатись екземпляри лейблів, комбобоксів, кнопок видалення
        # кожної штатної одиниці бригади
        self.lst = []



    def setupUi(self, Dialog):

        #об'єкт діалога робимо глобальним, щоб мати доуступ до його внутрішніх об'єктів
        self.Dialog = Dialog

        #ініціалізація вікна
        Dialog.setObjectName("Dialog")
        Dialog.resize(710, 600)

        #кнопка додавання штатної одиниці. дія - додати лейбл-комбобокс-кнопку як одну штатно одиницю
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(510, 90, 150, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add_update_position_comboboxes)

        #додавання зони скроллінгу
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(10, 80, 481, 48))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setVisible(False)
        #ініціалізація якогось розміщувача віджетів на зоні скроллінгу
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 477, 297))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        #ініціалізація макета віджетів із сіткою
        self.button_layout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.button_layout.setGeometry(QtCore.QRect(0, 0, 481, 42))
        #встановлення трьох колонок зі співвідношенням сторін 5:10:1
        self.button_layout.setColumnStretch(0, 5)
        self.button_layout.setColumnStretch(1, 10)
        self.button_layout.setColumnStretch(2, 1)

        #додаємо стрічку редагування коментаря до нової бригади
        # + при зміні тексту викликаємо функцію, яка виконує певні перевірки
        self.brigade_comment_lineedit = QtWidgets.QLineEdit(Dialog)
        self.brigade_comment_lineedit.setGeometry(QtCore.QRect(10, 100, 481, 26))
        self.brigade_comment_lineedit.setObjectName("lineEdit")
        self.brigade_comment_lineedit.textChanged.connect(self.position_combobox_changed)

        #створення пари кнопок - Зберегти і Скасувати
        #вказуємо дії при їх натисненні. Кнопка Зберегти неактивна по дефолту
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(520, 380, 166, 27))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.ok_button_pressed)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(Dialog.close)

        #лейбл підпису рядка коментів
        self.brigade_comment_label = QtWidgets.QLabel(Dialog)
        self.brigade_comment_label.setGeometry(QtCore.QRect(10, 80, 200, 16))
        self.brigade_comment_label.setObjectName("label")

        #лейбл підису "Склад бригади"
        self.brigade_compos_label = QtWidgets.QLabel(Dialog)
        self.brigade_compos_label.setGeometry(QtCore.QRect(10, 420, 200, 16))
        self.brigade_compos_label.setObjectName("label")
        self.brigade_compos_label.setText('Склад бригади:')

        #динамічний лейбл, де висвітлюється динамічна інфа про обраний склад бригади
        self.brigade_compos_active_label = QtWidgets.QLabel(Dialog)
        self.brigade_compos_active_label.setGeometry(QtCore.QRect(135, 420, 600, 16))
        self.brigade_compos_active_label.setObjectName("label")
        self.font_br_compos_lbl = self.brigade_compos_active_label.font()
        self.font_br_compos_lbl.setPointSize(9)
        self.brigade_compos_active_label.setFont(self.font_br_compos_lbl)


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "< Додати позицію"))
        self.brigade_comment_label.setText(_translate("Dialog", "Коментар про бригаду"))



    def add_update_position_comboboxes(self, Dialog):
        #при натисненні додавання групи віджетів додавання штатної одиниці створюються екземпляри лейбл-комбобокс-кнопка
        #і додабться у вигляді сету до списку, який триматиме всі додані групи віджетів

        but, combobox, label = self.add_position_button_combobox()
        self.lst.append((label, combobox, but))
        #після кожного додвання запускається оновлення(перемальовування)
        self.update()



    def add_position_button_combobox(self):
        #створення екземпляра лейбла
        self.pisition_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pisition_label.setFont(font)

        #створення екземпларя комобобокса і запуск функції переевірок при зміні значення комбобокса
        self.position_combobox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.position_combobox.addItems(sqlite_positions_list())
        self.position_combobox.currentTextChanged.connect(self.position_combobox_changed)

        #створення екземпляра кнопки + дія (функція) при натисенні
        self.delete_position_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.delete_position_button.clicked.connect(self.del_worker)
        self.delete_position_button.setToolTip('Видалити')

        #повернення всіх цих екземплярів, які потім будуть додані до списку
        return self.delete_position_button, self.position_combobox, self.pisition_label


    def update(self):
        #оновлення елементів скролліногового поля і їх перемальовування

        for index, element in enumerate(self.lst):
            # оновлення лейблів. якщо видалено один чи додано інший, оновлюються підписи так, щоб вони були завжди по черзі пронумеровані
            element[0].setText(f"Працівник #{index + 1}")
            element[0].setObjectName(f"position_label_{index}")

            # оновлення комбобоксів аналогічно лейблам
            element[1].setObjectName(f"position_combobox_{index}")

            # оновлення кнопок видалення аналогічно лейблам
            element[2].setText("X")
            element[2].setObjectName(f"{index}")

        #Якщо ще не додано жодної групи, то поле скроллінгу не видно, якщо є елементи, то видно
        if len(self.lst) > 0:
            self.scrollArea.setVisible(True)
        else:
            self.scrollArea.setVisible(False)

        #встановлення меж поля скроллінгу. Якщо створено лише один елемент, то поле підігнане під один розмір
        #під більшу кількість елементів підганяється свій розмір поля
        for index, element in enumerate(self.lst):
            if index == 0:
                self.scrollArea.setGeometry(QtCore.QRect(10, 80, 481, 48))
            if index < 9 and index != 0:
                self.scrollArea.setGeometry(QtCore.QRect(10, 80, 481, 10+35*(index+1)))

            #і додаємо кожен елемент у кожне поле сітки скорлліногового поля
            self.button_layout.addWidget(element[0], index, 0)
            self.button_layout.addWidget(element[1], index, 1)
            self.button_layout.addWidget(element[2], index, 2)

            #показуємо кожен елемент
            element[0].show()
            element[1].show()
            element[2].show()




    def del_worker(self):
        #видалення групи елементів кожної штатної одиниці
        #при натисненні кнопки видаення певного елемента метод sender() класу Dialog отримує унікальну назву кнопки (індекс)
        #і за цим індексом отримується група елементів зі списку груп елементів додавання штатної одиниці
        index = int(self.Dialog.sender().objectName())

        #кожен елемент відповідно приховується, а потім видаляється зі списку елементів
        for element in self.lst[index]:
            element.hide()
        self.lst.pop(index)
        #зменшений список елементів мусить одновитись і відобразитись
        self.update()



    def position_combobox_changed(self):
        #при оновленні комбобоксів і поля введення отримується вся інфа з комбобоксів і цього поля введення

        #рядок, який містить через кому кожен обраний елемент всіх комбобоксів
        brigade_composition_string = ', '.join(i[1].currentText() for i in self.lst)
        #встановлення цього рядка у динамічний коментар
        self.brigade_compos_active_label.setText(brigade_composition_string)

        # перебираємо кожен склад бригади з бази даних
        for i in brigades_request_qt():
            #якщо така бригада вже існує, то кнопка збереження нективна і встановлюємо підпис про те, що бригада існує
            if brigade_composition_string == i[1]:
                self.brigade_compos_active_label.setText(f'Такий склад бригади вже існує! Назва: "{i[2]}"')
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
                break
            #якщо введено хочаб найменший коментар і обрано хоч одну штатну одиницю, то кнопка зебереження активна
            elif self.brigade_comment_lineedit.text() != '' and len(brigade_composition_string) > 0:
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
            #інакше кнопка не активна
            else:
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)



    def ok_button_pressed(self):
        #при натисненні кнопки збереження викликається функція, яка зберігає склад бригади, отриманий з комбобоксів
        #у вигляді переліку через кому, і коментар до цієї бригади, після збереження діалог заривається
        brigade_composition_string = ', '.join(i[1].currentText() for i in self.lst)
        sqlite_insert_brigade_composition(brigade_composition_string, self.brigade_comment_lineedit.text())
        self.Dialog.close()







if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    MainWindow = QtWidgets.QWidget()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
