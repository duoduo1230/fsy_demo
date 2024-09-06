# -*- coding:utf8 -*-
# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
import os
import sys
from functools import partial
if sys.version_info.major>2:
    from importlib import reload

# Import third-party modules
from Qt import QtWidgets, QtCore, QtGui
from dayu_widgets import item_view
from dayu_widgets.item_view import MTreeView
from dayu_widgets.menu import MMenu
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets import dayu_theme
from dayu_widgets.message import MMessage
from dayu_widgets.toast import MToast
from Magician_Toolbox.widgets import tool_view_model
from Magician_Toolbox.widgets import tool_delegate

reload(tool_view_model)
reload(tool_delegate)
from Magician_Toolbox.widgets.tool_view_model import MyViewModel, TreeFilterProxyModel, TreeItem


class MyMenu(MMenu):

    def __init__(self, parent=None):
        super(MyMenu, self).__init__()
        self._parent = parent

    def add_default_action(self):
        pass


class MySplitter(QtWidgets.QSplitter):
    def __init__(self, Orientation=QtCore.Qt.Horizontal, parent=None):
        super(MySplitter, self).__init__(Orientation, parent=parent)
        self.setHandleWidth(10)
        self.animatable = False
        self.default_size = 100
        self.anim_move_duration = 300
        dayu_theme.apply(self)

    def slot_splitter_click(self, index, first=True):
        size_list = self.sizes()
        prev = index - 1
        prev_size = size_list[prev]
        next_size = size_list[index]
        default_size = self.default_size
        if not prev_size:
            size_list[prev] = default_size
            size_list[index] -= default_size
        elif not next_size:
            size_list[index] = default_size
            size_list[prev] -= default_size
        else:

            if first:
                size_list[index] += prev_size
                size_list[prev] = 0
            else:
                size_list[prev] += next_size
                size_list[index] = 0

        if self.animatable:
            anim = QtCore.QVariantAnimation(self)

            def anim_size(index, size_list, v):
                size_list[index - 1] += size_list[index] - v
                size_list[index] = v
                self.setSizes(size_list)

            anim.valueChanged.connect(partial(anim_size, index, size_list))
            anim.setDuration(self.anim_move_duration)
            anim.setStartValue(next_size)
            anim.setEndValue(size_list[index])
            anim.start()
        else:
            self.setSizes(size_list)

    def createHandle(self):
        count = self.count()

        orient = self.orientation()
        is_horizontal = orient is QtCore.Qt.Horizontal
        handle = QtWidgets.QSplitterHandle(orient, self)

        # NOTES: double click average size
        handle.mouseDoubleClickEvent = lambda e: self.setSizes(
            [1 for i in range(self.count())]
        )

        layout = QtWidgets.QVBoxLayout() if is_horizontal else QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        handle.setLayout(layout)

        button = QtWidgets.QToolButton(handle)
        button.setArrowType(QtCore.Qt.LeftArrow if is_horizontal else QtCore.Qt.UpArrow)
        button.clicked.connect(lambda: self.slot_splitter_click(count, True))
        layout.addWidget(button)
        button = QtWidgets.QToolButton(handle)
        arrow = QtCore.Qt.RightArrow if is_horizontal else QtCore.Qt.DownArrow
        button.setArrowType(arrow)
        button.clicked.connect(lambda: self.slot_splitter_click(count, False))
        layout.addWidget(button)

        return handle


class MyTextEdit(MTextEdit):

    def __init__(self, parent=None):
        super(MyTextEdit, self).__init__(parent)

    def paintEvent(self, event):
        if not self.toPlainText():
            item_view.draw_empty_content(self.viewport(), "No Data")

        return super(MyTextEdit, self).paintEvent(event)


