#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2018.8
# Email : muyanru345@163.com
###################################################################


from functools import partial
import ui_utils
from ui_center.qt import *
import collections

class MOptionMenu(QMenu):
    sig_finish_edit = Signal()

    def __init__(self, exclusive=False, parent=None):
        super(MOptionMenu, self).__init__(parent)
        self.selected_data = None
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.action_group = QActionGroup(self)
        self.action_group.setExclusive(exclusive)
        self.action_group.triggered.connect(self.slot_on_action_triggered)

    def set_current(self, data):
        self.selected_data = data
        data_list = data if isinstance(data, list) else [data]
        for act in self.action_group.actions():
            act.setChecked(act.data() in data_list)

    def setup_data(self, option_list):
        self.clear()
        for act in self.action_group.actions():
            self.action_group.removeAction(act)

        if not option_list:
            return
        for value in option_list:
            action = self.action_group.addAction(ui_utils.default_formatter(value))
            action.setData(value)
            action.setCheckable(True)
        self.addActions(self.action_group.actions())

    def get_data(self):
        return self.selected_data

    @Slot(QAction)
    def slot_on_action_triggered(self, action):
        if self.action_group.isExclusive():
            self.selected_data = next(act.data() for act in self.action_group.actions() if act.isChecked())
        else:
            self.selected_data = [act.data() for act in self.action_group.actions() if act.isChecked()]
        self.sig_finish_edit.emit()


class MOptionDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(MOptionDelegate, self).__init__(parent)
        self.editor = None
        self.showed = False
        self.exclusive = True
        self.parent_widget = None
        self.arrow_space = 20
        self.arrow_height = 6

    def set_exclusive(self, flag):
        self.exclusive = flag

    def createEditor(self, parent, option, index):
        self.parent_widget = parent
        self.editor = MOptionMenu(exclusive=self.exclusive, parent=parent)
        self.editor.setup_data(index.data(Qt.UserRole))
        self.editor.sig_finish_edit.connect(self.finish_edit)
        return self.editor

    def setEditorData(self, editor, index):
        editor.set_current(index.data(Qt.EditRole))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.get_data())

    def updateEditorGeometry(self, editor, option, index):
        editor.move(self.parent_widget.mapToGlobal(QPoint(option.rect.x(), option.rect.y() + option.rect.height())))

    def paint(self, painter, option, index):
        super(MOptionDelegate, self).paint(painter, option, index)
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(Qt.white))

        h = option.rect.height()
        polygon = QPolygonF(
            [QPointF(option.rect.x() + option.rect.width() - self.arrow_space / 2 - self.arrow_height / 2,
                     option.rect.y() + h / 2 - self.arrow_height / 2),
             QPointF(option.rect.x() + option.rect.width() - self.arrow_space / 2 + self.arrow_height / 2,
                     option.rect.y() + h / 2 - self.arrow_height / 2),
             QPointF(option.rect.x() + option.rect.width() - self.arrow_space / 2,
                     option.rect.y() + h / 2 + self.arrow_height / 2)])
        painter.drawPolygon(polygon)
        painter.restore()

    def finish_edit(self):
        self.commitData.emit(self.editor)

    def sizeHint(self, option, index):
        orig = super(MOptionDelegate, self).sizeHint(option, index)
        return QSize(orig.width() + self.arrow_space, orig.height())


class MVerticalCheckBoxHeaderView(QHeaderView):
    sig_check_state_changed = Signal()

    def __init__(self, parent=None):
        super(MVerticalCheckBoxHeaderView, self).__init__(Qt.Vertical, parent)

    def paintSection(self, painter, rect, logical_index):
        option = QStyleOptionButton()
        if ui_utils.get_obj_value(self.model().logical_index.internalPointer(), 'checked'):
            option.state = QStyle.State_On
        else:
            option.state = QStyle.State_Off
        check_box_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, option)
        start_point = QPoint(rect.x() + rect.width() / 2 - check_box_rect.width() / 2,
                             rect.y() + rect.height() / 2 - check_box_rect.height() / 2)
        option.rect = QRect(start_point, check_box_rect.size())
        return QApplication.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 修改数据
            index = self.logicalIndexAt(event.pos().x())
            data_obj = index.internalPointer()
            ui_utils.set_obj_value(data_obj, 'checked', not ui_utils.get_obj_value(data_obj, 'checked'))
            self.updateSection(index)
            self.sig_check_state_changed.emit()
        QHeaderView.mousePressEvent(self, event)


