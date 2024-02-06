#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets
from ui_center.workspace_widget.example import _mock_data as mock
from dayu_widgets import dayu_theme
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTableView


class MetadataFileView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MetadataFileView, self).__init__(parent)
        self.version_ui()

    def version_ui(self):
        self.metadata_widget = MTableModel()
        self.metadata_widget_sort = MSortFilterModel()
        self.metadata_widget_sort.setSourceModel(self.metadata_widget)
        self.metadata_table_child = MTableView(size=dayu_theme.small)
        self.metadata_table_child.setModel(self.metadata_widget_sort)

        metadata_lay = QtWidgets.QVBoxLayout()
        metadata_lay.addWidget(self.metadata_table_child)

        self.setLayout(metadata_lay)

        self.set_header_data(mock.metadata_header_list)
        self.update_data(mock.metadata_data_list)

    def set_header_data(self, data):
        """
        Update header data.
        :param data: <list>
        :return:
        """
        self.metadata_widget.set_header_list(data)
        self.metadata_table_child.set_header_list(data)
        self.metadata_widget_sort.set_header_list(data)

    def update_data(self, data):
        """
        Update table view data.
        :param data: <list>
        :return:
        """
        self.metadata_widget.set_data_list(data)


if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = MetadataFileView()
        dayu_theme.apply(test)
        test.show()
