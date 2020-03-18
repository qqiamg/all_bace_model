from PyQt5 import QtWidgets
from main_windows import Ui_Form
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QTableWidgetItem, QMessageBox, QFileDialog)
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QCoreApplication

class MyWindow(QtWidgets.QWidget, Ui_Form):
    def  __init__ (self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

class Ui_window(object):
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = MyWindow()
        self.ui = Ui_Form()
        # self.ui.setupUi(self.main_window)
        self.main_window.setFont(QFont("Microsoft YaHei", 9))
        self.connect()
        self.main_window.show()
        sys.exit(self.app.exec_())

    def connect(self):
        pass


if __name__ == '__main__':
	Ui_window()