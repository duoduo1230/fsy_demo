#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QSplitter
from ui_center.workspace_widget import _mock_data as mock
from dayu_widgets import dayu_theme
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTableView

class CloudFileWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CloudFileWidget, self).__init__(parent)
        self.cloud_ui()

    def cloud_ui(self):
        self.resources_model = MTableModel()
        self.resources_sort_model = MSortFilterModel()
        self.resources_sort_model.setSourceModel(self.resources_model)
        self.resources_model.set_header_list(mock.resources_file_header_list)
        self.resources_view = MTableView(size=dayu_theme.small)
        self.resources_view.setModel(self.resources_sort_model)

        self.version_model = MTableModel()
        self.version_sort_model = MSortFilterModel()
        self.version_sort_model.setSourceModel(self.version_model)
        self.version_model.set_header_list(mock.version_header_list)
        self.version_view = MTableView(size=dayu_theme.small)
        self.version_view.setModel(self.version_sort_model)

        grp_style_sheet = """
            QGroupBox {color: #F7922D;}
        """
        resource_grp = QtWidgets.QGroupBox(self.tr('Resources'))
        resource_grp.setAlignment(Qt.AlignCenter)
        resource_grp.setStyleSheet(grp_style_sheet)

        version_grp = QtWidgets.QGroupBox(self.tr('Versions'))
        version_grp.setAlignment(Qt.AlignCenter)
        version_grp.setStyleSheet(grp_style_sheet)

        resource_lay = QtWidgets.QVBoxLayout()
        resource_lay.addWidget(self.resources_view)
        resource_grp.setLayout(resource_lay)

        version_lay = QtWidgets.QVBoxLayout()
        version_lay.addWidget(self.version_view)
        version_grp.setLayout(version_lay)

        splitter = QSplitter(self)
        splitter.setHandleWidth(15)
        splitter.setOrientation(Qt.Horizontal)
        splitter.addWidget(resource_grp)
        splitter.addWidget(version_grp)
        splitter.setStretchFactor(0, 50)
        splitter.setStretchFactor(1, 50)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(splitter)
        self.setLayout(main_lay)

if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = CloudFileWidget()
        dayu_theme.apply(test)
        test.show()