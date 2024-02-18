#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan Shiyuan
# Date  : 2023.12.12

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets
from PySide2.QtCore import Qt
from dayu_widgets import dayu_theme
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTableView
from ui_center.workspace_widget.example import _mock_data as mock


class WorkResourcesView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(WorkResourcesView, self).__init__(parent)

        self.work_resources_model = MTableModel()
        self.work_resources_sort_model = MSortFilterModel()
        self.work_resources_sort_model.setSourceModel(self.work_resources_model)
        self.work_resources_model.set_header_list(mock.work_resources_header_list)
        self.work_resources_view = MTableView(size=dayu_theme.small)
        self.work_resources_view.setModel(self.work_resources_sort_model)

        metadata_lay = QtWidgets.QVBoxLayout()
        metadata_lay.addWidget(self.work_resources_view)

        filter_groupbox = QtWidgets.QGroupBox()
        # 设置边缘线颜色
        filter_groupbox.setStyleSheet("QGroupBox { border: 1px solid #A0A0A0;}")
        # 设置字体颜色
        filter_groupbox.setStyleSheet("QGroupBox { color: #F7A72D;}")
        filter_groupbox.setTitle("Resources")
        # Title居中
        filter_groupbox.setAlignment(Qt.AlignCenter)
        filter_groupbox.setLayout(metadata_lay)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(filter_groupbox)

        self.setLayout(layout)

        self.update_data(mock.work_resources_data_list)

    def update_data(self, data):
        """
        Update table view data.
        :param data: <list>
        :return:
        """
        self.work_resources_model.set_data_list(data)


class WorkVersionView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(WorkVersionView, self).__init__(parent)

        self.work_version_model = MTableModel()
        self.work_version_sort_model = MSortFilterModel()
        self.work_version_sort_model.setSourceModel(self.work_version_model)
        self.work_version_model.set_header_list(mock.work_version_header_list)
        self.work_version_view = MTableView(size=dayu_theme.small)
        self.work_version_view.setModel(self.work_version_sort_model)

        metadata_lay = QtWidgets.QVBoxLayout()
        metadata_lay.addWidget(self.work_version_view)

        layout = QtWidgets.QGridLayout()
        filter_groupbox = QtWidgets.QGroupBox()
        # filter_groupbox.setStyleSheet("QGroupBox { border: 1px solid #A0A0A0;}")
        layout.addWidget(filter_groupbox)
        filter_groupbox.setLayout(metadata_lay)

        self.setLayout(layout)

        self.update_data(mock.work_version_data_list)

    def update_data(self, data):
        """
        Update table view data.
        :param data: <list>
        :return:
        """
        self.work_version_model.set_data_list(data)


class WorkResources(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WorkResources, self).__init__(parent)
        self.work_resources_ui()

    def work_resources_ui(self):
        resources_widget = WorkResourcesView()
        version_widget = WorkVersionView()
        Snapshots_View = WorkVersionView()

        main_lay = QtWidgets.QHBoxLayout()
        main_lay.addWidget(resources_widget)
        main_lay.addWidget(version_widget)
        main_lay.addWidget(Snapshots_View)

        self.setLayout(main_lay)

    def update(self, data):
        print("waork update")


if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = WorkResources()
        dayu_theme.apply(test)
        test.show()
