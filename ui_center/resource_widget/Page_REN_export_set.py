#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.3

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtCore
from PySide2.QtCore import Qt
from Qt import QtWidgets
from dayu_widgets import dayu_theme
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.browser import MDragFolderButton
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.text_edit import MTextEdit
from wizards.wizard import MWizardPage
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTableView
from ui_center.resource_widget import _mock_data as mock
import os


class TaskTableView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TaskTableView, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.task_model = MTableModel()
        self.task_sort_model = MSortFilterModel()
        self.task_sort_model.setSourceModel(self.task_model)
        self.table_view = MTableView(size=dayu_theme.small)
        self.table_view.setModel(self.task_sort_model)

        self.search_line_edit = MLineEdit().search().tiny()
        self.search_line_edit.setFixedWidth(200)
        self.search_line_edit.textChanged.connect(self.task_sort_model.set_search_pattern)

        self.search_lay = QtWidgets.QHBoxLayout()
        # self.search_lay.addWidget(self.search_line_edit)
        self.search_lay.addStretch()

        task_view_lay = QtWidgets.QVBoxLayout()
        task_view_lay.addLayout(self.search_lay)
        task_view_lay.addWidget(self.table_view)

        self.setLayout(task_view_lay)


    def set_header_data(self, data):
        """
        Update header data.
        :param data: <list>
        :return:
        """
        self.task_model.set_header_list(data)
        self.table_view.set_header_list(data)
        self.task_sort_model.set_header_list(data)

    def update_data(self, data):
        """
        Update table view data.
        :param data: <list>
        :return:
        """
        self.task_model.set_data_list(data)


class GetSequenceFolderPage(MWizardPage):
    def __init__(self, parent=None):
        super(GetSequenceFolderPage, self).__init__(parent)
        self.setWindowTitle("Upload File")
        # self.setFixedSize(800, 600)
        self._init_ui()
        self.bind_function()

    def _init_ui(self):

        self.upload_folder_button = MDragFolderButton()
        self.upload_folder_button.setMaximumHeight(250)
        self.folder_path_label = MLabel()
        self.folder_path_label.set_elide_mode(QtCore.Qt.ElideRight)

        self.folder_lay = QtWidgets.QVBoxLayout()
        self.folder_lay.addWidget(self.upload_folder_button)
        # self.folder_lay.addWidget(self.folder_path_label)

        self.task_model = TaskTableView()
        self.search_line_edit = MLineEdit().search().small()
        self.search_line_edit.setFixedWidth(200)

        self.error_lay = QtWidgets.QHBoxLayout()
        self.error_label = MLineEdit().small()
        self.show_detail_button = MPushButton("Show Detail").small()
        self.error_lay.addWidget(self.error_label)
        self.error_lay.addWidget(self.show_detail_button)

        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setLabelAlignment(Qt.AlignRight)
        self.form_layout.addRow(MLabel('Folder:').h4(), self.folder_lay)
        self.form_layout.addRow(MLabel('Result Layers:').h4(), self.task_model)
        self.form_layout.addRow(MLabel('Error Info:').h4(), self.error_lay)

        self.setLayout(self.form_layout)

        self.detail_text = MTextEdit(self)
        self.detail_dock_widget = QtWidgets.QDockWidget(self)
        self.detail_dock_widget.setFeatures(
            QtWidgets.QDockWidget.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetClosable)
        self.detail_dock_widget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.detail_dock_widget.setWidget(self.detail_text)
        self.detail_dock_widget.setFloating(True)
        self.detail_dock_widget.setVisible(False)

    def bind_function(self):
        self.upload_folder_button.sig_folder_changed.connect(self.folder_path_label.setText)
        self.upload_folder_button.sig_folder_changed.connect(self.get_file_info)
        self.search_line_edit.textChanged.connect(self.task_model.task_sort_model.set_search_pattern)
        self.show_detail_button.clicked.connect(self.show_detail)

    def get_file_info(self):
        """
        这里目前以阿诺德输出的文件为例
        "...\arnold\crypto_asset\ep15_3020_ren_prp_prp_arnold_crypto_asset_v0001.1001.exr"
        """
        input_path = self.folder_path_label.text()
        render_type = input_path.split("/")[-1]
        file_info_list = []
        for root, dirs, files in os.walk(input_path):
            _dict = {}
            if root == input_path:
                continue
            _dict["folder"] = root
            if files:
                first_frame = files[0]
                last_frame = files[-1]
                first_frame_name = first_frame.split(".")[0]
                frame_num = first_frame.split(".")[1]
                last_num = last_frame.split(".")[1]
                file_name = first_frame.replace(frame_num, '%04d')

                task_total = "_{type}_".format(type=render_type)
                _type = first_frame_name.split(task_total)[1]
                layer = _type.split("_")[0]
                _pass = _type.replace(layer + "_", '')

                _dict["file name"] = file_name
                _dict["engine"] = render_type
                _dict["layer"] = layer
                _dict["pass"] = _pass
                _dict["frame range"] = "_".join([frame_num, last_num])
                _dict["frame count"] = len(files)

                file_info_list.append(_dict)

        self.task_model.set_header_data(mock.render_resource_header_list)
        self.task_model.update_data(file_info_list)

    def show_detail(self):
        if self.detail_dock_widget.isVisible():
            self.detail_dock_widget.hide()
        else:
            self.detail_dock_widget.show()


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = GetSequenceFolderPage()
        dayu_theme.apply(test)
        test.show()





