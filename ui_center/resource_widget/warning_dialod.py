from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets, QtCore
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QMessageBox
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
import os
folder = os.path.dirname(__file__)
icon_folder = folder.replace("resource_widget", "_icon")

class MErrorMessageBox(QMessageBox):
    def __init__(self, msg, detail=None, parent=None):
        super(MErrorMessageBox, self).__init__(parent)
        self.setWindowTitle(self.tr('Error'))

        pix = QPixmap(os.path.join(icon_folder, "tip_error.jpg"))
        self.setIconPixmap(pix.scaledToWidth(160, QtCore.Qt.SmoothTransformation))
        self.setText('<span style="font-size:18px;color:#ddd">' + self.tr('Something is wrong') + '</span>')
        self.setInformativeText('<span style="font-size:16px;color:#888">' + msg + '</span>')
        if detail:
            self.setDetailedText(detail)
        self.setStandardButtons(QMessageBox.Ok)


class MSuccessMessageBox(QMessageBox):
    def __init__(self, msg, parent=None):
        super(MSuccessMessageBox, self).__init__(parent)
        self.setWindowTitle(self.tr('Success'))
        pix = QPixmap(os.path.join(icon_folder, "tip_success.jpg"))
        self.setIconPixmap(pix.scaledToWidth(160, QtCore.Qt.SmoothTransformation))
        self.setText('<span style="font-size:18px;color:#ddd">' + self.tr('Congratulations') + '</span>')
        self.setInformativeText('<span style="font-size:16px;color:#888">' + msg + '</span>')
        self.setStandardButtons(QMessageBox.Ok)


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = MSuccessMessageBox('test')
        dayu_theme.apply(test)

        test.show()