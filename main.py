import os
import sys

import requests
from func import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

SCREEN_SIZE = [600, 450]
spn_limits = [0.00001, 90]
ll_limits = [-180, 180]


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ll = [37.530887, 55.703118]
        self.spn = [0.002, 0.002]
        self.info = ''

        uic.loadUi('design.ui', self)
        self.type_map = self.comboBox.currentText()
        self.map = None
        self.pixmap = QPixmap()
        self.marks = []

        self.comboBox.currentTextChanged.connect(self.change_type_map)
        self.pushButton.clicked.connect(self.change_ll)
        self.pushButton_2.clicked.connect(self.clean_last_pt)

        self.update_map()

    def change_type_map(self):
        self.type_map = self.comboBox.currentText()
        self.update_map()

    def change_ll(self):
        search_text = self.lineEdit.text()
        top = geocoder({'geocode': search_text})

        self.info = top['metaDataProperty']['GeocoderMetaData']['text']
        self.label_2.setText(self.info)
        self.ll = list(map(float, top['Point']['pos'].split()))
        self.marks.append(self.ll[:])
        self.update_map()

    def clean_last_pt(self):
        if self.marks:
            self.marks.pop()
        self.update_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown or event.key() == Qt.Key_Minus:
            if self.spn[0] * 2 < spn_limits[1] and self.spn[1] * 2 < spn_limits[1]:
                self.spn[0] *= 2
                self.spn[1] *= 2
                self.update_map()

        if event.key() == Qt.Key_PageUp or event.key() == Qt.Key_Plus:
            if self.spn[0] / 2 > spn_limits[0] and self.spn[1] / 2 > spn_limits[0]:
                self.spn[0] /= 2
                self.spn[1] /= 2
                self.update_map()

        if event.key() == Qt.Key_Up and -180 < self.ll[1] + self.spn[0] < 90:
            self.ll[1] += self.spn[0]
            self.update_map()
        if event.key() == Qt.Key_Down and -90 < self.ll[1] - self.spn[0] < 90:
            self.ll[1] -= self.spn[0]
            self.update_map()
        if event.key() == Qt.Key_Right:
            if -180 + self.spn[1] < self.ll[0] < 180 - self.spn[1]:
                self.ll[0] += self.spn[1]
            else:
                self.ll[0] = -180 + self.spn[1]
            self.update_map()
        if event.key() == Qt.Key_Left:
            if -180 + self.spn[1] < self.ll[0] < 180 - self.spn[1]:
                self.ll[0] -= self.spn[1]
            else:
                self.ll[0] = 180 - self.spn[1]
            self.update_map()

    def update_map(self):
        self.map = get_image(self.ll, self.spn, self.type_map, self.marks)
        self.pixmap.loadFromData(self.map)
        self.label.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
