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

        uic.loadUi('design.ui', self)
        self.comboBox.currentTextChanged.connect(self.change_type_map)
        self.type_map = self.comboBox.currentText()
        self.map = get_image(self.ll, self.spn, self.type_map)
        self.pixmap = QPixmap()
        self.map = None

        self.update_map()

    def change_type_map(self):
        self.type_map = self.comboBox.currentText()
        self.update_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown or event.key() == Qt.Key_Minus:
            if self.spn[0] * 2 < spn_limits[1] and self.spn[1] * 2 < spn_limits[1]:
                self.spn[0] *= 2
                self.spn[1] *= 2

        if event.key() == Qt.Key_PageUp or event.key() == Qt.Key_Plus:
            if self.spn[0] / 2 > spn_limits[0] and self.spn[1] / 2 > spn_limits[0]:
                self.spn[0] /= 2
                self.spn[1] /= 2

        if event.key() == Qt.Key_Up and -180 < self.ll[1] + self.spn[0] < 90:
            self.ll[1] += self.spn[0]
        if event.key() == Qt.Key_Down and -90 < self.ll[1] - self.spn[0] < 90:
            self.ll[1] -= self.spn[0]
        if event.key() == Qt.Key_Right:
            if -180 + self.spn[1] < self.ll[0] < 180 - self.spn[1]:
                self.ll[0] += self.spn[1]
            else:
                self.ll[0] = -180 + self.spn[1]
        if event.key() == Qt.Key_Left:
            if -180 + self.spn[1] < self.ll[0] < 180 - self.spn[1]:
                self.ll[0] -= self.spn[1]
            else:
                self.ll[0] = 180 - self.spn[1]

        self.update_map()

    def update_map(self):
        self.map = get_image(self.ll, self.spn, self.type_map)
        self.pixmap.loadFromData(self.map)
        self.label.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
