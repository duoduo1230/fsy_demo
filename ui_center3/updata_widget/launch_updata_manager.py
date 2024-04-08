#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets, QtCore, QtGui

from dayu_widgets import dayu_theme
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTreeView
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.push_button import MPushButton
from dayu_widgets.label import MLabel
from ui_center3.updata_widget import _mock_data as mock


class DataTreeView(QtWidgets.QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(DataTreeView, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        data_model = MTableModel()
        data_model.set_header_list(mock.header_list)
        data_model_sort = MSortFilterModel()
        data_model_sort.setSourceModel(data_model)

        data_tree_view = MTreeView()
        data_tree_view.setModel(data_model_sort)
        data_model_sort.set_header_list(mock.header_list)
        data_tree_view.set_header_list(mock.header_list)
        data_model.set_data_list(mock.tree_data_list)

        line_edit = MLineEdit().search().small()
        line_edit.textChanged.connect(data_model_sort.set_search_pattern)

        expand_all_button = MPushButton("Expand All").small()
        expand_all_button.clicked.connect(data_tree_view.expandAll)
        collapse_all_button = MPushButton("Collapse All").small()
        collapse_all_button.clicked.connect(data_tree_view.collapseAll)
        button_lay = QtWidgets.QHBoxLayout()
        button_lay.addWidget(expand_all_button)
        button_lay.addWidget(collapse_all_button)
        button_lay.addWidget(line_edit)
        button_lay.addStretch()

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(button_lay)
        main_lay.addWidget(data_tree_view)
        self.setLayout(main_lay)

        # _index = data_model.index(1, 1)
        row_count = data_model.rowCount()
        for row in range(row_count):
            if row % 2 == 0:
                _index = data_model.index(row, 1)
                print(_index)


class UpdataManager(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(UpdataManager, self).__init__(parent)
        self.setWindowTitle(self.tr('Updata Manager'))
        self.resize(1000, 600)
        self._init_ui()

    def _init_ui(self):
        title_label = QtWidgets.QLabel('Updata Manager')
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 36px;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_lay = QtWidgets.QHBoxLayout()
        title_lay.addStretch()
        title_lay.addWidget(title_label)
        title_lay.addStretch()

        self.parse_sel_bnt = MPushButton("Parse Selection").small()
        self.parse_all_bnt = MPushButton("Parse All").small()

        bnt_lay = QtWidgets.QHBoxLayout()
        bnt_lay.addWidget(self.parse_sel_bnt)
        bnt_lay.addWidget(self.parse_all_bnt)

        data_tree_widget = DataTreeView()

        error_label = MLabel('Has new version,need updata')
        error_label.setStyleSheet("background-color: #FF2727; color: black;")
        warning_label = MLabel("Already newest, no need updata")
        warning_label.setStyleSheet("background-color: #FFB14B; color: black;")
        success_label = MLabel("Has new version  but no matched level")
        success_label.setStyleSheet("background-color: #53FF4B; color: black;")

        tips_label_lay = QtWidgets.QHBoxLayout()
        tips_label_lay.addWidget(error_label)
        tips_label_lay.addWidget(warning_label)
        tips_label_lay.addWidget(success_label)
        tips_label_lay.addStretch()

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(title_label)
        main_lay.addLayout(bnt_lay)
        main_lay.addWidget(data_tree_widget)
        main_lay.addLayout(tips_label_lay)

        self.setLayout(main_lay)


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = UpdataManager()
        dayu_theme.apply(test)
        test.show()