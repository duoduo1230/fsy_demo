# -*- coding: utf-8 -*-
import sys

sys.path.append(r'D:\My_code\fsy_demo\third_package\win32')
import Qt
from Qt import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from dayu_widgets import dayu_theme
import maya.cmds as cmds
import pymel.core as pm
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.line_edit import MLineEdit
from functools import partial
from datetime import datetime
import getpass


FONT_EDIT = [
    ["topLeftText", "topCenterText", "topRightText"],
    ["bottomLeftText", "bottomCenterText", "bottomRightText"]
]

def maya_main_window(typ=QtWidgets.QWidget):
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), typ)

def delete_shotmask():
    """
    Delete all shotmask nodes.
    """
    shot_mask_nodes = cmds.ls("zshotmask*")
    for i in shot_mask_nodes:
        trf = cmds.listRelatives(i, p=1)
        cmds.delete(trf)

def create_shot_mask():
    delete_shotmask()
    plugin = "zshotmask.py"
    if not cmds.pluginInfo(plugin, q=True, loaded=True):
        cmds.loadPlugin(plugin)

    return cmds.createNode("zshotmask")

def init_shot_mask(node):
    # 遮幅透明度
    cmds.setAttr("{}.borderAlpha".format(node), 0.39)
    # 字号
    cmds.setAttr("{}.fontScale".format(node), 0.63)
    # 字体颜色
    cmds.setAttr("{}.fontColorR".format(node), 1)
    cmds.setAttr("{}.fontColorG".format(node), 0.647)
    cmds.setAttr("{}.fontColorB".format(node), 0)

class MaskWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MaskWindow, self).__init__(parent)

        self.resize(950, 750)
        self._init_ui()
        self.bind_function()
        self._zshotmask = create_shot_mask()
        init_shot_mask(self._zshotmask)

    def _init_ui(self):
        # 创建了窗口
        self.model_editor_widget = self.create_model_widget()
        self.model_editor_widget.setParent(self)
        self.model_editor_widget.setObjectName("model_editor_widget")

        self.model_editor_widget.setFixedWidth(766)
        self.model_editor_widget.setFixedHeight(430)

        self.model_editor_layout = QtWidgets.QHBoxLayout()
        self.model_editor_layout.addStretch()
        self.model_editor_layout.addWidget(self.model_editor_widget)
        self.model_editor_layout.addStretch()

        # 控制窗口显示的信息
        self.light_check_box = MCheckBox(u"显示灯光")
        self.srf_check_box = MCheckBox(u"显示贴图")
        self.smooth_check_box = MCheckBox(u"抗锯齿")

        self.show_lay = QtWidgets.QGridLayout()
        self.show_lay.addWidget(self.light_check_box, 1, 1)
        self.show_lay.addWidget(self.srf_check_box, 1, 2)
        self.show_lay.addWidget(self.smooth_check_box, 1, 3)

        self.collapse = self.create_collapse()

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(self.model_editor_layout)
        main_lay.addLayout(self.show_lay)
        main_lay.addWidget(self.collapse)

        self.setLayout(main_lay)

    def _init_ui_data(self):
        """
        Initialize UI data.
        """
        # # 获取当前maya间滑块的起始时间还有结束时间
        # start = int(cmds.playbackOptions(minTime=1, q=1))
        # end = int(cmds.playbackOptions(maxTime=1, q=1))
        #
        # # 设置字体大小
        # self.font_size_spinbox.setValue(1)
        #
        # # Set slider value.
        # # 给进度滑块设置值
        # self.slider.setRange(start, end)
        # current_time = int(cmds.currentTime(q=1))
        # self.slider.setValue(current_time)

        self.set_mask_text()

    def set_mask_text(self):
        """ Set shot mask text one by one, and update line edit. """

        cmds.setAttr("{}.topLeftText".format(self._zshotmask), u"ceshi", typ="string")

        tct_text = u"{}-{}x{}".format(self.proj_line.text(), get_resolution()[0], get_resolution()[1])
        cmds.setAttr("{}.topCenterText".format(self._zshotmask), tct_text, typ="string")

        trt_text = u"{}-{}({}-{})".format(self.seq_line.text(), self.shot_line.text(), self.frame_start_line.text(),
                                          self.frame_end_line.text())
        cmds.setAttr("{}.topRightText".format(self._zshotmask), trt_text, typ="string")

        focal_length = cmds.getAttr(pm.PyNode(get_active_camera()) + '.focalLength')
        tlt_txt = u"焦距:{0}".format(str(round(focal_length, 1)))
        cmds.setAttr("{}.bottomLeftText".format(self._zshotmask), tlt_txt, typ="string")

        tct_txt = u"{}-{}".format(getpass.getuser(), datetime.now().strftime("%Y/%m/%d"))
        cmds.setAttr("{}.bottomCenterText".format(self._zshotmask), tct_txt, typ="string")

        t = int(cmds.currentTime(q=True))
        padding = 5 if t < 0 else 4
        current_time = "{}".format(t).zfill(padding)
        cmds.setAttr("{}.bottomRightText".format(self._zshotmask), current_time, typ="string")

        # Update line edit
        for row, row_ls in enumerate(self.font_edit):
            for index, font_edit in enumerate(row_ls):
                text = cmds.getAttr("{}.{}".format(self._zshotmask, font_edit))
                edit = getattr(self, font_edit)
                edit.setText(text)

    def bind_function(self):
        # 抗锯齿 灯光 贴图
        self.smooth_check_box.stateChanged.connect(self.change_anti_aliasing)
        self.light_check_box.stateChanged.connect(self.change_lighting)
        self.srf_check_box.stateChanged.connect(self.change_texture)

    def create_model_widget(self):
        if cmds.window("ModelEditor", exists=True):
            cmds.deleteUI("ModelEditor")
            # 创建一个窗口，名称为 “ModelEditor”
        window1 = cmds.window('ModelEditor')
        # 创建一个表单布局控件
        form = cmds.formLayout()
        # 中用于查看和编辑 3D 模型的视图
        self._model_editor = cmds.modelEditor()
        # 创建一个列布局控件。列布局允许将控件按照垂直方向排列
        column = cmds.columnLayout('true')
        cmds.formLayout(form, edit=True,
                        attachForm=[(column, 'top', 0), (column, 'left', 0), (self._model_editor, 'top', 0),
                                    (self._model_editor, 'bottom', 0), (self._model_editor, 'right', 0)],
                        attachNone=[(column, 'bottom'), (column, 'right')],
                        attachControl=(self._model_editor, 'left', 0, column))
        # 获取当前活动视图的相机名称
        current_cam = cmds.modelEditor("modelPanel4", q=1, av=1, cam=1)
        cam_shape = cmds.listRelatives(current_cam, s=True)[0]
        # overscan 属性控制相机视图的扩展范围，设置为1表示不进行扩展
        cmds.setAttr("{}.overscan".format(cam_shape), 1)
        # allObjects=False 模型编辑器不会显示所有对象
        cmds.modelEditor(self._model_editor, edit=True, allObjects=False)
        cmds.modelEditor(self._model_editor, edit=True, camera=current_cam, imagePlane=True,
                         displayAppearance='smoothShaded', hud=0, polymeshes=True)
        # 获取窗口的指针
        ptr = omui.MQtUtil.findControl(window1)
        # 将指针转换为QtWidget
        return wrapInstance(int(ptr), QtWidgets.QWidget)

    def create_collapse(self):
        mask_widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(mask_widget)
        for row, row_ls in enumerate(FONT_EDIT):
            for index, font_edit in enumerate(row_ls):
                edit = MLineEdit()
                edit.textChanged.connect(partial(self.change_mask_text, font_edit))
                setattr(self, font_edit, edit)
                layout.addWidget(getattr(self, font_edit), row, index)
        return mask_widget

    def get_playbackOptions(self):
        # 获取当前maya间滑块的起始时间还有结束时间
        start = int(cmds.playbackOptions(minTime=1, q=1))
        end = int(cmds.playbackOptions(maxTime=1, q=1))
        return start, end

    @classmethod
    def change_anti_aliasing(cls, value):
        v = True if value == 2 else False
        cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", 2)

    def change_lighting(self, value):
        v = "all" if value == 2 else "default"
        cmds.modelEditor(self._model_editor, edit=True, displayLights=v)
        cmds.modelEditor(self._model_editor, edit=True, displayTextures=v)

    def change_texture(self, value):
        """
        Shot model editor's texture.
        :param value: [int]
        """
        v = True if value == 2 else False
        cmds.modelEditor(self._model_editor, edit=True, displayTextures=v)

    def change_mask_text(self, index, text):
        cmds.setAttr("{}.{}".format(self._zshotmask, index), text, typ="string")

    def closeEvent(self, *args):
        if cmds.window(self._model_editor, exists=True):
            cmds.deleteUI(self._model_editor)
        delete_shotmask()

if __name__ == "__main__":
    from dayu_widgets.qt import application

    with application() as app:
        test = MaskWindow()
        dayu_theme.apply(test)
        test.show()

# import sys
# sys.path.append(r'D:\My_code\fsy_demo\demo\pb_with_shotmask')
# import tset_func
# reload(tset_func)
# widget = tset_func.MaskWindow()
# widget.show()