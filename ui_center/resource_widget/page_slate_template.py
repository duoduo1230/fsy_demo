#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PySide2.QtCore import Qt
from Qt import QtWidgets

from dayu_widgets import dayu_theme
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.menu import MMenu
from dayu_widgets.line_edit import MLineEdit
from ui_center.resource_widget.wizards.wizard import MWizardPage
from ui_center.resource_widget import _mock_data as mock


class WorkFileSlatePage(MWizardPage):
    def __init__(self, parent=None):
        super(WorkFileSlatePage, self).__init__(parent)
        self.setWindowTitle("Select Slate Config")
        self._init_ui()
        self.bind_function()

    def _init_ui(self):

        self.mode_lay = QtWidgets.QVBoxLayout()
        self.interior_button = MPushButton("Comp Interior").small()
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
        self.form_layout.setLabelAlignment(Qt.AlignRight)
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
        test = WorkFileSlatePage()
        dayu_theme.apply(test)
        test.show()