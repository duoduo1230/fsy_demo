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

from ui_center.resource_widget.page_upload_sequence_file import MGetSequenceFilePage
from ui_center.resource_widget.page_slate_template import WorkFileSlatePage
from ui_center.resource_widget.page_comment import CommentPage


class NewDailiesResourceWizard(MWizard):
    def __init__(self, parent=None):
        super(NewDailiesResourceWizard, self).__init__(parent)
        self.resize(800, 1000)
        self._init_ui()

    def _init_ui(self):
        self.set_title('Give Sequence File')

        self.resource_page = MGetSequenceFilePage("Create Sequence File")
        self.workfile_page = WorkFileSlatePage("Select Slate Config")
        self.comment_page = CommentPage("Write comment")

        self.add_page(self.resource_page)
        self.add_page(self.workfile_page)
        self.add_page(self.comment_page)
        self.go_to(0)


class CreateResource(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CreateResource, self).__init__(parent)

        self.resize(800, 1000)
        self._init_ui()

    def _init_ui(self):
        title_label = MLabel("Create Workfile Resource").h1()
        page_add = NewDailiesResourceWizard()
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(title_label)
        main_lay.addWidget(page_add)

        self.setLayout(main_lay)


if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = NewDailiesResourceWizard()
        test.show()
