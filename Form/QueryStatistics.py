# -*- coding: utf-8 -*-

import os

"""
Module implementing DialogQueryStatistics.
"""

from PyQt5.QtCore import pyqtSlot, QDate, QTime, QDateTime
from PyQt5.QtWidgets import QDialog, QFileDialog

from .Ui_QueryStatistics import Ui_DialogQueryStatistics

from DataBase import Util
import Print

class DialogQueryStatistics(QDialog, Ui_DialogQueryStatistics):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DialogQueryStatistics, self).__init__(parent)
        self.setupUi(self)
        self.comboBoxPeriodType.addItems(['天', '周', '月'])
        self.radioButtonRecent.setChecked(True)
        self.lineEditPeriodCount.setText(str(5))
    
    def getQueryTimeLine(self):

        start_time = None
        end_time = None
        # 近期时间
        if self.radioButtonRecent.isChecked():
            end_time = QDateTime.currentDateTime()
            if self.comboBoxPeriodType.currentText() == '天':
                start_time = end_time.addDays(-int(self.lineEditPeriodCount.text()) * 1)
            elif self.comboBoxPeriodType.currentText() == '周':
                start_time = end_time.addDays(-int(self.lineEditPeriodCount.text()) * 7)
            elif self.comboBoxPeriodType.currentText() == '月':
                start_time = end_time.addDays(-int(self.lineEditPeriodCount.text()) * 30)
            else:
                pass
        if self.radioButtonPrevious.isChecked():
            start_time = self.dateEditDateStart.dateTime()
            end_time = self.dateEditDateEnd.dateTime()
        return start_time, end_time

    @pyqtSlot()
    def on_pushButtonQuery_pressed(self):
        """
        按钮： 查询.
        """
        business = Util()
        start_time,end_time = self.getQueryTimeLine()

        car_count,charge = business.query_timecar(start_time.toPyDateTime(), end_time.toPyDateTime())
        self.lineEditVehicleTotalCount.setText(str(car_count))
        self.lineEditVehicleTotalCharge.setText(str(charge))

    @pyqtSlot()
    def on_pushButtonSave_pressed(self):
        """
        按钮： 保存.
        """
        self.pushButtonQuery.pressed.emit()
        start_time,end_time = self.getQueryTimeLine()
        save_path = QFileDialog.getSaveFileName(self,'保存记录',os.getcwd()+'/one.xls', "Excel(*.xls)")
        if save_path[0] != '':
            Print.printCarIfo(start_time.toPyDateTime(), end_time.toPyDateTime(), save_path[0])
    
    @pyqtSlot()
    def on_pushButtonPrint_pressed(self):
        """
        按钮： 打印.
        """
        self.pushButtonQuery.pressed.emit()
        start_time,end_time = self.getQueryTimeLine()
        Print.printCarIfo(start_time.toPyDateTime(), end_time.toPyDateTime(), 'one.xls')
        os.startfile('one.xls','print')
