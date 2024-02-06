#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2018.5
# Email : muyanru345@163.com
###################################################################

from ui_center.qt import *
from MItemView import MTableView
from MItemModel import MTableModel, MSortFilterModel
from ui_utils import default_formatter, get_obj_value, set_obj_value
from line_edit import MSearchLineEdit
from functools import partial
from collections import Counter
from operator import itemgetter


class MFilterToolBox(QWidget):
    sig_filter_changed = Signal(str, str)

    def __init__(self, parent=None):
        super(MFilterToolBox, self).__init__(parent)
        self.widget_list = []
        self.source_model = None
        self.clear_all_filters_button = QToolButton()
        self.clear_all_filters_button.setText(self.tr('Clear All Filter'))
        self.clear_all_filters_button.clicked.connect(self.slot_clear_all_filter)

        top_lay = QHBoxLayout()
        top_lay.setContentsMargins(0, 0, 0, 0)
        top_lay.addWidget(self.clear_all_filters_button)
        top_lay.addStretch()

        self.more_filters_button = QToolButton()
        self.more_filters_button.setText(self.tr('More Filters'))
        self.more_filters_button.clicked.connect(self.more_filters_button.showMenu)
        bottom_lay = QHBoxLayout()
        bottom_lay.setContentsMargins(0, 0, 0, 0)
        bottom_lay.addWidget(self.more_filters_button)
        bottom_lay.addStretch()

        scroll_area = QScrollArea()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.addStretch()
        scroll_area.setLayout(self.scroll_layout)

        main_lay = QVBoxLayout()
        main_lay.setContentsMargins(0, 0, 5, 0)
        main_lay.addLayout(top_lay)
        main_lay.addWidget(scroll_area)
        main_lay.addLayout(bottom_lay)
        self.setLayout(main_lay)

    def update_data(self):
        for tool_item in self.widget_list:
            self._refresh_data(tool_item)

    def add_item(self, attr, name):
        tool_item = MFilterToolBoxItem(name, attr)
        tool_item.sig_filter_changed.connect(self.sig_filter_changed)
        self._refresh_data(tool_item)
        self.widget_list.insert(0, tool_item)
        self.scroll_layout.insertWidget(0, tool_item)

    def _refresh_data(self, tool_item):
        if self.source_model is None:
            return
        value_counter = Counter([default_formatter(get_obj_value(data, tool_item.attr))
                                 for data in self.source_model.get_data_list()])
        tool_item.setup_data([{'value': v[0], 'count': v[1], 'value_checked': 0}
                              for v in sorted(value_counter.items(), key=itemgetter(1), reverse=True)])

    def set_source_model(self, source_model):
        self.source_model = source_model

    def delete_item(self, name):
        for index in range(len(self.widget_list)):
            widget = self.widget_list[index]
            widget.slot_set_select(Qt.Unchecked)
            self.sig_filter_changed.emit(widget.attr, '')
            if widget.name == name:
                self.scroll_layout.removeWidget(widget)
                widget.close()
                self.widget_list.remove(widget)
                return

    def set_header_list(self, header_list):
        menu = QMenu(self)
        for data_dict in header_list:
            action = QAction(data_dict.get('name'), self)
            action.setData(data_dict.get('attr'))
            action.setCheckable(True)
            if data_dict.get('default_filter', False):
                action.setChecked(True)
                self.add_item(data_dict.get('attr'), data_dict.get('name'))

            menu.addAction(action)
            action.toggled.connect(partial(self.slot_filter_changed, data_dict.get('attr'), data_dict.get('name')))

        self.more_filters_button.setMenu(menu)

    @Slot(str, str, bool)
    def slot_filter_changed(self, attr, name, checked):
        if checked:
            self.add_item(attr, name)
        else:
            self.delete_item(name)

    @Slot()
    def slot_clear_all_filter(self):
        for widget in self.widget_list:
            widget.slot_set_select(Qt.Unchecked)
            self.sig_filter_changed.emit(widget.attr, '')


