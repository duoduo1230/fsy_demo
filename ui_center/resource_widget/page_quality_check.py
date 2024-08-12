#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Qt import QtWidgets, QtCore
from dayu_widgets import dayu_theme
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTableView
from dayu_widgets.push_button import MPushButton
from dayu_widgets.text_edit import MTextEdit
from ui_center.resource_widget import _mock_data as mock
from ui_center.resource_widget.wizards.wizard import MWizardPage


class QualityCheckPage(MWizardPage):

    finished = QtCore.Signal()

    def __init__(self, parent=None):
        super(QualityCheckPage, self).__init__(parent)
        self._init_ui()
        self.bind_function()

        # NOTE: dayu重写了激活下一步的方法，参考 D:\td\DaYu\ui_center\tools\batch_create_asset_wizard.py的152行
        # Note: 注册的属性可以在每一页共享，就是说每一页可以调用，比如某一页的项目名注册成属性，其它页就可以使用这个属性来使用
        self.register_field(
            'qc_result',  # 注册一个qc_result的属性，
            self.detail_text.toPlainText,  # qc_result属性的值，
            signal=self.finished,  # 触发下一步的信号（finished发射信号的时候触发）
            required=True
        )

    def _init_ui(self):
        self.metadata_model = MTableModel()
        self.metadata_sort_model = MSortFilterModel()
        self.metadata_sort_model.setSourceModel(self.metadata_model)
        self.metadata_model.set_header_list(mock.qc_header_list)
        self.metadata_model.set_data_list(mock.qc_data_list)
        self.metadata_view = MTableView(size=dayu_theme.small)
        self.metadata_view.setModel(self.metadata_sort_model)

        # 写三个button
        self.selected_button = MPushButton("Run Selected Test").small()
        self.all_button = MPushButton("Run All Test").small()
        self.repair_button = MPushButton("Repair It").small()

        self.selected_button.setDisabled(True)
        self.repair_button.setDisabled(True)
        
        self.qc_button_lay = QtWidgets.QHBoxLayout()
        self.qc_button_lay.addWidget(self.selected_button)
        self.qc_button_lay.addWidget(self.all_button)
        self.qc_button_lay.addWidget(self.repair_button)

        grp_style_sheet = """
            QGroupBox {color: #F7922D;}
        """
        qc_grp = QtWidgets.QGroupBox(self.tr('Quality Check List'))
        qc_grp.setAlignment(QtCore.Qt.AlignCenter)
        qc_grp.setStyleSheet(grp_style_sheet)

        qc_lay = QtWidgets.QVBoxLayout()
        qc_lay.addWidget(self.metadata_view)
        qc_lay.addLayout(self.qc_button_lay)
        qc_grp.setLayout(qc_lay)

        detail_lay = QtWidgets.QVBoxLayout()
        self.detail_text = MTextEdit(self)
        self.detail_text.setPlaceholderText(self.tr("质检项没有运行"))
        detail_lay.addWidget(self.detail_text)
        detail_grp = QtWidgets.QGroupBox(self.tr('Detail Information'))
        detail_grp.setAlignment(QtCore.Qt.AlignCenter)
        detail_grp.setStyleSheet(grp_style_sheet)
        detail_grp.setLayout(detail_lay)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(qc_grp)
        main_lay.addWidget(detail_grp)
        self.setLayout(main_lay)

    def bind_function(self):
        self.all_button.clicked.connect(self.chenge_table_color)
        self.detail_text.textChanged.connect(self.confirm_next)

    def set_header_data(self, data):
        """
        Update header data.
        :param data: <list>
        :return:
        """
        self.metadata_widget.set_header_list(data)
        self.metadata_table_child.set_header_list(data)
        self.metadata_widget_sort.set_header_list(data)

    def update_data(self, data):
        """
        Update table view data.
        :param data: <list>
        :return:
        """
        self.metadata_widget.set_data_list(data)

    def chenge_table_color(self):
        for item in mock.qc_data_list:
            item["result"] = "PASSED"
        self.metadata_model.set_data_list(mock.qc_data_list)
        self.detail_text.setText(self.tr("质检全部通过"))
        self.detail_text.setStyleSheet("color: #02C136;")

        """
        点击中间按钮会出现两种情况，质检全部通过 两侧的按钮也是禁用的  然后 MTextEdit 填写质检全部通过（绿色字体）
        # 未全部通过的 还没有写
        未全部通过 会提示有哪一项有问题。
        "【Validate File Node File Path】没有通过\n点击那一项查看详细信息"
        点击上面的item以后  两侧的按钮启用 MTextEdit 填写以下信息
        "Usage:\n校验所有引用外部文件的文件路径是否都在服务器上\nResult:\nFAILED\nInfo:\nRead1: D:/My_code/fsy_demo/ui_center/_icon/minus.png"
        """

    def confirm_next(self):
        # NOTE: 这里判断textedit的内容来作为是否发射成功的信号
        if self.detail_text.toPlainText() == self.tr("质检全部通过"):
            self.finished.emit()
        else:
            pass


if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = QualityCheckPage()
        dayu_theme.apply(test)
        test.show()
