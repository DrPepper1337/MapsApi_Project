import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QCheckBox, QPlainTextEdit, \
    QMainWindow, QTextEdit, QTableWidget, QTableWidgetItem, QInputDialog, QListWidgetItem, QListWidget, QHeaderView
import sqlite3
from PyQt5.QtGui import QPainter, QColor, QPolygon
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import os
import requests


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('y.ui', self)
        self.setWindowTitle('MapApi_project')

        self.lon = 37.620070
        self.lat = 55.753630
        self.delta = 0.002

        self.prev_lon = self.lon
        self.prev_lat = self.lat
        self.prev_delta = self.delta

        self.map_type = 'map'

        self.getImage()
        self.initUI()

    def getImage(self):
        api_server = "http://static-maps.yandex.ru/1.x/"

        params = {
            "ll": ",".join([str(self.lon), str(self.lat)]),
            "spn": ",".join([str(self.delta), str(self.delta)]),
            "l": self.map_type,
        }

        response = requests.get(api_server, params=params)

        if not response:
            self.lon = self.prev_lon
            self.lat = self.prev_lat
            self.delta = self.prev_delta
            params = {
                "ll": ",".join([str(self.lon), str(self.lat)]),
                "spn": ",".join([str(self.delta), str(self.delta)]),
                "l": self.map_type,
            }
            api_server = "http://static-maps.yandex.ru/1.x/"
            response = requests.get(api_server, params=params)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap("map.png")
        self.label.setPixmap(self.pixmap)
        self.label.adjustSize()

    def initUI(self):
        self.pushButton_2.clicked.connect(self.change_map_type)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_PageUp:
            self.prev_delta = self.delta
            self.delta *= 2
        if event.key() == QtCore.Qt.Key_PageDown and self.delta != 0.0005:
            self.prev_delta = self.delta
            self.delta /= 2

        if event.key() == Qt.Key_Up:
            self.prev_lat = self.lat
            self.lat += self.delta * 1.4
        if event.key() == Qt.Key_Down:
            self.prev_lat = self.lat
            self.lat -= self.delta * 1.4
        if event.key() == Qt.Key_Left:
            self.prev_lon = self.lon
            self.lon -= self.delta * 3
        if event.key() == Qt.Key_Right:
            self.prev_lon = self.lon
            self.lon += self.delta * 3

        self.getImage()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def change_map_type(self):
        if self.map_type == 'map':
            self.map_type = 'sat'
        elif self.map_type == 'sat':
            self.map_type = 'sat,skl'
        else:
            self.map_type = 'map'
        self.getImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
