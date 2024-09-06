# 导入必要的模块
import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget

# 创建应用程序实例
app = QApplication(sys.argv)

# 创建主窗口
window = QWidget()
window.setWindowTitle("PySide2 Wizard Example")
window.setGeometry(100, 100, 400, 300)

# 创建一个堆叠窗口，用于切换不同的页面
stacked_widget = QStackedWidget()

# 第一页
page1 = QWidget()
layout1 = QVBoxLayout()
label1 = QLabel("Welcome to the Wizard!")
next_button1 = QPushButton("Next")
layout1.addWidget(label1)
layout1.addWidget(next_button1)
page1.setLayout(layout1)

# 第二页
page2 = QWidget()
layout2 = QVBoxLayout()
label2 = QLabel("Congratulations! You've reached the end of the Wizard.")
finish_button = QPushButton("Finish")
layout2.addWidget(label2)
layout2.addWidget(finish_button)
page2.setLayout(layout2)

# 将页面添加到堆叠窗口
stacked_widget.addWidget(page1)
stacked_widget.addWidget(page2)

# 设置初始页面
stacked_widget.setCurrentIndex(0)

# 连接按钮信号和槽函数
next_button1.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
finish_button.clicked.connect(app.quit)

# 将堆叠窗口添加到主窗口
layout = QVBoxLayout()
layout.addWidget(stacked_widget)
window.setLayout(layout)

# 显示窗口
window.show()

# 运行应用程序
sys.exit(app.exec_())
