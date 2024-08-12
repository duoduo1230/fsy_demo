#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets

from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MListView
from ui_center.resource_widget.wizards.wizard import MWizardPage
from ui_center.resource_widget import _mock_data as mock


class EfxExportSetPage(MWizardPage):
    def __init__(self, parent=None):
        super(EfxExportSetPage, self).__init__(parent)
        self.setWindowTitle("EFX")
        self._init_ui()

    def _init_ui(self):
        self.button_lay = QtWidgets.QHBoxLayout()
        self.add_node_button = MPushButton("Add Selected Nodes").small()
        self.add_node_button.setMaximumWidth(200)
        self.button_lay.addStretch()
        self.button_lay.addWidget(self.add_node_button)
        self.button_lay.addStretch()

        self.houdini_node_label = MLabel("   Houdini Node:\n   [位于Obj下的节点]\n   该列表下的节点供houdini节点使用\n")
        hou_node_model = MTableModel()
        hou_model_sort = MSortFilterModel()
        hou_model_sort.setSourceModel(hou_node_model)
        hou_model_sort.set_header_list(mock.houdini_node_header_list)
        hou_tabel_view = MListView()
        hou_tabel_view.setModel(hou_model_sort)
        self.hou_lay = QtWidgets.QVBoxLayout()
        self.hou_lay.addWidget(self.houdini_node_label)
        self.hou_lay.addWidget(hou_tabel_view)

        self.cache_node_label = MLabel("   Cache Node\n   [选中 rop_alembic acb 输出节点]\n   该列表下的abc缓存供maya使用\n")
        ma_node_model = MTableModel()
        ma_model_sort = MSortFilterModel()
        ma_model_sort.setSourceModel(ma_node_model)
        ma_model_sort.set_header_list(mock.houdini_node_header_list)
        ma_tabel_view = MListView()
        ma_tabel_view.setModel(ma_model_sort)
        self.ma_lay = QtWidgets.QVBoxLayout()
        self.ma_lay.addWidget(self.cache_node_label)
        self.ma_lay.addWidget(ma_tabel_view)

        node_lay = QtWidgets.QHBoxLayout()
        node_lay.addLayout(self.hou_lay)
        node_lay.addLayout(self.ma_lay)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(self.button_lay)
        main_lay.addLayout(node_lay)

        self.setLayout(main_lay)


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = EfxExportSetPage()
        dayu_theme.apply(test)
        test.show()