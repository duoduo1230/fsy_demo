#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools

from Qt import QtWidgets, QtCore

from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.button_group import MRadioButtonGroup
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.menu import MMenu
from dayu_widgets.line_edit import MLineEdit
from ui_center3.resource_widget.wizards.wizard import MWizardPage
from ui_center3.resource_widget import _mock_data as mock
from dayu_widgets.button_group import MToolButtonGroup


class RadioButtonGroup(QtWidgets.QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(RadioButtonGroup, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        app_data = [
            {"text": "Default Interior"},
            {"text": "No Config"},
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


class HouWorkFileSlatePage(MWizardPage):
    def __init__(self, parent=None):
        super(HouWorkFileSlatePage, self).__init__(parent)
        self.setWindowTitle("Select Slate Config")
        self._init_ui()

    def _init_ui(self):
        self.mode_button_widget = RadioButtonGroup()

        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        self.form_layout.addRow(MLabel('Config List:').h4(), self.mode_button_widget)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(self.form_layout)
        main_lay.addStretch()

        self.setLayout(main_lay)


class NukeWorkFileSlatePage(MWizardPage):
    def __init__(self, parent=None):
        super(NukeWorkFileSlatePage, self).__init__(parent)
        self.setWindowTitle("Select Slate Config")
        self._init_ui()
        self.bind_function()

    def _init_ui(self):

        self.mode_lay = QtWidgets.QVBoxLayout()
        self.interior_button = MPushButton("default Interior").small()
        self.no_config_button = MPushButton("No Config").small()
        self.custom_button = MPushButton("Custom Config").small()
        self.interior_button.setMaximumWidth(140)
        self.no_config_button.setMaximumWidth(140)
        self.custom_button.setMaximumWidth(140)
        self.mode_lay.addWidget(self.interior_button)
        self.mode_lay.addWidget(self.no_config_button)
        self.mode_lay.addWidget(self.custom_button)
        self.mode_button_widget = QtWidgets.QWidget()
        self.mode_button_widget.setLayout(self.mode_lay)

        self.config_button = MMenu(exclusive=False, parent=self)
        self.config_button.set_data(mock.config_list)
        self.config_combobox = MComboBox().small()
        self.config_combobox.set_placeholder(self.tr("Select Slate Config"))
        self.config_combobox.setMaximumWidth(200)
        self.config_combobox._root_menu = self.config_button
        
        self.timecode_line_edt = MLineEdit().small()
        self.timecode_line_edt.setPlaceholderText(self.tr(""))
        self.refresh_button = MPushButton("refresh").small()
        self.timecode_lay = QtWidgets.QHBoxLayout()
        self.timecode_lay.addWidget(self.timecode_line_edt)
        self.timecode_lay.addWidget(self.refresh_button)
        self.timecode_widget = QtWidgets.QWidget()
        self.timecode_widget.setLayout(self.timecode_lay)

        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        self.form_layout.addRow(MLabel('Config List:').h4(), self.mode_button_widget)
        self.config_label = MLabel('Config File:').h4()
        self.form_layout.addRow(self.config_label, self.config_combobox)
        self.form_layout.addRow(MLabel('TimeCode:').h4(), self.timecode_widget)

        self.config_label.hide()
        self.config_combobox.hide()
        
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(self.form_layout)
        main_lay.addStretch()

        self.setLayout(main_lay)

    def bind_function(self):
        self.custom_button.clicked.connect(self.show_config_item)
        self.config_button._action_group.triggered.connect(self.select_slate_config)
        self.interior_button.clicked.connect(self.hide_config_button)
        self.no_config_button.clicked.connect(self.hide_config_button)
        
    def show_config_item(self):
        self.config_label.show()
        self.config_combobox.show()

    def select_slate_config(self, action):
        if action.isChecked():
            self.config_combobox._set_value(action.text())

    def hide_config_button(self):
        self.config_label.hide()
        self.config_combobox.hide()


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = NukeWorkFileSlatePage()
        dayu_theme.apply(test)
        test.show()