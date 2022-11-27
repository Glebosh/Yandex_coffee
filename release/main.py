import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget

import main_ui as form_1
import addEditCoffeeForm_ui as form_2


class Add_redact(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('release\\UI\\addEditCoffeeForm.ui', self)
        self.initUI()
    
    def initUI(self):
        self.connection = sqlite3.connect("release\\data\\coffee.sqlite")

        t = []
        for i in [i[0] for i in self.connection.cursor().execute("""SELECT name FROM roasting""").fetchall()]:
            t.append(i)
        self.comBox1.addItems(t)

        t = []
        for i in [i[0] for i in self.connection.cursor().execute("""SELECT name FROM types""").fetchall()]:
            t.append(i)
        self.comBox2.addItems(t)

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
                        coffee.volume,
                        coffee.ID
                        FROM coffee
                        LEFT JOIN roasting ON coffee.roasting = roasting.ID
                        LEFT JOIN sorts ON coffee.name = sorts.ID
                        LEFT JOIN types ON coffee.type = types.ID
                        WHERE coffee.ID = {int(id)}"""
                    
                    res = self.connection.cursor().execute(self.query).fetchone()
                    
                    self.id = res[4]
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
        name = self.line_addname.text()
        price = self.line_addprice.text()
        volume = self.line_addvolume.text()
        text = self.plainText1.toPlainText()
        rost = self.comBox1.currentText()
        type = self.comBox2.currentText()

        # Проверка имени
        names = self.connection.cursor().execute("""SELECT name FROM sorts""").fetchall()
        try:
            int(''.join(''.join(''.join(''.join(name.split('.')).split(',')).split(';')).split(':')))
            print('Введите строковое значение у имени')
        except Exception:
            # Проверка цены и объёма
            try:
                price = int(price)
                volume = int(volume)
            except ValueError:
                print('Введено не целое число у цены или объёма')
            else:
                if price <= 0 or volume <= 0:
                    print('Введено отрицательное число или ноль у цены или объёма')
                else:
                    # Проверка вкуса
                    if not text:
                        print('Не введено описание вкуса')
                    else:
                        try:
                            cur = self.connection.cursor()

                            if name not in names:
                                cur.execute("""INSERT INTO sorts(name)
                                    VALUES(?)""", (name,))
                                
                            name = cur.execute("""SELECT ID FROM sorts
                            WHERE name = ?""", (name,)).fetchone()

                            rost = cur.execute("""SELECT ID FROM roasting
                            WHERE name = ?""", (rost,)).fetchone()

                            type = cur.execute("""SELECT ID FROM types
                            WHERE name = ?""", (type,)).fetchone()
                                
                            cur.execute("""INSERT INTO coffee(name, roasting, type, taste, price, volume)
                            VALUES(?, ?, ?, ?, ?, ?)""", (name[0], rost[0], type[0], text, price, volume))

                            self.connection.commit()
                            self.close()
                        except Exception:
                                print('Неизвестная ошибка')
                                self.close

    def redact(self):
        name = self.line_redname.text()
        price = self.line_redprice.text()
        volume = self.line_redvolume.text()
        text = self.plainText2.toPlainText()
        rost = self.comBox3.currentText()
        type = self.comboBox_2.currentText()

        # Проверка имени
        names = self.connection.cursor().execute("""SELECT name FROM sorts""").fetchall()
        try:
            int(''.join(''.join(''.join(''.join(name.split('.')).split(',')).split(';')).split(':')))
            print('Введите строковое значение у имени')
        except Exception:
            # Проверка цены и объёма
            try:
                price = int(price)
                volume = int(volume)
            except ValueError:
                print('Введено не целое число у цены или объёма')
            else:
                if price <= 0 or volume <= 0:
                    print('Введено отрицательное число или ноль у цены или объёма')
                else:
                    # Проверка вкуса
                    if not text:
                        print('Не введено описание вкуса')
                    else:
                        try:
                            cur = self.connection.cursor()

                            if name not in names:
                                cur.execute("""INSERT INTO sorts(name)
                                    VALUES(?)""", (name,))
                                
                            name = cur.execute("""SELECT ID FROM sorts
                            WHERE name = ?""", (name,)).fetchone()

                            rost = cur.execute("""SELECT ID FROM roasting
                            WHERE name = ?""", (rost,)).fetchone()

                            type = cur.execute("""SELECT ID FROM types
                            WHERE name = ?""", (type,)).fetchone()

                            # Изменение coffee
                            cur.execute("""UPDATE coffee
                            SET name = ?, roasting = ?,
                            type = ?, taste = ?, price = ?,
                            volume = ?
                            WHERE ID = ?""", (name[0], rost[0], type[0], text, price, volume, self.id))

                            self.connection.commit()
                            self.close()
                        except Exception:
                            print('Неизвестная ошибка')
                            self.close


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('release\\UI\\main.ui', self)
        self.initUI()

    def initUI(self):
        self.connection = sqlite3.connect("release\\data\\coffee.sqlite")
        self.pushButton.clicked.connect(self.add)
        self.btn_ref.clicked.connect(self.refresh_table)
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
    
    def refresh_table(self):
        self.query = self.query
        self.select_data()
    
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