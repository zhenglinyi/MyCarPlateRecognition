# -*- coding: utf-8 -*-

"""
Module implementing DialogChangeStandard.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox

from .Ui_ChargeStandard import Ui_DialogChangeStandard

from DataBase import Util

class DialogChangeStandard(QDialog, Ui_DialogChangeStandard):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DialogChangeStandard, self).__init__(parent)
        self.setupUi(self)
        print("DialogChangeStandard.__init__")
    
    @pyqtSlot()
    def on_pushButtonOK_pressed(self):
        """
        按钮： 确定.
        """
        
        business = Util()
        if business.set_charge(
            int(self.lineEdit_1.text()),
            int(self.lineEdit_2.text()), 
            int(self.lineEdit_3.text())
            ):
            QMessageBox.about(self, "提示", "设置成功")
        else:
            QMessageBox.information(self, "提示", "设置失败")
