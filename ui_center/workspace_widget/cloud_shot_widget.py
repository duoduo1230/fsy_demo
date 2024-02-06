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

name_header_list = [
    {
        "label": "Name",
        "key": "name",
        "searchable": True,
        "width": 80,
    },
]
name_data_list = [
]


class ShotView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ShotView, self).__init__(parent)
        self.name_ui()

    def name_ui(self):
        self.name_model = MTableModel()
        self.name_sort_model = MSortFilterModel()
        self.name_sort_model.setSourceModel(self.name_model)
        self.name_view = MTableView(size=dayu_theme.small)
        self.name_view.setModel(self.name_sort_model)

        name_lay = QtWidgets.QVBoxLayout()
        name_lay.addWidget(self.name_view)

        self.setLayout(name_lay)

        self.set_header_data(name_header_list)
        self.update_data(name_data_list)

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
        self.name_model.set_header_list(data)
        self.name_view.set_header_list(data)
        self.name_sort_model.set_header_list(data)

    def update_data(self, data):
        """
        Update table view data.
        :param data: <list>
        :return:
        """
        self.name_model.set_data_list(data)


class CloudShotFile(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CloudShotFile, self).__init__(parent)
        self.cloud_ui()

    def cloud_ui(self):
        name_widget0 = ShotView()
        name_widget1 = ShotView()
        name_widget2 = ShotView()
        name_widget3 = ShotView()

        main_lay = QtWidgets.QHBoxLayout()
        main_lay.addWidget(name_widget0)
        main_lay.addWidget(name_widget1)
        main_lay.addWidget(name_widget2)
        main_lay.addWidget(name_widget3)

        self.setLayout(main_lay)


if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = CloudShotFile()
        dayu_theme.apply(test)
        test.show()