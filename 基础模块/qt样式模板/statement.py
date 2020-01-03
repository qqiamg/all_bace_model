# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'statement.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QFont


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(435, 260)
        Form.setMinimumSize(QtCore.QSize(435, 260))
        Form.setMaximumSize(QtCore.QSize(435, 260))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 400, 210))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(220, 220, 71, 16))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.checkBox.setFont(font)
        self.checkBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox.setIconSize(QtCore.QSize(20, 20))
        self.checkBox.setObjectName("checkBox")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(300, 210, 101, 31))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "声明"))
        self.label.setText(_translate("Form", "       本程序只是采集数据的工具，我们不对数据版权负责。\n"
                                              "\n"
                                              "我们尊重版权，您必须在采集数据之前联系数据所有者取得\n"
                                              "\n"
                                              "授权，任何因数据授权产生的问题由使用者负全部责任，另\n"
                                              "\n"
                                              "外对于数据的使用请严格遵守《国家网络安全法》，使用本\n"
                                              "\n"
                                              "软件即代表您同意此声明。\n"
                                              ""))
        self.checkBox.setText(_translate("Form", "同意"))
        self.pushButton.setText(_translate("Form", "下一步"))


class Statement(object):
    def __init__(self):
        # self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.main_window)
        self.main_window.setFont(QFont("Microsoft YaHei", 9))
        self.main_window.setWindowIcon(QIcon('ico.png'))
        self.connect()
        self.ui.pushButton.setEnabled(False)
        self.accept = False
        try:
            with open('accept.txt', 'r', encoding='utf-8') as f:
                text = f.read()
            accept = """    本程序只是采集数据的工具，我们不对数据版权负责。
我们尊重版权，您必须在采集数据之前联系数据所有者取得
授权，任何因数据授权产生的问题由使用者负全部责任，另
外对于数据的使用请严格遵守《国家网络安全法》，使用本
软件即代表您同意此声明。
已同意
"""
            if text == accept:
                self.accept = True
            else:
                self.main_window.show()
        except:
            self.main_window.show()
        # sys.exit(self.app.exec_())

    def connect(self):
        self.ui.checkBox.stateChanged.connect(self.check)
        self.ui.pushButton.clicked.connect(self.accepted)

    def check(self, check_state):
        if check_state == 2:
            self.ui.pushButton.setEnabled(True)
        else:
            self.ui.pushButton.setEnabled(False)

    def accepted(self):
        self.main_window.close()
        with open('accept.txt', 'w', encoding='utf-8') as f:
            f.write(
"""    本程序只是采集数据的工具，我们不对数据版权负责。
我们尊重版权，您必须在采集数据之前联系数据所有者取得
授权，任何因数据授权产生的问题由使用者负全部责任，另
外对于数据的使用请严格遵守《国家网络安全法》，使用本
软件即代表您同意此声明。
已同意
""")


if __name__ == '__main__':
    Statement()
