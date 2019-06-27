import asyncio
import logging
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, \
    QInputDialog, QMessageBox, QHeaderView, QLabel, QAbstractItemView
from quamash import QEventLoop

from lib.ui_base import BaseUI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("iot-device-id.log"),
        logging.StreamHandler()
    ])


class QtUI(BaseUI):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.app = None
        self.tableWidget = None
        self.start_button = None
        self.stop_button = None
        self.headers = []
        self.heading = None

    def run(self):
        self.app = QApplication(sys.argv)

        self.heading = QLabel("<h1>Local IoT devices</h1>")

        self.tableWidget = QTableWidget()
        QTimer.singleShot(100, lambda: self.tableWidget.setHorizontalHeaderLabels(
            self.headers))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        w = QWidget()
        l = QVBoxLayout()
        l.addWidget(self.heading)
        l.addWidget(self.tableWidget)

        self.start_button = QPushButton("Add new device type")
        self.start_button.clicked.connect(self.record)
        self.start_button.setIcon(QIcon("lib/assets/start.png"))
        l.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop recording")
        self.stop_button.clicked.connect(self.stop_record)
        self.stop_button.setIcon(QIcon("lib/assets/stop.png"))
        self.stop_button.hide()
        l.addWidget(self.stop_button)

        w.setLayout(l)
        w.setWindowTitle("IoT Device ID")
        w.setWindowIcon(QIcon("lib/assets/icons8-smart-home-checked.png"))
        w.setMinimumHeight(300)
        w.setMinimumWidth(500)

        w.show()

        self.start_detecting()

        sys.exit(app.exec_())

    def record(self):
        ip, success = QInputDialog.getText(self.tableWidget, "Which device should be recorded?",
                                           "Please enter the device's IP address.")
        if not success:
            return
        name, success = QInputDialog.getText(self.tableWidget, "Which device should be recorded?",
                                             "Please enter the device name (e.g. Philips Hue Bridge v1)")
        if not success:
            return
        self.heading.setText("<h1>Recording characteristics of {} device at {}</h1>".format(name, ip))
        self.stop_button.show()
        self.start_button.hide()
        self.start_recording(ip, name)

    def stop_record(self):
        QMessageBox.information(self.tableWidget, "Success", "Device has been successfully saved to the database.")
        self.stop_button.hide()
        self.heading.setText("<h1>Local IoT devices</h1>")
        self.start_button.show()
        self.start_detecting()

    def set_headers(self, headers):
        self.headers = headers
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setColumnCount(len(headers))

    def add_row(self, values):
        self.tableWidget.setVisible(True)
        self.rows.append(values)

    def draw(self):
        self.tableWidget.setRowCount(len(self.rows))
        for x, row in enumerate(self.rows):
            for y, value in enumerate(row):
                self.tableWidget.setItem(x, y, QTableWidgetItem(value))
        self.rows = []

    def sort_by_row(self, i):
        pass


app = QApplication(sys.argv)
loop = QEventLoop(app)
asyncio.set_event_loop(loop)

with loop:
    loop.run_until_complete(QtUI().run())
