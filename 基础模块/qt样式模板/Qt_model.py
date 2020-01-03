import os
import sys
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QTableWidgetItem, QMessageBox, QFileDialog,QHeaderView)
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QCoreApplication
from PyQt5.QtMultimedia import QSound

from main_windows import Ui_MainWindow
from statement import Statement


class VisitMain():
    '''界面'''

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = NewWidget()      #重写了退出弹窗的界面文件
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        self.main_window.setFont(QFont("Microsoft YaHei", 9))
        self.main_window.setWindowIcon(QIcon('2.jpg'))      #设置图标
        sound_file = '预警提示音.wav'                        #设置提示音
        self.sound = PyQt5.QtMultimedia.QSound(sound_file)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)    #设置列为自动延升等分大小
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)   #设置第5列为根据内容长度调整大小
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.main_window.setFixedSize(self.main_window.width(), self.main_window.height())      #锁死窗口大小
        self.ui.lineEdit.setText('1.20')
        self.connect()
        self.read_txt()
        # 创建声明（显示一次后就不再显示）
        self.statement = Statement()
        if self.statement.accept:
            self.main_window.show()
        else:
            self.statement.ui.pushButton.clicked.connect(self.main_window.show)
        # self.main_window.show()
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_3.setEnabled(True)
        self.ui.pushButton_2.setEnabled(False)
        sys.exit(self.app.exec_())

    def read_txt(self): #设置初始值，如果没有就跳过
        try:
            with open("./system_File/small_peilv.txt") as txtData:
                sender = txtData.readlines()[0]
            self.ui.lineEdit.setText(sender)
        except:
            pass

    def connect(self):
        pass
        # self.ui.pushButton.clicked.connect(self.save_mes)
        self.ui.pushButton_3.clicked.connect(self.start_spider)
        # self.ui.pushButton_2.clicked.connect(self.stoped)

    def record_min(self):   #记录数值，下次进行读取
        try:
            if not os.path.exists('./system_File'):
                os.makedirs('./system_File')
            with open("./system_File/small_peilv.txt", 'w') as txtData:
                txtData.write(self.ui.lineEdit.text())
            print('记录成功')
        except:
            pass

    def start_spider(self):
        self.record_min()


class NewWidget(QtWidgets.QMainWindow):  # 重写退出方法

    def closeEvent(self, event):
        self.box = QMessageBox(QMessageBox.Question, '退出程序', '确认退出吗(注意数据存储)?')
        self.box.setStyleSheet('font: 75 13pt "微软雅黑";')
        # 添加按钮，可用中文
        self.box.addButton('确定', QMessageBox.YesRole)
        self.box.addButton('取消', QMessageBox.NoRole)
        # 显示该问答框
        # 接收按下对话框按钮的信息：
        reply = self.box.exec_()
        print(reply)
        if reply == 0:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    VisitMain()