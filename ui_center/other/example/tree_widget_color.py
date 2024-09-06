from PySide2 import QtWidgets, QtGui, QtCore

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("修改行数据颜色")
        self.resize(400, 300)

        # 创建一个 QTreeView 控件
        self.tree_view = QtWidgets.QTreeView()

        # 设置模型
        self.model = QtGui.QStandardItemModel()
        self.tree_view.setModel(self.model)

        # 添加数据
        for i in range(5):
            item = QtGui.QStandardItem(f"Row {i}")
            self.model.appendRow(item)

        # 设置第2行的背景色为红色
        red_item = self.model.item(1)
        red_item.setBackground(QtGui.QColor("red"))

        # 设置第3行的背景色为绿色
        green_item = self.model.item(2)
        green_item.setBackground(QtGui.QColor("green"))

        # 布局
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = MyWidget()
    win.show()
    app.exec_()
