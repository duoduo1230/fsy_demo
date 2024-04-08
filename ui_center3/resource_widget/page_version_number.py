#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools

from Qt import QtCore
from Qt import QtWidgets

from dayu_widgets import dayu_theme
from dayu_widgets.divider import MDivider
from dayu_widgets.label import MLabel
from dayu_widgets.spin_box import MSpinBox
from dayu_widgets.field_mixin import MFieldMixin

from ui_center3.resource_widget.wizards.wizard import MWizardPage


class RadioButton(QtWidgets.QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(RadioButton, self).__init__(parent)
        self._init_ui()
        self.bind_function()

    def _init_ui(self):
        self.normal_radio_button = QtWidgets.QRadioButton(u'正常升级版本号 Normal Version Number')
        self.normal_radio_button.setChecked(True)
        self.continue_version_radio_button = QtWidgets.QRadioButton(u'使用连续版本号 Continue Version number')
        self.sync_version_radio_button = QtWidgets.QRadioButton(u'workfile/dailies/element三版本号保持一致')
        self.spec_version_radio_button = QtWidgets.QRadioButton(u'升级到指定版本号 To Specified Version number')
        self.version_spinbox = MSpinBox().small()
        self.version_spinbox.setEnabled(False)

        self.spec_version_lay = QtWidgets.QHBoxLayout()
        self.spec_version_lay.addWidget(self.spec_version_radio_button)
        self.spec_version_lay.addWidget(self.version_spinbox)
        self.spec_version_lay.addStretch()

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(self.normal_radio_button)
        main_lay.addWidget(self.continue_version_radio_button)
        main_lay.addWidget(self.sync_version_radio_button)
        main_lay.addLayout(self.spec_version_lay)
        self.setLayout(main_lay)

    def bind_function(self):
        self.spec_version_radio_button.clicked.connect(self.enable_version_spinbox)
        self.normal_radio_button.clicked.connect(self.disable_version_spinbox)
        self.continue_version_radio_button.clicked.connect(self.disable_version_spinbox)
        self.sync_version_radio_button.clicked.connect(self.disable_version_spinbox)

    def enable_version_spinbox(self):
        self.version_spinbox.setEnabled(True)

    def disable_version_spinbox(self):
        self.version_spinbox.setEnabled(False)


class VersionPage(MWizardPage):
    def __init__(self, parent=None):
        super(VersionPage, self).__init__(parent)
        self.setWindowTitle("Warning")
        self._init_ui()

    def _init_ui(self):
        _text = "   Incoming Version Number:\n   {}\n".format("1001")
        version_label = MLabel(_text)

        self.version_checkbox_lay = QtWidgets.QVBoxLayout()
        self.version_spinbox = MSpinBox().small()
        self.radio_button_group = RadioButton()

        self.spinbox_lay = QtWidgets.QHBoxLayout()
        self.spinbox_lay.addWidget(self.version_spinbox)
        self.spinbox_lay.addStretch()

        widget_lay = QtWidgets.QVBoxLayout()
        # widget_lay.addWidget(MLabel())
        widget_lay.addLayout(self.spinbox_lay)

        self.button_lay = QtWidgets.QHBoxLayout()
        self.button_lay.addWidget(self.radio_button_group)
        # self.button_lay.addLayout(widget_lay)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addStretch()
        main_lay.addWidget(version_label)
        main_lay.addWidget(MDivider(""))
        main_lay.addLayout(self.button_lay)
        main_lay.addStretch()

        self.setLayout(main_lay)

    def value_to_text(self, field, data_list):
        return (
            "Please Select One"
            if self.field(field) < 0
            else "You Selected [{}]".format(data_list[self.field(field)].get("text"))
        )


if __name__ == "__main__":
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = VersionPage()
        dayu_theme.apply(test)
        test.show()
