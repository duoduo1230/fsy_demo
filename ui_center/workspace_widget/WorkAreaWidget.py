#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan Shiyuan
# Date  : 2024.2.8

from Qt import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QSplitter
from dayu_widgets import dayu_theme
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTableView
from ui_center.workspace_widget.example import _mock_data as mock


class WorkResources(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WorkResources, self).__init__(parent)
        self.work_resources_ui()

    def work_resources_ui(self):

        self.resources_model = MTableModel()
        self.resources_sort_model = MSortFilterModel()
        self.resources_sort_model.setSourceModel(self.resources_model)
        self.resources_model.set_header_list(mock.work_resources_header_list)
        self.resources_view = MTableView(size=dayu_theme.small)
        self.resources_view.setModel(self.resources_sort_model)

        self.version_model = MTableModel()
        self.version_sort_model = MSortFilterModel()
        self.version_sort_model.setSourceModel(self.version_model)
        self.version_model.set_header_list(mock.work_version_header_list)
        self.version_view = MTableView(size=dayu_theme.small)
        self.version_view.setModel(self.version_sort_model)

        self.snapshots_model = MTableModel()
        self.snapshots_sort_model = MSortFilterModel()
        self.snapshots_sort_model.setSourceModel(self.snapshots_model)
        self.snapshots_model.set_header_list(mock.work_version_header_list)
        self.snapshots_view = MTableView(size=dayu_theme.small)
        self.snapshots_view.setModel(self.snapshots_sort_model)

        resource_grp = QtWidgets.QGroupBox(self.tr('resources'))
        resource_grp.setAlignment(Qt.AlignCenter)
        resource_grp.setStyleSheet("QGroupBox { border: 1px solid #A0A0A0;}")
        resource_grp.setStyleSheet("QGroupBox { color: #F7922D;}")

        version_grp = QtWidgets.QGroupBox(self.tr('versions'))
        version_grp.setAlignment(Qt.AlignCenter)
        version_grp.setStyleSheet("QGroupBox { border: 1px solid #A0A0A0;}")
        version_grp.setStyleSheet("QGroupBox { color: #F7922D;}")

        snapshot_grp = QtWidgets.QGroupBox(self.tr('snapshots'))
        snapshot_grp.setAlignment(Qt.AlignCenter)
        snapshot_grp.setStyleSheet("QGroupBox { border: 1px solid #A0A0A0;}")
        snapshot_grp.setStyleSheet("QGroupBox { color: #F7922D;}")

        resource_lay = QtWidgets.QVBoxLayout()
        resource_lay.addWidget(self.resources_view)
        resource_grp.setLayout(resource_lay)

        version_lay = QtWidgets.QVBoxLayout()
        version_lay.addWidget(self.version_view)
        version_grp.setLayout(version_lay)

        snapshot_lay = QtWidgets.QVBoxLayout()
        snapshot_lay.addWidget(self.snapshots_view)
        snapshot_grp.setLayout(snapshot_lay)

        self.splitter = QSplitter(self)
        self.splitter.setHandleWidth(15)
        # main_splitter_v.setOrientation(QtCore.Qt.Vertical)
        # self.splitter.setFrameStyle('#fa8c16')
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.addWidget(resource_grp)
        self.splitter.addWidget(version_grp)
        self.splitter.addWidget(snapshot_grp)
        self.splitter.setStretchFactor(0, 17)
        self.splitter.setStretchFactor(1, 37)
        self.splitter.setStretchFactor(2, 46)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(self.splitter)
        self.setLayout(main_lay)


if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = WorkResources()
        dayu_theme.apply(test)
        test.show()

