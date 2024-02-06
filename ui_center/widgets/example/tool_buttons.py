#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Fan Shiyuan
# Date  : 2023.11
###################################################################
from Qt import QtWidgets

class MToolButton(QtWidgets.QToolButton):
    sig_clicked = Signal(object)
    _toolTip = 'tooltips'
    _toolTip_unchecked = 'tooltips_unchecked'
    _icon = 'icon-default.png'
    _icon_unchecked = 'icon-default.png'

    def __init__(self, size=24, checkable=False, user_data=None, parent=None):
        super(MToolButton, self).__init__(parent)
        if checkable:
            self.setCheckable(checkable)
            self.toggled.connect(self.slot_check_state_changed)
            self.setChecked(True)
        self.user_data = user_data
        self.clicked.connect(self.slot_clicked)
        self.setToolTip(self._toolTip)
        self.setIcon(MIcon(DAYU.request('/static/image/{}'.format(self._icon))))
        self.setFixedSize(size + 1, size + 1)
        self.setIconSize(QSize(size, size))
        self.setAutoRaise(True)

    @Slot(bool)
    def slot_check_state_changed(self, checked):
        self.setChecked(checked)
        if checked:
            self.setToolTip(self._toolTip)
        else:
            self.setToolTip(self._toolTip_unchecked)

    @Slot()
    def slot_clicked(self):
        self.sig_clicked.emit(self.user_data)


class MRefreshButton(MToolButton):
    _toolTip = 'refresh_data'
    _icon = 'icon-refresh.png'