class MyTreeView(MTreeView):
    emitData = QtCore.Signal(object)
    emitText = QtCore.Signal(str)
    emitError = QtCore.Signal(str)
    left_clicked = QtCore.Signal()
    double_clicked = QtCore.Signal()

    def __init__(self, settings=None, show_menu=False, parent=None):
        super(MyTreeView, self).__init__(parent)
        self.__source_data = dict()
        self._parent = parent
        self.setting = settings

        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.timeout)

        self.is_double = False
        self.is_left_click = True

        self.setObjectName("MyTreeView")
        # self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.customContextMenuRequested.connect(self.create_menu)

        self.set_ui()
        self.bind_func()
        self.set_delegate()

    def create_menu(self, position):
        index = self.indexAt(position)
        self.setCurrentIndex(index)
        self._parent.create_menu(position)

    def set_ui(self):
        self.setSortingEnabled(False)
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # Set model
        self.source_model = MyViewModel(self.__source_data)
        self.proxy_model = TreeFilterProxyModel()
        self.proxy_model.setSourceModel(self.source_model)
        self.setModel(self.proxy_model)

    def bind_func(self):
        """ Bind function """
        self.doubleClicked.connect(self._emit_item_data)
        self.clicked.connect(self._emit_description)

    def set_delegate(self):
        """
        创建并设置delegate
        """
        delegate = tool_delegate.HelpDelegate(self)
        self.setItemDelegateForColumn(0, delegate)

    def resizeEvent(self, event):
        # 重置第一列的宽度
        if self.verticalScrollBar().isVisible():
            width = event.size().width() - self.verticalScrollBar().width() - 3
        else:
            width = event.size().width() - 10
        self.setColumnWidth(0, width)

        super(MyTreeView, self).resizeEvent(event)

    def mousePressEvent(self, event):
        if not self.timer.isActive():
            self.timer.start()
        self.is_left_click = False
        if event.button() == QtCore.Qt.LeftButton:
            self.is_left_click = True

        super(MyTreeView, self).mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.is_double = True
        super(MyTreeView, self).mouseDoubleClickEvent(event)

    def timeout(self):
        if self.is_double:
            self.double_clicked.emit()
        else:
            if self.is_left_click:
                self.left_clicked.emit()

        self.is_double = False

    @property
    def source_data(self):
        return self.__source_data

    def root_index(self, row, column=0):
        return self.source_model.index(row, column)

    @staticmethod
    def favorite_root_label():
        """ 个人收藏夹的root节点数据 """
        favorite_data = {
            "label": u"个人收藏夹",
            "type": "menu",
            "description": u"收藏的工具集合，方便个人习惯使用",
            "icon": "{Magician_Toolbox}/icons/favorite.png",
            "items": list()
        }
        return favorite_data

    def favorite_root(self):
        root = self.root_index(0).internalPointer()
        return root

    def is_favorite_item(self, index):
        item = self.proxy_model.data(index, QtCore.Qt.UserRole)
        return [i for i in self.favorite_root().children() if item["label"] == i.name()]

    def update_data(self, data):
        """
        更新 data
        :param data: [dict]
        """
        # 更新model的数据
        self.__source_data = data
        self.source_model.update_source_data(data)

        # 插入个人收藏节点
        if data[0]["label"] != u"个人收藏夹":
            favorite_data = self.favorite_root_label()
            data.insert(0, favorite_data)
            # 添加个人收藏的data
            self.source_model.update_source_data(data)
            # 更新个人收藏的ui
            self.restore_personal_data()

    def add_favorite_data(self, index):
        """
        添加个人收藏夹的数据
        Args:
            index: QtCore.QModelIndex
        """
        user_data = self.proxy_model.data(index, QtCore.Qt.UserRole)
        icon_data = self.proxy_model.data(index, QtCore.Qt.DecorationRole)
        item_data = user_data.copy()
        item_data.update({"icon": icon_data})

        favorite_root = self.favorite_root()
        if favorite_root.find_child_by_name(user_data.get("label")):
            return

        favorite_root_index = self.root_index(0)
        child_item = TreeItem(item_data.get("label"))
        child_item.set_user_data(item_data)
        self.source_model.add_child(favorite_root_index, child_item)

        self.cache_personal_data()

    def remove_favorite_data(self, index):
        favorite_root_index = self.root_index(0)
        item_label = self.proxy_model.data(index, QtCore.Qt.UserRole).get("label")

        for child_item in self.favorite_root().children():
            if item_label == child_item.name():
                self.source_model.remove_child(favorite_root_index, child_item)

        self.cache_personal_data()

    def open_help(self, index):
        """
        打开帮助文档
        :param index: <QtCore.QModelIndex>
        """
        data = self.proxy_model.data(index, QtCore.Qt.UserRole)
        page = data.get("help")
        if page:
            import webbrowser
            webbrowser.open(page)
            box = MMessage.info(parent=self, text=u"文档已打开")
            box._content_label.h4()
            box.resize(180, 60)
        else:
            box = MMessage.warning(parent=self, text=u"该工具没有帮助文档", duration=3)
            box._content_label.h4()
            box.resize(250, 60)

    def set_filter_key(self, column=0):
        """
        设置根据某一列的内容，进行过滤
        """
        self.proxy_model.setFilterKeyColumn(column)

    def update_search(self, text):
        """
        根据文本更新显示内容
        :param text: [str]
        """
        self.proxy_model.setFilterFixedString(text)
        if text:
            self.expandAll()
        else:
            self.restore_state()

    def current_item_data(self):
        """
        获取当前选中节点的 user data
        :return: dict
        """
        return self.proxy_model.data(self.currentIndex(), QtCore.Qt.UserRole)

    def _emit_item_data(self, index):
        """
        获取当前选中项的user data，并发送信号
        :param index: [QtCore.QModelIndex]
        """
        self.emitData.emit(self.current_item_data())

    def _emit_description(self, index):
        """
        获取当前选中项的user data，并发送信号
        :param index: [QtCore.QModelIndex]
        """
        self.setCurrentIndex(index)
        data = self.current_item_data()
        self.emitText.emit(data.get("description"))

    def save_state(self):
        """记录节点的展开状态"""
        result = []
        for index in self.proxy_model.persistentIndexList():
            if self.isExpanded(index):
                result.append(index.data(QtCore.Qt.DisplayRole))

        settings = QtCore.QSettings(self.setting, QtCore.QSettings.IniFormat)
        settings.beginGroup(self._parent.project_data.get("name"))
        settings.setValue("ExpandedItems", result)
        settings.endGroup()

    def restore_state(self):
        """复原节点的展开状态"""
        try:
            if not os.path.exists(self.setting):
                return
            settings = QtCore.QSettings(self.setting, QtCore.QSettings.IniFormat)
            settings.beginGroup(self._parent.project_data.get("name"))
            result = settings.value("ExpandedItems", [])
            settings.endGroup()

            if not result:
                return

            for item in result:
                index_list = self.proxy_model.match(self.proxy_model.index(0, 0), QtCore.Qt.DisplayRole, item, hits=2)
                if not index_list:
                    continue
                for index in index_list:
                    self.setExpanded(index, True)
        except:
            pass

    def cache_personal_data(self):
        """记录个人收藏夹的内容"""
        favorite_items = self.favorite_root().children()
        if not favorite_items:
            labels = []
        else:
            labels = [item.user_data().get("label") for item in favorite_items]
        settings = QtCore.QSettings(self.setting, QtCore.QSettings.IniFormat)
        settings.beginGroup(self._parent.project_data.get("name"))
        settings.setValue("FavoriteItems", labels)
        settings.endGroup()

    def restore_personal_data(self):
        """复原个人收藏夹的内容"""
        settings = QtCore.QSettings(self.setting, QtCore.QSettings.IniFormat)
        settings.beginGroup(self._parent.project_data.get("name"))
        labels = settings.value("FavoriteItems", [])
        settings.endGroup()

        if not labels:
            return

        if not isinstance(labels, list):
            labels = [labels]
        for label in labels:
            index_list = self.proxy_model.match(self.proxy_model.index(1, 0), QtCore.Qt.DisplayRole, label, hits=-1,
                                                flags=QtCore.Qt.MatchRecursive)  # Searches the entire hierarchy.
            for index in index_list:
                self.add_favorite_data(index)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    window = MyTreeView()
    window.show()
    sys.exit(app.exec_())
