# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

# Qt模块
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QDialog

# Ui模块
from .Ui_Login import Ui_Dialog

# 数据库模块
from DataBase import Util

import sys

class DialogLogin(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    failed_count = 0
    business = 0
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(QDialog, self).__init__(parent)
        self.business = Util()

        self.setupUi(self)
        self.labelFailedMessage.setVisible(0)
        self.lineEditUser.setText('admin')
        self.lineEditPassword.setText('123456')
    
    def check_password(self, user, password, is_admin):
        #Util.check_password(user, password)
        return self.business.check_password(user, password, is_admin)

    def closeEvent(self, e):
        self.reject()

    @pyqtSlot()
    def on_pushButtonLogin_pressed(self):
        """
        登录按钮
        """

        # 获取用户名和密码
        is_admin = self.checkBoxIsAdmin.isChecked()
        user = self.lineEditUser.text()
        password = self.lineEditPassword.text()

        # 检查用户名和密码
        if self.check_password(user, password, is_admin):
            if is_admin:
                self.done(2)
            else:
                self.done(3)
            self.failed_count = 0
            self.labelFailedMessage.setVisible(0)
        else:
            self.failed_count += 1
            self.labelFailedMessage.setVisible(1)
