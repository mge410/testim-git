import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget

connection = sqlite3.connect("coffee.sqlite")
cur = connection.cursor()
res = connection.cursor().execute(f"SELECT * FROM coffee").fetchall()
flag = True

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setvartable_1()
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.reprem)
        self.about = AddWin()

    # Обновление таблиц
    def setvartable_1(self):
        try:
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(res):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

            rez2 = connection.cursor().execute(f"SELECT name FROM PRAGMA_TABLE_INFO('coffee')").fetchall()
            spis = []
            for i in rez2:
                spis.append(*i)
            self.tableWidget.setHorizontalHeaderLabels(spis)
        except Exception:
            pass

    def add(self):
        global flag
        flag = True
        self.about.prin()
        self.about.show()

    def reprem(self):
        global flag
        flag = False
        self.about.prin()
        self.about.show()


class AddWin(QWidget):
    def __init__(self):
        super(AddWin, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.flag1 = False

    def prin(self):
        if flag:
            self.lineEdit.setText("id")
            self.lineEdit_2.setText("name")
            self.lineEdit_3.setText("roast")
            self.lineEdit_4.setText("type")
            self.lineEdit_5.setText("taste")
            self.lineEdit_6.setText("price")
            self.lineEdit_7.setText("weight")
            self.addbut.setText("Добавить")
            if self.flag1:
                self.addbut.clicked.disconnect()
            self.addbut.clicked.connect(self.addrun)
            self.flag1 = True
        else:
            self.lineEdit.setText("Напишите id который вам нужно изменить")
            self.lineEdit_2.setText("name")
            self.lineEdit_3.setText("roast")
            self.lineEdit_4.setText("type")
            self.lineEdit_5.setText("taste")
            self.lineEdit_6.setText("price")
            self.lineEdit_7.setText("weight")
            self.addbut.setText("Изменить")
            if self.flag1:
                self.addbut.clicked.disconnect()
            self.addbut.clicked.connect(self.peremena)
            self.flag1 = True



    def addrun(self):
        global res, cur, connection
        cur.execute("""INSERT INTO coffee (id,name,roast,type,taste,price,weight) VALUES(?, ?, ?, ?, ?, ?, ?)""",
                    (self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit_6.text(), self.lineEdit_7.text()))
        connection.commit()
        res = connection.cursor().execute(f"SELECT * FROM coffee").fetchall()
        ex.setvartable_1()

    def peremena(self):
        global res, cur, connection
        try:
            print(1)
            cur.execute("UPDATE coffee SET name = ?, roast = ?, type = ?, taste = ?, price = ?, weight = ? WHERE id = ?",
                        (self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit_6.text(), self.lineEdit_7.text(), self.lineEdit.text()))
            connection.commit()
            res = connection.cursor().execute(f"SELECT * FROM coffee").fetchall()
            ex.setvartable_1()
        except Exception:
            pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())