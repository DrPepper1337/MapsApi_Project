import sys
import os
import requests
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from MainWidget import Ui_MainWindow


class MainWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.lon = 37.620070
        self.lat = 55.753630
        self.delta = 0.002

        self.prev_lon = self.lon
        self.prev_lat = self.lat
        self.prev_delta = self.delta

        self.map_type = 'map'

        self.setupUi(self)
        self.initUI()
        self.update()

    def initUI(self):
        self.change_type_btn.clicked.connect(self.change_map_type)
        self.search_btn.clicked.connect(self.search_to_geocode)

    def update(self):
        self.getImage()

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
        self.map_label.setPixmap(self.pixmap)


    def search_to_geocode(self):
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={self.search_le.text()}&format=json"
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            # Получаем первый топоним из ответа геокодера.
            # Согласно описанию ответа, он находится по следующему пути:
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            # Полный адрес топонима:
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            # Координаты центра топонима:
            toponym_coodrinates = toponym["Point"]["pos"]
            self.lon, self.lat = [float(i) for i in toponym_coodrinates.split()]
        else:
            # Произошла ошибка выполнения запроса. Обрабатываем http-статус.
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
        self.update()

    def change_map_type(self):
        if self.map_type == 'map':
            self.map_type = 'sat'
        elif self.map_type == 'sat':
            self.map_type = 'sat,skl'
        else:
            self.map_type = 'map'
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.prev_delta = self.delta
            self.delta *= 2
        if event.key() == Qt.Key_PageDown and self.delta != 0.0005:
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

        self.update()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec())
