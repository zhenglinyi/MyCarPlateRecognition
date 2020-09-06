# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import sys, os

# Qt模块
from PyQt5.QtCore import pyqtSlot, Qt, QRect, QTime, QDate, QDateTime, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QGraphicsView, QFileDialog, QStatusBar
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QImage
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

# Ui模块
from .Ui_MainWindow import Ui_MainWindow

# 对话框模块
from .QueryStatistics import DialogQueryStatistics
from .ChargeStandard import DialogChangeStandard

# 道闸动画模块
# from BarrierGate import BarrierGate

# 数据库模块
from DataBase import Util

# 车牌识别模块
from LPRThread import LPRThread

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    主窗口
    """
    barrier_gate = 0
    lpr_thread = 0
    status_bar = 0
    business = 0
    is_autoBarrierControl = 0
    video_widgets = 0
    def __init__(self, is_admin, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setStatusBar(self.statusbar)

        self.lpr_thread = LPRThread()
        self.business = Util()

        self.statusbar.showMessage("程序正在初始化...")

        # 在模型加载完成之前这两个菜单不可用
        self.actionSimulateEnter.setEnabled(False)
        self.actionSimulateLeave.setEnabled(False)

        self.lpr_thread.initComplete.connect(self.on_lpr_initComplete)
        self.lpr_thread.identifyComplete.connect(self.on_lpr_identifyComplete)

        # 只有管理员可以设置收费标准
        if not is_admin:
            self.actionChangeStandard.setEnabled(False)

        # 显示汽车入库和出库动画的VideoWidget
        self.video_widgets = QVideoWidget(self.labelGateAnimation.parent())
        self.video_widgets.show()
        self.video_widgets.setGeometry(self.labelGateAnimation.geometry())
        # 显示汽车入库和出库动画的QMediaPlayer
        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widgets)

        # 显示汽车照片的lable
        #self.labelCarPhote.setStyleSheet("border: 2px solid red")
        self.labelCarPhote.setScaledContents(True)
        #self.labelGateAnimation.setStyleSheet("border: 2px solid red")
        self.labelGateAnimation.setScaledContents(True)

        # 开闸和关闸按钮根据自动设置决定是否显示
        if self.actionAutoBarrierControl.isChecked():
            self.pushButtonEnter.setEnabled(False)
            self.pushButtonLeave.setEnabled(False)
        else:
            self.pushButtonEnter.setEnabled(True)
            self.pushButtonLeave.setEnabled(True)            



    def on_lpr_initComplete(self):
        """
        槽函数：车牌识别模型初始化完成
        """
        self.actionSimulateEnter.setEnabled(True)
        self.actionSimulateLeave.setEnabled(True)
        self.statusbar.showMessage("初始化完成...")
    
    def on_lpr_identifyComplete(self, file_path, lpn, is_enter):
        """
        槽函数：车牌识别完成
        
        @param file_path 车牌文件路径
        @param lpn, license plate number 车牌号
        @param is_enter 当前车辆是否是驶入车辆
        """
        self.statusbar.showMessage(lpn + "已完成识别...")
        self.labelLicensePlateNumber.setText(lpn)
        
        # 车辆将要进入停车场
        if is_enter:
            self.labelLicensePlateNumber.setText(lpn)
            self.labelMessage.setText("感谢您使用一路顺风停车场")
            # 保存停车时间
            self.business.car_entry(lpn)
            self.pushButtonEnter.pressed.emit()

        # 车辆将要离开停车场
        else:
            parking_history_time, history_charge = self.business.car_out(lpn)
            self.labelMessage.setText("共计停放" + str(parking_history_time) + "，共计收费" + str(history_charge) + "元")
            self.pushButtonLeave.pressed.emit()

    @pyqtSlot()
    def on_actionSimulateEnter_triggered(self):
        """
        菜单： 文件 - 模拟进入.
        """

        file_dialog = QFileDialog()
        if file_dialog.exec():
            files = file_dialog.selectedFiles()
            if len(files) == 1:
                self.lpr_thread.identify(files[0], True)
                
                pixmap = QPixmap(files[0])
                self.labelCarPhote.setPixmap(pixmap)
    
    @pyqtSlot()
    def on_actionSimulateLeave_triggered(self):
        """
        菜单： 文件 - 模拟离开.
        """

        file_dialog = QFileDialog()
        if file_dialog.exec():
            files = file_dialog.selectedFiles()
            if len(files) == 1:
                self.lpr_thread.identify(files[0], False)

                pixmap = QPixmap(files[0])
                self.labelCarPhote.setPixmap(pixmap)

    
    @pyqtSlot()
    def on_actionSave_triggered(self):
        """
        菜单： 文件 - 保存.
        """

        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionPrint_triggered(self):
        """
        菜单： 文件 - 打印.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionQuit_triggered(self):
        """
        菜单： 文件 - 退出.
        """
        sys.exit(0)
    
    @pyqtSlot()
    def on_actionChangeStandard_triggered(self):
        """
        菜单： 设置 - 收费标准.
        """
        dialogChangeStandard = DialogChangeStandard(self)
        dialogChangeStandard.show()
        dialogChangeStandard.exec()

    @pyqtSlot()
    def on_actionAutoBarrierControl_triggered(self):
        """
        菜单： 设置 - 自动开闸.
        """
        if self.actionAutoBarrierControl.isChecked():
            self.pushButtonEnter.setEnabled(False)
            self.pushButtonLeave.setEnabled(False)
        else:
            self.pushButtonEnter.setEnabled(True)
            self.pushButtonLeave.setEnabled(True)
    
    @pyqtSlot()
    def on_actionQueryStatistics_triggered(self):
        """
        菜单： 查询 - 查询统计.
        """

        dialogQueryStatistics = DialogQueryStatistics(self)
        dialogQueryStatistics.show()
        dialogQueryStatistics.exec()
    
    @pyqtSlot(QAction)
    def on_menuAbout_triggered(self, action):
        """
        菜单： 关于.
        
        @param action DESCRIPTION
        @type QAction
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButtonEnter_pressed(self):
        """
        按钮 - 开闸
        """

        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(r"Resource\入库.avi")))
        self.media_player.play()
    
    @pyqtSlot()
    def on_pushButtonLeave_pressed(self):
        """
        按钮 - 关闸
        """
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(r"Resource\出库.avi")))
        self.media_player.play()
