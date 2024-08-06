from Qt import QtWidgets, QtCore
from dayu_widgets import dayu_theme
from dayu_widgets.label import MLabel
from dayu_widgets.browser import MDragFolderButton
from dayu_widgets.divider import MDivider
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTableView
from dayu_widgets.menu import MMenu
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.push_button import MPushButton
from dayu_widgets.qt import MIcon
from dayu_widgets.browser import MClickBrowserFolderPushButton
from dayu_widgets.message import MMessage
from dayu_widgets.drawer import MDrawer
from dayu_widgets.browser import MClickBrowserFolderToolButton
from ui_center.resource_widget.warning_dialod import MErrorMessageBox, MSuccessMessageBox
import os
import functools
import tempfile

cache_dir = tempfile.gettempdir()
# scripts_path = os.path.join(cache_dir, 'add_slate_template.py')
# print(scripts_path)

file_type = ['mov']
trans_code_list = ['prores 4444', 'prores 422 proxy', 'prores 422', 'prores 422 hq']
slate_list = ['slate_1920', 'slate_2048']
fps_list = ['24', '25']


header_list = [
    {
        "label": "File_Name",
        "key": "file_name",
        "checkable": True,
        "width": 200,
    },
    {
        "label": "File_Path",
        "key": "file_path",
        "width": 300,
    }
]

META_CODEC_DICT = {
    'h264': 'avc1',
    'prores 422': 'apcn',
    'prores 422 hq': 'apch',
    'prores 422 proxy': 'apco',
    'prores 4444': 'ap4h',
    'prores 422 lt': 'apcs',
    'prores 422 xq': 'ap4h',
    'tiff': 'tiff',
    'jpg': 'jpeg',
}

REFORMAT_DICT = {
    '1920*1080': 'HD_1080',
    '2048*1152': '2K_2048',
}
reformat_list = list(REFORMAT_DICT.keys())

