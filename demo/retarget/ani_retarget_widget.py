# -*- coding: utf-8 -*-
import sys
sys.path.append(r'D:\My_code\fsy_demo')
from Qt import QtWidgets, QtCore
from dayu_widgets import dayu_theme
from dayu_widgets.label import MLabel
from dayu_widgets.browser import MClickBrowserFileToolButton, MClickBrowserFolderToolButton
from dayu_widgets.menu import MMenu
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.push_button import MPushButton
from ui_center.resource_widget.warning_dialod import MErrorMessageBox, MSuccessMessageBox
import pathlib
import glob
import importlib

import FBX_Scene
importlib.reload(FBX_Scene)

import maya.cmds as cmds
from maya import mel
import pymel.core as pm

class HumanIKWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(HumanIKWidget, self).__init__(parent)
        self.setWindowTitle(self.tr(u'批量重定向工具'))
        self.resize(750, 400)
        self._init_ui()
        self.bind_function()
    def _init_ui(self):
        self.fps_button = MMenu(exclusive=False, parent=self)
        self.fps_button.set_data(['24', '25', '60'])
        self.fps_comb = MComboBox().small()
        self.fps_comb.setMaximumWidth(120)
        self.fps_comb._root_menu = self.fps_button
        self.fps_comb._set_value('24')

        # 目标ma
        self.retarget_button = MClickBrowserFileToolButton().huge()
        self.retarget_button.set_dayu_filters(['.ma'])
        path_ = r'D:\My_code\pro\rig_pro'
        self.retarget_button.set_dayu_path(path_)
        self.retarget_lineedit = MLineEdit().small()
        self.retarget_layout = QtWidgets.QHBoxLayout()
        self.retarget_layout.addWidget(self.retarget_lineedit)
        self.retarget_layout.addWidget(self.retarget_button)

        # 源ma
        self.source_button = MClickBrowserFileToolButton().huge()
        self.source_button.set_dayu_filters(['.ma'])
        path_ = r'D:\My_code\pro\rig_pro'
        self.source_button.set_dayu_path(path_)
        self.source_lineedit = MLineEdit().small()
        self.source_layout = QtWidgets.QHBoxLayout()
        self.source_layout.addWidget(self.source_lineedit)
        self.source_layout.addWidget(self.source_button)

        
        # 动画fbx文件夹
        self.fbx_folder_button = MClickBrowserFolderToolButton().huge()
        self.fbx_folder_lineedit = MLineEdit().small()
        self.fbx_folder_layout = QtWidgets.QHBoxLayout()
        self.fbx_folder_layout.addWidget(self.fbx_folder_lineedit)
        self.fbx_folder_layout.addWidget(self.fbx_folder_button)

        # 输出文件夹
        self.output_folder_button = MClickBrowserFolderToolButton().huge()
        self.output_folder_lineedit = MLineEdit().small()
        self.output_folder_layout = QtWidgets.QHBoxLayout()
        self.output_folder_layout.addWidget(self.output_folder_lineedit)
        self.output_folder_layout.addWidget(self.output_folder_button)
        
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        self.form_layout.addRow(MLabel(u'目标角色:').h4(), self.retarget_layout)
        self.form_layout.addRow(MLabel(u'源角色:').h4(), self.source_layout)
        self.form_layout.addRow(MLabel('动画FBX文件夹:').h4(), self.fbx_folder_layout)
        self.form_layout.addRow(MLabel('输出文件夹:').h4(), self.output_folder_layout)
        self.form_layout.addRow(MLabel(u'帧率:').h4(), self.fps_comb)

        self.run_button = MPushButton(text=u"输出").small()

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(self.form_layout)
        main_lay.addWidget(self.run_button)

        self.setLayout(main_lay)

    def bind_function(self):
        self.retarget_button.sig_file_changed.connect(self.retarget_lineedit.setText)
        self.source_button.sig_file_changed.connect(self.source_lineedit.setText)
        self.fbx_folder_button.sig_folder_changed.connect(self.fbx_folder_lineedit.setText)
        self.output_folder_button.sig_folder_changed.connect(self.output_folder_lineedit.setText)

        self.fps_button._action_group.triggered.connect(
            lambda action: self.select_config(action, self.fps_comb))

        self.run_button.clicked.connect(self.create)

    def select_config(self, action, combobox):
        if action.isChecked():
            combobox._set_value(action.text())

    def get_frame_range(self):
        """
        从所有骨骼上获取所有动画帧，取最小和最大为第一帧和最后一帧
        :return: <tuple>
        """
        start, end = 0, 0
        joints = cmds.ls(long=True, type="joint")
        cmds.select(joints)
        all_keys = sorted(cmds.keyframe(joints, q=True) or [])
        if all_keys:
            start = int(all_keys[0])
            end = int(all_keys[-1])
        return start, end

    def get_current_hik_character(self):
        # 打开 HumanIK 角色控制工具
        mel.eval("HIKCharacterControlsTool;")
        # 获取当前 HumanIK 角色
        char = mel.eval("hikGetCurrentCharacter();")
        return char

    def hik_update_tool(self):
        # 刷新工具
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

    def set_hik_char(self, targetChar):
        # 这个命令用于打开HumanIK角色控制工具界面
        mel.eval("HIKCharacterControlsTool;")
        # 这个命令用于设置当前的HIK角色为 targetChar， targetChar 是一个变量，代表你想要设置的角色名称。
        mel.eval('hikSetCurrentCharacter("{0}")'.format(targetChar))
        self.hik_update_tool()

    def get_hik_character_list(self):
        # 打开 HumanIK 角色控制工具
        mel.eval("HIKCharacterControlsTool;")
        # _HUMAN_IK_CHARACTER_MENU和_HUMAN_IK_CHARACTER_MENU_OPTION是两个常量
        # 分别表示HumanIK角色菜单的名称和选项菜单的名称
        _HUMAN_IK_CHARACTER_MENU = "hikCharacterList"
        _HUMAN_IK_CHARACTER_MENU_OPTION = _HUMAN_IK_CHARACTER_MENU + "|OptionMenu"
        # 查询 HumanIK 角色菜单中的所有项目，并将它们存储在 items 列表中
        items = cmds.optionMenuGrp(_HUMAN_IK_CHARACTER_MENU, q=True, ill=True)
        hik_list = []
        # 遍历菜单项,查询每个菜单项的标签,将每个标签添加到 hik_list 列表中
        for i in range(0, len(items)):
            label = cmds.menuItem(items[i], q=True, l=True)
            hik_list.append(label)

        return hik_list

    def set_hik_source_char(self, source):
        # 定义了 HumanIK 源角色菜单和选项菜单的名称
        _HUMAN_IK_SOURCE_MENU = "hikSourceList"
        _HUMAN_IK_SOURCE_MENU_OPTION = _HUMAN_IK_SOURCE_MENU + "|OptionMenu"
        # 使用 cmds.optionMenuGrp 查询 HumanIK 源角色菜单中的所有项目，并将它们存储在 items 列表中
        items = cmds.optionMenuGrp(_HUMAN_IK_SOURCE_MENU, q=True, ill=True)
        # 遍历 items 列表中的每个项目，查询每个菜单项的标签（名称）。
        # 使用 label.lstrip() 去掉标签开头的空格，并与 source.lstrip() 进行比较。
        # 如果标签与 source 匹配，则使用 cmds.optionMenu 设置 HumanIK 源角色菜单的选项，并调用 MEL 命令更新 HumanIK UI。
        for i in range(0, len(items)):
            label = cmds.menuItem(items[i], q=True, l=True)
            #  开头有空格，去掉
            if label.lstrip() == source.lstrip():
                cmds.optionMenu(_HUMAN_IK_SOURCE_MENU_OPTION, e=True, sl=i + 1)
                mel.eval("hikUpdateCurrentSourceFromUI()")
                mel.eval("hikUpdateContextualUI()")
                mel.eval("hikControlRigSelectionChangedCallback")
                break

    def bake_skeleton(self):
        return mel.eval("hikBakeCharacter 0;")

    def set_fps(self, fps):
        if fps == 15:
            unit = 'game'
        elif fps == 24:
            unit = 'film'
        elif fps == 25:
            unit = 'pal'
        elif fps == 30:
            unit = 'ntsc'
        elif fps == 48:
            unit = 'show'
        elif fps == 50:
            unit = 'palf'
        elif fps == 60:
            unit = 'ntscf'
        else:
            unit = str(fps) + 'fps'

        cmds.currentUnit(time=unit)
        fps = mel.eval('currentTimeUnitToFPS')
        return fps

    def remove_import_nodes(self):
        # 删除引用import节点
        default_node = ['persp', 'top', 'front', 'side']
        # 列出所有顶级节点(assemblies)
        for i in cmds.ls(assemblies=1):
            # 节点是引用节点，则跳过该节点
            if cmds.referenceQuery(i, isNodeReferenced=True):
                continue
            elif i in default_node:  # without namespace
                continue
            cmds.delete(i)

    def bake(self, objects, start, end):
        # Bake Animation
        cmds.bakeResults(
            objects,
            simulation=False,
            t=(start, end),
            sampleBy=1,
            oversamplingRate=1,
            disableImplicitControl=True,
            preserveOutsideKeys=False,
            sparseAnimCurveBake=False,
            removeBakedAttributeFromLayer=False,
            bakeOnOverrideLayer=False,
            minimizeRotation=True
        )

    def fbx_parameter(self):
        """设置输出fbx预设"""
        if not pm.pluginInfo("fbxmaya", q=True, loaded=True):
            pm.loadPlugin("fbxmaya")
        pm.mel.eval("FBXResetExport")  # ----------------------------------- 重置设置
        pm.mel.eval("FBXExportFileVersion -v FBX201600")  # ---------------- FBX版本
        pm.mel.eval("FBXExportInAscii -v false")  # ------------------------ 使用Binary编码导出
        # pm.mel.eval("FBXExportInAscii -v %s" % str(self.debug).lower())  # - 使用Ascii|Binary编码导出
        pm.mel.eval("FBXExportScaleFactor 1.0")  # ------------------------- 使用缩放比，不要在输出的时候改变比例，关闭
        pm.mel.eval("FBXExportUpAxis y")  # -------------------------------- y 轴向上
        pm.mel.eval("FBXExportIncludeChildren -v false")  # ---------------- 导出子对象即使它未选中，仅导出选中，关闭
        pm.mel.eval("FBXExportLights -v false")  # ------------------------- 导出灯光， 默认不需要
        pm.mel.eval("FBXExportCameras -v true")  # ------------------------- 导出摄像机
        pm.mel.eval("FBXExportSmoothingGroups -v false")  # ---------------- 软硬边转换为光滑组，保持软硬边信息，关闭
        pm.mel.eval("FBXExportSmoothMesh -v false")  # ------------A--------- 导出细分信息，需导出原始模型，关闭
        pm.mel.eval("FBXExportTriangulate -v true")  # --------------------- 以三角面导出Mesh, 为保持maya计算结果，开启
        pm.mel.eval("FBXExportEmbeddedTextures -v false")  # --------------- 导出FBX嵌入贴图，关闭
        pm.mel.eval("FBXExportShapes -v true")  # - 导出 blendshape 混合变形
        pm.mel.eval("FBXExportConstraints -v false")  # -------------------- 导出约束关系，输出前都会bake, 关闭
        pm.mel.eval("FBXExportSkins -v false")  # -------------------------- 导出蒙皮信息，关闭
        pm.mel.eval("FBXExportBakeResampleAnimation -v true")  # ---------- 导出时bake动画， 提前bake过，关闭
        pm.mel.eval("FBXExportInputConnections -v false")  # ----------------避免控制器被导出 关闭
        pm.mel.eval("FBXExportUseSceneName -v false")  # -------------------- 默认动画会使用 Take 001, 开启则使用文件名

    def export_fbx(self, sel, in_path):
        self.fbx_parameter()
        pm.select(sel, r=1)
        print('FBXExport -f "{0}" -s'.format(str(in_path).replace("\\", "/")))
        mel.eval('FBXExport -f "{0}" -s'.format(str(in_path).replace("\\", "/")))

    def create(self):

        fps = self.fps_comb.currentText()
        animation_fbx_folder = self.fbx_folder_lineedit.text()
        if not animation_fbx_folder:
            msg = MErrorMessageBox(parent=self, msg=self.tr(u'请选择fbx文件夹'))
            msg.exec_()
            return
        character1 = self.retarget_lineedit.text()
        if not character1:
            msg = MErrorMessageBox(parent=self, msg=self.tr(u'请选择'))
            msg.exec_()
            return
        source = self.source_lineedit.text()
        if not source:
            msg = MErrorMessageBox(parent=self, msg=self.tr(u'请选择'))
            msg.exec_()
            return
        output_folder = self.output_folder_lineedit.text()
        if not output_folder:
            msg = MErrorMessageBox(parent=self, msg=self.tr(u'选择输出路径'))
            msg.exec_()
            return

        animation_file_list = glob.glob(r"{}\*.fbx".format(animation_fbx_folder))
        anim_fbx = animation_file_list[0].replace("\\", "/")
        anim_path = pathlib.Path(anim_fbx)

        character_path = pathlib.Path(character1)
        name_space = character_path.stem

        fbx_path = '{}/{}_retarget.fbx'.format(output_folder, anim_path.stem)
        ma_path = '{}/{}_retarget.ma'.format(output_folder, anim_path.stem)

        # 从fbx文件中得到骨骼动画的首尾帧
        fbx_file = FBX_Scene.FBX_Class(anim_path.as_posix())
        start, end = fbx_file.get_time_range()
        if not start and not end:
            start, end = self.get_frame_range()
        fbx_file.close()

        # 新建场景
        cmds.file(force=True, new=True)
        # reference 驱动者 不加命名空间
        cmds.file(source, r=True, options="v=0;", namespace=":")
        current_source = self.get_current_hik_character()

        # 导入带动画骨骼的fbx文件，给驱动者加动画
        cmds.file(anim_path, i=True)
        # 设置动画播放范围
        cmds.playbackOptions(animationStartTime=start, minTime=start, maxTime=end, animationEndTime=end)
        default_character_list = self.get_hik_character_list()
        # reference 被驱动者 加命名空间
        cmds.file(character1, r=True, namespace=name_space)
        source_list = self.get_hik_character_list()
        current_character = list(set(source_list) ^ set(default_character_list))

        # 打开HumanIK角色控制工具界面
        # 页面中设置被驱动者
        self.set_hik_char(current_character[0])
        # 页面中设置驱动者
        self.set_hik_source_char(current_source)
        # bake骨骼动画
        self.bake_skeleton()
        # 设置fps
        self.set_fps(fps)
        # 移除引用并另存文件
        self.remove_import_nodes()  # 清理import节点

        # 清理命名空间
        for rf_node in cmds.ls(rf=1):
            if rf_node == name_space + "RN":
                continue
            cmds.file(removeReference=True, referenceNode=rf_node)

        cmds.file(rename=ma_path)
        cmds.file(force=True, type='mayaAscii', save=True)
        # 设置另存得文件名

        # 选中骨骼
        joints = cmds.ls(type="joint")
        # bake骨骼
        self.bake(joints, start, end)
        # 导出fbx
        self.export_fbx(joints, fbx_path)

        # 去除FBX的命名空间
        fbx_file = FBX_Scene.FBX_Class(fbx_path)
        fbx_file.remove_namespace()
        fbx_file.save(fbx_path)

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