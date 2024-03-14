#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets
from PySide2.QtWidgets import QGraphicsScene
from PySide2.QtGui import QBrush, QColor
from PySide2.QtGui import QPixmap, QClipboard
from dayu_widgets.push_button import MPushButton
from ui_center.resource_widget.wizards.wizard import MWizardPage


# 这里是启动界面之前做的
# import subprocess
# 这个exe应当在外面执行 不然界面关闭程序会崩溃
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
        # self.view.setScene(self.scene)
        # self.view.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        self.browser_button = MPushButton("Screen Shot").small()
        self.clipboard_button = MPushButton("Save").small()

        preview_lay = QtWidgets.QVBoxLayout()
        preview_lay.addWidget(self.browser_button)
        preview_lay.addStretch()
        preview_lay.addWidget(self.clipboard_button)
        preview_lay.addStretch()
        
        setting_lay = QtWidgets.QHBoxLayout()
        setting_lay.addWidget(self.graphics_view)
        setting_lay.addSpacing(30)
        setting_lay.addLayout(preview_lay)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(setting_lay)

        self.setLayout(main_lay)

    def bind_function(self):
        self.browser_button.clicked.connect(self.creat_screen_shot)
        self.clipboard_button.clicked.connect(self.input_screen_shot)

    def creat_screen_shot(self):
        import keyboard
        keyboard.press("F1")
        keyboard.release("F1")

    def input_screen_shot(self):
        # 传入图像
        clipboard = app.clipboard()
        image_data = clipboard.image(QClipboard.Clipboard)

        if image_data:
            pixmap = QPixmap.fromImage(image_data)
            self.view.addPixmap(pixmap)
        else:
            print("剪贴板中没有图像数据")


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = ThumbnailPage()
        dayu_theme.apply(test)
        test.show()