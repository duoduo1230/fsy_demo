#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools

from Qt import QtWidgets
from PySide2.QtWidgets import QGraphicsScene
from PySide2.QtGui import QBrush, QColor
from PySide2.QtGui import QPixmap, QClipboard

from dayu_widgets.push_button import MPushButton
from dayu_widgets.message import MMessage
from ui_center3.resource_widget.wizards.wizard import MWizardPage


# 启动界面之前做的,打开截图工具
# import subprocess
# exe_path = r"D:\software\Snipaste\Snipaste.exe"
# subprocess.run(exe_path, shell=True)

class ThumbnailPage(MWizardPage):
    def __init__(self, parent=None):
        super(ThumbnailPage, self).__init__(parent)
        self.radius = 300
        self._init_ui()
        self.bind_function()

    def _init_ui(self):

        self.scene = QGraphicsScene(0, 0, self.radius, self.radius)
        self.scene.setBackgroundBrush(QBrush(QColor('#666')))

        self.view = QtWidgets.QGraphicsScene()
        self.graphics_view = QtWidgets.QGraphicsView(self.view)

        self.browser_button = MPushButton("Screen Shot").small().primary()
        self.clipboard_button = MPushButton("Save Image").small().primary()

        preview_lay = QtWidgets.QVBoxLayout()
        preview_lay.addStretch()
        preview_lay.addWidget(self.browser_button)
        preview_lay.addStretch()
        preview_lay.addWidget(self.clipboard_button)
        preview_lay.addStretch()
        
        setting_lay = QtWidgets.QHBoxLayout()
        setting_lay.addWidget(self.graphics_view)
        setting_lay.addSpacing(30)
        setting_lay.addLayout(preview_lay)

        self.main = QtWidgets.QVBoxLayout()
        self.main.addLayout(setting_lay)

        self.setLayout(self.main)

    def bind_function(self):
        self.browser_button.clicked.connect(self.creat_screen_shot)
        self.clipboard_button.clicked.connect(self.save_screen_shot)

    def creat_screen_shot(self):
        import keyboard
        keyboard.press("F1")
        keyboard.release("F1")

    def save_screen_shot(self):
        from dayu_widgets.qt import application
        with application() as app:
            clipboard = app.clipboard()
            image_data = clipboard.image(QClipboard.Clipboard)

            if image_data:
                pixmap = QPixmap.fromImage(image_data)
                self.view.addPixmap(pixmap)
            else:
                MainWindow = QtWidgets.QMainWindow()
                MessageBox = QtWidgets.QMessageBox()
                MessageBox.warning(self, "warning", "剪贴板中没有图片")
                MainWindow.show()

    def slot_show_message(self, func, config):
        func(parent=self, **config)


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = ThumbnailPage()
        dayu_theme.apply(test)
        test.show()