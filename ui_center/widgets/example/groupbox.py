from PySide2.QtWidgets import *
import sys


class GroupBox(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.resize(600, 600)

        self.setWindowTitle("GroupBox")

        radiobutton1 = QRadioButton("RadioButton 1")
        radiobutton2 = QRadioButton("RadioButton 2")
        radiobutton3 = QRadioButton("RadioButton 3")
        radiobutton4 = QRadioButton("RadioButton 4")

        vbox = QVBoxLayout()
        vbox.addWidget(radiobutton1)
        vbox.addWidget(radiobutton2)
        vbox.addWidget(radiobutton3)
        vbox.addWidget(radiobutton4)

        layout = QGridLayout()
        groupbox = QGroupBox()
        layout.addWidget(groupbox)
        groupbox.setLayout(vbox)

        self.setLayout(layout)


app = QApplication(sys.argv)
screen = GroupBox()
screen.show()
sys.exit(app.exec_())