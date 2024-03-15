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
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton

from ui_center.resource_widget.wizards.wizard import MWizardPage


class WorkFileVersionPage(MWizardPage):
    def __init__(self, parent=None):
        super(WorkFileVersionPage, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):

        mode_lay = QtWidgets.QHBoxLayout()
        self.current_button = MPushButton("Current File").small()
        startup_button = MPushButton("Startup File").small()
        empty_button = MPushButton("Empty File").small()

        self.current_button.setMaximumWidth(140)
        startup_button.setMaximumWidth(140)
        empty_button.setMaximumWidth(140)

        # 设置默认选中self.current_button按钮
        self.current_button.setCheckable(True)
        self.current_button.setChecked(True)

        mode_lay.addWidget(self.current_button)
        mode_lay.addWidget(startup_button)
        mode_lay.addWidget(empty_button)
        mode_lay.addStretch()

        mode_button_widget = QtWidgets.QWidget()
        mode_button_widget.setLayout(mode_lay)

        format_lay = QtWidgets.QHBoxLayout()
        format_button = MPushButton('.hip').small()
        format_button.setMaximumWidth(140)
        format_lay.addWidget(format_button)
        format_lay.addStretch()
        format_button_widget = QtWidgets.QWidget()
        format_button_widget.setLayout(format_lay)

        form_layout = QtWidgets.QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
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
        dayu_theme.apply(test)
        test.show()
