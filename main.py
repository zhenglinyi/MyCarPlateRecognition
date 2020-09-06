import sys, time

from PyQt5.QtWidgets import QApplication

from Form.MainWindow import MainWindow
from Form.Login import DialogLogin

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 登录对话框
    dialogChangeStandard = DialogLogin()

    while 1:
        dialogChangeStandard.show()
        dialog_code = dialogChangeStandard.exec()

        # 对话框被关闭
        if 0 == dialog_code:
            sys.exit(0)
        
        # 登录成功
        else:
            is_admin = True
            # 管理员登录成功
            if 2 == dialog_code:
                is_admin = True
            # 收费员登录成功
            elif 3 == dialog_code:
                is_admin = False
            # 未定义的操作
            else:
                raise NotImplementedError

            # MainWindow实例
            window = MainWindow(is_admin)
            # 显示MainWindow
            window.show()

            # 执行消息循环
            sys.exit(app.exec())