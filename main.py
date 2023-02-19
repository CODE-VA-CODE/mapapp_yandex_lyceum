import sys
import os

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5 import uic

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("map.ui", self)
        self.long = 37.53
        self.lat = 55.70
        self.spn_x = 0.005
        self.spn_y = 0.005
        self.zoom = 17
        self.map_type = "map"
        for b in self.buttonGroup.buttons():
            b.clicked.connect(self.choose_type)

        #self.groupBox.clicked.connect(self.choose_type)
        self.getImage()

    def choose_type(self, event):
        indexOfChecked = [self.buttonGroup.buttons()[x].isChecked() for x in
                          range(len(self.buttonGroup.buttons()))].index(True)
        if indexOfChecked == 0:
            self.map_type = "map"
            self.getImage()
        elif indexOfChecked == 1:
            self.map_type = "sat"
            self.getImage()
        elif indexOfChecked == 2:
            self.map_type = "sat,skl"
            self.getImage()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_O:
            self.spn_x /= 2
            self.spn_y /= 2
            self.getImage()
        elif event.key() == Qt.Key_L:
            self.spn_x *= 2
            self.spn_y *= 2
            self.getImage()
        elif event.key() == Qt.Key_Down:
            self.lat -= self.spn_y
            self.getImage()
        elif event.key() == Qt.Key_Up:
            self.lat += self.spn_y
            self.getImage()
        elif event.key() == Qt.Key_Left:
            self.long -= self.spn_x
            self.getImage()
        elif event.key() == Qt.Key_Right:
            self.long += self.spn_x
            self.getImage()

    # code
    def getImage(self):
        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": f"{self.long},{self.lat}",
            "spn": f"{self.spn_x},{self.spn_y}",
            #"zoom": self.zoom,
            "l": self.map_type
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.label.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())