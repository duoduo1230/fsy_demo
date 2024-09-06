import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QButtonGroup

app = QApplication(sys.argv)
window = QMainWindow()
window.resize(500, 400)
window.move(300, 310)
window.setWindowTitle("QPushButtonGroup Example")

# 创建单选按钮
radio_button1 = QPushButton("Option 1", window)
radio_button2 = QPushButton("Option 2", window)
radio_button3 = QPushButton("Option 3", window)

# 创建按钮组并将按钮添加到组中
button_group = QButtonGroup(window)
button_group.addButton(radio_button1)
button_group.addButton(radio_button2)
button_group.addButton(radio_button3)

# 默认选中第一个按钮
radio_button1.setChecked(True)

# 设置按钮布局
radio_button1.move(50, 50)
radio_button2.move(50, 100)
radio_button3.move(50, 150)

window.show()
sys.exit(app.exec_())
