#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets, QtCore
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.push_button import MPushButton
from ui_center3.resource_widget.wizards.wizard import MWizardPage
from ui_center3.resource_widget import _mock_data as mock


class CommentPage(MWizardPage):
    def __init__(self, parent=None):
        super(CommentPage, self).__init__(parent)
        self._init_ui()
        self.bind_function()
        self.register_field(
            'comment',
            self.comment_text.toPlainText,
            signal=self.comment_text.textChanged,
            required=True
        )

    def _init_ui(self):

        self.comment_text = MTextEdit(self)
        self.comment_text.setPlaceholderText(self.tr("点击下方按钮自动设置comment模板，没有按钮就是没有预设。"))

        self.preset_button = MPushButton("Preset").small()
        self.preset_button.setMaximumWidth(140)
        self.clear_button = MPushButton("Clear").small()
        self.clear_button.setMaximumWidth(140)
        self.timecode_lay = QtWidgets.QHBoxLayout()
        self.timecode_lay.addWidget(self.preset_button)
        self.timecode_lay.addWidget(self.clear_button)
        self.timecode_lay.addStretch()

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(self.comment_text)
        main_lay.addLayout(self.timecode_lay)
        main_lay.addStretch()

        self.setLayout(main_lay)

    def bind_function(self):
        self.preset_button.clicked.connect(self.set_comment_preset)
        self.clear_button.clicked.connect(self.clear_comment)

    def set_comment_preset(self):
        self.comment_text.setText(mock.comment_preset)

    def clear_comment(self):
        self.comment_text.clear()


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = CommentPage()
        dayu_theme.apply(test)
        test.show()