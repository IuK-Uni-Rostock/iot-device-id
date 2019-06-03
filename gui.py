import asyncio
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QHBoxLayout, QTableWidgetItem
from quamash import QEventLoop

from lib.ui_base import BaseUI


class QtUI(BaseUI):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.app = None
        self.tableWidget = None

    def run(self):
        self.app = QApplication(sys.argv)

        self.tableWidget = QTableWidget()

        w = QWidget()
        l = QHBoxLayout()
        l.addWidget(self.tableWidget)
        w.setLayout(l)
        w.setWindowTitle("IoT Device ID")
        w.setWindowIcon(QIcon("lib/assets/icons8-smart-home-checked.png"))
        w.show()

        self.start_detecting()

        sys.exit(app.exec_())

    def set_headers(self, headers):
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setColumnCount(len(headers))

    def add_row(self, values):
        self.rows.append(values)

    def draw(self):
        self.tableWidget.setRowCount(len(self.rows))
        for x, row in enumerate(self.rows):
            for y, value in enumerate(row):
                print(x, y, value)
                self.tableWidget.setItem(x, y, QTableWidgetItem(value))
        self.rows = []

    def sort_by_row(self, i):
        pass


app = QApplication(sys.argv)
loop = QEventLoop(app)
asyncio.set_event_loop(loop)

with loop:
    loop.run_until_complete(QtUI().run())
