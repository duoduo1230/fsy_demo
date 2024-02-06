from PySide2.QtWidgets import QApplication, QWidget, QCheckBox, QVBoxLayout
from PySide2.QtCore import QSettings

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 创建一个QSettings对象，用于保存和读取设置
        self.settings = QSettings("MyApp", "CheckBoxDemo")
        # 创建一个垂直布局管理器
        self.layout = QVBoxLayout()
        # 创建三个checkbox，并添加到布局中
        self.checkBox1 = QCheckBox("First")
        self.checkBox2 = QCheckBox("Second")
        self.checkBox3 = QCheckBox("Third")
        self.layout.addWidget(self.checkBox1)
        self.layout.addWidget(self.checkBox2)
        self.layout.addWidget(self.checkBox3)
        # 设置窗口的布局
        self.setLayout(self.layout)
        # 从设置中恢复checkbox的状态
        self.restoreState()

    def restoreState(self):
        # 使用QSettings的value方法来获取之前保存的状态，如果没有则返回默认值
        # 使用QSettings的setValue方法来保存当前的状态
        # 使用QCheckBox的isChecked方法来判断是否被勾选
        # 使用QCheckBox的setChecked方法来设置勾选状态
        self.checkBox1.setChecked(self.settings.value("checkBox1", False, bool))
        self.checkBox2.setChecked(self.settings.value("checkBox2", False, bool))
        self.checkBox3.setChecked(self.settings.value("checkBox3", False, bool))

    def closeEvent(self, event):
        # 当窗口关闭时，保存checkbox的状态到设置中
        self.settings.setValue("checkBox1", self.checkBox1.isChecked())
        self.settings.setValue("checkBox2", self.checkBox2.isChecked())
        self.settings.setValue("checkBox3", self.checkBox3.isChecked())
        print(self.checkBox3.isChecked())
        print(self.checkBox2.isChecked())
        print(self.checkBox1.isChecked())
        # 调用父类的方法，完成关闭操作
        super().closeEvent(event)

# 创建一个应用程序对象
app = QApplication([])
# 创建一个主窗口对象
window = MainWindow()
# 显示主窗口
window.show()
# 运行应用程序
app.exec_()