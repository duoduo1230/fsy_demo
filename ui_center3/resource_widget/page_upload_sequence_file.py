#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets, QtCore
from PySide2.QtWidgets import QFrame
from dayu_widgets.qt import MIcon
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.browser import MDragFileButton
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.line_edit import MLineEdit
from ui_center3.resource_widget.wizards.wizard import MWizardPage

import os

file_type_list = ['.jpg', '.png', 'tif', 'exr', 'dpx', 'tiff', 'jpeg']


class MGetSequenceFilePage(MWizardPage):
    def __init__(self, parent=None):
        super(MGetSequenceFilePage, self).__init__(parent)
        self.setWindowTitle("Upload File")

        self.file_pattern = ""

        self._init_ui()
        self.bind_function()
        self.register_field(
            'file_path',
            self._line_edit.text,
            signal=self._line_edit.textChanged,
            required=True
        )

    def _init_ui(self):

        self.file_filter_label = MLabel(str(file_type_list))

        self.upload_file_button = MDragFileButton(text="Click or drag file here")
        self.upload_file_button.setMinimumHeight(200)
        self.upload_file_button.set_dayu_filters(file_type_list)
        self._line_edit = MLineEdit().tiny()
        self.upload_file_button.set_dayu_svg("attachment_line.svg")

        self.delete_button = MPushButton().tiny()
        self.delete_button.setMaximumWidth(100)
        self.delete_button.setIcon(MIcon("minus.png"))
        self.delete_button.setObjectName("minus")
        self.folder_button = MPushButton().tiny()
        self.folder_button.setIcon(MIcon("folder_line.svg"))
        self.folder_button.setObjectName("folder_line")
        self.file_type_label = MLabel("")

        self.file_lay = QtWidgets.QHBoxLayout()
        self.file_lay.addWidget(self.delete_button)
        self.file_lay.addWidget(self.file_type_label)
        self.file_lay.addWidget(self._line_edit)
        self.file_lay.addWidget(self.folder_button)

        self.sequence_checkbox = MCheckBox(self.tr("Sequence"))
        self.frame_button = MCheckBox(self.tr("Keep Frame"))
        self.rename_button = MCheckBox(self.tr("Is Order Rename"))
        self.splicing_button = MCheckBox(self.tr("Splicing the first self.frame"))

        self.file_checkbox_lay = QtWidgets.QGridLayout()
        self.file_checkbox_lay.addWidget(self.sequence_checkbox, 1, 0)
        self.file_checkbox_lay.addWidget(self.frame_button, 1, 1)
        self.file_checkbox_lay.addWidget(self.rename_button, 2, 0)
        self.file_checkbox_lay.addWidget(self.splicing_button, 2, 1)

        self.file_result_lay = QtWidgets.QVBoxLayout()
        self.file_result_lay.addLayout(self.file_lay)
        self.file_result_lay.addLayout(self.file_checkbox_lay)

        self.frame = QFrame()
        self.frame.setLayout(self.file_result_lay)

        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        self.form_layout.addRow(MLabel('File Filter:').h4(), self.file_filter_label)
        self.form_layout.addRow(MLabel('Give File:').h4(), self.upload_file_button)
        self.form_layout.addRow(MLabel('File Result:').h4(), self.frame)

        self.frame.setVisible(False)
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(self.form_layout)
        main_lay.addStretch()

        self.setLayout(main_lay)

    def bind_function(self):
        self.upload_file_button.sig_file_changed.connect(self.show_widget)
        self.delete_button.clicked.connect(self.hide_widget)
        self.upload_file_button.sig_file_changed.connect(self.change_line_edit)
        self._line_edit.textChanged.connect(self.input_file_type)
        self.folder_button.clicked.connect(self.open_file_folder)
        self.sequence_checkbox.stateChanged.connect(self.change_file_pattern)

    def show_widget(self):
        self.frame.setVisible(True)

    def hide_widget(self):
        self._line_edit.clear()
        self.sequence_checkbox.setChecked(0)
        self.frame.setVisible(False)

    def input_file_type(self):
        name, suf = os.path.splitext(self._line_edit.text())
        self.file_type_label.setText(suf)

    def change_line_edit(self, text):
        """
        Change line edit and check the sequence button.
        """
        self.file_pattern = text
        self._line_edit.setText(text)
        self.check_sequence_button(2)

    def open_file_folder(self):
        folder, filename = os.path.split(self._line_edit.text())
        command = 'start {}'.format(folder)
        os.system(command)

    def check_sequence_button(self, status):
        self.sequence_checkbox.setChecked(status)

    def change_file_pattern(self, *args):
        """
        Change file pattern form "%04d" to "1001" if sequence checkbox is checked, otherwise
        change file pattern form "1001" to "%04d".
        """
        original_text = self._line_edit.text()
        if args[0] == 2:
            frame = original_text.split(".")[1]
            new_text = original_text.replace(frame, '%04d')
            self.frame_button.setDisabled(False)
        else:
            frame = self.file_pattern.split(".")[1]
            new_text = original_text.replace("%04d", frame)
            self.frame_button.setDisabled(True)

        self._line_edit.setText(new_text)


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = MGetSequenceFilePage()
        dayu_theme.apply(test)
        test.show()





