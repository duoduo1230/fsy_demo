import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class DockDemo(QMainWindow):
    def __init__(self,parent=None):
        super(DockDemo, self).__init__(parent)
        layout=QHBoxLayout()
        bar=self.menuBar()
        file=bar.addMenu('File')
        file.addAction('New')
        file.addAction('Save')
        file.addAction('quit')

        self.items=QDockWidget('Dockable',self)

        self.listWidget=QListWidget()
        self.listWidget.addItem('Item1')
        self.listWidget.addItem('Item2')
        self.listWidget.addItem('Item3')
        self.listWidget.addItem('Item4')

        self.items.setWidget(self.listWidget)
        self.items.setFloating(False)
        self.setCentralWidget(QTextEdit())
        self.addDockWidget(Qt.RightDockWidgetArea,self.items)

        self.setLayout(layout)
        self.setWindowTitle('Dock Demo with PyQt')

if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=DockDemo()
    demo.show()
    sys.exit(app.exec_())