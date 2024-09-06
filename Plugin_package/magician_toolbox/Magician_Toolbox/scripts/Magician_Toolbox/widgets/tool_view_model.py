# -*- coding:utf8 -*-

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
import os
import re

# Import local modules
from Qt import QtGui, QtCore


class TreeItem(object):
    def __init__(self, name="", parent=None):
        self._parent = parent
        self._name = name
        self._children = []
        self._user_data = None

    def children(self):
        return self._children

    def child_count(self):
        return len(self._children)

    def has_children(self):
        return bool(self.children())

    def parent(self):
        return self._parent

    def name(self):
        return self._name

    def user_data(self):
        return self._user_data

    def set_user_data(self, data):
        self._user_data = data

    def set_name(self, name):
        self._name = name

    def append_child(self, child):
        self._children.append(child)
        child._parent = self

    def insert_child(self, position, child):
        if 0 <= position < self.child_count():
            self._children.insert(position, child)
            child._parent = self
            return True
        return False

    def clear_children(self):
        self._children = []

    def remove_child(self, position):
        if 0 <= position < len(self._children):
            child = self._children.pop(position)
            child._parent = None
            return True
        return False

    def child(self, row):
        if 0 <= row < self.child_count():
            return self._children[row]

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)
        return 0

    def find_child_by_name(self, name):
        for child in self._children:
            if child.name() == name:
                return child
        return None


class MyViewModel(QtCore.QAbstractItemModel):

    def __init__(self, data, parent=None):
        super(MyViewModel, self).__init__(parent)

        self.__source_data = data
        self._root_item = TreeItem()

    @property
    def source_data(self):
        return self.__source_data

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return "Test"

        return super(MyViewModel, self).headerData(section, orientation, role)

    def rowCount(self, parent=QtCore.QModelIndex()):
        node = parent.internalPointer() if parent.isValid() else self._root_item
        return node.child_count()

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 1

    def index(self, row, column, index=QtCore.QModelIndex()):
        if not self.hasIndex(row, column, index):
            return QtCore.QModelIndex()
        if not index.isValid():
            item = self._root_item
        else:
            item = index.internalPointer()

        child = item.child(row)
        if child:
            return self.createIndex(row, column, child)
        return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        item = index.internalPointer()
        if not item:
            return QtCore.QModelIndex()

        parent = item.parent()
        if parent == self._root_item:
            return QtCore.QModelIndex()
        else:
            return self.createIndex(parent.row(), 0, parent)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == QtCore.Qt.UserRole:
            return item.user_data()

        elif role == QtCore.Qt.DisplayRole:
            if item.has_children():
                return u"{} ({})".format(item.name(), item.child_count())
            else:
                return item.name()

        elif role == QtCore.Qt.DecorationRole:
            icon = item.user_data().get("icon")
            if isinstance(icon, QtGui.QIcon):
                return icon
            if not icon:
                return
            env_ls = re.findall(r"{(\w+)}", icon)
            if not env_ls:
                return
            _icon = ""
            for key in env_ls:
                v = os.environ.get(key)
                _icon = icon.replace('{%s}' % key, v) if v else ""
            if os.path.exists(_icon):
                return QtGui.QIcon(_icon)

        return

    def set_model_data(self, parent=None, data=None):
        for item in data:
            tree_item = TreeItem(item.get("label"), parent=parent)
            tree_item.set_user_data(item)
            if item.get("sub_items"):
                parent.append_child(tree_item)
                self.set_model_data(tree_item, item.get("sub_items"))
            else:
                if item.get("items"):
                    parent.append_child(tree_item)
                    self.set_model_data(tree_item, item.get("items"))
                else:
                    parent.append_child(tree_item)

    def add_child(self, index, child):
        item = index.internalPointer()
        self.beginInsertRows(index, item.child_count(), item.child_count())

        item.append_child(child)

        self.endInsertRows()

    def remove_child(self, index, child):
        item = index.internalPointer()
        children_index = item.children().index(child)

        self.beginRemoveRows(index, children_index, children_index)
        item.remove_child(children_index)
        self.endRemoveRows()

    def update_source_data(self, source_data):
        self.beginResetModel()
        self.__source_data = source_data
        self._root_item.clear_children()
        self.set_model_data(self._root_item, data=self.source_data)
        self.endResetModel()

    def get_item_form_index(self, index):
        item = index.internalPointer()
        return item


class TreeFilterProxyModel(QtCore.QSortFilterProxyModel):

    def filterAcceptsRow(self, source_row, source_parent):
        """
        重写 filterAcceptsRow方法，排除父节点进行过滤
        :return:
        """
        is_filter = self.filter_accepts_row_itself(source_row, source_parent)
        # 如果该节点允许显示，则返回True
        if is_filter:
            return True
        # 如果该节点不允许显示，则需要判断此节点下面子节点是否有满足过滤条件的，如果有，则显示该节点，返回True
        else:
            source_index = self.sourceModel().index(source_row, 0, source_parent)
            for i in range(self.sourceModel().rowCount(source_index)):
                if self.filterAcceptsRow(i, source_index):
                    return True

        return False

    def filter_accepts_row_itself(self, row_num, parent):
        return super(TreeFilterProxyModel, self).filterAcceptsRow(row_num, parent)
