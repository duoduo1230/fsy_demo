# -*- coding: utf-8 -*-

# Import built-in modules

import os
import traceback
import re
import sys
from functools import partial
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import getpass
from datetime import datetime

if sys.version_info.major > 2:
    from importlib import reload

try:
    from shiboken import wrapInstance
except ImportError:
    from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtGui, QtCore

# Import third-party modules
from pathlib import Path
import yaml
from dayu_widgets.label import MLabel
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.push_button import MPushButton
from dayu_widgets.message import MMessage
from dayu_widgets.qt import MIcon
from dayu_widgets import dayu_theme
import pymysql

# Import local modules
from Magician_Toolbox.widgets import tool_widgets

reload(tool_widgets)
from Magician_Toolbox.widgets import dockable_class

reload(dockable_class)

MyDockingWindow = dockable_class.MyDockingWindow


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major > 2:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


def tools_config():
    """
    从 MF_TOOLS_CONFIG 环境变量中，获取.yaml配置文件
    Returns: [dict] yaml中的数据
    """
    mf_tools_configs = os.environ.get("MF_TOOLS_CONFIG")
    if not mf_tools_configs:
        return

    mf_tools_config = mf_tools_configs.split(";")[0]

    if os.path.splitext(mf_tools_config)[-1] not in [".yaml", ".yml"]:
        return
    if sys.version_info.major > 2:
        with open(mf_tools_config, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f.read())
    else:
        with open(mf_tools_config, "r") as f:
            data = yaml.safe_load(f.read())

    return data


def execute_cmd_by_type(cmd_string, typ="python"):
    the_executer = cmds.cmdScrollFieldExecuter('mftoolCMD',
                                               p=cmds.iconTextButton('statusFieldButton', q=True, p=True),
                                               vis=False, st=typ)
    cmds.cmdScrollFieldExecuter(the_executer, e=True, at=cmd_string)
    cmds.cmdScrollFieldExecuter(the_executer, e=True, exa=True)
    cmds.deleteUI(the_executer)


def to_upper(match):
    """
     自定义替换函数，将匹配到的内容转换为大写
    """
    return '{' + match.group(1).upper() + '}'


def replace_environment_to_upper(input_str):
    """
    查找字符串中的{}内容，并替换成大写
    "{magician_public_plugin}/{aaa}/animation"  --> "{MAGICIAN_PUBLIC_PLUGIN}/{AAA}/animation"

    """
    pattern = r'\{(.*?)\}'
    return re.sub(pattern, to_upper, input_str)