class MHeaderView(QHeaderView):
    def __init__(self, orientation, parent=None):
        super(MHeaderView, self).__init__(orientation, parent)
        self.setMovable(True)
        self.setClickable(True)
        self.setSortIndicatorShown(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.slot_context_menu)
        self.setDefaultAlignment(Qt.AlignLeft)

    @Slot(QPoint)
    def slot_context_menu(self, point):
        context_menu = QMenu(self)
        logical_column = self.logicalIndexAt(point)
        if logical_column >= 0 and self.model().header_list[logical_column].get('checkable', False):
            action_select_all = context_menu.addAction(self.tr('Select All'))
            action_select_none = context_menu.addAction(self.tr('Select None'))
            action_select_invert = context_menu.addAction(self.tr('Select Invert'))
            self.connect(action_select_all, SIGNAL('triggered()'),
                         partial(self.slot_set_select, logical_column, Qt.Checked))
            self.connect(action_select_none, SIGNAL('triggered()'),
                         partial(self.slot_set_select, logical_column, Qt.Unchecked))
            self.connect(action_select_invert, SIGNAL('triggered()'),
                         partial(self.slot_set_select, logical_column, None))
            context_menu.addSeparator()

        fit_action = context_menu.addAction(self.tr('fit_size'))
        fit_action.setCheckable(True)
        fit_action.setChecked(True if self.resizeMode(0) == QHeaderView.ResizeToContents else False)
        fit_action.toggled.connect(self.slot_set_resize_mode)
        for column in range(self.count()):
            action = context_menu.addAction(self.model().headerData(column, Qt.Horizontal, Qt.DisplayRole))
            action.setCheckable(True)
            action.setChecked(not self.isSectionHidden(column))
            action.toggled.connect(partial(self.slot_set_section_visible, column))
        context_menu.exec_(QCursor.pos() + QPoint(10, 10))

    @Slot(int, int)
    def slot_set_select(self, column, state):
        model = self.model()
        model.beginResetModel()
        attr = '{}_checked'.format(model.header_list[column].get('attr'))
        for row in range(model.rowCount()):
            real_index = model.mapToSource(model.index(row, column))
            data_obj = real_index.internalPointer()
            if state is None:
                old_state = ui_utils.get_obj_value(data_obj, attr)
                ui_utils.set_obj_value(data_obj, attr, Qt.Unchecked if old_state == Qt.Checked else Qt.Checked)
            else:
                ui_utils.set_obj_value(data_obj, attr, state)
        model.endResetModel()
        model.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), None, None)

    @Slot(QModelIndex, int)
    def slot_set_section_visible(self, index, flag):
        self.setSectionHidden(index, not flag)

    @Slot(bool)
    def slot_set_resize_mode(self, flag):
        if flag:
            self.resizeSections(QHeaderView.ResizeToContents)
        else:
            self.resizeSections(QHeaderView.Interactive)

    def setClickable(self, flag):
        try:
            QHeaderView.setSectionsClickable(self, flag)
        except AttributeError:
            QHeaderView.setClickable(self, flag)

    def setMovable(self, flag):
        try:
            QHeaderView.setSectionsMovable(self, flag)
        except AttributeError:
            QHeaderView.setMovable(self, flag)

    def resizeMode(self, index):
        try:
            QHeaderView.sectionResizeMode(self, index)
        except AttributeError:
            QHeaderView.resizeMode(self, index)

    def setResizeMode(self, mode):
        try:
            QHeaderView.setResizeMode(self, mode)
        except AttributeError:
            QHeaderView.setSectionResizeMode(self, mode)


def set_header_list(self, header_list):
    self.header_list = header_list
    if self.header_view:
        self.header_view.setSortIndicator(-1, Qt.AscendingOrder)
        for index, i in enumerate(header_list):
            self.header_view.setSectionHidden(index, i.get('hide', False))
            self.header_view.resizeSection(index, i.get('width', 100))
            if i.get('order', None) is not None:
                self.header_view.setSortIndicator(index, i.get('order'))
            if i.get('selectable', False):
                delegate = MOptionDelegate(parent=self)
                delegate.set_exclusive(i.get('exclusive', True))
                self.setItemDelegateForColumn(index, delegate)
            elif self.itemDelegateForColumn(index):
                self.setItemDelegateForColumn(index, None)


