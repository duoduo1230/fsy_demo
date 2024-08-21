# -*- coding: utf-8 -*-
from PySide2 import QtCore
from PySide2 import QtWidgets


class ProcessUI(QtWidgets.QWidget):
    def __init__(self):
        super(ProcessUI, self).__init__()
        self.setWindowTitle("Tool Progress")
        self.setGeometry(300, 300, 400, 100)

        # 创建进度条部件
        self.progress_bar = QtWidgets.QProgressBar(self)
        # 设置左上角 x 坐标、左上角 y 坐标、宽度、高度
        self.progress_bar.setGeometry(20, 20, 360, 30)

        # 初始化计数器
        self.counter = 0

        # 创建了一个名为 timer 的定时器
        self.timer = QtCore.QTimer(self)
        # timer 的 timeout 信号连接到 update_progress 方法
        self.timer.timeout.connect(self.update_progress)
        # 每隔 100 毫秒触发一次 timeout 信号
        self.timer.start(100)

    def update_progress(self):
        # 模拟进度，每次增加 1
        self.counter += 1
        if self.counter > 100:
            # self.counter = 0  # 重置计数器
            self.counter = 100  # 保持100
        # 更新进度条的值
        self.progress_bar.setValue(self.counter)


window1 = FixModelInfo()
window1.show()
