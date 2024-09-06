import sys
from PySide2.QtWidgets import QApplication, QWizard, QWizardPage, QLabel, QVBoxLayout, QPushButton

class FirstPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("第一页")
        label = QLabel("这是第一页的内容")
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

class SecondPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("第二页")
        label = QLabel("这是第二页的内容")
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

class ThirdPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("第三页")
        label = QLabel("这是第三页的内容")
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wizard = QWizard()
    wizard.addPage(FirstPage())
    wizard.addPage(SecondPage())
    wizard.addPage(ThirdPage())
    wizard.setWindowTitle("Previous")
    wizard.show()
    sys.exit(app.exec_())
