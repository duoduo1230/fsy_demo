#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets
from dayu_widgets.label import MLabel
from ui_center.resource_widget.wizards.wizard import MWizard

from ui_center.resource_widget.page_create_resource import GetResourcePage
from ui_center.resource_widget.page_quality_check import QualityCheckPage
from ui_center.resource_widget.page_EFX_export_set import EfxExportSetPage
from ui_center.resource_widget.page_thumbnail import ThumbnailPage
from ui_center.resource_widget.page_comment import CommentPage


class EFXResourceWizard(MWizard):
    def __init__(self, parent=None):
        super(EFXResourceWizard, self).__init__(parent)
        self.resize(800, 1000)
        self._init_ui()

    def _init_ui(self):
        self.set_title('Publish EFX Element')

        self.resource_page = GetResourcePage("Create Resource")
        self.resource_page.parent = self
        self.quality_page = QualityCheckPage("Quality Check")
        self.settings_page = EfxExportSetPage("Export Settings")
        self.thumbnail_page = ThumbnailPage("Upload Thumbnail")
        self.comment_page = CommentPage("Write comment")

        self.add_page(self.resource_page)
        self.add_page(self.quality_page)
        self.add_page(self.settings_page)
        self.add_page(self.thumbnail_page)
        self.add_page(self.comment_page)
        self.go_to(0)


if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = EFXResourceWizard()
        test.show()
