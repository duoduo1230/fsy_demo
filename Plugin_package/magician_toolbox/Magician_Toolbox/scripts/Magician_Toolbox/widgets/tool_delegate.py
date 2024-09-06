# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from Qt import QtWidgets
from Qt import QtCore
from functools import partial


class DelegateButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(DelegateButton, self).__init__(parent)

        self.setToolTip(u"点击打开帮助文档")

        size = 33
        self.setFixedSize(size, size)
        style_sheet = """
            QPushButton{
                font: 12px "Roboto Thin";
                border-radius: 25;
                image: url("%(Magician_Toolbox)s/icons/help.png");
            }
            QPushButton:hover{
                image: url("%(Magician_Toolbox)s/icons/help_press.png");
                border-radius: 25;
            }
            QPushButton:pressed{
                image: url("%(Magician_Toolbox)s/icons/help.png");
                border-radius: 50;
            }
            """
        self.setStyleSheet(style_sheet % {"Magician_Toolbox": os.environ["Magician_Toolbox"].replace("\\", "/")})


class HelpDelegate(QtWidgets.QStyledItemDelegate):
    onClicked = QtCore.Signal(QtCore.QModelIndex)

    def __init__(self, parent=None):
        super(HelpDelegate, self).__init__(parent)
        self.parent = parent
        self._my_btn = None
        self._pressed = None
        self.rf_btn = DelegateButton()

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QWidget(parent)
        editor.setStyleSheet("background-color:transparent")
        editor.button = DelegateButton(editor)
        editor.button.setObjectName('edit_btn')
        editor.button.clicked.connect(partial(self.parent.open_help, index))

        layout = QtWidgets.QHBoxLayout(editor)
        layout.setMargin(0)
        layout.addStretch()
        layout.addWidget(editor.button)
        return editor

    def paint(self, painter, option, index):
        if index.model().hasChildren(index):
            return super(HelpDelegate, self).paint(painter, option, index)

        if option.state & QtWidgets.QStyle.State_MouseOver:
            self.parent.openPersistentEditor(index)

        else:
            self.parent.closePersistentEditor(index)

        QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)
