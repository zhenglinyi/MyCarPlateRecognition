import time
import skimage.io
# qt模块
from PyQt5.QtCore import QThread, pyqtSignal

# 车牌识别模块
import CarplateInterface
graph=[]
class LPRThread(QThread):
    """
    车牌识别线程，载入车牌识别模型，并进行车牌识别
    """
    model = 0
    model_char = 0
    # 0: 初始化
    # 1: 车牌识别
    run_state = 0
    file_name = 0
    is_enter = 0

    """
    信号实例
    """
    # 车牌模型导入完成信号
    initComplete = pyqtSignal()
    # 车牌识别完成信号
    identifyComplete = pyqtSignal(str, str, bool)
    def __init__(self, parent=None):
        print("QThread.__init__")
        super(QThread, self).__init__(parent)
        self.start()

    def __del__(self):
        print("QThread.__del__")

    def identify(self, file_name, is_enter):
        self.run_state = 1
        self.file_name = file_name
        self.is_enter = is_enter

        while 1:
            if self.isFinished:
                self.start()
                break
            time.sleep(0.1)

    def run(self):
        if self.run_state == 0:
            self.model, self.model_char = CarplateInterface.initialize()
            self.initComplete.emit()

            print("initialize")
        elif self.run_state == 1:
            img, carplatenum = CarplateInterface.identify(self.model, self.model_char, self.file_name)
            self.identifyComplete.emit(self.file_name, carplatenum, self.is_enter)
            
            print("identify")
        else:
            pass

        