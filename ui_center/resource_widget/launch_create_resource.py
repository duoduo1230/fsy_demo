#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ui_center.resource_widget.wizards.wizard import MWizard
from ui_center.resource_widget.page_creat_resource import GetResourcePage
from ui_center.resource_widget.page_project_template import WorkFileVersionPage
from ui_center.resource_widget.page_thumbnail import ThumbnailPage
from ui_center.resource_widget.page_comment import CommentPage


class WorkFileResourceWizard(MWizard):
    def __init__(self, parent=None):
        super(WorkFileResourceWizard, self).__init__(parent)
        self.resize(800, 1000)
        self._init_ui()

    def _init_ui(self):
        self.set_title('Create Workfile Resource')

        self.resource_page = GetResourcePage("Create Resource")
        self.workfile_page = WorkFileVersionPage("Work File")
        self.thumbnail_page = ThumbnailPage("Upload Thumbnail")
        self.comment_page = CommentPage("Write comment")

        self.add_page(self.resource_page)
        self.add_page(self.workfile_page)
        self.add_page(self.thumbnail_page)
        self.add_page(self.comment_page)
        self.go_to(0)

        # self.next_button.setEnabled(False)
        # 第一页需要写  self.resource_page.name_label.text() 没有内容 Next 启用
        # 第二页默认选中了button  不用写
        # 第三页缩略图不用写  缩略图页在这运行会报错
        # 第四页描述 需要写  没有描述信息 next 禁用


if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = WorkFileResourceWizard()
        test.show()
