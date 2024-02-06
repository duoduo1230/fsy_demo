# -*- coding:utf-8 -*-

from dayu_widgets.qt import QtWidgets, QtCore
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.push_button import MPushButton

import sys


class AddFileItem(QtWidgets.QWidget):

    def __init__(self, text, parent=None):
        super(AddFileItem, self).__init__(parent)

        self.text = text
        self._parent = parent

        self.setObjectName("AddFileItem")

        self.init_ui()
        self.bind_function()

    def init_ui(self):
        self.del_btn = MPushButton("-").small()
        self.path_edit = MLineEdit(self.text)

        main_lay = QtWidgets.QHBoxLayout(self)
        main_lay.addWidget(self.del_btn)
        main_lay.addWidget(self.path_edit)

    def bind_function(self):
        self.del_btn.clicked.connect(self.remove_self)

    def remove_self(self):
        self._parent.remove_folder(self.text)
        self.deleteLater()
        self.setParent(None)


class FileWidget(QtWidgets.QWidget):

    # 定义has_file信号，用来发送当前窗口是否有文件的信息
    has_file = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super(FileWidget, self).__init__(parent)

        self.folder_list = []
        self._patent = parent

        self.setObjectName("FileWidget")

        self.init_ui()

    def init_ui(self):
        self.main_lay = QtWidgets.QVBoxLayout(self)

    def add_folder(self, folder):
        if folder in self.folder_list:
            return

        self.folder_list.append(folder)

        self.add_item(folder)

    def add_item(self, folder):
        file_item = AddFileItem(folder, self)
        self.main_lay.addWidget(file_item)

        # 发射信号
        self.has_file.emit(len(self.folder_list))

    def get_items(self):
        return self.main_lay.children()

    def remove_folder(self, folder):
        self.folder_list.remove(folder)

        # 重置父窗口大小
        self._patent.adjustSize()

        # 发射信号
        self.has_file.emit(len(self.folder_list))

