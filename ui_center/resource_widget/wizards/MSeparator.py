#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Qt.QtWidgets import *


class MHSeparator(QFrame):
    def __init__(self, parent=None):
        super(MHSeparator, self).__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class MVSeparator(QFrame):
    def __init__(self, parent=None):
        super(MVSeparator, self).__init__(parent)
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Plain)
