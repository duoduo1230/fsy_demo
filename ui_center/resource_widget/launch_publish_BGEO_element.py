#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets
from dayu_widgets.label import MLabel
from wizards.wizard import MWizard

from ui_center.resource_widget.page_creat_resource import GetResourcePage
from ui_center.resource_widget.page_quality_check import QualityCheckView
from ui_center.resource_widget.page_BGEO_export_set import BgeoExportSetPage
from ui_center.resource_widget.page_thumbnail import ThumbnailPage
from ui_center.resource_widget.page_comment import CommentPage


class WorkFileResourceWizard(MWizard):
    def __init__(self, parent=None):
        super(WorkFileResourceWizard, self).__init__(parent)
        self.resize(800, 1000)
        self._init_ui()

    def _init_ui(self):
        self.set_title('Publish BGEO Cache')

        self.resource_page = GetResourcePage("Create Resource")
        self.quality_page = QualityCheckView("Quality Check")
        self.settings_page = BgeoExportSetPage("Export Settings")
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
        page_add = WorkFileResourceWizard()
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(title_label)
        main_lay.addWidget(page_add)

        self.setLayout(main_lay)


if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = WorkFileResourceWizard()
        test.show()
