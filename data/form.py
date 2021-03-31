# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 640)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.map = QtWidgets.QLabel(self.centralwidget)
        self.map.setGeometry(QtCore.QRect(80, 140, 640, 480))
        self.map.setText("")
        self.map.setObjectName("map")
        self.sch = QtWidgets.QRadioButton(self.centralwidget)
        self.sch.setGeometry(QtCore.QRect(80, 40, 82, 17))
        self.sch.setObjectName("sch")
        self.sat = QtWidgets.QRadioButton(self.centralwidget)
        self.sat.setGeometry(QtCore.QRect(80, 70, 82, 17))
        self.sat.setObjectName("sat")
        self.skl = QtWidgets.QRadioButton(self.centralwidget)
        self.skl.setGeometry(QtCore.QRect(80, 10, 82, 17))
        self.skl.setObjectName("skl")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(170, 10, 461, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(640, 10, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(80, 90, 61, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.clr_btn = QtWidgets.QPushButton(self.centralwidget)
        self.clr_btn.setGeometry(QtCore.QRect(640, 40, 75, 23))
        self.clr_btn.setObjectName("clr_btn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sch.setText(_translate("MainWindow", "Схема"))
        self.sat.setText(_translate("MainWindow", "Спутник"))
        self.skl.setText(_translate("MainWindow", "Гибрид"))
        self.pushButton.setText(_translate("MainWindow", "Найти"))
        self.pushButton_2.setText(_translate("MainWindow", "Ок"))
        self.clr_btn.setText(_translate("MainWindow", "Сброс"))
