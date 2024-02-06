#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets

from dayu_widgets import dayu_theme
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTableView


resources_file_header_list = [
    {
        "label": "Name",
        "key": "name",
        "width": 200,
    },
    {
        "label": "Comment",
        "key": "comment",
        "width": 100,
    },
    {
        "label": "Created By",
        "key": "created by",
        "width": 100,
    },
    {
        "label": "Created At",
        "key": "created at",
        "width": 200,
    },
]
resources_file_data_list = [
]

version_header_list = [
    {
        "label": "Name",
        "key": "name",
        "width": 200,
    },
    {
        "label": "Comment",
        "key": "comment",
        "width": 100,
    },
    {
        "label": "Created By",
        "key": "created by",
        "width": 100,
    },
    {
        "label": "Created At",
        "key": "created at",
        "width": 200,
    },
]
version_data_list = [
]


class ResourceFileView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ResourceFileView, self).__init__(parent)
        self.resources_ui()

    def resources_ui(self):
        self.cloud_file_model = MTableModel()
        self.cloud_file_sort_model = MSortFilterModel()
        self.cloud_file_sort_model.setSourceModel(self.cloud_file_model)
        self.file_veiw = MTableView(size=dayu_theme.small)
        self.file_veiw.setModel(self.cloud_file_sort_model)

        cloud_file_lay = QtWidgets.QVBoxLayout()
        cloud_file_lay.addWidget(self.file_veiw)

        self.setLayout(cloud_file_lay)

        self.set_header_data(resources_file_header_list)
        self.update_data(resources_file_data_list)

    def get_selected_item(self):
        """
        Get current select item
        :return: <>
        """
        pass

    def set_header_data(self, data):
        """
        Update header data.
        :param data: <list>
        :return:
        """
        self.cloud_file_model.set_header_list(data)
        self.file_veiw.set_header_list(data)
        self.cloud_file_sort_model.set_header_list(data)

    def update_data(self, data):
        """
        Update table view data.
        :param data: <list>
        :return:
        """
        self.cloud_file_model.set_data_list(data)


class VersionFileView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(VersionFileView, self).__init__(parent)
        self.version_ui()

    def version_ui(self):
        self.version_model = MTableModel()
        self.version_sort_model = MSortFilterModel()
        self.version_sort_model.setSourceModel(self.version_model)
        self.version_view = MTableView(size=dayu_theme.small)
        self.version_view.setModel(self.version_sort_model)

        version_lay = QtWidgets.QVBoxLayout()
        version_lay.addWidget(self.version_view)

        self.setLayout(version_lay)

        self.set_header_data(version_header_list)
        self.update_data(version_data_list)

    def get_selected_item(self):
        """
        Get current select item
        :return: <>
        """
        pass

    def set_header_data(self, data):
        """
        Update header data.
        :param data: <list>
        :return:
        """
        self.version_model.set_header_list(data)
        self.version_view.set_header_list(data)
        self.version_sort_model.set_header_list(data)

    def update_data(self, data):
        """
        Update table view data.
        :param data: <list>
        :return:
        """
        self.version_model.set_data_list(data)


class CloudFile(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CloudFile, self).__init__(parent)
        self.cloud_ui()

    def cloud_ui(self):
        resources_widget = ResourceFileView()
        version_widget = VersionFileView()

        main_lay = QtWidgets.QHBoxLayout()
        main_lay.addWidget(resources_widget)
        main_lay.addWidget(version_widget)

        self.setLayout(main_lay)


if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = CloudFile()
        dayu_theme.apply(test)
        test.show()