# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wyy.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(662, 576)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet("\n"
"    background:#d5e6ff;\n"
"\n"
"")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setStyleSheet("QFrame { \n"
"border: 2px solid gray;\n"
"border-radius:5px;\n"
"border-color: rgb(1, 115, 255);\n"
"background-color: rgb(255, 255, 255);\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 0))
        self.pushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"\n"
"background-color: rgb(167, 205, 255);\n"
"\n"
"padding: 3px;\n"
"\n"
"font-family: \"Verdana\";\n"
"\n"
"font-size: 15px;\n"
"\n"
"text-align: center;\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 4, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 0))
        self.pushButton_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"\n"
"background-color: rgb(167, 205, 255);\n"
"\n"
"padding: 3px;\n"
"\n"
"font-family: \"Verdana\";\n"
"\n"
"font-size: 15px;\n"
"\n"
"text-align: center;\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 2, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("\n"
"border: 0px solid gray; \n"
"")
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("\n"
"border:0px solid gray; \n"
"")
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 2, 3, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 2, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setMaximumSize(QtCore.QSize(200, 20))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.frame)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem2)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setMinimumSize(QtCore.QSize(580, 400))
        self.tableWidget.setStyleSheet("\n"
"QHeaderView::section\n"
"{\n"
"    font-size:15px;\n"
"    font-family:\"Microsoft YaHei\";\n"
"    bold:75;\n"
"    color:#FFFFFF;\n"
" \n"
"    background-color: rgb(167, 205, 255);\n"
"\n"
"    border-color: rgb(1, 115, 255);\n"
"    border-radius:10px;\n"
"    border:none;\n"
"};\n"
"background-color: rgb(255, 255, 255);\n"
"\n"
"\n"
"")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(160)
        self.verticalLayout_2.addWidget(self.tableWidget)
        from PyQt5.QtWidgets import QHeaderView
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "歌曲"))
        self.pushButton.setText(_translate("Form", "搜索"))
        self.pushButton_2.setText(_translate("Form", "下载"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">歌名:</span></p></body></html>"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">歌手：</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "注：可下载会员才能下载的歌曲，但不可下载需单独付费的歌曲及需开会员才可听的歌曲。"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "歌名"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "歌手"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "专辑"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "时常"))

