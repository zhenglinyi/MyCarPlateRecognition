# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\33 综合实践\数字图形图像\parking_roll_management_system\Form\Login.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(386, 213)
        Dialog.setSizeGripEnabled(True)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(80, 40, 221, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEditUser = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditUser.setObjectName("lineEditUser")
        self.gridLayout.addWidget(self.lineEditUser, 0, 1, 1, 1)
        self.labelUser = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei Mono")
        self.labelUser.setFont(font)
        self.labelUser.setObjectName("labelUser")
        self.gridLayout.addWidget(self.labelUser, 0, 0, 1, 1)
        self.labelPassword = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei Mono")
        self.labelPassword.setFont(font)
        self.labelPassword.setObjectName("labelPassword")
        self.gridLayout.addWidget(self.labelPassword, 1, 0, 1, 1)
        self.lineEditPassword = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.gridLayout.addWidget(self.lineEditPassword, 1, 1, 1, 1)
        self.labelFailedMessage = QtWidgets.QLabel(Dialog)
        self.labelFailedMessage.setEnabled(False)
        self.labelFailedMessage.setGeometry(QtCore.QRect(70, 180, 240, 12))
        self.labelFailedMessage.setObjectName("labelFailedMessage")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(120, 140, 142, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBoxIsAdmin = QtWidgets.QCheckBox(self.widget)
        self.checkBoxIsAdmin.setObjectName("checkBoxIsAdmin")
        self.horizontalLayout.addWidget(self.checkBoxIsAdmin)
        self.pushButtonLogin = QtWidgets.QPushButton(self.widget)
        self.pushButtonLogin.setObjectName("pushButtonLogin")
        self.horizontalLayout.addWidget(self.pushButtonLogin)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "登录"))
        self.labelUser.setText(_translate("Dialog", "用户名"))
        self.labelPassword.setText(_translate("Dialog", "密  码"))
        self.labelFailedMessage.setText(_translate("Dialog", "登录失败，请检查用户名及密码是否输入正确"))
        self.checkBoxIsAdmin.setText(_translate("Dialog", "管理员"))
        self.pushButtonLogin.setText(_translate("Dialog", "登录"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
