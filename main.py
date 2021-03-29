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
        self.setStyleSheet("background-color: #eeeeee")
        self.ll = "54.04,54.1"
        self.l = "map"
        self.pt = None
        self.max_spn = [2, 2]
        self.min_spn = [0.00001, 0.00001]
        self.spn = self.get_map_spn()
        self.img = f"{DATA_DIR}/map.png"
        self.refresh_map()
        self.pushButton.clicked.connect(self.search_object)
        self.sch.clicked.connect(self.change_map)
        self.sat.clicked.connect(self.change_map)
        self.skl.clicked.connect(self.change_map)
        self.sch.click()

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
    def get_map_spn(self, geocode=None):
        if not geocode:
            geocode = self.ll
        gp = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": geocode,
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
                  "l": self.l,
                  "size": "640,450",
                  }
        if self.pt:
            params["pt"] = self.pt
        return params

    def refresh_map(self):
        self.map.setPixmap(self.get_map())

    # проверяем не неажата ли кнопка
    # если если нажата, то выполняем соответствующее действие
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

    # меняем вид карты
    def change_map(self):
        if self.sch.isChecked():
            self.l = "map"
        elif self.skl.isChecked():
            self.l = "sat,skl"
        else:
            self.l = "sat"
        self.refresh_map()

    def search_object(self):
        text = self.lineEdit.text()
        if not text:
            return 0
        params = {
            "geocode": text,
            "format": "json",
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b"
        }
        res = requests.get(GEOCODER_API_SERVER, params=params)
        if res:
            js = res.json()
            if js["response"]["GeoObjectCollection"]["featureMember"]:
                tp = js["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                cord = tp["Point"]["pos"]
                self.ll = ",".join(cord.split(" "))
                self.spn = self.get_map_spn(geocode=text)
                self.pt = f"{self.ll},pm2rdm"
                self.refresh_map()
            else:
                self.lineEdit.setText(f"No results")
        else:
            self.lineEdit.setText(f"Error {res.status_code}")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
