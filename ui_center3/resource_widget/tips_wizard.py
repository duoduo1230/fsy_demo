#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan Shiyuan
# Date  : 2019.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets
from PySide2.QtGui import QPixmap
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
import os

folder = os.path.dirname(__file__)
icon_folder = folder.replace("resource_widget", "_icon")


class SuccessMessage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SuccessMessage, self).__init__(parent)
        self.setWindowTitle("Success")
        self.resize(400, 350)
        self._init_ui()

    def _init_ui(self):
        pixmap = QPixmap(os.path.join(icon_folder, "tip_success.jpg"))
        image_label = MLabel()
        image_label.setPixmap(pixmap)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(image_label)
        _label = MLabel("successfully")
        top_layout.addWidget(_label)

        self.close_button = MPushButton("OK").small()
        self.close_button.setMinimumWidth(80)
        self.close_button.clicked.connect(self.close)
        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.close_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)


class FailMessage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FailMessage, self).__init__(parent)
        self.setWindowTitle("Error")
        self.resize(400, 350)
        self._init_ui()

    def _init_ui(self):
        pixmap = QPixmap(os.path.join(icon_folder, "tip_error.jpg"))
        image_label = MLabel()
        image_label.setPixmap(pixmap)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(image_label)
        _label = MLabel("Error")
        top_layout.addWidget(_label)

        self.close_button = MPushButton("OK").small()
        self.close_button.setMinimumWidth(80)
        self.close_button.clicked.connect(self.close)
        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.close_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)


class QuestionMessage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QuestionMessage, self).__init__(parent)
        self.setWindowTitle("Error")
        self.resize(400, 350)
        self._init_ui()

    def _init_ui(self):
        pixmap = QPixmap(os.path.join(icon_folder, "tip_question.jpg"))
        image_label = MLabel()
        image_label.setPixmap(pixmap)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(image_label)
        _label = MLabel("Are you sure to \nopen file?")
        top_layout.addWidget(_label)

        self.accept_button = MPushButton("Yes").small()
        self.close_button = MPushButton("No").small()
        self.accept_button.setMinimumWidth(80)
        self.close_button.setMinimumWidth(80)
        self.close_button.clicked.connect(self.close)
        
        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.accept_button)
        bottom_layout.addWidget(self.close_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = SuccessMessage()
        dayu_theme.apply(test)
        print(__file__)
        test.show()