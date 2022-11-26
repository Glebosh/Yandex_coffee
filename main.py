import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget


class Add_redact(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.initUI()
    
    def initUI(self):
        self.connection = sqlite3.connect("coffee.sqlite")

        self.btn_add.clicked.connect(self.adding)
        self.btn_red.clicked.connect(self.redact)
        self.pushButton_2.clicked.connect(self.choose)

        self.query = ''
        self.modified = {}

    def choose(self):
        try:
            id = self.line_id.text()
            if id:
                ids = self.connection.cursor().execute("""SELECT ID FROM coffee""").fetchall()
                ids = [i[0] for i in ids]
                if int(id) in ids:
                    self.query = f"""SELECT
                        sorts.name,
                        coffee.taste,
                        coffee.price,
                        coffee.volume
                        FROM coffee
                        LEFT JOIN roasting ON coffee.roasting = roasting.ID
                        LEFT JOIN sorts ON coffee.name = sorts.ID
                        LEFT JOIN types ON coffee.type = types.ID
                        WHERE coffee.ID = {int(id)}"""
                    
                    res = self.connection.cursor().execute(self.query).fetchone()
                    
                    self.line_redname.setText(res[0])
                    self.plainText2.setPlainText(res[1])
                    self.line_redprice.setText(str(res[2]))
                    self.line_redvolume.setText(str(res[3]))

                    t = []
                    for i in [i[0] for i in self.connection.cursor().execute("""SELECT name FROM roasting""").fetchall()]:
                        t.append(i)
                    self.comBox3.addItems(t)

                    t = []
                    for i in [i[0] for i in self.connection.cursor().execute("""SELECT name FROM types""").fetchall()]:
                        t.append(i)
                    self.comboBox_2.addItems(t)

        except ValueError:
            print('Введено не число')
        # except Exception:
        #     print('Неизвестная ошибка')

    def adding(self):
        pass

    def redact(self):
        pass


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        self.connection = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.add)
        self.query = """SELECT
            sorts.name,
            roasting.name,
            types.name,
            coffee.taste,
            coffee.price,
            coffee.volume
            FROM coffee
            LEFT JOIN roasting ON coffee.roasting = roasting.ID
            LEFT JOIN sorts ON coffee.name = sorts.ID
            LEFT JOIN types ON coffee.type = types.ID"""
        
        self.select_data()

    def add(self):
        self.form = Add_redact(self)
        self.form.show()
    
    def select_data(self):
        res = self.connection.cursor().execute(self.query).fetchall()

        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setRowCount(0)

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        
        
        self.tableWidget.setColumnWidth(3, 200)
        self.tableWidget.setColumnWidth(2, 140)
        self.tableWidget.setColumnWidth(1, 115)
        self.tableWidget.setHorizontalHeaderLabels(['Сорт кофе', 'Степень прожарки', 'Молотый/в зёрнах', 'Описание', 'Цена', 'Объём упаковки'])


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = Main()
        ex.show()
        sys.exit(app.exec())
    except Exception:
        print("Ошибка с файлами!!!")