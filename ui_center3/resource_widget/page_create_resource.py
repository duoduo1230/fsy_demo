#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets, QtCore

from dayu_widgets import dayu_theme
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MListView
from ui_center3.resource_widget import _mock_data as mock
from ui_center3.resource_widget.wizards.wizard import MWizardPage


class GetResourcePage(MWizardPage):

    finished = QtCore.Signal()

    def __init__(self, parent=None):
        super(GetResourcePage, self).__init__(parent)
        self._init_ui()
        self.bind_function()
        self.register_field(
            'project_name',
            self.current_select_item,
            signal=self.finished,
            required=True
        )
        self.parent = ""

    def _init_ui(self):

        self.resource_view = MListView(size=dayu_theme.small)
        self.resource_model = MTableModel()
        self.resource_model.set_header_list(mock.header_list)
        self.resource_view.setModel(self.resource_model)
        self.resource_model.set_header_list(mock.header_list)
        self.resource_model.set_data_list(mock.data_list)

        self.name_line_edit = MLineEdit().small()
        self.name_line_edit.setPlaceholderText(self.tr("点击下面按钮设置对应的名字"))
        self.warn_label = MLabel('Name not filled in')
        self.warn_label.setObjectName("error")
        self.name_lay = QtWidgets.QHBoxLayout()
        self.name_lay.addWidget(self.name_line_edit)
        self.name_lay.addWidget(self.warn_label)
        self.name_widget = QtWidgets.QWidget()
        self.name_widget.setLayout(self.name_lay)

        preset_lay = QtWidgets.QHBoxLayout()
        self.master_button = MPushButton("Master").small()
        self.task_button = MPushButton("Task Name").small()
        self.template_button = MPushButton("Template").small()

        self.master_button.setMaximumWidth(140)
        self.task_button.setMaximumWidth(140)
        self.template_button.setMaximumWidth(140)

        preset_lay.addWidget(self.master_button)
        preset_lay.addWidget(self.task_button)
        preset_lay.addWidget(self.template_button)
        preset_lay.addStretch()

        self.preset_widget = QtWidgets.QWidget()
        self.preset_widget.setLayout(preset_lay)

        self.version_lay = QtWidgets.QVBoxLayout()
        self.version_label = QtWidgets.QLabel()
        self.continue_version_button = MCheckBox(self.tr("使用连续版本号"))
        self.version_lay.addWidget(self.version_label)
        self.version_lay.addWidget(self.continue_version_button)

        self.current_version_button = MCheckBox(self.tr("work/dailies/element三个版本号一致"))
        self.version_lay.addWidget(self.current_version_button)

        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight)

        self.form_layout.addRow(MLabel('Available Resource List:').h4(), self.resource_view)

        self.name_title_label = MLabel('New Name:').h4()
        self.preset_title_label = MLabel('Preset:').h4()
        self.form_layout.addRow(self.name_title_label, self.name_widget)
        self.form_layout.addRow(self.preset_title_label, self.preset_widget)
        self.form_layout.addRow(MLabel('Incoming Version:').h4(), self.version_lay)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(self.form_layout)

        self.setLayout(main_lay)

    def bind_function(self):
        self.resource_view.clicked.connect(self.show_preset_lay)

        self.master_button.clicked.connect(self.get_button_text)
        self.task_button.clicked.connect(self.get_button_text)
        self.template_button.clicked.connect(self.get_button_text)

        self.resource_view.clicked.connect(self.confirm_next)
        self.master_button.clicked.connect(self.confirm_next)
        self.task_button.clicked.connect(self.confirm_next)
        self.template_button.clicked.connect(self.confirm_next)

        self.name_line_edit.textChanged.connect(self.name_line_edit_change)

    def get_button_text(self):
        sender_button = self.sender()
        button_text = sender_button.text().lower()
        self.name_line_edit.setText(button_text)

    def show_preset_lay(self, *args):
        index = args[0]
        value = self.resource_model.data(index, QtCore.Qt.DisplayRole)
        if value == 'New Resource':
            if self.form_layout.rowCount() == 4:
                self.name_title_label.show()
                self.name_widget.show()
                self.preset_title_label.show()
                self.preset_widget.show()

            self.name_line_edit.setText('')
            self.name_line_edit.setFocus()
            self.warn_label.setText('Name Is Not Valid')
            self.version_label.setText("v0000")

        else:
            version = value.split("_")[4]
            number_part = version[1:]
            new_number = int(number_part) + 1
            new_version = 'v{:04d}'.format(new_number)
            self.version_label.setText(new_version)
            if self.form_layout.rowCount() == 4:
                self.name_title_label.hide()
                self.name_widget.hide()
                self.preset_title_label.hide()
                self.preset_widget.hide()

    def get_name_data_list(self):
        value_list = []
        row_count = self.resource_view.model().rowCount()
        for row in range(row_count):
            value = self.resource_view.model().data(self.resource_view.model().index(row, 0), QtCore.Qt.DisplayRole)
            if value != 'New Resource':
                value1 = value.split("_")[3]
                value_list.append(value1)

        return value_list

    def name_line_edit_change(self, *args):
        value_list = self.get_name_data_list()
        if args[0] != '':
            if args[0] in value_list:
                self.warn_label.setText('Name Exists')
            else:
                self.warn_label.setText('')
        else:
            self.warn_label.setText('Name Is Not Valid')

    def current_select_item(self):
        """ 得当前选中内容 """
        index = self.resource_view.currentIndex()
        item_name = self.resource_model.data(index, QtCore.Qt.DisplayRole)
        return item_name

    def confirm_next(self):
        self.parent.next_button.setEnabled(False)
        current_text = self.current_select_item()
        if current_text != 'New Resource':
            self.finished.emit()
        else:
            self.name_line_edit.textChanged.connect(self._line_edit_change())

    def _line_edit_change(self):
        # self.parent.next_button.setEnabled(False)
        value_list = self.get_name_data_list()
        if self.name_line_edit.text():
            if self.name_line_edit.text() in value_list:
                self.parent.next_button.setEnabled(False)
            else:
                self.finished.emit()


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = GetResourcePage()
        dayu_theme.apply(test)
        test.show()