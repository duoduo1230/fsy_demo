#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan shiyuan
# Date  : 2024.2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets
from PySide2.QtCore import Qt
from Qt.QtWidgets import QDateEdit
from PySide2.QtCore import QDate

from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.spin_box import MDoubleSpinBox
from dayu_widgets.divider import MDivider


class GetResourcePage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(GetResourcePage, self).__init__(parent)
        self.setWindowTitle(self.tr('Add Time Log'))
        self.setFixedSize(600, 600)
        self._init_ui()

    def _init_ui(self):

        self.title_label = MLabel(str("Add Time Log")).h2()

        self.date_widget = QDateEdit(QDate.currentDate())
        self.date_widget.setCalendarPopup(True)

        today_hours = "Today already {num1} hours, {num2} hours left".format(num1=0.0, num2=8.0)
        self.file_filter_label = MLabel(str(today_hours))

        task_total = "{num3} hrs".format(num3=0.0)
        self.task_total_label = MLabel(str(task_total))

        bid = "{num4} hrs".format(num4=8.0)
        self.bid_label = MLabel(str(bid))
        self.duration_spinbox = MDoubleSpinBox().small()
        self.is_overtime_checkbox = MCheckBox()
        self.description = MTextEdit(self)

        self.button_lay = QtWidgets.QHBoxLayout()
        self.mode_lay = QtWidgets.QVBoxLayout()
        self.ok_button = MPushButton("OK").small()
        self.cancel_button = MPushButton("Cancel").small()

        self.button_lay.addWidget(self.ok_button)
        self.button_lay.addWidget(self.cancel_button)

        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setLabelAlignment(Qt.AlignRight)
        self.form_layout.addRow(MLabel('Task:').h2(), self.title_label)
        self.form_layout.addRow(MLabel('Date:').h4(), self.date_widget)
        self.form_layout.addRow(MLabel('Today Total:').h4(), self.file_filter_label)
        self.form_layout.addRow(MLabel('Task Total:').h4(), self.task_total_label)
        self.form_layout.addRow(MLabel('Bid:').h4(), self.bid_label)
        self.form_layout.addRow(MLabel('Is Overtime:').h4(), self.is_overtime_checkbox)
        self.form_layout.addRow(MLabel('Description:').h4(), self.description)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(self.form_layout)
        main_lay.addWidget(MDivider(""))
        main_lay.addLayout(self.button_lay)

        self.setLayout(main_lay)


if __name__ == "__main__":
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = GetResourcePage()
        dayu_theme.apply(test)
        test.show()