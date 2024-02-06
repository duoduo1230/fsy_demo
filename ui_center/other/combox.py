from PySide2.QtWidgets import QComboBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem


class ComboCheckBox(QComboBox):
    def __init__(self, items):  # items==[str,str...]
        super(ComboCheckBox, self).__init__()
        self.items = items
        self.items.insert(0, '全部')
        self.row_num = len(self.items)
        self.Selectedrow_num = 0
        self.qCheckBox = []
        self.qLineEdit = QLineEdit()
        self.qLineEdit.setReadOnly(True)
        self.qListWidget = QListWidget()
        self.addQCheckBox(0)
        self.qCheckBox[0].stateChanged.connect(self.All)
        for i in range(1, self.row_num):
            self.addQCheckBox(i)
            self.qCheckBox[i].stateChanged.connect(self.show)
        self.setModel(self.qListWidget.model())
        self.setView(self.qListWidget)
        self.setLineEdit(self.qLineEdit)

    def addQCheckBox(self, i):
        self.qCheckBox.append(QCheckBox())
        qItem = QListWidgetItem(self.qListWidget)
        self.qCheckBox[i].setText(self.items[i])
        self.qListWidget.setItemWidget(qItem, self.qCheckBox[i])

    def Selectlist(self):
        Outputlist = []
        for i in range(1, self.row_num):
            if self.qCheckBox[i].isChecked() == True:
                Outputlist.append(self.qCheckBox[i].text())
        self.Selectedrow_num = len(Outputlist)
        return Outputlist

    def show(self):
        show = ''
        Outputlist = self.Selectlist()
        self.qLineEdit.setReadOnly(False)
        self.qLineEdit.clear()
        for i in Outputlist:
            show += i + ';'
        if self.Selectedrow_num == 0:
            self.qCheckBox[0].setCheckState(QtCore.Qt.Unchecked)
        elif self.Selectedrow_num == self.row_num - 1:
            self.qCheckBox[0].setCheckState(QtCore.Qt.Checked)
        else:
            self.qCheckBox[0].setCheckState(QtCore.Qt.PartiallyChecked)
        self.qLineEdit.setText(show)
        self.qLineEdit.setReadOnly(True)

    def All(self, zhuangtai):
        if zhuangtai == 2:
            for i in range(1, self.row_num):
                self.qCheckBox[i].setChecked(True)
        elif zhuangtai == 1:
            if self.Selectedrow_num == 0:
                self.qCheckBox[0].setCheckState(QtCore.Qt.Checked)
        elif zhuangtai == 0:
            self.clear()

    def clear(self):
        for i in range(self.row_num):
            self.qCheckBox[i].setChecked(False)


if __name__ == '__main__':
    from PySide2 import QtWidgets,QtCore
    import sys
    items = ['Python', 'R', 'Java', 'C++', 'CSS']

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout()
    Form.setLayout(lay)
    comboBox1 = ComboCheckBox(items)
    comboBox1.setGeometry(QtCore.QRect(10, 10, 100, 20))
    comboBox1.setMinimumSize(QtCore.QSize(100, 20))
    lay.addWidget(comboBox1)

    Form.show()
    sys.exit(app.exec_())
