import sys
import requests
from PyQt5.QtCore import Qt

from data.form import Ui_MainWindow as UW
from PIL import Image
from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets, QtCore

DATA_DIR = "data"

# API сервера
GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"
MAP_API_SERVER = "http://static-maps.yandex.ru/1.x/"
SEARCH_API_SERVER = "https://search-maps.yandex.ru/v1/"


# Основной класс
class Window(QtWidgets.QMainWindow, UW):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ll = "54.04,54.1"
        self.spn = self.get_map_spn()
        self.img = f"{DATA_DIR}/map.png"
        self.refresh_map()

    # получаем карту
    def get_map(self):
        params = self.get_params()
        res = requests.get(MAP_API_SERVER, params)
        if not res:
            print(f"Error {res.status_code}")
        with open(self.img, "wb") as im:
            im.write(res.content)
        img = Image.open(self.img)
        img.save(self.img, "png")
        pxm = QtGui.QPixmap(self.img)
        return pxm

    def get_map_spn(self):
        gp = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.ll,
            "format": "json"}
        res = requests.get(GEOCODER_API_SERVER, params=gp)
        if not res:
            print(res.status_code)
        jr = res.json()
        sp = jr["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"]["Envelope"]
        sp0 = abs(list(map(float, sp["lowerCorner"].split()))[0] - list(map(float, sp["upperCorner"].split()))[0])
        sp1 = abs(list(map(float, sp["lowerCorner"].split()))[1] - list(map(float, sp["upperCorner"].split()))[1])
        self.spn = str(sp0) + "," + str(sp1)
        return self.spn

    # получаем параметры карты
    def get_params(self):
        params = {"spn": self.spn,
                  "ll": self.ll,
                  "l": "map",
                  "size": "640,450"
                  }
        return params

    def refresh_map(self):
        self.map.setPixmap(self.get_map())

    def keyPressEvent(self, event):
        x = float(self.ll.split(",")[0])
        y = float(self.ll.split(",")[1])
        if event.key() == Qt.Key_Down:
            y -= 0.01
        elif event.key() == Qt.Key_Up:
            y += 0.01
        elif event.key() == Qt.Key_Right:
            x += 0.01
        elif event.key() == Qt.Key_Left:
            x -= 0.01
        self.ll = str(x) + "," + str(y)
        self.refresh_map()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