def enable_context_menu(self, enable):
    if enable:
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.slot_context_menu)
    else:
        self.setContextMenuPolicy(Qt.NoContextMenu)


@Slot(QPoint)
def slot_context_menu(self, point):
    proxy_index = self.indexAt(point)
    if proxy_index.isValid():
        need_map = isinstance(self.model(), QSortFilterProxyModel)
        selection = []
        for index in self.selectionModel().selectedRows() or self.selectionModel().selectedIndexes():
            data_obj = self.model().mapToSource(index).internalPointer() if need_map else index.internalPointer()
            selection.append(data_obj)
        event = ui_utils.MenuEvent(view=self, selection=selection, extra={})
        self.sig_context_menu.emit(event)
    else:
        event = ui_utils.MenuEvent(view=self, selection=[], extra={})
        self.sig_context_menu.emit(event)

def copy_item_view_data(self):
    select_model = self.selectionModel()
    result = collections.defaultdict(dict)
    for index in select_model.selectedIndexes():
        result[index.row()].update({index.column(): self.model().data(index, Qt.DisplayRole)})
    clip_text = u'\n'.join([u'\t'.join(map(lambda x:u'"{}"'.format(x), result[key].values()))
                            for key in sorted(result.keys())])
    QApplication.clipboard().setText(clip_text)


class MTableView(QTableView):
    set_header_list = set_header_list
    enable_context_menu = enable_context_menu
    slot_context_menu = slot_context_menu
    sig_context_menu = Signal(object)
    sig_link_clicked = Signal(object)

    def __init__(self, parent=None):
        super(MTableView, self).__init__(parent)
        self.header_list = []
        self.header_view = MHeaderView(Qt.Horizontal)
        self.verticalHeader().hide()
        self.setHorizontalHeader(self.header_view)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.setMouseTracking(True)

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            copy_item_view_data(self)
            event.accept()
        else:
            return super(MTableView, self).keyPressEvent(event)

    # def mouseMoveEvent(self, event):
    #     index = self.indexAt(event.pos())
    #     real_index = self.model().mapToSource(index)
    #     if self.header_list[real_index.column()].get('clickable', False):
    #         data_obj = real_index.internalPointer()
    #         value = ui_utils.get_obj_value(data_obj, self.header_list[real_index.column()].get('attr'))
    #         if value:
    #             self.setCursor(Qt.PointingHandCursor)
    #             return super(MTableView, self).mouseMoveEvent(event)
    #     self.setCursor(Qt.ArrowCursor)
    #     return super(MTableView, self).mouseMoveEvent(event)
    #
    # def mouseReleaseEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         index = self.indexAt(event.pos())
    #         real_index = self.model().mapToSource(index)
    #         if self.header_list[real_index.column()].get('clickable', False):
    #             data_obj = real_index.internalPointer()
    #             value = ui_utils.get_obj_value(data_obj, self.header_list[real_index.column()].get('attr'))
    #             if value:
    #                 self.sig_link_clicked.emit(value)
    #     return super(MTableView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())
        real_index = ui_utils.real_index(index)

        if self.header_list:
            real_index = self.model().mapToSource(index)
            if self.header_list[real_index.column()].get('is_link', False):
                data_obj = real_index.internalPointer()
                value = ui_utils.get_obj_value(data_obj, self.header_list[real_index.column()].get('attr'))
                if value:
                    self.setCursor(Qt.PointingHandCursor)
                    return super(MTableView, self).mouseMoveEvent(event)
            self.setCursor(Qt.ArrowCursor)
        return super(MTableView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.header_list:
            index = self.indexAt(event.pos())
            real_index = ui_utils.real_index(index)
            if self.header_list[real_index.column()].get('is_link', False):
                data_obj = real_index.internalPointer()
                value = ui_utils.get_obj_value(data_obj, self.header_list[real_index.column()].get('attr'))
                if value:
                    re = {"row": data_obj,
                          'value': value,
                          'column': self.header_list[real_index.column()]}
                    self.sig_link_clicked.emit(re)
        return super(MTableView, self).mouseReleaseEvent(event)


class MTreeView(QTreeView):
    set_header_list = set_header_list
    enable_context_menu = enable_context_menu
    slot_context_menu = slot_context_menu
    sig_context_menu = Signal(object)

    def __init__(self, parent=None):
        super(MTreeView, self).__init__(parent)
        self.header_list = []
        self.header_view = MHeaderView(Qt.Horizontal)
        self.setHeader(self.header_view)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)


