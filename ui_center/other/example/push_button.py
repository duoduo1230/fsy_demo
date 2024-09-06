import sys

from PySide2.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.btnOne = QPushButton(text="I'm Down!", parent=self)
        self.btnOne.setFixedSize(150, 60)
        self.btnOne.setDown(True)
        self.btnOne.clicked.connect(self.onBtnOneClicked)

        self.btnTwo = QPushButton(text="I'm Disabled!", parent=self)
        self.btnTwo.setFixedSize(150, 60)
        self.btnTwo.setEnabled(False)

        self.btnThree = QPushButton(text="I'm Checked!", parent=self)
        self.btnThree.setFixedSize(150, 60)
        self.btnThree.setCheckable(True)
        self.btnThree.setChecked(True)
        self.btnThree.clicked.connect(self.onBtnThreeClicked)

        layout = QVBoxLayout()
        layout.addWidget(self.btnOne)
        layout.addWidget(self.btnTwo)
        layout.addWidget(self.btnThree)
        self.setLayout(layout)

    def onBtnOneClicked(self):
        if not self.btnOne.isDown():
            self.btnOne.setText("I'm Up!")
            self.btnOne.setDown(False)

    def onBtnThreeClicked(self):
        if self.btnThree.isChecked():
            self.btnThree.setText("I'm Checked!")
        else:
            self.btnThree.setText("I'm Unchecked!")

if __name__ == "__main__":
    from dayu_widgets.qt import application
    with application() as app:
        test = Window()
        test.show()