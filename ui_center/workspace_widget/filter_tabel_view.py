#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets, QtCore
from dayu_widgets.tool_button import MToolButton
from dayu_widgets.push_button import MPushButton
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTreeView
from dayu_widgets.line_edit import MLineEdit


class FilterTableView(QtWidgets.QWidget, MFieldMixin):
    check = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super(FilterTableView, self).__init__(parent)
        self._init_ui()
        self.bind_function()
        self.setMinimumHeight(100)

    def _init_ui(self):
        self.table_model = MTableModel()
        self.table_model_sort = MSortFilterModel()

        self.table_model_sort.setSourceModel(self.table_model)
        self.table_view = MTreeView()
        self.table_view.setModel(self.table_model_sort)

        self.collapse_all_button = MToolButton().svg("down_line.svg").icon_only().small()
        self.expand_all_button = MToolButton().svg("right_line.svg").icon_only().small()
        self.clear_button = MPushButton('clear').tiny()
        self.clear_button.hide()

        line_edit = MLineEdit().search().tiny()
        line_edit.textChanged.connect(self.table_model_sort.set_search_pattern)

        self.search_lay = QtWidgets.QHBoxLayout()
        self.search_lay.addWidget(line_edit)
        self.search_lay.addStretch()
        self.search_lay.addWidget(self.expand_all_button)
        self.search_lay.addWidget(self.collapse_all_button)

        main_lay = QtWidgets.QVBoxLayout(self)
        main_lay.addLayout(self.search_lay)
        main_lay.addWidget(self.table_view)

        layout = QtWidgets.QGridLayout()
        filter_groupbox = QtWidgets.QGroupBox()
        filter_groupbox.setStyleSheet("QGroupBox { border: 1px solid #A0A0A0;}")
        layout.addWidget(filter_groupbox)
        filter_groupbox.setLayout(main_lay)

        self.setLayout(layout)

    def bind_function(self):
        self.collapse_all_button.clicked.connect(self.table_view.close)
        self.expand_all_button.clicked.connect(self.table_view.show)
        self.table_model.dataChanged.connect(self.data_changed)
        self.clear_button.clicked.connect(self.clear_check_item)

    def clear_check_item(self, *args, **kwargs):
        """
        清理所有勾选的checkbox
        :return:
        """
        row_count = self.table_view.model().rowCount()
        for row in range(row_count):
            self.change_item_status(row, 0)
            continue

    def set_header_hidden(self, hidden):
        """
        Set header hidden.
        :param hidden: <bool>
        """
        self.table_view.setHeaderHidden(hidden)

    def data_changed(self, *args, **kwargs):
        result = {}
        # 当前行的第一列的index是 args[0]
        row_index = args[0].row()
        column_index = self.table_model.columnCount()
        for column in range(column_index):
            header = self.table_model.header_list[column]
            index = self.table_model.index(row_index, column)
            value = self.table_model.data(index, QtCore.Qt.DisplayRole)
            result[header["key"]] = value

        status = self.table_model.data(self.table_model.index(row_index, 0), QtCore.Qt.CheckStateRole)
        result["status"] = status
        print(result)
        self.check.emit(result)

    def change_item_status(self, row, status):
        """
        Change item status by row.
        :param row: <int> The row of an item.
        :param status: <bool> 0, 1, 2
        :return:
        """
        index = self.table_view.model().index(row, 0)
        self.table_view.model().setData(
            index, status, QtCore.Qt.CheckStateRole
        )

    def set_filter_titel(self, name):
        filter_label = QtWidgets.QLabel()
        filter_label.setText(name)
        self.search_lay.insertWidget(0, filter_label)

    def set_header_data(self, data):
        """
        Update header data.
        :param data: <list>
        :return:
        """
        self.table_model.set_header_list(data)
        self.table_view.set_header_list(data)
        self.table_model_sort.set_header_list(data)

    def update_data(self, data):
        """
        Update table view data.
        :param data: <list>
        :return:
        """
        self.table_model.set_data_list(data)


if __name__ == "__main__":
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    filter_head_list = [
        {'label': 'Project', 'key': 'project', 'checkable': True, 'searchable': True, 'width': 80},
        {'label': 'Count', 'key': 'count', 'searchable': True, 'width': 50},
    ]

    filter_data_list = [
        {'project': 'wyd', 'count': 2},
        {'project': 'tdtest', 'count': 5},
        {'project': 'qaz', 'count': 1},
        {'project': 'wsx', 'count': 1},
        {'project': 'edc', 'count': 1},
    ]

    with application() as app:
        test = FilterTableView()
        test.set_filter_titel("project : ")
        test.set_header_data(filter_head_list)
        test.update_data(filter_data_list)
        dayu_theme.apply(test)
        test.show()