class MBigView(QListView):
    set_header_list = set_header_list
    enable_context_menu = enable_context_menu
    slot_context_menu = slot_context_menu
    sig_context_menu = Signal(object)

    def __init__(self, parent=None):
        super(MBigView, self).__init__(parent)
        self.header_list = []
        self.header_view = None
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setMovement(QListView.Static)
        self.setSpacing(10)
        self.setIconSize(QSize(128, 128))

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            num_degrees = event.delta() / 8.0
            num_steps = num_degrees / 15.0
            factor = pow(1.125, num_steps)
            new_size = self.iconSize() * factor
            if new_size.width() > 480:
                new_size = QSize(480, 480)
            elif new_size.width() < 24:
                new_size = QSize(24, 24)
            self.setIconSize(new_size)
        else:
            super(MBigView, self).wheelEvent(event)

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            copy_item_view_data(self)
            event.accept()
        else:
            return super(MBigView, self).keyPressEvent(event)


class MListView(QListView):
    set_header_list = set_header_list
    enable_context_menu = enable_context_menu
    slot_context_menu = slot_context_menu
    sig_context_menu = Signal(object)

    def __init__(self, parent=None):
        super(MListView, self).__init__(parent)
        self.header_list = []
        self.header_view = None
        self.setModelColumn(0)
        self.setAlternatingRowColors(True)

    def set_show_column(self, attr):
        for index, attr_dict in enumerate(self.header_list):
            if attr_dict.get('attr') == attr:
                self.setModelColumn(index)
                break
        else:
            self.setModelColumn(0)

    def minimumSizeHint(self, *args, **kwargs):
        return QSize(200, 50)

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            copy_item_view_data(self)
            event.accept()
        else:
            return super(MListView, self).keyPressEvent(event)

    '''
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        file_list = [url.toLocalFile() for url in event.mimeData().urls()]
        result = []
        if sys.platform == 'darwin':
            for url in file_list:
                p = subprocess.Popen(
                    'osascript -e \'get posix path of posix file \"file://{}\" -- kthxbai\''.format(url),
                    stdout=subprocess.PIPE,
                    shell=True)
                # print p.communicate()[0].strip()
                result.append(p.communicate()[0].strip())
                p.wait()
        else:
            result = file_list

        self.emit(SIGNAL('sigDropFile(PyObject)'), result)
'''


class MDragTreeView(QTreeView):
    set_header_list = set_header_list
    enable_context_menu = enable_context_menu
    slot_context_menu = slot_context_menu
    sig_context_menu = Signal(object)
    sig_dropped = Signal(object)

    def __init__(self, parent=None):
        super(MDragTreeView, self).__init__(parent)
        self.header_list = []
        self.header_view = MHeaderView(Qt.Horizontal)
        self.header_view.setStretchLastSection(True)
        self.setHeader(self.header_view)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setMouseTracking(True)

        self.start_press_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_press_pos = event.pos()
        return super(MDragTreeView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            distance = (event.pos() - self.start_press_pos).manhattanLength()
            if distance >= QApplication.startDragDistance():
                selected_index_list = self.selectedIndexes()
                if selected_index_list:
                    mime_data = QMimeData()
                    mime_data.setData('dayu/orm-list', QByteArray())
                    drag = QDrag(self)
                    drag.setMimeData(mime_data)
                    drag.exec_()
        return super(MDragTreeView, self).mouseMoveEvent(event)

    def dropEvent(self, event):
        dropped_index = self.indexAt(event.pos())
        real_index = ui_utils.real_index(dropped_index)
        parent_obj = real_index.internalPointer()
        self.sig_dropped.emit(parent_obj)
        super(MDragTreeView, self).dropEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('dayu/orm-list'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('dayu/orm-list'):
            parent_orm = ui_utils.real_index(self.indexAt(event.pos())).internalPointer()
            if parent_orm:
                for i in self.selectedIndexes():
                    child_orm = ui_utils.real_index(i).internalPointer()
                    if child_orm is parent_orm:
                        event.ignore()
                        return
            event.accept()
        else:
            event.ignore()
