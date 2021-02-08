import os
import sys

import requests
from func import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

SCREEN_SIZE = [600, 450]


class MyWidget(QMainWindow):
    def __init__(self):
        self.ll = [37.530887, 55.703118]
        self.spn = [0.002, 0.002]
        self.spn_limits = [0.00001, 90]
        self.ll_limits = [-180, 180]
        super().__init__()
        uic.loadUi('design.ui', self)
        self.map = get_image(self.ll, self.spn)
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(self.map)
        self.label.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.spn[0] *= 2
            self.spn[1] *= 2
            self.spn[0] = min(self.spn[0], self.spn_limits[1])
            self.spn[1] = min(self.spn[1], self.spn_limits[1])
        if event.key() == Qt.Key_PageUp:
            self.spn[0] /= 2
            self.spn[1] /= 2
            self.spn[0] = max(self.spn[0], self.spn_limits[0])
            self.spn[1] = max(self.spn[1], self.spn_limits[0])
        if event.key() == Qt.Key_Up and -180 < self.ll[1] + self.spn[0] < 90:
            self.ll[1] += self.spn[0]
        if event.key() == Qt.Key_Down and -90 < self.ll[1] - self.spn[0] < 90:
            self.ll[1] -= self.spn[0]
        if event.key() == Qt.Key_Right:
            if -180 + self.spn[1] < self.ll[0]< 180 - self.spn[1]:
                self.ll[0] += self.spn[1]
                print(self.ll)
            else:
                self.ll[0] = -180 + self.spn[1]
                print(self.ll)
                print(1)
        if event.key() == Qt.Key_Left:
            if -180 + self.spn[1]< self.ll[0] < 180 - self.spn[1]:
                self.ll[0] -= self.spn[1]
                print(self.ll)
            else:
                self.ll[0] = 180 - self.spn[1]
                print(self.ll)
        self.update_map()

    def update_map(self):
        self.map = get_image(self.ll, self.spn)
        self.pixmap.loadFromData(self.map)
        self.label.setPixmap(self.pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