def row_data(data):
    return {
        "tool": data.get("label"),
        "project": tools_config().get("Project").get("name"),
        "user": os.environ["PIPELINE_USER"] if os.environ.get("PIPELINE_USER") else getpass.getuser(),
        "last_used_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

class ToolsWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ToolsWindow, self).__init__(parent)

        self.project_data = ""
        self.steps_data = ""

        # 设置窗口属性
        self.setWindowTitle(u"魔术师工具盒")
        self.resize(650, 800)

        # 设置UI
        self.set_theme()
        self.set_ui()
        self.bind_func()

    def hideEvent(self, event):
        self.tools_view.save_state()

    def set_theme(self):
        # 设置字体
        font_path = os.path.join(os.path.dirname(__file__), "Alibaba-PuHuiTi-Medium.ttf")
        _id = QtGui.QFontDatabase.addApplicationFont(font_path)
        dayu_theme.font_family = "Alibaba PuHuiTi M"

        # 设置主题
        dayu_theme.apply(self)

    def set_ui(self):
        # ------------------ Top widget ------------------
        self.magician_lab = MLabel(u"魔术师工具盒").h1().warning()
        self.refresh_btn = MPushButton(u"刷新", MIcon("refresh_line.svg", "#ddd"))
        self.refresh_btn.setMinimumWidth(100)
        self.refresh_btn.setMinimumHeight(90)
        self.search_line = MLineEdit().search().large()
        self.search_line.setPlaceholderText(u"搜索栏(根据工具名检索)")

        # ------------------ Middle widget ------------------
        # UI Setting
        settings = os.path.join(cmds.internalVar(usd=True), "mf_toolbox_settings.ini")

        # Tree View
        self.tools_view = tool_widgets.MyTreeView(settings, show_menu=True, parent=self)
        self.tools_view.setColumnWidth(0, 200)
        self.tools_view.setAnimated(True)
        # self.tools_view.installEventFilter(self)
        view_style_sheet = """
            QTreeView { 
                font-size: 11pt;
                outline: none;
                show-decoration-selected: 0;
            }
            QTreeView::item { 
                padding: 2px;
                border-radius: 7px;
                margin-top: 2px;
                margin-bottom: 2px;
            }
            QTreeView::branch:selected {
                background-color: transparent;
            }
            QTreeView::branch:closed:has-children {
                image: url("%(Magician_Toolbox)s/icons/add.png");
            }
            QTreeView::branch:open:has-children {
                image: url("%(Magician_Toolbox)s/icons/minus.png");
            }
        """
        env_dict = {"Magician_Toolbox": os.environ["Magician_Toolbox"].replace("\\", "/")}
        self.tools_view.setStyleSheet(view_style_sheet % env_dict)
        scroll_bar_style_sheet = """
            QScrollBar:vertical { 
                width: 20px;
            }
            QScrollBar::handle:vertical { 
                background: #5d5d5d;
            }
        """
        self.tools_view.verticalScrollBar().setStyleSheet(scroll_bar_style_sheet)

        # ------------------ Bottom widget ------------------
        self.bottom_widget = QtWidgets.QWidget()
        bottom_lay = QtWidgets.QVBoxLayout(self.bottom_widget)
        description_lab = MLabel(u"工具描述").h3()
        self.description_text = tool_widgets.MyTextEdit()
        self.description_text.setStyleSheet("QTextEdit { font-size: 11pt; }")
        bottom_lay.addWidget(description_lab)
        bottom_lay.addWidget(self.description_text)

        # ------------------ Splitter ------------------
        self.splitter = tool_widgets.MySplitter(QtCore.Qt.Vertical)
        self.splitter.addWidget(self.tools_view)
        self.splitter.addWidget(self.bottom_widget)
        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 1)

        # ------------------ 布局 ------------------
        header_lay = QtWidgets.QHBoxLayout()
        header_lay.addWidget(self.magician_lab)
        header_lay.addStretch()
        header_lay.addWidget(self.refresh_btn)
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(header_lay)
        layout.addWidget(self.search_line)
        layout.addWidget(self.splitter)
        self.setLayout(layout)

    def bind_func(self):
        """ Bind function """
        self.tools_view.emitData.connect(self._eval_command)
        self.tools_view.emitText.connect(self.update_description)
        self.search_line.textChanged.connect(self.update_search)
        self.refresh_btn.clicked.connect(self.refresh)
        # self.tools_view.customContextMenuRequested.connect(self.create_menu)
        self.tools_view.expanded.connect(self.save_state)
        self.tools_view.left_clicked.connect(self.print_cmd)

    def create_menu(self, position):
        """
        设置右键目录
        """
        current_index = self.tools_view.currentIndex()
        if not current_index.data():
            return

        menu = tool_widgets.MMenu()
        actions = self.create_actions(current_index)
        for action in actions:
            menu.addAction(action)

        menu.exec_(self.tools_view.viewport().mapToGlobal(position))

    @property
    def common_action_items(self):
        items = {
            "refresh": {
                "label": u"刷新",
                "triggered": self.refresh,
                "icon": "{Magician_Toolbox}/icons/refresh.png".format(
                    Magician_Toolbox=os.environ.get("Magician_Toolbox")),
            },
            "add_favorite": {
                "label": u"添加到收藏",
                "icon": "{Magician_Toolbox}/icons/favorite.png".format(
                    Magician_Toolbox=os.environ.get("Magician_Toolbox")),
            },
            "cancel_favorite": {
                "label": u"取消收藏",
                "icon": "{Magician_Toolbox}/icons/favorite.png".format(
                    Magician_Toolbox=os.environ.get("Magician_Toolbox"))
            }

        }
        return items

    def create_action_item(self, data):
        label = data.get("label", "")
        icon = data.get("icon", "")
        triggered = data.get("triggered")
        if data.get("icon"):
            action = QtWidgets.QAction(QtGui.QIcon(icon), label, self)
        else:
            action = QtWidgets.QAction(label, self)
        if triggered:
            action.triggered.connect(triggered)

        return action

    def create_actions(self, current_index):
        """
        创建右键菜单的action
        :param current_index: <QtCore.QModelIndex>
        """
        actions = list()
        index_data = self.tools_view.current_item_data()
        item_type = "group" if index_data.get("items") or index_data.get("sub_items") else "item"

        # 通用action
        item_actions = ['refresh', "help"]
        for name, data in self.common_action_items.items():
            if name not in item_actions:
                continue
            action = self.create_action_item(data)
            actions.append(action)

        # 子节点的action
        if item_type == "item":
            # 收藏栏的action
            if self.tools_view.is_favorite_item(current_index):
                action = self.create_action_item(self.common_action_items["cancel_favorite"])
                action.triggered.connect(partial(self.tools_view.remove_favorite_data, current_index))
                actions.append(action)
            # 非收藏栏的action
            else:
                action = self.create_action_item(self.common_action_items["add_favorite"])
                action.triggered.connect(partial(self.tools_view.add_favorite_data, current_index))
                actions.append(action)

        return actions

    def _eval_command(self, data):
        """
        获取当前选中项的user data，找到command并执行
        """
        item_data = data
        command = item_data.get("command")
        if not command:
            return

        # 执行script
        command_type = item_data.get("command_type", "script")
        if command_type == "script":
            try:
                exec(command)
            except:
                self.show_error(traceback.format_exc())
        elif command_type == "module" or command_type == "file":
            try:
                # 执行script
                file_path = replace_environment_to_upper(command)
                file_path = file_path.format(**os.environ).replace("\n", "")
                ext = os.path.splitext(file_path)[1][1:]
                string_cmd = Path(file_path).read_text(encoding="utf-8")
                execute_cmd_by_type(string_cmd, typ=ext)
            except:
                self.show_error(traceback.format_exc())

    def print_cmd(self):
        data = self.tools_view.current_item_data()
        if not data:
            return
        if data.get("command"):
            print("\n>>>>>>>>>>>>>>>>  Command  <<<<<<<<<<<<<<<< ")
            if data.get("command_type", "script") in ["module", "file"]:
                file_path = replace_environment_to_upper(data.get("command"))
                file_path = file_path.format(**os.environ).replace("\n", "")
                print(file_path)
            else:
                print(data.get("command"))

    def update_data(self, data):
        """
        更新UI显示数据
        :param data: [dict]
        """
        self.project_data = data.get("Project")
        self.steps_data = data.get("Steps")

        txt = "{} 工具盒".format(self.project_data.get("name"))
        self.update_title(txt)
        self.update_view(self.steps_data)

    def update_title(self, text):
        self.magician_lab.setText(text)

    def update_view(self, data):
        """
        更新 tree view
        :param data: [dict]
        """
        self.tools_view.update_data(data)
        self.tools_view.restore_state()

    def update_description(self, text):
        """
        更新描述窗口
        :param text: [str]
        """
        self.description_text.setText(text)

    def update_search(self, text):
        """
        根据关键字，更新tree view
        :param text: [str]
        """
        self.tools_view.update_search(text)

    def show_error(self, text, title=u"警告", icon=QtWidgets.QMessageBox.Warning, button_text=u"确定"):
        if not text:
            return

        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.addButton(button_text, QtWidgets.QMessageBox.AcceptRole)
        dayu_theme.apply(msg_box)
        msg_box.show()

    def slot_show_message(self, func, config):
        func(parent=self, **config)

    def refresh(self):
        """ 重新读取yaml文件，刷新tree view. """
        data = tools_config()

        if not data:
            info = {
                "text": "未找到工具的config文件，请联系TA",
                "duration": 4,
                "top": 50
            }
            self.slot_show_message(MMessage.error, info)
            return

        self.update_data(data)

    def save_state(self, index):
        self.tools_view.save_state()


def main():
    data = tools_config()
    if not data:
        om.MGlobal.displayError(u'【未找到工具的config文件，请联系TA】"')
        return

    widget = ToolsWindow()
    widget.update_data(data)

    dockable_window = MyDockingWindow(widget, maya_main_window())
    dockable_window.setWindowTitle(u"魔术师工具盒")
    dockable_window.run()


if __name__ == "__main__":
    main()
