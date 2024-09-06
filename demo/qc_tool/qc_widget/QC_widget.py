# -*- coding: utf-8 -*-

import pathlib
from Qt import QtWidgets, QtCore
from dayu_widgets import dayu_theme
from dayu_widgets.label import MLabel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTableView
from dayu_widgets.menu import MMenu
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.push_button import MPushButton
# from resource_widget.warning_dialod import MErrorMessageBox

import os
from manager_qc import MyQC

QC_CONFIG_PATH = r"D:\My_code\fsy_demo\demo\qc_tool\qc_function"


header_list = [
    {
        "label": "QC Item",
        "key": "qc_item",
        "width": 300,
        "checkable": True
    },
    {
        "label": "Result",
        "key": "result",
        'bg_color': {
            "EXCEPTION": "#119",
            "FAILED": "#911",
            "PASSED": "#191",
            "IDLE": "#999"},
    }
]

class QCManager(MyQC, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QCManager, self).__init__(parent)
        self.setWindowTitle(self.tr('QC Manager'))
        self.resize(700, 750)

        self.current_step_folder = ""
        self.qc_item_list = []
        self.error_qc_list = []

        self._init_ui()
        self._init_data()
        self.bind_function()
    def _init_ui(self):
        # title
        title_label = QtWidgets.QLabel('QC Manager')
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 26px;")
        title_lay = QtWidgets.QHBoxLayout()
        title_lay.addStretch()
        title_lay.addWidget(title_label)
        title_lay.addStretch()

        self.step_combobox = MComboBox().small()
        self.step_combobox.setMaximumWidth(150)
        self.step_label = MLabel('Step:')

        choose_lay = QtWidgets.QHBoxLayout()
        choose_lay.addWidget(self.step_label)
        choose_lay.addWidget(self.step_combobox)
        choose_lay.addStretch()

        self.qc_item_tableview = MTableView(size=dayu_theme.large, show_row_count=False)
        self.qc_tablemodel = MTableModel()
        self.qc_tablemodel.set_header_list(header_list)
        self.qc_item_tableview.setModel(self.qc_tablemodel)

        # button
        self.run_qc_btn = MPushButton(text="Run QC").small()
        self.repair_btn = MPushButton(text="Repair All").small()
        self.repair_btn.setEnabled(False)
        
        button_lay = QtWidgets.QHBoxLayout()
        button_lay.addWidget(self.run_qc_btn)
        button_lay.addWidget(self.repair_btn)

        grp_style_sheet = """
            QGroupBox {
                color: #F7922D;
                border: 2px solid gray;
                border-radius: 8px;
                margin-top: 8px; /* 调整这个值来控制标题的垂直位置 */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center; /* 将标题放置在顶部中央 */
                padding: 0 3px;
            }
        """
        self.choose_item_layout = QtWidgets.QVBoxLayout()
        self.choose_item_layout.addWidget(self.qc_item_tableview)
        self.choose_item_layout.addLayout(button_lay)

        self.check_item_groupBox = QtWidgets.QGroupBox('Quality Check List')
        self.check_item_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.check_item_groupBox.setMinimumHeight(80)
        self.check_item_groupBox.setStyleSheet(grp_style_sheet)
        self.check_item_groupBox.setLayout(self.choose_item_layout)

        # 信息窗口
        self.comment_text = MTextEdit(self)
        self.check_info_layout = QtWidgets.QVBoxLayout()
        self.check_info_layout.addWidget(self.comment_text)
        self.check_info_groupBox = QtWidgets.QGroupBox('Detail Information')
        self.check_info_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.check_info_groupBox.setMinimumHeight(40)
        self.check_info_groupBox.setStyleSheet(grp_style_sheet)
        self.check_info_groupBox.setLayout(self.check_info_layout)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(title_lay)
        main_lay.addLayout(choose_lay)
        main_lay.addWidget(self.check_item_groupBox)
        main_lay.addWidget(self.check_info_groupBox)

        self.setLayout(main_lay)

    def _init_data(self):
        self.step_menu = MMenu(exclusive=False, parent=self)
        step_list = os.listdir(QC_CONFIG_PATH)
        self.step_menu.set_data(step_list)
        self.step_combobox._root_menu = self.step_menu

    def bind_function(self):
        self.step_menu._action_group.triggered.connect(
            lambda action: self.select_config(action, self.step_combobox))

        self.qc_item_tableview.clicked.connect(self.select_item_info)
        self.run_qc_btn.clicked.connect(self.run_all_qc)
        self.repair_btn.clicked.connect(self.repair_all)
        
    def select_config(self, action, combobox):
        if action.isChecked():
            combobox._set_value(action.text())
        step = self.step_combobox.currentText()
        step_path = os.path.join(QC_CONFIG_PATH, step)

        self.current_step_folder = step_path
        self.qc_item_list = self.get_qc_items(step_path)
        data_list = []
        for item in self.qc_item_list:
            item_name = item.replace('_', ' ').title()
            # 这里是将py文件的路径变成模块可调用  不是py文件名
            qc_path = os.path.join(self.current_step_folder, item + ".py")
            qc_module = self.import_module(pathlib.Path(qc_path))
            item_data = {
                "qc_item": item_name,
                'qc_item_checked': 2,
                "result": 'IDLE',
                'qc_path': qc_path,
                'error_info': '',
                'module': qc_module
            }
            data_list.append(item_data)

        self.qc_tablemodel.set_data_list(data_list)

    def select_item_info(self, index):
        row = index.row()
        index1 = self.qc_tablemodel.index(row, 0)
        qc_name = self.qc_tablemodel.data(index1)
        index2 = self.qc_tablemodel.index(row, 1)
        qc_result = self.qc_tablemodel.data(index2)
        data = self.qc_tablemodel.get_data_list()
        qc_module = data[row].get('module')
        description = qc_module.description
        error_info = [item.get("error_info") for item in data if item.get("qc_item") == qc_name][0]
        text = "Usage: \n{}\n\n\n\nResult: \n{}\n\n\n\nInfo: \n{}".format(description, qc_result, error_info)
        self.comment_text.setPlainText(text)

        # column_count = self.qc_tablemodel.columnCount()
        # for column in range(column_count):
        #     index = self.qc_tablemodel.index(row, column)
        #     data = self.qc_tablemodel.data(index)
        #     print(data)

    def run_all_qc(self):
        self.error_qc_list.clear()
        self.comment_text.clear()
        data = self.qc_tablemodel.get_data_list()

        for item in data:
            if item.get('qc_item_checked') == 0:
                continue

            qc_module = item.get('module')
            check_info, check_result = qc_module.run()
            item['result'] = check_result
            if check_result != 'PASSED':
                item['error_info'] = check_info
                self.error_qc_list.append(qc_module)

        if self.error_qc_list:
            self.repair_btn.setEnabled(True)

        self.qc_tablemodel.set_data_list(data)

    def repair_all(self):
        data = self.qc_tablemodel.get_data_list()
        for item in data:
            if item.get('result') == 'FAILED':
                qc_module = item.get("module")
                check_info, check_result = qc_module.repair()
                item['result'] = check_result
                item['error_info'] = check_info
        self.qc_tablemodel.set_data_list(data)


        # if self.error_qc_list:
        #     data = self.qc_tablemodel.get_data_list()
        #     for qc in self.error_qc_list:
        #         self.comment_text.clear()
        #         check_info, check_result = qc.repair()
        #
        # else:
        #     error_tips = MErrorMessageBox(u'质检通过，没有可修复项!')
        #     dayu_theme.apply(error_tips)
        #     error_tips.show()
        #     error_tips.exec_()
        #     return


def main():
    from dayu_widgets.qt import application
    with application() as app:
        erro_tips = QCManager()
        dayu_theme.apply(erro_tips)
        erro_tips.show()


if __name__ == "__main__":
    main()