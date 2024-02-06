
from PySide2 import QtCore, QtWidgets, QtGui
import sys

class TestWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        group = QtWidgets.QGroupBox()
        layout.addWidget(group)

        group_layout = QtWidgets.QHBoxLayout()
        group.setLayout(group_layout)

        labelContainerWidget = QtWidgets.QWidget()
        labelContainer_layout = QtWidgets.QHBoxLayout()
        labelContainerWidget.setLayout(labelContainer_layout)
        label1 = QtWidgets.QLabel('test1')
        label2 = QtWidgets.QLabel('test2')
        group_layout.setAlignment(QtCore.Qt.AlignCenter)
        group_layout.addWidget(label1)
        group_layout.addWidget(label2)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = TestWidget()
    form.show()
    app.exec_()