import pathlib
from Qt import QtWidgets, QtCore
from dayu_widgets import dayu_theme
from dayu_widgets.label import MLabel
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTableView
from dayu_widgets.menu import MMenu
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.text_edit import MTextEdit
from dayu_widgets.push_button import MPushButton

import os
from  manager_qc import MyQC

QC_CONFIG_PATH = r"D:\My_code\fsy_demo\demo\qc_tool\qc_function"

type_group = ['workfile', 'element']

header_list = [
    {
        "label": "QC Item",
        "key": "qc_item",
        "width": 200,
        "checkable": True
    },
    {
        "label": "Result",
        "key": "result",
        "width": 100,
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

        self.type_group = MMenu(exclusive=False, parent=self)
        self.type_group.set_data(type_group)
        self.type_group_combobox = MComboBox().small()
        self.type_group_combobox.setMinimumWidth(100)
        self.type_group_combobox._root_menu = self.type_group
        self.type_group_label = MLabel('Type Group')


        # self.type_name.set_data(type_name)
        self.type_name_combobox = MComboBox().small()
        self.type_name_combobox.setMaximumWidth(150)

        self.type_name_label = MLabel('Step')

        choose_lay = QtWidgets.QHBoxLayout()
        choose_lay.addWidget(self.type_name_label)
        choose_lay.addWidget(self.type_name_combobox)
        choose_lay.addStretch()

        self.table_large = MTableView(size=dayu_theme.large, show_row_count=False)
        self.file_model = MTableModel()
        self.file_model.set_header_list(header_list)
        file_model_sort = MSortFilterModel()
        file_model_sort.setSourceModel(self.file_model)
        self.table_large.setModel(file_model_sort)
        # file_model_sort.set_header_list(header_list)
        # self.table_large.set_header_list(header_list)

        # button
        self.run_qc = MPushButton(text="Run QC").small()
        self.repair_btn = MPushButton(text="Repair All").small()
        self.repair_btn.setEnabled(False)
        
        button_lay = QtWidgets.QHBoxLayout()
        button_lay.addWidget(self.run_qc)
        button_lay.addWidget(self.repair_btn)

        self.check_item_groupBox = QtWidgets.QGroupBox('')
        self.check_item_groupBox.setMinimumHeight(80)
        self.check_item_groupBox.setStyleSheet("""
            QGroupBox {
                border: 2px solid gray;
                border-radius: 8px;
                margin-top: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: center;
                padding: 0 3px;
            }
        """)

        self.choose_grp_layout = QtWidgets.QVBoxLayout()
        self.choose_grp_layout.addWidget(self.table_large)
        self.choose_grp_layout.addLayout(button_lay)
        self.check_item_groupBox.setLayout(self.choose_grp_layout)

        self.comment_text = MTextEdit(self)
        self.check_info_groupBox = QtWidgets.QGroupBox('')
        self.check_info_groupBox.setMinimumHeight(40)
        self.check_info_groupBox.setStyleSheet("""
            QGroupBox {
                border: 2px solid gray;
                border-radius: 8px;
                margin-top: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: center;
                padding: 0 3px;
            }
        """)
        self.check_info_layout = QtWidgets.QVBoxLayout()
        self.check_info_layout.addWidget(self.comment_text)
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
        self.type_name_combobox._root_menu = self.step_menu

    def bind_function(self):
        self.type_group._action_group.triggered.connect(
            lambda action: self.select_config(action, self.type_group_combobox))
        self.step_menu._action_group.triggered.connect(
            lambda action: self.select_config(action, self.type_name_combobox))

        self.run_qc.clicked.connect(self.run_all_qc)
        self.repair_btn.clicked.connect(self.run_repair_all)

    def select_config(self, action, combobox):
        if action.isChecked():
            combobox._set_value(action.text())
        step = self.type_name_combobox.currentText()
        step_path = os.path.join(QC_CONFIG_PATH, step)

        self.current_step_folder = step_path
        self.qc_item_list = self.get_qc_items(step_path)
        data_list = []
        for item in self.qc_item_list:
            item_data = {
                "qc_item": item,
                'qc_item_checked': 2,
                "result": 'IDLE',
            }
            data_list.append(item_data)

        self.file_model.set_data_list(data_list)

    def run_all_qc(self):
        self.error_qc_list.clear()
        qc_item_list = [os.path.join(self.current_step_folder, i+".py") for i in self.qc_item_list]
        for item in qc_item_list:
            qc_module = self.import_module(pathlib.Path(item))
            print(item)
            print(qc_module)
            is_right = qc_module.run()
            if not is_right:
                self.error_qc_list.append(qc_module)
                self.repair_btn.setEnabled(True)

    def run_repair_all(self):
        if self.error_qc_list:
            for qc in self.error_qc_list:
                result = qc.repair()

def main():
    from dayu_widgets.qt import application
    with application() as app:
        test = QCManager()
        dayu_theme.apply(test)
        test.show()


if __name__ == "__main__":
    main()