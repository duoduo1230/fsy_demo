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
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.spin_box import MSpinBox
from wizards.wizard import MWizardPage
from dayu_widgets.button_group import MRadioButtonGroup


class VersionPage(MWizardPage):
    def __init__(self, parent=None):
        super(VersionPage, self).__init__(parent)
        self.setWindowTitle("Warning")
        self._init_ui()
        # self.bind_function()

    def _init_ui(self):
        # "v0001" 应该是动态获取的
        version_label = MLabel("   Incoming Version Number:\n   v0001\n")
        self.version_checkbox_lay = QtWidgets.QVBoxLayout()

        self.normal_button = MCheckBox(self.tr("正常升级版本号 Normal Version Number"))
        self.normal_button.setChecked(True)
        self.order_button = MCheckBox(self.tr("使用连续版本号 Continue Version Number"))
        self.version_button = MCheckBox(self.tr("workfile/dailies/element 三版本号保持一致"))

        self.spinbox_lay = QtWidgets.QHBoxLayout()
        self.version_spinbox = MSpinBox().small()
        self.spinbox_lay.addWidget(self.version_spinbox)
        self.spinbox_lay.addStretch()

        self.button_group = MRadioButtonGroup(orientation=QtCore.Qt.Vertical)
        self.button_group.set_button_list(
            ["正常升级版本号 Normal Version Number", {"text": "使用连续版本号 Continue Version Number"},
             {"text": "workfile/dailies/element 三版本号保持一致"}, {"text": "升级到指定版本号 To Specified Version Number"}])
        self.button_lay = QtWidgets.QHBoxLayout()
        self.button_lay.addWidget(self.button_group)
        self.button_lay.addLayout(self.spinbox_lay)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addStretch()
        main_lay.addWidget(version_label)
        main_lay.addWidget(MDivider(""))
        main_lay.addLayout(self.button_lay)
        # main_lay.addLayout(self.spinbox_lay)
        main_lay.addStretch()

        self.setLayout(main_lay)


if __name__ == "__main__":
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = VersionPage()
        dayu_theme.apply(test)
        test.show()
