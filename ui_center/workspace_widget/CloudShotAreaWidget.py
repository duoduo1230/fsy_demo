#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QSplitter
from dayu_widgets import dayu_theme
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTableView
from ui_center.workspace_widget import _mock_data as mock


class CloudShotView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(CloudShotView, self).__init__(parent)
        self.name_ui()

    def name_ui(self):
        self.metadata_model = MTableModel()
        self.metadata_sort_model = MSortFilterModel()
        self.metadata_sort_model.setSourceModel(self.metadata_model)
        self.metadata_model.set_header_list(mock.name_header_list)
        self.metadata_view = MTableView(size=dayu_theme.small)
        self.metadata_view.setModel(self.metadata_sort_model)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(self.metadata_view)
        self.setLayout(main_lay)


class CloudShotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CloudShotWidget, self).__init__(parent)
        self.cloud_ui()

    def cloud_ui(self):
        name_widget0 = CloudShotView()
        name_widget1 = CloudShotView()
        name_widget2 = CloudShotView()
        name_widget3 = CloudShotView()

        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.addWidget(name_widget0)
        self.splitter.addWidget(name_widget1)
        self.splitter.addWidget(name_widget2)
        self.splitter.addWidget(name_widget3)
        self.splitter.setStretchFactor(0, 25)
        self.splitter.setStretchFactor(1, 25)
        self.splitter.setStretchFactor(2, 25)
        self.splitter.setStretchFactor(3, 25)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget( self.splitter)
        self.setLayout(main_lay)

if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = CloudShotWidget()
        dayu_theme.apply(test)
        test.show()