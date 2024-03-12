#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtCore
from Qt import QtWidgets
from PySide2.QtCore import Qt

from dayu_widgets import dayu_theme
from dayu_widgets.divider import MDivider
from dayu_widgets.label import MLabel
from dayu_widgets.text_edit import MTextEdit


class WarningPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(WarningPage, self).__init__(parent)
        self.setWindowTitle("Warning")
        self._init_ui()

    def _init_ui(self):

        describe_label = MLabel("   当前版本已经提交过\n   点击next覆盖提交版本\n   不覆盖请升级当前工程文件\n")
        describe_lay = QtWidgets.QVBoxLayout()
        describe_lay.addStretch()
        describe_lay.addWidget(describe_label)
        describe_lay.addStretch()

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(describe_lay)
        main_lay.addStretch()

        self.setLayout(main_lay)


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = WarningPage()
        dayu_theme.apply(test)
        test.show()