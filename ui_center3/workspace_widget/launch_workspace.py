#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan Shiyuan
# Date  : 2023.12.12

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import importlib

from Qt import QtWidgets, QtCore
from dayu_widgets import dayu_theme
from dayu_widgets.tool_button import MToolButton
from dayu_widgets.tab_widget import MTabWidget

from ui_center3.workspace_widget.task_widget import TaskWidget
from ui_center3.workspace_widget.CloudFileWidget import CloudFileWidget
from ui_center3.workspace_widget.CloudShotAreaWidget import CloudShotWidget
from ui_center3.workspace_widget.WorkAreaWidget import WorkResources
from ui_center3.workspace_widget.MetadataAreaWidget import MetadataFileView
from ui_center3.resource_widget.launch_create_resource import WorkFileResourceWizard
from ui_center3.workspace_widget import _mock_data as mock


class WorkspaceManager(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WorkspaceManager, self).__init__(parent)
        self.settings = QtCore.QSettings("WorkSpace", "CheckBox")
        self.setWindowTitle(self.tr('Workspace'))
        self.resize(1600, 850)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._init_ui()
        self.bind_function()
        self.add_actions()

    def _init_ui(self):
        title_label = QtWidgets.QLabel('Workspace Manager')
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 32px;")
        self.refresh_button = MToolButton().svg("refresh_line.svg").icon_only()
        title_lay = QtWidgets.QHBoxLayout()
        title_lay.addStretch()
        title_lay.addWidget(title_label)
        title_lay.addWidget(self.refresh_button)
        title_lay.addStretch()

        self.task_widget = TaskWidget()
        self.task_widget.set_task_data(mock)

        self.work_area_widget = WorkResources()
        could_dailies_file = CloudFileWidget()
        could_element_file = CloudFileWidget()
        could_reference_file = CloudFileWidget()
        could_work_file = CloudFileWidget()
        could_cache_file = CloudFileWidget()
        metadata_view = MetadataFileView()
        cloud_shot_view = CloudShotWidget()
        table_default = MTabWidget()
        table_default.setMinimumHeight(350)
        table_default.addTab(self.work_area_widget, "Work Area")
        table_default.addTab(could_cache_file, "Cloud-Cache")
        table_default.addTab(could_dailies_file, "Cloud-Dailies File")
        table_default.addTab(could_element_file, "Could-Element File")
        table_default.addTab(could_reference_file, "Could-Reference File")
        table_default.addTab(could_work_file, "Could-Workfile File")
        table_default.addTab(metadata_view, "Linked Metadata")
        table_default.addTab(cloud_shot_view, "Cloud-Shot/Asset")

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(title_lay)

        main_splitter_v = QtWidgets.QSplitter()
        main_splitter_v.setOrientation(QtCore.Qt.Vertical)
        main_splitter_v.addWidget(self.task_widget)
        main_splitter_v.addWidget(table_default)

        main_lay.addWidget(main_splitter_v)
        self.setLayout(main_lay)

    def bind_function(self):
        self.task_widget.item_clicked.connect(self.work_area_widget.update)
        self.refresh_button.clicked.connect(self.refresh_data)

    def refresh_data(self):
        """
        Refresh task view data
        :return
        """
        importlib.reload(mock)
        self.filter_item_dict = {}
        _count = self.task_widget.filter_widget._filter_widget.count()
        for index in range(_count):
            widget_item = self.task_widget.filter_widget._filter_widget.itemAt(index).widget()
            widget_name = widget_item.objectName()
            row_count = widget_item.table_view.model().rowCount()
            for row in range(row_count):
                status = widget_item.table_view.model().data(widget_item.table_view.model().index(row, 0), QtCore.Qt.CheckStateRole)
                value = widget_item.table_view.model().data(widget_item.table_view.model().index(row, 0), QtCore.Qt.DisplayRole)
                if status == 2:
                    if widget_name in self.filter_item_dict:
                        self.filter_item_dict[widget_name].append(value)
                    else:
                        self.filter_item_dict[widget_name] = [value]

        new_data = []
        for item_dict in mock.data_list:
            is_match = []
            for f, v in self.filter_item_dict.items():
                if item_dict.get(f) in v:
                    is_match.append(f)
            if len(is_match) == len(self.filter_item_dict):
                new_data.append(item_dict)
        self.task_widget.task_table_view.update_data(new_data)

    def setup_data(self, mock):
        self.task_widget.task_table_view.update_data(mock.data_list)

    def restoreState(self):
        filter_cache = self.settings.value("filter_cache")
        filtered_keys = [key for key in filter_cache]
        key_count = len(filtered_keys)
        for key in filter_cache:
            if key not in ["project", "sequence type"]:
                add_filter = self.task_widget.filter_widget.set_checkbox_check(key)
                self.task_widget.filter_widget._filter_widget.addWidget(add_filter)
        for index in range(key_count):
            widget_item = self.task_widget.filter_widget._filter_widget.itemAt(index).widget()
            widget_name = widget_item.objectName()
            for item in filter_cache.get(widget_name):
                widget_item.change_item_status(item[0], 2)

    def closeEvent(self, event):
        """
        When the window is closed, save the current filtering window check box as checked
        :param event:
        :return:
        """
        filter_cache = {}
        count = self.task_widget.filter_widget._filter_widget.count()
        for index in range(count):
            widget_item = self.task_widget.filter_widget._filter_widget.itemAt(index).widget()
            widget_name = widget_item.objectName()
            filter_cache.update({widget_name: []})
            row_count = widget_item.table_view.model().rowCount()
            for row in range(row_count):
                _value = widget_item.table_view.model().index(row, 0).data(role=QtCore.Qt.DisplayRole)
                _state = widget_item.table_view.model().index(row, 0).data(role=QtCore.Qt.CheckStateRole)
                if _state == 2:
                    if widget_name in filter_cache:
                        filter_cache[widget_name].append((row, _value))
                    else:
                        filter_cache[widget_name] = [(row, _value)]

        self.settings.setValue('filter_cache', filter_cache)
        super().closeEvent(event)

    def add_actions(self):
        action = QtWidgets.QAction('creat workfile ', self.task_widget)
        action.triggered.connect(self.current)
        self.task_widget.menu.addAction(action)

    def current(self):
        print(self.task_widget.task_table_view.current_item())
        test = WorkFileResourceWizard()
        test.show()


def main():
    from dayu_widgets.qt import application

    with application() as app:
        test = WorkspaceManager()
        test.restoreState()
        dayu_theme.apply(test)
        test.show()


if __name__ == "__main__":
    main()
