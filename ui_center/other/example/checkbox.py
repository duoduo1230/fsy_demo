#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2019.2
# Email : muyanru345@163.com
###################################################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtCore
from Qt import QtWidgets

from dayu_widgets.check_box import MCheckBox
from dayu_widgets.field_mixin import MFieldMixin


class CheckBoxExample(QtWidgets.QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(CheckBoxExample, self).__init__(parent)
        self.setWindowTitle("Example for MCheckBox")


        check_box_normal = MCheckBox('Checked')
        check_box_normal.setCheckState(QtCore.Qt.Checked)




        main_lay = QtWidgets.QVBoxLayout()

        main_lay.addWidget(check_box_normal)

        self.setLayout(main_lay)


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = CheckBoxExample()
        dayu_theme.apply(test)
        test.show()