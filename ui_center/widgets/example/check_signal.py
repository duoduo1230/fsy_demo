from PySide2 import QtWidgets
from PySide2 import QtCore

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # 创建 QCheckBox
        self.checkbox = QtWidgets.QCheckBox("启用过滤")
        self.checkbox.stateChanged.connect(self.handle_checkbox_state_changed)

        # 创建 QTreeView（您的 self.filter_widget）
        self.tree_view = QtWidgets.QTreeView()

        # 将 QCheckBox 添加到 QTreeView
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.checkbox)
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

    def handle_checkbox_state_changed(self, state):
        if state == QtCore.Qt.Checked:
            print("复选框已勾选")
            # 在这里执行您的操作
        else:
            print("复选框已取消勾选")
            # 在这里执行其他操作

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyWidget()
    window.show()
    app.exec_()
