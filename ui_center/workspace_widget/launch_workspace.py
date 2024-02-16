#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan Shiyuan
# Date  : 2023.12.12

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets
from dayu_widgets.tool_button import MToolButton
from PySide2.QtWidgets import QSplitter
from PySide2.QtCore import QSettings
from dayu_widgets import dayu_theme
from dayu_widgets.tab_widget import MTabWidget
from ui_center.workspace_widget.task_widget import TaskWidget
from ui_center.workspace_widget.cloud_file_widget import CloudFile
from ui_center.workspace_widget.cloud_shot_widget import CloudShotFile
from ui_center.workspace_widget.workarea_widget import WorkResources
from ui_center.workspace_widget.metadata_widget import MetadataFileView
from ui_center.workspace_widget import _mock_data as mock
import importlib

from PySide2 import QtWidgets, QtCore


class WorkspaceManager(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WorkspaceManager, self).__init__(parent)
        self.settings = QSettings("WorkSpace", "CheckBox")
        self.setWindowTitle(self.tr('Workspace'))
        self.resize(2200, 1200)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._init_ui()
        self.bind_function()

    def _init_ui(self):
        # 标题
        title_label = QtWidgets.QLabel('Workspace Manager')
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 42px;")
        self.refresh_button = MToolButton().svg("refresh_line.svg").icon_only()
        title_lay = QtWidgets.QHBoxLayout()
        title_lay.addStretch()
        title_lay.addWidget(title_label)
        title_lay.addWidget(self.refresh_button)
        title_lay.addStretch()

        # 上半部分
        self.task_widget = TaskWidget()
        self.task_widget.set_task_data(mock)
        # 下半部分
        self.work_area_widget = WorkResources()
        could_dailies_file = CloudFile()
        could_element_file = CloudFile()
        could_reference_file = CloudFile()
        could_work_file = CloudFile()
        could_cache_file = CloudFile()
        metadata_view = MetadataFileView()
        cloud_shot_view = CloudShotFile()
        table_default = MTabWidget()
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

        main_splitter_v = QSplitter()
        main_splitter_v.setOrientation(QtCore.Qt.Vertical)
        main_splitter_v.addWidget(self.task_widget)
        main_splitter_v.addWidget(table_default)

        main_lay.addWidget(main_splitter_v)
        self.setLayout(main_lay)

    def bind_function(self):
        """
        Bind function
        :return:
        """
        self.task_widget.item_clicked.connect(self.work_area_widget.update)
        # 设置刷新功能
        self.refresh_button.clicked.connect(self.refresh_data)

    def refresh_data(self):
        """
        Refresh task view data
        :return:
        """
        importlib.reload(mock)
        self.setup_data(mock)

        # 再把勾选的checkbox全部取消了
        for i in range(self.task_widget.filter_widget._filter_widget.count()):
            self.widget = self.task_widget.filter_widget._filter_widget.itemAt(i).widget()
            row_count = self.widget.table_view.model().rowCount()
            for row in range(row_count):
                self.widget.change_item_status(row, 0)
                continue

    def setup_data(self, mock):
        self.task_widget.task_table_view.update_data(mock.data_list)

    def restoreState(self):
        # 这一部分逻辑混款了,应该只关注界面的checkbox是否需要勾选
        # 而不是再把数据更新一遍
        # checkbox勾上就触发了
        # 还要把默认过滤界面以外的,也加进来
        filter_cache = self.settings.value("filter_cache")
        count = self.task_widget.filter_widget._filter_widget.count()
        for index in range(count):
            widget_item = self.task_widget.filter_widget._filter_widget.itemAt(index).widget()
            widget_name = widget_item.objectName()
            row_count = widget_item.table_view.model().rowCount()
            for row, status in enumerate(filter_cache.get(widget_name)):
                widget_item.change_item_status(row, status)

                # TODO: check to update model data

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # self.project_table_view = self.task_widget.filter_widget.project_filter_widget.table_view
        # self.project_table_model = self.task_widget.filter_widget.project_filter_widget
        # row_count = self.project_table_view.model().rowCount()
        # for row in range(row_count):
        #     item_name = self.project_table_view.model().index(row, 0).data(role=QtCore.Qt.DisplayRole)
        #     status = self.settings.value(item_name)
        #     if status == 2:
        #         pro_filtered_data = [item for item in mock.data_list if item.get("project") == item_name]
        #
        #         self.project_table_model.change_item_status(row, status)
        #         # 数据也添上了  但是应该是被后面的覆盖了
        #         self.task_widget.task_table_view.update_data(pro_filtered_data)
        #
        # # 第二个是从窗口已有数据筛选
        # current_data = self.task_widget.task_table_view.task_model.get_data_list()
        # self.shot_table_view = self.task_widget.filter_widget.shot_filter_widget.table_view
        # self.shot_table_model = self.task_widget.filter_widget.shot_filter_widget
        # row_count = self.shot_table_view.model().rowCount()
        # for row in range(row_count):
        #     item_name = self.shot_table_view.model().index(row, 0).data(role=QtCore.Qt.DisplayRole)
        #     status = self.settings.value(item_name)
        #     if status == 2:
        #         shot_filtered_data = [item for item in current_data if item.get("shot asset") == item_name]
        #         self.shot_table_model.change_item_status(row, status)
        #         self.task_widget.task_table_view.update_data(shot_filtered_data)

    def closeEvent(self, event):
        """
        When the window is closed, save the current filtering window check box as checked
        :param event:
        :return:
        """
        # 以下是动态获取filter当前界面的存在checkbox的状态
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
                # self.settings.setValue(_value, _state)
                # print(_value, _state)
                # if _value not in cache["filter_cache"][widget_name]:
                #     cache["filter_cache"][widget_name] = {_value: _state}
                # else:
                filter_cache[widget_name].append(_state)
        self.settings.setValue('filter_cache', filter_cache)
        print(filter_cache)


        # # 以下是写死的只保存了三个窗口,不够灵活
        # self.project_table_view = self.task_widget.filter_widget.project_filter_widget.table_view
        # project_row_count = self.project_table_view.model().rowCount()
        # for row in range(project_row_count):
        #     pro_value = self.project_table_view.model().index(row, 0).data(role=QtCore.Qt.DisplayRole)
        #     pro_state = self.project_table_view.model().index(row, 0).data(role=QtCore.Qt.CheckStateRole)
        #     self.settings.setValue(pro_value, pro_state)
        #
        # self.sequence_table_view = self.task_widget.filter_widget.sequence_filter_widget.table_view
        # shot_row_count = self.shot_table_view.model().rowCount()
        # for row in range(shot_row_count):
        #     shot_value = self.sequence_table_view.model().index(row, 0).data(role=QtCore.Qt.DisplayRole)
        #     shot_state = self.sequence_table_view.model().index(row, 0).data(role=QtCore.Qt.CheckStateRole)
        #     self.settings.setValue(shot_value, shot_state)
        #
        # self.shot_table_view = self.task_widget.filter_widget.shot_filter_widget.table_view
        # shot_row_count = self.shot_table_view.model().rowCount()
        # for row in range(shot_row_count):
        #     shot_value = self.shot_table_view.model().index(row, 0).data(role=QtCore.Qt.DisplayRole)
        #     shot_state = self.shot_table_view.model().index(row, 0).data(role=QtCore.Qt.CheckStateRole)
        #     self.settings.setValue(shot_value, shot_state)

        super().closeEvent(event)


def main():
    from dayu_widgets.qt import application

    with application() as app:
        test = WorkspaceManager()
        test.restoreState()
        dayu_theme.apply(test)
        test.show()


if __name__ == "__main__":
    main()
