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
from dayu_widgets.divider import MDivider
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton


class WorkFileVersionPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(WorkFileVersionPage, self).__init__(parent)
        self.setWindowTitle("Slate Config")
        self.setFixedSize(800, 600)
        self._init_ui()

    def _init_ui(self):

        mode_lay = QtWidgets.QHBoxLayout()
        current_button = MPushButton("Current File").small()
        startup_button = MPushButton("Startup File").small()
        empty_button = MPushButton("Empty File").small()

        current_button.setMaximumWidth(140)
        startup_button.setMaximumWidth(140)
        empty_button.setMaximumWidth(140)

        mode_lay.addWidget(current_button)
        mode_lay.addWidget(startup_button)
        mode_lay.addWidget(empty_button)
        mode_lay.addStretch()

        mode_button_widget = QtWidgets.QWidget()
        mode_button_widget.setLayout(mode_lay)

        format_lay = QtWidgets.QHBoxLayout()
        format_button = MPushButton('').small()
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
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = WorkFileVersionPage()
        dayu_theme.apply(test)
        test.show()