class AddSlateTool(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AddSlateTool, self).__init__(parent)
        self.setWindowTitle(self.tr('Add Slate'))
        self.resize(700, 750)
        self._init_ui()
        self.bind_function()
    def _init_ui(self):
        # title 层
        title_label = QtWidgets.QLabel('Add Slate')
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 26px;")
        title_lay = QtWidgets.QHBoxLayout()
        title_lay.addStretch()
        title_lay.addWidget(title_label)
        title_lay.addStretch()

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # 功能区的按钮
        self.fps_type_button = MMenu(exclusive=False, parent=self)
        self.fps_type_button.set_data(fps_list)
        self.fps_type_combobox = MComboBox().small()
        self.fps_type_combobox.setMinimumWidth(60)
        self.fps_type_combobox._root_menu = self.fps_type_button
        self.fps_type_label = MLabel('Fps')

        self.trans_code_button = MMenu(exclusive=False, parent=self)
        self.trans_code_button.set_data(trans_code_list)
        self.trans_code_combobox = MComboBox().small()
        self.trans_code_combobox.setMinimumWidth(100)
        self.trans_code_combobox._root_menu = self.trans_code_button
        self.trans_code_label = MLabel('Codec')

        self.slate_button = MMenu(exclusive=False, parent=self)
        self.slate_button.set_data(slate_list)
        self.slate_combobox = MComboBox().small()
        self.slate_combobox.setMinimumWidth(130)
        self.slate_combobox._root_menu = self.slate_button
        self.slate_label = MLabel('Slate')

        self.reformat_button = MMenu(exclusive=False, parent=self)
        self.reformat_button.set_data(reformat_list)
        self.reformat_combobox = MComboBox().small()
        self.reformat_combobox.setMinimumWidth(130)
        self.reformat_combobox._root_menu = self.reformat_button
        self.reformat_label = MLabel('Reformat')

        tips_lay = QtWidgets.QHBoxLayout()
        tips_lay.addWidget(MLabel("Tips: 以上功能不选择，将保持原素材设置导出").warning())

        choose_lay = QtWidgets.QHBoxLayout()
        choose_lay.addWidget(self.fps_type_label)
        choose_lay.addWidget(self.fps_type_combobox)
        choose_lay.addStretch()
        choose_lay.addWidget(self.trans_code_label)
        choose_lay.addWidget(self.trans_code_combobox)
        choose_lay.addStretch()
        choose_lay.addWidget(self.slate_label)
        choose_lay.addWidget(self.slate_combobox)
        choose_lay.addStretch()
        choose_lay.addWidget(self.reformat_label)
        choose_lay.addWidget(self.reformat_combobox)
        choose_lay.addStretch()

        # 功能区的样式
        self.choose_grp = QtWidgets.QGroupBox('')
        self.choose_grp.setMinimumHeight(60)
        self.choose_grp.setStyleSheet("""
            QGroupBox {
                border: 2px dashed gray;
                border-radius: 5px;
                margin-top: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: center;
                padding: 0 3px;
            }
        """)
        self.choose_grp.setLayout(choose_lay)
        # 输出文件夹
        self.folder_button = MClickBrowserFolderToolButton().huge()
        self.folder_lineedit = MLineEdit().small()

        self.folder_layout = QtWidgets.QHBoxLayout()
        self.folder_layout.addWidget(self.folder_lineedit)
        self.folder_layout.addWidget(self.folder_button)

        # 拖入文件夹的UI, 以及拖入文件夹的路径
        self.drag_folder_button = MDragFolderButton()
        self.drag_folder_button.setMinimumHeight(80)
        self.drag_folder_lineedit = MLineEdit().small()

        # 将拖入的文件夹item识别的下面的UI当中
        self.table_large = MTableView(size=dayu_theme.large, show_row_count=False)
        self.file_model = MTableModel()
        self.file_model.set_header_list(header_list)
        file_model_sort = MSortFilterModel()
        file_model_sort.setSourceModel(self.file_model)
        self.table_large.setModel(file_model_sort)
        file_model_sort.set_header_list(header_list)
        self.table_large.set_header_list(header_list)
        # 重命名文件夹
        self.file_filter_label = MLabel(str(file_type))
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.addRow(MLabel('Output Path:').h4(), self.folder_layout)
        self.form_layout.addRow(MDivider(""))
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        self.form_layout.addRow(MLabel('File Filter:'), self.file_filter_label)
        self.form_layout.addRow(MLabel('Give Folder:'), self.drag_folder_button)
        self.form_layout.addRow(MLabel('Folder Result:'), self.drag_folder_lineedit)

        self.run_button = MPushButton( text="Nuke Render").small()
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(title_lay)
        main_lay.addWidget(self.choose_grp)
        # main_lay.addLayout(tips_lay)
        main_lay.addWidget(MDivider(""))
        main_lay.addLayout(self.form_layout)
        main_lay.addWidget(self.table_large)
        main_lay.addWidget(MDivider(""))
        main_lay.addWidget(self.run_button)

        self.setLayout(main_lay)

    def bind_function(self):
        self.folder_button.sig_folder_changed.connect(self.folder_lineedit.setText)
        self.drag_folder_button.sig_folder_changed.connect(self.drag_folder_lineedit.setText)
        self.drag_folder_lineedit.textChanged.connect(self.set_date)
        self.fps_type_button._action_group.triggered.connect(
            lambda action: self.select_config(action, self.fps_type_combobox))
        self.trans_code_button._action_group.triggered.connect(
            lambda action: self.select_config(action, self.trans_code_combobox))
        self.slate_button._action_group.triggered.connect(
            lambda action: self.select_config(action, self.slate_combobox))
        self.reformat_button._action_group.triggered.connect(
            lambda action: self.select_config(action, self.reformat_combobox))

        self.run_button.clicked.connect(self.slot_download)

    def select_config(self, action, combobox):
        if action.isChecked():
            combobox._set_value(action.text())

    def set_date(self):
        folder_path = self.drag_folder_lineedit.text()
        result_list = []
        if folder_path:
            for root, dirs, files in os.walk(folder_path):
                for f in files:
                    _, suf = os.path.splitext(f)
                    if suf == '.mov':
                        data_dict = {
                            "file_name": f,
                            "file_path": root,
                            "file_name_checked": 2,
                        }
                        result_list.append(data_dict)

        self.file_model.set_data_list(result_list)

    def slot_download(self):
        '''
        Please upload the output path
        Please upload the file
        '''
        if not self.drag_folder_button.get_dayu_path():
            test = MErrorMessageBox('Please input the file !')
            dayu_theme.apply(test)
            test.show()
            test.exec_()
            return
        if not self.folder_lineedit.text():
            test = MErrorMessageBox('Please set the output path !')
            dayu_theme.apply(test)
            test.show()
            test.exec_()
            return

        # 功能区
        version_dict = {}
        # 若没有选择就默认
        fps = self.fps_type_combobox.currentText() if self.fps_type_combobox.currentText() else 24
        meta_codec_type = META_CODEC_DICT.get(self.trans_code_combobox.currentText()) if self.trans_code_combobox.currentText() else 'apcn'
        slate = self.slate_combobox.currentText() if self.slate_combobox.currentText() else 'Masking_1'
        format_ = self.reformat_combobox.currentText() if self.reformat_combobox.currentText() else '1920*1080'
        reformat = REFORMAT_DICT.get(format_)

        data_list = self.file_model.get_data_list()
        # 首先判断勾选了没
        for data in data_list:
            if data.get('file_name_checked') == 2:
                version_name = data.get('file_name')
                new_name = data.get('file_name')
                input_path = os.path.join(data.get('file_path'), version_name)
                output_path = os.path.join(self.folder_lineedit.text(), new_name).replace('\\', '/')
                name_ = new_name.split('.')[0]
                version_dict.setdefault(name_, {
                    'read_filename': input_path,
                    'out_path': str(output_path),
                    'fps': fps,
                    'meta_codec_type': meta_codec_type,
                    'slate': slate,
                    'reformat': reformat,
                })

        # 渲染并判断是否成功
        if not self.nuke_render(version_dict):
            msg = MSuccessMessageBox(parent=self, msg=self.tr('Finished rendering.'))
            msg.exec_()
            return
        else:
            msg = MErrorMessageBox(parent=self, msg=self.tr('Rendering error.'))
            msg.exec_()
            return

    def nuke_render(self, version_dict):
        current_folder = os.path.dirname(__file__)
        nuke_template = os.path.join(current_folder, 'template_script.py')

        with open(nuke_template, 'r') as r:
            template_code = r.read()

        result = template_code.format('{}', version_data=version_dict)
        scripts_path = r"D:\temp\demo_tool\PY\add_slate_template.py"
        with open(scripts_path, 'w') as f:
            f.write(result)

        if os.path.exists(scripts_path):
            cmd = r'"C:\Program Files\Nuke11.2v2\Nuke11.2.exe" --nukex -i --tg {}'.format(scripts_path)
            render_result = os.system(cmd)
            return render_result

def main():
    from dayu_widgets.qt import application

    with application() as app:
        test = AddSlateTool()
        dayu_theme.apply(test)
        test.show()


if __name__ == "__main__":
    main()