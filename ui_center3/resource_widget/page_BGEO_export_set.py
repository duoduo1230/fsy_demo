#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets

from dayu_widgets import dayu_theme
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MListView
from ui_center3.resource_widget.wizards.wizard import MWizardPage
from ui_center3.resource_widget import _mock_data as mock


class BgeoExportSetPage(MWizardPage):
    def __init__(self, parent=None):
        super(BgeoExportSetPage, self).__init__(parent)
        self.setWindowTitle("EFX")
        self._init_ui()

    def _init_ui(self):

        self.node_label = MLabel("Support node type [file filecache geometry rop_geometry]")
        self.add_node_button = MPushButton("Add Selected Nodes").small()
        self.add_node_button.setMaximumWidth(200)

        node_lay = QtWidgets.QHBoxLayout()
        node_lay.addWidget(self.node_label)
        node_lay.addWidget(self.add_node_button)

        hou_node_model = MTableModel()
        hou_model_sort = MSortFilterModel()
        hou_model_sort.setSourceModel(hou_node_model)
        hou_model_sort.set_header_list(mock.houdini_node_header_list)
        hou_tabel_view = MListView()
        hou_tabel_view.setModel(hou_model_sort)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(node_lay)
        main_lay.addWidget(hou_tabel_view)

        self.setLayout(main_lay)


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = BgeoExportSetPage()
        dayu_theme.apply(test)
        test.show()