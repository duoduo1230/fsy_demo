#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan Shiyuan
# Date  : 2023.12.12

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PySide2.QtCore import Qt
from PySide2 import QtCore
from Qt import QtWidgets
from dayu_widgets import dayu_theme
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTableView
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.push_button import MPushButton
from dayu_widgets.menu import MMenu
from dayu_widgets.combo_box import MComboBox
from PySide2.QtWidgets import QSplitter
from functools import partial

from filter_tabel_view import FilterTableView
import _mock_data as mock

filter_list = []
for label in mock.header_list:
    filter_list.append(label.get("key"))
    # 以下三个个窗口为默认显示窗口
    remove_item = ["shot asset", "project", "sequence type"]
    filter_items = [item for item in filter_list if item not in remove_item]


class TaskTableView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TaskTableView, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.task_model = MTableModel()
        self.task_sort_model = MSortFilterModel()
        self.task_sort_model.setSourceModel(self.task_model)
        self.table_view = MTableView(size=dayu_theme.small)
        self.table_view.setModel(self.task_sort_model)

        search_line_edit = MLineEdit().search().small()
        search_line_edit.setFixedWidth(200)
        search_line_edit.textChanged.connect(self.task_sort_model.set_search_pattern)
        self.filter_button = MPushButton("Filter").small()
        self.filter_button.setMinimumSize(100, 25)

        self.search_lay = QtWidgets.QHBoxLayout()
        self.search_lay.addWidget(search_line_edit)
        self.search_lay.addWidget(self.filter_button)
        self.search_lay.addStretch()

        task_view_lay = QtWidgets.QVBoxLayout()
        task_view_lay.addLayout(self.search_lay)
        task_view_lay.addWidget(self.table_view)

        self.setLayout(task_view_lay)
        self.set_header_data(mock.header_list)
        self.update_data(mock.data_list)

    def set_header_data(self, data):
        """
        Update header data.
        :param data: <list>
        :return:
        """
        self.task_model.set_header_list(data)
        self.table_view.set_header_list(data)
        self.task_sort_model.set_header_list(data)

    def update_data(self, data):
        """
        Update table view data.
        :param data: <list>
        :return:
        """
        self.task_model.set_data_list(data)


class FilterWidget(QtWidgets.QWidget, MFieldMixin):
    current_check = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super(FilterWidget, self).__init__(parent)
        self.resize(500, 1200)
        self._init_ui()
        self.bind_function()

    def _init_ui(self):
        self.clear_filter_button = MPushButton("Clear").small()
        self.more_filter_button = MMenu(exclusive=False, parent=self)
        self.more_filter_button.set_data(filter_items)
        self.more_filter_combobox = MComboBox().small()
        self.more_filter_combobox.lineEdit().setText("More Filter")
        self.more_filter_combobox._root_menu = self.more_filter_button

        filter_button_lay = QtWidgets.QHBoxLayout()
        filter_button_lay.addWidget(self.more_filter_combobox)
        filter_button_lay.addWidget(self.clear_filter_button)

        #创建默认存在得窗口
        self._filter_widget = QtWidgets.QVBoxLayout()
        self.project_filter_widget = self.create_filter_widget("project")
        self.sequence_filter_widget = self.create_filter_widget("sequence type")
        self.shot_filter_widget = self.create_filter_widget("shot asset")
        self._filter_widget.addWidget(self.project_filter_widget)
        self._filter_widget.addWidget(self.sequence_filter_widget)
        self._filter_widget.addWidget(self.shot_filter_widget)

        self.main_lay = QtWidgets.QVBoxLayout(self)
        self.main_lay.addLayout(filter_button_lay)
        self.main_lay.addLayout(self._filter_widget)

        self.setLayout(self.main_lay)

    def bind_function(self):
        # 默认存在窗口的信号
        self.project_filter_widget.check.connect(partial(self.current, self.project_filter_widget.objectName()))
        setattr(self, self.project_filter_widget.objectName(), self.project_filter_widget)
        self.sequence_filter_widget.check.connect(partial(self.current, self.sequence_filter_widget.objectName()))
        setattr(self, self.sequence_filter_widget.objectName(), self.sequence_filter_widget)
        self.shot_filter_widget.check.connect(partial(self.current, self.shot_filter_widget.objectName()))
        setattr(self, self.shot_filter_widget.objectName(), self.shot_filter_widget)
        self.clear_filter_button.clicked.connect(self.clear_all_check_item)

        # 动态添加窗口的信号
        self.more_filter_button._action_group.triggered.connect(self.add_filter_widget)

    def add_filter_widget(self, action):
        """
        Dynamically create a filter view
        """
        if action.isChecked():
            add_filter = self.create_filter_widget(action.text())
            add_filter.check.connect(partial(self.current, add_filter.objectName()))
            setattr(self, add_filter.objectName(), add_filter)
            self._filter_widget.addWidget(add_filter)
        else:
            self.clear_filter_widget(action.text())

    def current(self, *args):
        object_name, current_item_data = args
        current_item_data.update({"filter": object_name})
        self.current_check.emit(current_item_data)

    def create_filter_widget(self, target_name):
        """
        create a filter view
        :param target_name: "pipeline step"
        :return:
        """
        self.view = FilterTableView()
        self.view.set_filter_titel(target_name + " :")
        self.view.setObjectName(target_name)
        self.view.set_header_hidden(True)
        filter_head_list, filter_data_list = mock.filter_data_create(target_name, mock.data_list)
        self.view.set_header_data(filter_head_list)
        self.view.update_data(filter_data_list)

        return self.view

    def clear_filter_widget(self, target_name):
        """
        clear unchecked filtering windows
        :param target_name: "pipeline step"
        :return:
        """
        count = self._filter_widget.count()
        for index in range(count):
            widget_item = self._filter_widget.itemAt(index).widget()
            widget_name = widget_item.objectName()
            if widget_name == target_name:
                # 这个删除有错误,没有完全删除.
                self._filter_widget.removeWidget(widget_item)

    def clear_all_check_item(self, *args, **kwargs):
        """
        clear all checked boxes
        :return:
        """
        for i in range(self._filter_widget.count()):
            self.widget = self._filter_widget.itemAt(i).widget()
            row_count = self.widget.table_view.model().rowCount()
            for row in range(row_count):
                self.change_item_status(row, 0)
                continue

    def change_item_status(self, row, status):
        """
        change item status by row.
        :param row: <int> The row of an item.
        :param status: <bool> 0, 1, 2
        :return:
        """
        index = self.widget.table_view.model().index(row, 0)
        self.widget.table_view.model().setData(
            index, status, QtCore.Qt.CheckStateRole
        )


