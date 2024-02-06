import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QDockWidget, QTextEdit, QWidget, QGridLayout
from PySide2.QtWidgets import QCalendarWidget

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
        self.dock_widget = QDockWidget("Calendar")
        self.calendar = QCalendarWidget()
        self.dock_widget.setWidget(self.calendar)
        # 将浮动widget添加到主窗口的右侧
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

# 创建一个应用程序对象
app = QApplication(sys.argv)
# 创建一个主窗口对象
window = MainWindow()
# 显示主窗口
window.show()
# 运行应用程序
app.exec_()