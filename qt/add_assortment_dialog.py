#РОБОЧА!!!!

from PyQt5 import QtCore, QtGui, QtWidgets
from sqlite_request import brigades_request_qt, work_centres_list, sqlite_is_assortment_exist, sqlite_insert_assortment


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        # ініціалізація макету, який буде розміщено у вікні. Макет розкидує елементи вертикально
        self.maket = QtWidgets.QVBoxLayout(Dialog)
        # випадаючий спиок робочих центрів і розміщення у ньому результату запиту у базу даних з таблиці назв робочих центрів
        # нульовий індекс - це коротка назва
        self.work_centres_combobox = QtWidgets.QComboBox(Dialog)
        self.work_centres_combobox.addItems([i[0] for i in work_centres_list()])
        # підпис
        self.work_centres_label = QtWidgets.QLabel(Dialog)
        self.work_centres_label.setText('Робочий центр:')
        # додаємо елементи ( вище ініціалізовані елементи)
        self.maket.addWidget(self.work_centres_label)
        self.maket.addWidget(self.work_centres_combobox)

        # випадаючий список складу бригад згідно відповіді із запиту у боазу даних таблиці бригад
        # перши індекс - це склад бригади
        self.brigade_composition_combobox = QtWidgets.QComboBox(Dialog)
        self.brigade_composition_combobox.addItems([i[1] for i in brigades_request_qt()])
        # при зміні вибраного занчення у списку бригад викликається функція зміни підпису під ним,
        # якій передається індекс обраного елемента списку
        self.brigade_composition_combobox.currentTextChanged.connect(
            lambda: self.brigade_comment(self.brigade_composition_combobox.currentIndex()))
        # верхній підпис
        self.brigade_composition_label = QtWidgets.QLabel(Dialog)
        self.brigade_composition_label.setText('Склад бригади:')
        # нижній динамічний підпис
        self.brigade_comment_label = QtWidgets.QLabel(Dialog)
        self.font_br_cmmnt = self.brigade_comment_label.font()
        self.font_br_cmmnt.setPointSize(10)
        self.brigade_comment_label.setFont(self.font_br_cmmnt)
        # додаємо елементи ( вище ініціалізовані елементи)
        self.maket.addWidget(self.brigade_composition_label)
        self.maket.addWidget(self.brigade_composition_combobox)
        self.maket.addWidget(self.brigade_comment_label)
        self.brigade_comment(self.brigade_composition_combobox.currentIndex())
        # додається відступ (висота 20)
        self.spacer = QtWidgets.QSpacerItem(100, 20, 0, 0)
        self.maket.addItem(self.spacer)
        # Ініціалізація поля введення і пидпису під полем
        self.assortment_label = QtWidgets.QLabel(Dialog)
        self.input_assortment = QtWidgets.QLineEdit(Dialog)
        self.temp_comment = QtWidgets.QLabel(Dialog)
        self.temp_comment.setText('Введіть назву асортименту')
        self.assortment_label.setText('Назва асортименту:')
        self.maket.addWidget(self.assortment_label)
        self.maket.addWidget(self.input_assortment)
        self.maket.addWidget(self.temp_comment)

        # підпис під полем введення. Якщо поле введення не пусте, перевіряється чи є у базі даних введений асортимент
        self.input_assortment.textChanged.connect(self.is_assortment_exists)

        # ініціалізація кнопок збереження і скасування
        self.buttons = QtWidgets.QDialogButtonBox(Dialog)
        # встановлення двох кнопок
        self.buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        # по дефолту кнопка збереження не активна, щоб не можна було випадково додати пустий асортимент (без назви)
        self.buttons.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
        # дія на натиснення на кнопку скасування і на кнопку збереження відповідно
        self.buttons.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(Dialog.close)
        self.buttons.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.save_button_action)
        self.maket.addWidget(self.buttons)




        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Додати Асортимент"))



    # за індексом комбобокса (х) повертається коментар до бригади у лейбл коментаря
    def brigade_comment(self, x):
        self.brigade_comment_label.setText([i[2] for i in brigades_request_qt()][x])


    # перевірка чи існує асортимент у базі даних
    def is_assortment_exists(self):
        # встановлення підпису під полем додавання асортименту залежно від відповіді функції
        # sqlite_is_assortment_exist(), якій передається текст з поля введення
        self.temp_comment.setText(sqlite_is_assortment_exist(self.input_assortment.text()))

        # Якщо відповідь (поле підпису) пуста і поле не пусте, то кнопка збереження стає активною
        # У іншому випадку кнопка неактивна
        if self.input_assortment.text() != '' and self.temp_comment.text() == '':
            self.buttons.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)
        else:
            self.buttons.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)

    # натиснення кнопки збереження вивкликає запит у базу даних
    # вставляються дані: назва асортименту, індекс робочого центру (id) та індекс (id) бригади
    def save_button_action(self):

        sqlite_insert_assortment(self.input_assortment.text(), work_centres_list()[self.work_centres_combobox.currentIndex()][1],
                                 brigades_request_qt()[self.brigade_composition_combobox.currentIndex()][0])
        # очищується поле введення
        self.input_assortment.clear()
        # підпис під полем про додання асортименту
        self.temp_comment.setText('Асортимент додано!')



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    MainWindow = QtWidgets.QWidget()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())