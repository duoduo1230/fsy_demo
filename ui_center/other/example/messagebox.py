from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox

# 创建应用程序对象
app = QApplication([])

# 创建主窗口
main_window = QMainWindow()

# 创建消息框并显示信息
QMessageBox.information(main_window, "信息", "这是一个信息对话框")

# 显示警告框
QMessageBox.warning(main_window, "警告", "这是一个警告对话框")

# 显示错误框
QMessageBox.critical(main_window, "错误", "这是一个错误对话框")

# 显示提问框并获取用户选择
result = QMessageBox.question(main_window, "提问", "你想继续吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
if result == QMessageBox.Yes:
    print("用户选择了Yes")
else:
    print("用户选择了No")

# 显示主窗口
main_window.show()

# 运行应用程序
app.exec_()
