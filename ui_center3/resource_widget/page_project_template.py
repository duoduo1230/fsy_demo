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
from ui_center3.resource_widget.wizards.wizard import MWizardPage


class RadioButtonGroup(QtWidgets.QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(RadioButtonGroup, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        app_data = [
            {"text": "Current File"},
            {"text": "Startup File"},
            {"text": "Empty File"},
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


class WorkFileVersionPage(MWizardPage):
    def __init__(self, parent=None):
        super(WorkFileVersionPage, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):

        mode_button_widget = RadioButtonGroup()

        format_lay = QtWidgets.QHBoxLayout()
        format_button = MPushButton('.hip').small()
        format_button.setMaximumWidth(140)
        format_lay.addWidget(format_button)
        format_lay.addStretch()
        format_button_widget = QtWidgets.QWidget()
        format_button_widget.setLayout(format_lay)

        form_layout = QtWidgets.QFormLayout()
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        form_layout.addRow(MLabel('Create Mode:').h4(), mode_button_widget)
        form_layout.addRow(MLabel('File Format:').h4(), format_button_widget)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(form_layout)
        main_lay.addStretch()

        self.setLayout(main_lay)


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = WorkFileVersionPage()
        # dayu_theme.apply(test)
        test.show()
