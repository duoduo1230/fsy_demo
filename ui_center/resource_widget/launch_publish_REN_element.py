#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets
from dayu_widgets.label import MLabel
from wizards.wizard import MWizard
from dayu_widgets import dayu_theme

from page_creat_resource import GetResourcePage
from page_quality_check import QualityCheckView
from Page_REN_export_set import GetSequenceFolderPage
from page_thumbnail import ThumbnailPage
from page_comment import CommentPage


class RENResourceWizard(MWizard):
    def __init__(self, parent=None):
        super(RENResourceWizard, self).__init__(parent)
        self.resize(800, 1000)
        self._init_ui()

    def _init_ui(self):
        self.set_title('Publish EFX Element')

        self.resource_page = GetResourcePage("Create Resource")
        self.quality_page = QualityCheckView("Quality Check")
        self.settings_page = GetSequenceFolderPage("Export Settings")
        self.thumbnail_page = ThumbnailPage("Upload Thumbnail")
        self.comment_page = CommentPage("Write comment")

        self.add_page(self.resource_page)
        self.add_page(self.quality_page)
        self.add_page(self.settings_page)
        self.add_page(self.thumbnail_page)
        self.add_page(self.comment_page)
        self.go_to(0)


class CreateResource(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CreateResource, self).__init__(parent)

        self.resize(800, 1000)
        self._init_ui()

    def _init_ui(self):
        title_label = MLabel("Create Workfile Resource").h1()
        page_add = RENResourceWizard()
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(title_label)
        main_lay.addWidget(page_add)

        self.setLayout(main_lay)


if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = RENResourceWizard()
        dayu_theme.set_theme(test)
        test.show()