class MFilterToolBoxItem(QWidget):
    sig_filter_changed = Signal(str, str)

    def __init__(self, name=None, attr=None, parent=None):
        super(MFilterToolBoxItem, self).__init__(parent)
        self.name = name
        self.attr = attr
        self.expanded = True

        self.sort_index = 1
        self.sort_by_name_button = QToolButton()
        self.sort_by_name_button.setArrowType(Qt.DownArrow)
        self.sort_by_name_button.clicked.connect(partial(self.slot_sort_changed, 0, self.sort_by_name_button))
        self.sort_by_count_button = QToolButton()
        self.sort_by_count_button.setArrowType(Qt.DownArrow)
        self.sort_by_count_button.clicked.connect(partial(self.slot_sort_changed, 1, self.sort_by_count_button))

        self.title_button = QToolButton()
        self.title_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.title_button.setText(self.name)
        self.title_button.setArrowType(Qt.DownArrow)
        self.title_button.clicked.connect(self.slot_clicked)
        button_lay = QHBoxLayout()
        button_lay.setContentsMargins(0, 0, 0, 0)
        button_lay.addWidget(self.title_button)
        button_lay.addStretch()
        button_lay.addWidget(self.sort_by_name_button)
        button_lay.addWidget(self.sort_by_count_button)
        button_frame = QFrame()
        button_frame.setObjectName('tool_box')
        button_frame.setLayout(button_lay)

        header_list = [{'name': 'Value', 'attr': 'value', 'searchable': True, 'width': 120, 'checkable': True,
                        'size': (120, 10)},
                       {'name': 'Count', 'attr': 'count', 'width': 40, }]
        self.table_view = MTableView()
        self.table_view.setShowGrid(False)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.set_header_list(header_list)
        self.source_model = MTableModel()
        self.sort_filter_model = MSortFilterModel()
        self.sort_filter_model.setSourceModel(self.source_model)
        self.source_model.set_headers(header_list)
        self.sort_filter_model.set_headers(header_list)
        self.table_view.setModel(self.sort_filter_model)

        action_select_all = QAction(self.tr('Select All'), self.table_view)
        action_select_none = QAction(self.tr('Select None'), self.table_view)
        action_select_invert = QAction(self.tr('Select Invert'), self.table_view)
        self.connect(action_select_all, SIGNAL('triggered()'), partial(self.slot_set_select, Qt.Checked))
        self.connect(action_select_none, SIGNAL('triggered()'), partial(self.slot_set_select, Qt.Unchecked))
        self.connect(action_select_invert, SIGNAL('triggered()'),
                     partial(self.slot_set_select, None))

        self.table_view.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.table_view.addActions([action_select_all, action_select_invert, action_select_none])
        self.table_view.verticalHeader().hide()
        self.table_view.horizontalHeader().hide()
        self.source_model.dataChanged.connect(self.slot_data_changed)

        self.search_line_edit = MSearchLineEdit()
        self.search_line_edit.textChanged.connect(self.sort_filter_model.set_search_pattern)
        main_lay = QVBoxLayout()
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(0)
        main_lay.addWidget(button_frame)
        main_lay.addWidget(self.table_view)
        main_lay.addWidget(self.search_line_edit)
        self.setLayout(main_lay)

    def slot_clicked(self):
        self.expanded = not self.expanded
        self.title_button.setArrowType(Qt.DownArrow if self.expanded else Qt.RightArrow)
        self.table_view.setVisible(self.expanded)
        self.search_line_edit.setVisible(self.expanded)
        self.parent().repaint()

    def setup_data(self, data_list):
        self.source_model.set_data_list(data_list)

    @Slot(int)
    def slot_set_select(self, state):
        self.source_model.beginResetModel()
        for data_obj in self.source_model.get_data_list():
            if state is None:
                old_state = get_obj_value(data_obj, 'value_checked')
                set_obj_value(data_obj, 'value_checked', Qt.Unchecked if old_state == Qt.Checked else Qt.Checked)
            else:
                set_obj_value(data_obj, 'value_checked', state)
        self.source_model.endResetModel()
        self.slot_data_changed(None, None)

    @Slot(QModelIndex, QModelIndex)
    def slot_data_changed(self, start_index, end_index):
        pattern_list = []
        for data_obj in self.source_model.get_data_list():
            if get_obj_value(data_obj, 'value_checked'):
                pattern_list.append(u'^{}$'.format(default_formatter(get_obj_value(data_obj, 'value'))))
        self.sig_filter_changed.emit(self.attr, '|'.join(pattern_list))

    @Slot(str, QToolButton)
    def slot_sort_changed(self, index, button):
        if button.arrowType() == Qt.DownArrow:
            self.table_view.sortByColumn(index, Qt.AscendingOrder)
            button.setArrowType(Qt.UpArrow)
        else:
            self.table_view.sortByColumn(index, Qt.DescendingOrder)
            button.setArrowType(Qt.DownArrow)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    test = MFilterToolBox()
    test.add_item('project', 'Project')
    test.show()
    sys.exit(app.exec_())
