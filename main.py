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
        self.max_spn = [2, 2]
        self.min_spn = [0.00001, 0.00001]
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

    # получаем размеры карты
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
        self.max_spn = [sp0 + 2, sp1 + 2]
        self.min_spn = [sp0 * 0.0001, sp1 * 0.0001]
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

    # смотрим не нажата ли клавиша
    # если нажата то либо увеличиваем, либо уменьшаем область карты
    def keyPressEvent(self, event):
        spn0 = float(self.spn.split(",")[0])
        spn1 = float(self.spn.split(",")[1])
        if event.key() == Qt.Key_PageUp:
            spn0 -= 0.25 * spn0 if spn0 > self.min_spn[0] + 0.25 * spn0 else 0
            spn1 -= 0.25 * spn1 if spn1 > self.min_spn[1] + 0.25 * spn1 else 0
        elif event.key() == Qt.Key_PageDown:
            spn0 += 0.25 * spn0 if spn0 < self.max_spn[0] - 0.25 * spn0 else 0
            spn1 += 0.25 * spn1 if spn1 < self.min_spn[1] - 0.25 * spn1 else 0
        self.spn = str(spn0) + "," + str(spn1)
        self.refresh_map()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
