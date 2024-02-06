#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2019.2
# Email : muyanru345@163.com
###################################################################

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import third-party modules
from Qt import QtWidgets

# Import local modules
from dayu_widgets import dayu_theme
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTreeView
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.push_button import MPushButton
import _mock_data as mock
from collections import Counter


class FilterViewExample(QtWidgets.QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(FilterViewExample, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.filter_model = MTableModel()
        self.filter_model_sort = MSortFilterModel()
        self.filter_model_sort.setSourceModel(self.filter_model)
        self.tree_view = MTreeView()
        self.tree_view.setModel(self.filter_model_sort)

        line_edit = MLineEdit().search().small()
        line_edit.textChanged.connect(self.filter_model_sort.set_search_pattern)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(self.tree_view)
        main_lay.addStretch()

        self.setLayout(main_lay)

    def set_header_data(self, data):
        """








        
        Update header data.
        :param data: <list>
        :return:
        """
        self.filter_model.set_header_list(data)
        self.tree_view.set_header_list(data)
        self.filter_model_sort.set_header_list(data)

    def update_data(self, data):
        """
        Update table view data.
        :param data: <list>
        :return:
        """
        self.filter_model.set_data_list(data)


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = FilterViewExample()
        dayu_theme.apply(test)
        test.show()