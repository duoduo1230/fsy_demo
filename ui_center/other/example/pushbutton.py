import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PushButton Example")
        self.setGeometry(100, 100, 400, 200)

        # 创建按钮
        button1 = QPushButton("Button 1", self)
        button2 = QPushButton("Button 2", self)
        button3 = QPushButton("Button 3", self)

        # 设置按钮默认状态
        button1.setDefault(True)  # 第一个按钮默认被选中

        # 创建垂直布局并将按钮添加到布局中
        layout = QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)

        # 创建一个 widget 并将布局设置给它
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
