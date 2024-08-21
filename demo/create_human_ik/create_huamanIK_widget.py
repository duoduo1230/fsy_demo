# -*- coding: utf-8 -*-

import sys
sys.path.append(r'D:\My_code\fsy_demo')
from Qt import QtWidgets, QtCore
from dayu_widgets import dayu_theme
from dayu_widgets.label import MLabel
from dayu_widgets.browser import MClickBrowserFileToolButton
from dayu_widgets.menu import MMenu
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.push_button import MPushButton
from ui_center.resource_widget.warning_dialod import MErrorMessageBox, MSuccessMessageBox
import os

from xml.dom.minidom import parse
import maya.cmds as cmds
from maya import mel
import pathlib

#  获取模板文件名组成一个list
from pathlib import Path
def get_temp_items(path):
    # 此处获取质检项环节的分类
    folder = Path(path)
    module_list = folder.glob("*.xml")
    result = []
    for md in module_list:
        result.append(md.stem)
    return result

TEMPLATE_PATH = r'D:\My_code\fsy_demo\demo\create_human_ik\template'
xml_list = get_temp_items(TEMPLATE_PATH)

class HumanIKWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(HumanIKWidget, self).__init__(parent)
        self.setWindowTitle(self.tr(u'创建 Human IK'))
        self.resize(750, 230)
        self._init_ui()
        self.bind_function()
    def _init_ui(self):
        self.template_button = MMenu(exclusive=False, parent=self)
        self.template_button.set_data(xml_list)
        self.template_comb = MComboBox().small()
        self.template_comb.setMaximumWidth(120)
        self.template_comb._root_menu = self.template_button

        # ma文件夹
        self.folder_button = MClickBrowserFileToolButton().huge()
        self.folder_button.set_dayu_filters(['.ma'])
        path_ = r'D:\My_code\pro\rig_pro'
        self.folder_button.set_dayu_path(path_)
        self.folder_lineedit = MLineEdit().small()

        self.folder_layout = QtWidgets.QHBoxLayout()
        self.folder_layout.addWidget(self.folder_lineedit)
        self.folder_layout.addWidget(self.folder_button)

        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        self.form_layout.addRow(MLabel(u'选择 Ma:').h4(), self.folder_layout)
        self.form_layout.addRow(MLabel(u'选择模板:').h4(), self.template_comb)

        self.run_button = MPushButton(text=u"创建").small()

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(self.form_layout)
        main_lay.addWidget(self.run_button)

        self.setLayout(main_lay)

    def bind_function(self):
        self.folder_button.sig_file_changed.connect(self.folder_lineedit.setText)
        self.template_button._action_group.triggered.connect(
            lambda action: self.select_config(action, self.template_comb))

        self.run_button.clicked.connect(self.creat)

    def select_config(self, action, combobox):
        if action.isChecked():
            combobox._set_value(action.text())

    def hik_update_tool(self):

        melCode = """
            if ( hikIsCharacterizationToolUICmdPluginLoaded() )
            {
                hikUpdateCharacterList();
                hikUpdateCurrentCharacterFromUI();
                hikUpdateContextualUI();
                hikControlRigSelectionChangedCallback;
                hikUpdateSourceList();
                hikUpdateCurrentSourceFromUI();
                hikUpdateContextualUI();
                hikControlRigSelectionChangedCallback;
            }
            """
        try:
            mel.eval(melCode)
        except:
            pass

        cmds.refresh()
        
    def create_definition(self, character_name):
        mel.eval('HIKCharacterControlsTool();')
        mel.eval("hikCreateDefinition();")
        mel.eval("HIKCharacterControlsTool;")
        mel.eval('hikSetCurrentCharacter("{0}")'.format(character_name))

    def set_definition(self, character_name, definition_info):
        for hik_name, d_info in definition_info.items():
            bone = d_info.get('bone')
            hikid = d_info.get('hikid')
            mel_str = 'setCharacterObject("{}", "{}", {}, 0)'.format(bone, character_name, hikid)
            mel.eval(mel_str)
    
    def parse_definition_xml(self, template_file):
        
        result = {}
        dom_tree = parse(template_file)
        root_node = dom_tree.documentElement
        items = root_node.getElementsByTagName("item")
        for index, item in enumerate(items):
            value = item.getAttribute("value")
            if value:
                key = item.getAttribute("key")
                result[key] = {
                    "bone": value,
                    "hikid": index
                }
        return result

    def save_ma(self, path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        cmds.file(rename=path)
        cmds.file(force=True, type='mayaAscii', save=True)

    def clear_file_with_nan(self, path):
        """
        清理文件中的 nan
        :param path: <str> MayaAscii文件
        """
        with open(path, "r") as f:
            s = f.read()

        with open(path, 'w') as f:
            s = s.replace("nan(ind)", "0").replace("nan", "0")
            f.write(s)
    
    def creat(self):
        # 获取到界面中选择的信息
        ma_ = self.folder_lineedit.text().replace('/', '\\')
        if not ma_:
            msg = MErrorMessageBox(parent=self, msg=self.tr(u'请上传ma文件'))
            msg.exec_()
            return

        if not self.template_comb.currentText():
            msg = MErrorMessageBox(parent=self, msg=self.tr(u'请选择模板'))
            msg.exec_()
            return

        character_name = 'Character1'
        xml_name = self.template_comb.currentText() + '.xml'
        ma_path = pathlib.Path(ma_)
        human_ik = ma_path.name.replace('.ma', '_humanIK.ma')
        output_path = os.path.join(ma_path.parent, human_ik)
        xml_path = os.path.join(TEMPLATE_PATH, xml_name)

        # 新建场景
        cmds.file(force=True, new=True)
        # 导入ma工程文件
        cmds.file(ma_path, i=True)
        self.create_definition(character_name)
        self.hik_update_tool()
        result = self.parse_definition_xml(xml_path)
        root = result.get("Hips").get("bone")
        cmds.select(root)

        self.set_definition(character_name, result)

        try:
            # 切换锁定状态
            mel.eval("hikToggleLockDefinition();")
        except:
            pass

        self.hik_update_tool()
        # 保存ma文件
        self.save_ma(output_path)
        # 修复 nan 值
        self.clear_file_with_nan(output_path)

        msg = MSuccessMessageBox(parent=self, msg=self.tr('输出完成'))
        msg.exec_()


def main():
    from dayu_widgets.qt import application

    with application() as app:
        test = HumanIKWidget()
        dayu_theme.apply(test)
        test.show()


if __name__ == "__main__":
    main()