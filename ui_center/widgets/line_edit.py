#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2018.5
# Email : muyanru345@163.com
###################################################################
from ui_center.qt import *
from app import DAYU


class MSearchLineEdit(QLineEdit):
    sig_delay_text_changed = Signal(unicode)
    def __init__(self, parent=None):
        super(MSearchLineEdit, self).__init__(parent)
        size = 18
        clear_button = QToolButton()
        clear_button.clicked.connect(self.clear)
        clear_button.setToolTip('clear')
        clear_button.setIcon(MIcon(DAYU.request('/static/image/icon-clear.png')))
        clear_button.setFixedSize(size + 1, size + 1)
        clear_button.setIconSize(QSize(size, size))
        clear_button.setAutoRaise(True)

        search_button = QToolButton()
        search_button.clicked.connect(self.slot_enter)
        search_button.setToolTip('clear')
        search_button.setIcon(MIcon(DAYU.request('/static/image/icon-search-engine.png')))
        search_button.setFixedSize(size + 1, size + 1)
        search_button.setIconSize(QSize(size, size))
        search_button.setAutoRaise(True)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addWidget(search_button)
        button_layout.addStretch()
        button_layout.addWidget(clear_button)
        self.setTextMargins(size, 0, size, 0)
        self.setLayout(button_layout)
        self.delay_timer = QTimer()
        self.delay_timer.setInterval(500)
        self.delay_timer.setSingleShot(True)
        self.delay_timer.timeout.connect(self._slot_delay_text_changed)

    @Slot()
    def _slot_delay_text_changed(self):
        self.sig_delay_text_changed.emit(self.text())

    def keyPressEvent(self, event):
        if event.key() not in [Qt.Key_Enter, Qt.Key_Tab]:
            if self.delay_timer.isActive():
                self.delay_timer.stop()
            self.delay_timer.start()
        super(MSearchLineEdit, self).keyPressEvent(event)

    def sizeHint(self, *args, **kwargs):
        return QSize(100, 20)

    @Slot()
    def slot_enter(self):
        self.returnPressed.emit()


class MErrorInfoLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(MErrorInfoLineEdit, self).__init__(parent)
        self.content = ''
        detail_button = QToolButton()
        size = 18
        detail_button.clicked.connect(self.slot_show_detail)
        detail_button.setToolTip(self.tr('Show Detail'))
        detail_button.setIcon(MIcon(DAYU.request('/static/image/icon-detail.png')))
        detail_button.setFixedSize(size + 1, size + 1)
        detail_button.setIconSize(QSize(size, size))
        detail_button.setAutoRaise(True)
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()
        button_layout.addWidget(detail_button)
        self.setTextMargins(0, 1, size, 1)
        self.setLayout(button_layout)
        self.setObjectName('error')
        self.setReadOnly(True)

    def sizeHint(self, *args, **kwargs):
        return QSize(100, 20)

    def append(self, text):
        self.setText(text)
        self.content += text + '\n'

    def clear(self):
        self.content = ''
        super(MErrorInfoLineEdit, self).clear()

    @Slot()
    def slot_show_detail(self):
        dialog = QTextEdit(self)
        dialog.setReadOnly(True)
        geo = QApplication.desktop().screenGeometry()
        dialog.setGeometry(geo.width() / 2, geo.height() / 2, geo.width() / 4, geo.height() / 4)
        dialog.setWindowTitle(self.tr('Error Detail Information'))
        dialog.setText(self.content)
        dialog.setWindowFlags(Qt.Dialog)
        dialog.show()
