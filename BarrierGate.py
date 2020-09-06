import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QLinearGradient, QPolygon
from PyQt5.QtCore import Qt, QRect, QPoint

class BarrierGate(QWidget):
    """description of class"""
    def __init__(self, parent):
        super().__init__(parent)

        self.setGeometry(200,140, 400, 250)

    def paintEvent(self, QPaintEvent):
        points = [
            QPoint(140, 80),
            QPoint(150, 10),
            QPoint(210, 30),
            QPoint(220, 70)
        ]

        rect = QRect(10, 20, 80, 60);

        painter = QPainter(self);     

        #linearGradient = QLinearGradient(0, 0, 100, 100);
        #linearGradient.setColorAt(0.0, Qt.white);
        #linearGradient.setColorAt(0.2, Qt.green);
        #linearGradient.setColorAt(1.0, Qt.black);
        #painter.setBrush(linearGradient);

        painter.setBrush(QColor(Qt.white))
        painter.setPen(QPen(Qt.white, 1.0));
        painter.drawRect(self.rect());

        painter.setBrush(QColor(Qt.blue))
        painter.setPen(QPen(Qt.blue, 1.0));
        painter.drawPolygon(QPolygon(points), 4);

    def drawGate(self):
        rect = QRect(10, 20, 80, 60);
        
        painter = QPainter(self);     

        #linearGradient = QLinearGradient(0, 0, 100, 100);
        #linearGradient.setColorAt(0.0, Qt.white);
        #linearGradient.setColorAt(0.2, Qt.green);
        #linearGradient.setColorAt(1.0, Qt.black);
        #painter.setBrush(linearGradient);

        painter.begin(self)
        painter.setBrush(QColor(Qt.white))
        painter.setPen(QPen(Qt.white, 1.0));
        painter.drawRect(self.rect());
        painter.end()

        #painter.drawPolygon(points, 4);