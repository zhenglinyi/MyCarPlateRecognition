from PyQt5.QtCore import QThread
from PyQt5.QtNetwork import QTcpServer, QHostAddress, QTcpSocket

class CameraListener(QThread):
    """
    网络线程，监听并接收摄像头拍摄的图片
    """
    tcpserver = 0
    tcpsocket = 0
    def __init__(self, parent=None):
        super(QThread, self).__init__(parent)

        self.tcpserver = QTcpServer()
        self.tcpserver.listen(QHostAddress.Any, 8888)
        
    def onClientConnection(self):
        self.tcpsocket = self.tcpserver.nextPendingConnection()
        self.start()

    def run(self):
        self.tcpsocket.readData()