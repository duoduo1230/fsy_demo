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
from dayu_widgets.button_group import MRadioButtonGroup
from dayu_widgets.field_mixin import MFieldMixin

from ui_center.resource_widget.wizards.wizard import MWizardPage


class RadioButtonGroup(QtWidgets.QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(RadioButtonGroup, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        app_data = [
            {"text": "正常升级版本号 Normal Version Number"},
            {"text": "使用连续版本号 Continue Version Number"},
            {"text": "workfile/dailies/element 三版本号保持一致"},
            {"text": "升级到指定版本号 To Specified Version Number"}
        ]

        radio_group_button_h = MRadioButtonGroup(orientation=QtCore.Qt.Vertical)
        radio_group_button_h.set_button_list(app_data)
        radio_grp_h_lay = QtWidgets.QHBoxLayout()
        radio_grp_h_lay.addWidget(radio_group_button_h)
        radio_grp_h_lay.addStretch()

        self.register_field("value2", 0)
        self.register_field(
            "value2_text", functools.partial(self.value_to_text, "value2", app_data)
        )
        self.bind(
            "value2", radio_group_button_h, "dayu_checked", signal="sig_checked_changed"
        )

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(radio_grp_h_lay)
        main_lay.addStretch()
        self.setLayout(main_lay)

    def value_to_text(self, field, data_list):
        return (
            "Please Select One"
            if self.field(field) < 0
            else "You Selected [{}]".format(data_list[self.field(field)].get("text"))
        )


class VersionPage(MWizardPage):
    def __init__(self, parent=None):
        super(VersionPage, self).__init__(parent)
        self.setWindowTitle("Warning")
        self._init_ui()
        # self.bind_function()

    def _init_ui(self):
        _text = "   Incoming Version Number:\n   {}\n".format("1001")
        version_label = MLabel(_text)

        self.version_checkbox_lay = QtWidgets.QVBoxLayout()
        self.spinbox_lay = QtWidgets.QHBoxLayout()
        self.version_spinbox = MSpinBox().small()
        self.spinbox_lay.addWidget(self.version_spinbox)
        self.spinbox_lay.addStretch()

        self.radio_button_group = RadioButtonGroup()

        widget_lay = QtWidgets.QVBoxLayout()
        widget_lay.addWidget(MLabel())
        widget_lay.addLayout(self.spinbox_lay)

        self.button_lay = QtWidgets.QHBoxLayout()
        self.button_lay.addWidget(self.radio_button_group)
        self.button_lay.addLayout(widget_lay)

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