class TaskWidget(QtWidgets.QMainWindow):
    item_clicked = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.resize(2200, 800)
        self.filter_data_list = []
        self._mock = []
        # 组成过滤信息得字典
        self.filter_item_dict = {}

        self.task_table_view = TaskTableView()
        self.setCentralWidget(self.task_table_view)
        self.filter_widget = FilterWidget()
        self.filter_dock_widget = QtWidgets.QDockWidget()
        self.filter_dock_widget.setFeatures(
            QtWidgets.QDockWidget.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetClosable)
        self.filter_dock_widget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.filter_dock_widget.setWidget(self.filter_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.filter_dock_widget)
        self.filter_dock_widget.setFloating(False)

        self.task_table_view.filter_button.clicked.connect(self.filter_dock_show)
        self.filter_widget.current_check.connect(self.update_task)
        self.item_clicked = self.task_table_view.table_view.clicked

    def filter_dock_show(self):
        """
        closing and displaying filtering windows
        :return:
        """
        if self.filter_dock_widget.isVisible():
            self.filter_dock_widget.hide()
        else:
            self.filter_dock_widget.show()

    def update_task(self, *args):
        """
        update data
        :param args: {'project': 'wyd', 'count': 3, 'status': 2, 'filter': 'project'}
        :return:
        """
        dict_ = {}
        _filter = args[0].get('filter')
        value = args[0].get(_filter)
        dict_[_filter] = value
        status = args[0].get('status')

        if status == 2:
            if _filter in self.filter_item_dict:
                self.filter_item_dict[_filter].append(value)
            else:
                self.filter_item_dict[_filter] = [value]
        else:
            self.filter_item_dict[_filter].remove(value)
            if not self.filter_item_dict.get(_filter):
                self.filter_item_dict.pop(_filter)

        # NOTE: self.filter_item_dict = {'project': ['yhg', 'wyd'], 'sequence type': ['test']}
        new_data = []
        for item_dict in self._mock.data_list:
            is_match = []  # 用来存储相同值的字段
            for f, v in self.filter_item_dict.items():
                if item_dict.get(f) in v:
                    is_match.append(f)
            if len(is_match) == len(self.filter_item_dict):  # 判断字段的数量是否相等
                new_data.append(item_dict)
        self.task_table_view.task_model.set_data_list(new_data)

    def clear_filter(self):
        self.filter_item_list = []
        self.task_table_view.task_model.set_data_list(self._mock.data_list)

    def set_task_data(self, mock):
        self._mock = mock


if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = TaskWidget()
        test.set_task_data(mock)
        # test.task_table_view.set_header_data(mock.header_list)
        # test.task_table_view.update_data(mock.data_list)
        dayu_theme.apply(test)
        test.show()
