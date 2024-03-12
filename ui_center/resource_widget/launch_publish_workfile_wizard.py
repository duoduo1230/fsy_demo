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

from page_version_number import VersionPage
from page_quality_check import QualityCheckView
from page_thumbnail import ThumbnailPage
from page_comment import CommentPage


class NewWorkFileResourceWizard(MWizard):
    def __init__(self, parent=None):
        super(NewWorkFileResourceWizard, self).__init__(parent)
        self.resize(800, 1000)
        self._init_ui()

    def _init_ui(self):
        self.set_title('Create Workfile Resource')

        self.resource_page = VersionPage("Version Number")
        self.quality_page = QualityCheckView("Quality Check")
        self.thumbnail_page = ThumbnailPage("Upload Thumbnail")
        self.comment_page = CommentPage("Write comment")

        self.add_page(self.resource_page)
        self.add_page(self.quality_page)
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
        page_add = NewWorkFileResourceWizard()
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(title_label)
        main_lay.addWidget(page_add)

        self.setLayout(main_lay)


if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = NewWorkFileResourceWizard()
        test.show()
