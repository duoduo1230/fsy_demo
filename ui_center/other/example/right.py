import sys
from PySide2 import QtGui, QtCore
from PySide2 import QtWidgets

class MainForm(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        # create button
        self.button = QtWidgets.QPushButton("test button", self)
        self.button.resize(100, 30)

        # set button context menu policy
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        # create context menu
        self.popMenu = QtWidgets.QMenu(self)
        self.popMenu.addAction(QtWidgets.QAction('test0', self))
        self.popMenu.addAction(QtWidgets.QAction('test1', self))
        self.popMenu.addSeparator()
        self.popMenu.addAction(QtWidgets.QAction('test2', self))

    def on_context_menu(self, point):
        # show context menu
        self.popMenu.exec_(self.button.mapToGlobal(point))

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()