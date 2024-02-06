from PySide2.QtWidgets import QApplication, QWidget, QScrollArea, QPushButton, QVBoxLayout
from PySide2.QtWidgets import QSizePolicy

import sys

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        # 创建一个垂直布局管理器
        self.layout = QVBoxLayout()
        # 创建10个按钮，并添加到布局中
        for i in range(10):
            button = QPushButton(f"Button {i+1}")
            self.layout.addWidget(button)
        # 设置widget的布局
        self.setLayout(self.layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 创建一个滚动区域
        self.scroll_area = QScrollArea()
        # 创建一个自定义的widget
        self.my_widget = MyWidget()
        # 将自定义的widget设置为滚动区域的内容
        self.scroll_area.setWidget(self.my_widget)
        # 设置滚动区域的大小策略
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 创建一个垂直布局管理器
        self.layout = QVBoxLayout()
        # 将滚动区域添加到布局中
        self.layout.addWidget(self.scroll_area)
        # 设置主窗口的布局
        self.setLayout(self.layout)

# 创建一个应用程序对象
app = QApplication(sys.argv)
# 创建一个主窗口对象
window = MainWindow()
# 显示主窗口
window.show()
# 运行应用程序
app.exec_()
