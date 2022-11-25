import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow QTableWidgetItem


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    
    def initUI(self):
        self.connection = sqlite3.connect("coffee.sqlite")
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