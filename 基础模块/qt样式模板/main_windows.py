# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class Ui_MainWindow(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1080, 572)
        Form.setStyleSheet("background-color: rgb(68, 68, 68);")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(10, 10, 1061, 121))
        self.frame_2.setStyleSheet("border: 1px solid gray;\n"
"border-radius:1px;\n"
"border-color: rgb(0, 0, 0);\n"
"background-color: rgb(131, 131, 131);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalFrame = QtWidgets.QFrame(self.frame_2)
        self.horizontalFrame.setGeometry(QtCore.QRect(800, 20, 239, 71))
        self.horizontalFrame.setStyleSheet("border: none;")
        self.horizontalFrame.setObjectName("horizontalFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalFrame)
        self.pushButton_3.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton_3.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("华文琥珀")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton\n"
"{\n"
"border: none;\n"
"font: 11pt \"华文琥珀\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 156, 0);\n"
"border-radius:25px;\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"    background-color:rgb(0, 220, 0);\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color:rgb(147, 147, 147);\n"
"    padding-left:3px;\n"
"    padding-top:3px;\n"
"}\n"
"\n"
"QPushButton:unchecked {\n"
"    background-color:rgb(147, 147, 147);\n"
"    color: rgb(255, 255, 0);\n"
"}\n"
"\n"
"")
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalFrame)
        self.pushButton_2.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton_2.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("华文琥珀")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton\n"
"{\n"
"border: none;\n"
"font: 11pt \"华文琥珀\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(184, 0, 0);\n"
"border-radius:25px;\n"
"\n"
"}\n"
"QPushButton:hover\n"
"{\n"
"    background-color:rgb(255, 0, 0);\n"
"}\n"
"QPushButton:unchecked {\n"
"    background-color:rgb(147, 147, 147);\n"
"    color: rgb(255, 255, 0);\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.horizontalFrame)
        self.pushButton.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("华文琥珀")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton\n"
"{\n"
"border: none;\n"
"font: 11pt \"华文琥珀\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 136, 204);\n"
"border-radius:25px;\n"
"}\n"
"QPushButton:hover\n"
"{\n"
"    background-color: rgb(0, 196, 255);\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color:rgb(147, 147, 147);\n"
"    padding-left:3px;\n"
"    padding-top:3px;\n"
"}\n"
"QPushButton:flat {\n"
"    border: none; /* no border for a flat push button */\n"
"    background-color:rgb(147, 147, 147);\n"
"}\n"
"\n"
"QPushButton:default {\n"
"    border-color: navy; /* make the default button prominent */\n"
"    background-color:rgb(147, 147, 147);\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.gridFrame = QtWidgets.QFrame(self.frame_2)
        self.gridFrame.setGeometry(QtCore.QRect(290, 10, 221, 101))
        self.gridFrame.setStyleSheet("border: none;")
        self.gridFrame.setObjectName("gridFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.gridFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_4 = QtWidgets.QCheckBox(self.gridFrame)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setStyleSheet("border: none;\n"
"font: 75 10pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout.addWidget(self.checkBox_4, 0, 1, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.gridFrame)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.checkBox.setFont(font)
        self.checkBox.setStyleSheet("border: none;\n"
"font: 75 10pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.gridFrame)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setStyleSheet("border: none;\n"
"font: 75 10pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 0, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.frame_2)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 221, 101))
        self.textEdit.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.textEdit.setObjectName("textEdit")
        self.lineEdit = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit.setGeometry(QtCore.QRect(610, 40, 50, 20))
        self.lineEdit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit.setStyleSheet("background-color:  rgb(240, 240, 240);")
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(530, 40, 71, 21))
        self.label.setStyleSheet("border: none;\n"
"\n"
"font: 75 10pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 150, 1061, 411))
        self.tableWidget.setStyleSheet("QTableCornerButton::section{background:yellow;}\n"
"QTableWidget\n"
"{\n"
"    background:rgb(95, 95, 95);\n"
"    border: 1px solid gray;\n"
"    font-size:13px;\n"
"    font-family:\"Microsoft YaHei\";\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QTableWidget::item               \n"
"{\n"
"    border-bottom:2px solid #343434; \n"
"}\n"
"\n"
"QHeaderView\n"
"{\n"
"    background:transparent;        \n"
"}\n"
"\n"
"QHeaderView::section\n"
"{\n"
"    font-size:15px;\n"
"    font-family:\"Microsoft YaHei\";\n"
"    bold:75;\n"
"    color:#FFFFFF;\n"
"    background-color: rgb(0, 85, 0);\n"
"}\n"
"\n"
"\n"
"")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ligo"))
        self.pushButton_3.setText(_translate("Form", "启动"))
        self.pushButton_2.setText(_translate("Form", "停止"))
        self.pushButton.setText(_translate("Form", "保存"))
        self.checkBox_4.setText(_translate("Form", "停止时保存"))
        self.checkBox.setText(_translate("Form", "弹窗提示"))
        self.checkBox_2.setText(_translate("Form", "提示音"))
        self.label.setText(_translate("Form", "监控赔率："))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", " 预警时间 "))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "状态"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "时间"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "联赛"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", " 主场 V 客场 "))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "比分"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "大球赔率"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "盘口"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Form", "小球赔率"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("Form", "完场比分"))

