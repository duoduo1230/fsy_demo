#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import future modules
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
# from filter_tabel_view import FilterTableView
from dayu_widgets.line_edit import MLineEdit


class MetadataFileView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MetadataFileView, self).__init__(parent)
        self.metadata_ui()

    def metadata_ui(self):
        self.metadata_model = MTableModel()
        self.metadata_sort_model = MSortFilterModel()
        self.metadata_sort_model.setSourceModel(self.metadata_model)
        self.metadata_model.set_header_list(mock.metadata_header_list)
        self.metadata_view = MTableView(size=dayu_theme.small)
        self.metadata_view.setModel(self.metadata_sort_model)

        line_edit = MLineEdit().search().tiny()
        line_edit.textChanged.connect(self.metadata_sort_model.set_search_pattern)
        line_edit.setMaximumWidth(200)

        metadata_grp = QtWidgets.QGroupBox(self.tr('Metadata'))
        metadata_grp.setAlignment(Qt.AlignCenter)
        metadata_grp.setStyleSheet("QGroupBox { border: 1px solid #A0A0A0;}")
        metadata_grp.setStyleSheet("QGroupBox { color: #F7922D;}")

        metadata_lay = QtWidgets.QVBoxLayout()
        metadata_lay.addWidget(line_edit)
        metadata_lay.addWidget(self.metadata_view)
        metadata_grp.setLayout(metadata_lay)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(metadata_grp)
        self.setLayout(main_lay)

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
