import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QDockWidget, QTextEdit, QWidget, QVBoxLayout, QLabel

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: lightgray;")  # 设置标题栏背景颜色
        self.layout = QVBoxLayout()
        self.title_label = QLabel("Calendar")  # 自定义标题
        self.layout.addWidget(self.title_label)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建主窗口的UI
        self.setWindowTitle("PySide2 Dock Widget Example")
        self.setGeometry(300, 300, 500, 400)
        # 创建一个中心widget，用于显示文本
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)
        # 创建一个浮动widget，用于显示日历
        self.dock_widget = QDockWidget()
        self.dock_widget.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.dock_widget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.widget = QWidget()
        self.custom_title_bar = CustomTitleBar()  # 使用自定义标题栏
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.custom_title_bar)
        self.widget.setLayout(self.layout)
        self.dock_widget.setWidget(self.widget)
        # 将浮动widget添加到主窗口的右侧
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

    def closeEvent(self, event):
        if self.dock_widget.isFloating():
            self.dock_widget.setFloating(False)
            event.ignore()
        else:
            event.accept()

# 创建一个应用程序对象
app = QApplication(sys.argv)
# 创建一个主窗口对象
window = MainWindow()
# 显示主窗口
window.show()
# 运行应用程序
app.exec_()
