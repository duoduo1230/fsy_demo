#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets, QtCore, QtGui
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTreeView
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.push_button import MPushButton
from dayu_widgets.label import MLabel
import get_read_node_info as mock
import importlib
importlib.reload(mock)


class DataTreeView(QtWidgets.QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(DataTreeView, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.data_model = MTableModel()
        self.data_tree_view = MTreeView()
        self.data_model_sort = MSortFilterModel()
        self.data_tree_view.setModel(self.data_model_sort)
        self.data_model_sort.setSourceModel(self.data_model)

        line_edit = MLineEdit().search().small()
        line_edit.textChanged.connect(self.data_model_sort.set_search_pattern)

        expand_all_button = MPushButton("Expand All").small()
        expand_all_button.clicked.connect(self.data_tree_view.expandAll)
        collapse_all_button = MPushButton("Collapse All").small()
        collapse_all_button.clicked.connect(self.data_tree_view.collapseAll)
        button_lay = QtWidgets.QHBoxLayout()
        button_lay.addWidget(expand_all_button)
        button_lay.addWidget(collapse_all_button)
        button_lay.addWidget(line_edit)
        button_lay.addStretch()

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(button_lay)
        main_lay.addWidget(self.data_tree_view)
        self.setLayout(main_lay)
        
    def set_header_data(self, data):
        self.data_model.set_header_list(data)
        self.data_model_sort.set_header_list(data)
        self.data_tree_view.set_header_list(data)

    def update_data(self, data):
        self.data_model.set_data_list(data)


class UpdateManager(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(UpdateManager, self).__init__(parent)
        self.setWindowTitle(self.tr('Updata Manager'))
        self.resize(1000, 600)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self._init_ui()
        self.bind_function()

    def _init_ui(self):
        title_label = QtWidgets.QLabel('Updata Manager')
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 36px;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_lay = QtWidgets.QHBoxLayout()
        title_lay.addStretch()
        title_lay.addWidget(title_label)
        title_lay.addStretch()

        self.parse_sel_bnt = MPushButton("Parse Selection").small()
        self.parse_all_bnt = MPushButton("Parse All").small()

        parse_btn_lay = QtWidgets.QHBoxLayout()
        parse_btn_lay.addWidget(self.parse_sel_bnt)
        parse_btn_lay.addWidget(self.parse_all_bnt)

        self.data_tree_widget = DataTreeView()

        error_label = MLabel('New version')
        error_label.setStyleSheet("background-color: #FF2727; color: black;")
        warning_label = MLabel("Has new version  but not in project")
        warning_label.setStyleSheet("background-color: #FFB14B; color: black;")
        success_label = MLabel("New version exists")
        success_label.setStyleSheet("background-color: #53FF4B; color: black;")
        self.update_btn = MPushButton("Update").small()

        tips_lay = QtWidgets.QHBoxLayout()
        tips_lay.addWidget(error_label)
        tips_lay.addWidget(warning_label)
        tips_lay.addWidget(success_label)
        tips_lay.addStretch()
        tips_lay.addWidget(self.update_btn)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(title_label)
        main_lay.addLayout(parse_btn_lay)
        main_lay.addWidget(self.data_tree_widget)
        main_lay.addLayout(tips_lay)

        self.setLayout(main_lay)

    def bind_function(self):
        self.update_btn.clicked.connect(self.update_read_node_file)

    def update_read_node_file(self):
        """
        更新read_node节点的file信息
        更新ui内容
        """
        import nuke
        item_model_view_info = self.data_tree_widget.data_model.get_data_list()
        for item in item_model_view_info:
            if item.get('node_name_checked') == 2:
                read_node = item.get("node_name")
                file_path = item.get('file_path')
                latest_version = mock.check_latest_version_exists(file_path)
                pro_read_node = nuke.toNode(read_node)
                if item['file_name'].split('/')[-1].split('_v')[0] in latest_version:
                    pro_read_node['file'].setValue(latest_version)

        update_version = mock.get_view_data()
        self.data_tree_widget.update_data(update_version)


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = UpdateManager()
        test.data_tree_widget.set_header_data(mock.header_list)
        tree_data_list = mock.get_view_data()
        test.data_tree_widget.update_data(tree_data_list)
        dayu_theme.apply(test)
        test.show()
