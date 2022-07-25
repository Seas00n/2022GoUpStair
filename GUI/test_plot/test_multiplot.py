"""
PyQt5之QGraphics 007 QGraphicsItem四连杆机构动画
2020-03-25
By Linyoubiao
"""

from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem)
from PyQt5.QtCore import (QPoint, QPointF, QRect, QRectF, QLine, QLineF, QTimer, Qt)
from PyQt5.QtGui import (QPainterPath, QBrush, QPen, QColor)
import math
import timer


class Line(QGraphicsItem):
    def __init__(self):
        super(Line, self).__init__()
        # 曲柄
        self.L1 = 16
        # 连杆
        self.L2 = 74
        # 剪刀杆
        self.L3 = 84
        # 支架
        self.L4 = 62
        # 曲柄的角速度
        self.angular_speed = math.pi / 2
        # 每一次动画转动的角度
        self.angle_animation = math.pi / 30
        # 夹角
        self.angle_1 = .0
        self.angle_2 = .0
        self.angle_3 = .0
        self.angle_BDA = .0
        self.angle_CBD = .0
        self.angle_CDB = .0
        # BD两点的距离
        self.e = .0

        # B点坐标
        self.bx = .0
        self.by = .0
        # C点坐标
        self.cx = .0
        self.cy = .0
        # B点坐标
        self.dx = .0
        self.dy = .0

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(2)

    def boundingRect(self):
        rect = QRectF(QPointF(-100, -100), QPointF(200, 100))
        return rect

    def timerEvent(self):
        # 要增加，以更新painter
        self.prepareGeometryChange()

        self.angle_1 -= self.angle_animation
        self.e = math.sqrt(self.L1 ** 2 + self.L4 ** 2 - 2 * self.L1 * self.L4 * math.cos(self.angle_1))
        self.angle_BDA = math.acos((self.e ** 2 + self.L4 ** 2 - self.L1 ** 2) / (2 * self.L4 * self.e))
        self.angle_CBD = math.acos((self.e ** 2 + self.L2 ** 2 - self.L3 ** 2) / (2 * self.L2 * self.e))
        self.angle_CDB = math.acos((self.e ** 2 + self.L3 ** 2 - self.L2 ** 2) / (2 * self.L3 * self.e))

        self.bx = self.L1 * math.cos(self.angle_1)
        self.by = self.L1 * math.sin(self.angle_1)

        if self.by > 0:
            self.angle_2 = self.angle_CBD - self.angle_BDA
        else:
            self.angle_2 = self.angle_CBD + self.angle_BDA

        self.angle_3 = math.pi - (self.angle_CDB + self.angle_BDA)

        self.cx = self.bx + self.L2 * math.cos(self.angle_2)
        self.cy = self.by + self.L2 * math.sin(self.angle_2)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(QBrush(Qt.black), 5))
        painter.drawLine(QLineF(QPointF(0, 0), QPointF(self.L4, 0)))

        painter.setPen(QPen(QBrush(Qt.red), 3))
        painter.drawLine(QLineF(QPointF(0, 0), QPointF(self.bx, self.by)))
        painter.setPen(QPen(QBrush(Qt.green), 3))
        painter.drawLine(QLineF(QPointF(self.bx, self.by), QPointF(self.cx, self.cy)))
        painter.setPen(QPen(QBrush(Qt.blue), 3))
        painter.drawLine(QLineF(QPointF(self.cx, self.cy), QPointF(self.L4, 0)))

        painter.setPen(QPen(QBrush(Qt.darkGray), 1))
        painter.drawEllipse(QPointF(0, 0), self.L1, self.L1)
        painter.drawEllipse(QPointF(self.L4, 0), self.L3, self.L3)


class Scene(QGraphicsScene):
    def __init__(self):
        super(Scene, self).__init__()
        item = Line()
        self.addItem(item)


class View(QGraphicsView):
    def __init__(self):
        super(View, self).__init__()
        scene = Scene()
        self.setScene(scene)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    view = View()
    view.setWindowTitle("四连杆")
    view.show()

    sys.exit(app.exec_())

