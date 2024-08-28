# -*- coding: utf-8 -*-
from Qt import QtWidgets, QtCore, QtGui
from dayu_widgets import dayu_theme
from dayu_widgets.label import MLabel
from dayu_widgets.divider import MDivider
from dayu_widgets.menu import MMenu
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.slider import MSlider
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.push_button import MPushButton
from dayu_widgets.collapse import MCollapse
from dayu_widgets.spin_box import MSpinBox
from dayu_widgets.browser import MClickBrowserFolderToolButton
# from ui_center.resource_widget.warning_dialod import MErrorMessageBox, MSuccessMessageBox
from shiboken2 import wrapInstance
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import pymel.core as pm
import maya.OpenMaya as om
import os
import getpass
import subprocess
from datetime import datetime
from functools import partial


def maya_main_window(typ=QtWidgets.QWidget):
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), typ)

def window_to_qt(window):
    ptr = omui.MQtUtil.findControl(window)
    return wrapInstance(int(ptr), QtWidgets.QWidget)

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
    cmds.setAttr("{}.borderAlpha".format(node), 0.3)
    # 字号
    cmds.setAttr("{}.fontScale".format(node), 0.63)
    # 字体颜色
    cmds.setAttr("{}.fontColorR".format(node), 1)
    cmds.setAttr("{}.fontColorG".format(node), 0.647)
    cmds.setAttr("{}.fontColorB".format(node), 0)

def get_desk_resolution(typ=QtWidgets.QApplication):
    app = maya_main_window(typ)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    return width, height

def get_dar():
    dar = pm.general.getAttr('defaultResolution.deviceAspectRatio')
    return float("%.4f" % dar)

def get_active_camera():
    # 获取当前maya里面
    activeCamera = om.MDagPath()
    omui.M3dView().active3dView().getCamera(activeCamera)
    return activeCamera.fullPathName()


def get_bounding_box(objects=[]):
    x = []
    y = []
    z = []
    _x = []
    _y = []
    _z = []

    allObject = []

    allT = cmds.ls(type="mesh")
    for i in allT:
        root = pm.PyNode(i)
        A = root.listRelatives(ap=True)
        objectName = A[0].longName()
        allObject.append(objectName)

    for i in allObject:
        si = cmds.xform(i, q=1, bb=1)
        x.append(si[0])
        y.append(si[1])
        z.append(si[2])
        _x.append(si[3])
        _y.append(si[4])
        _z.append(si[5])

    size = [min(x), min(y), min(z), max(_x), max(_y), max(_z)]
    maxLength = [abs(size[0]) + abs(size[3]),
                 abs(size[1]) + abs(size[4]),
                 abs(size[2]) + abs(size[5])]

    return size, maxLength


def make_suitable_camera(objects=[]):
    '''Makes a camera based the bounding box of the geometry.'''
    size, maxLength = get_bounding_box(objects=objects)

    x = (size[0] + size[3]) / 2
    y = (size[1] + size[4]) / 2
    z = (size[2] + size[5]) / 2

    cameraname = cmds.camera(name="scene_name")

    cmds.setAttr("%s.farClipPlane" % cameraname[0], 10000000)

    cmds.move(x, y + max(maxLength) * 0.1, z + max(maxLength) * 2.4, cameraname[0])
    cmds.move(x, y, z, "%s.scalePivot" % cameraname[0], "%s.rotatePivot" % cameraname[0])
    cmds.setAttr("%s.rotateX" % cameraname[0], -5)

    return cameraname[0]


def get_resolution(half=False):
    res_x = pm.general.getAttr('defaultResolution.width')
    res_y = pm.general.getAttr('defaultResolution.height')
    if half:
        return res_x / 2, res_y / 2
    else:
        return res_x, res_y


class MaskWindow(QtWidgets.QDialog):
    def __init__(self, zshotmask, parent=None):
        super(MaskWindow, self).__init__(parent)
        self.setWindowTitle(u"拍屏工具")
        self.setObjectName("MyMaskWindow")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # 创建加水印的节点
        self._zshotmask = zshotmask
        # 水印节点的属性
        self.font_edit = [
            ["topLeftText", "topCenterText", "topRightText"],
            ["bottomLeftText", "bottomCenterText", "bottomRightText"]
        ]
        self.resize(950, 750)
        self._init_ui()
        self.bind_function()
        self._init_ui_data()
    def _init_ui(self):

        # 给进度条
        self.slider = MSlider(QtCore.Qt.Horizontal)

        # 设置水印的 lineedit
        self.collapse = self.create_collapse()

        # 显示信息的checkbox
        self.light_check_box = MCheckBox(u"显示灯光")
        self.srf_check_box = MCheckBox(u"显示贴图")
        self.smooth_check_box = MCheckBox(u"抗锯齿")

        self.show_lay = QtWidgets.QGridLayout()
        self.show_lay.addWidget(self.light_check_box, 1, 1)
        self.show_lay.addWidget(self.srf_check_box, 1, 2)
        self.show_lay.addWidget(self.smooth_check_box, 1, 3)

        self.size_lab = MLabel(u"尺寸：")
        self.size_menu = MMenu(exclusive=False, parent=self)
        self.size_menu.set_data(['full', 'half'])

        self.size_combobox = MComboBox().small()
        self.size_combobox.setMinimumWidth(132)
        self.size_combobox._root_menu = self.size_menu
        self.size_combobox._set_value('full')
        self.size_lay = QtWidgets.QHBoxLayout()
        self.size_lay.addWidget(self.size_lab)
        self.size_lay.addWidget(self.size_combobox)
        self.size_lay.addStretch()

        self.cam_label = MLabel(u"摄像机：")
        self.cam_menu = MMenu(exclusive=False, parent=self)
        self.cam_combobox = MComboBox()
        self.cam_combobox.setMinimumWidth(118)
        self.cam_lay = QtWidgets.QHBoxLayout()
        self.cam_lay.addWidget(self.cam_label)
        self.cam_lay.addWidget(self.cam_combobox)
        self.cam_lay.addStretch()

        self.font_size_lab = MLabel(u"字号：")
        self.font_size_spinbox = QtWidgets.QDoubleSpinBox()
        self.font_size_spinbox.setRange(0.01, 2)
        self.font_size_spinbox.setSingleStep(0.02)
        self.font_size_spinbox.setMinimumWidth(80)

        self.font_lay = QtWidgets.QHBoxLayout()
        self.font_lay.addWidget(self.font_size_lab)
        self.font_lay.addWidget(self.font_size_spinbox)
        self.font_lay.addStretch()

        self.color_lab = MLabel(u"色彩空间：")
        self.color_menu = MMenu(exclusive=False, parent=self)
        self.color_menu.set_data(["sRGB", "Raw"])

        self.color_combobox = MComboBox().small()
        self.color_combobox.setMaximumWidth(150)
        self.color_combobox._root_menu = self.color_menu
        self.color_combobox._set_value('sRGB')
        self.color_lay = QtWidgets.QHBoxLayout()
        self.color_lay.addWidget(self.color_lab)
        self.color_lay.addWidget(self.color_combobox)
        self.color_lay.addStretch()

        self.format_lab = MLabel(u"格式：")
        self.format_menu = MMenu(exclusive=False, parent=self)
        self.format_menu.set_data(["mov", "avi"])
        self.format_combobox = MComboBox().small()
        self.format_combobox.setMinimumWidth(140)
        self.format_combobox._root_menu = self.format_menu
        self.format_combobox._set_value('mov')
        self.out_lay = QtWidgets.QHBoxLayout()
        self.out_lay.addWidget(self.format_lab)
        self.out_lay.addWidget(self.format_combobox)
        self.out_lay.addStretch()

        self.sequence_check_box = MCheckBox(u"序列")


        self.frame_range = MLabel(u"帧范围：")
        self.frame_start_line = MLineEdit().small()
        self.frame_start_line.setMaximumWidth(60)
        self.frame_end_line = MLineEdit().small()
        self.frame_end_line.setMaximumWidth(60)
        _lab = MLabel("-")

        self.frame_lay = QtWidgets.QHBoxLayout()
        self.frame_lay.addWidget(self.frame_range)
        self.frame_lay.addWidget(self.frame_start_line)
        self.frame_lay.addWidget(_lab)
        self.frame_lay.addWidget(self.frame_end_line)
        self.frame_lay.addStretch()

        self.cam_btn = MPushButton(u'创建360度相机')
        self.cam_btn.setMaximumWidth(185)

        self.selected_lay = QtWidgets.QGridLayout()
        self.selected_lay.addLayout(self.size_lay, 1, 1)
        self.selected_lay.addLayout(self.out_lay, 1, 2)
        self.selected_lay.addLayout(self.frame_lay, 1, 3)
        self.selected_lay.addLayout(self.cam_lay, 2, 1)
        self.selected_lay.addLayout(self.color_lay, 2, 2)
        self.selected_lay.addLayout(self.font_lay, 2, 3)
        self.selected_lay.addWidget(self.cam_btn, 3, 1)

        self.folder_button = MClickBrowserFolderToolButton().huge()
        self.folder_lineedit = MLineEdit().small()
        self.folder_layout = QtWidgets.QHBoxLayout()
        self.folder_layout.addWidget(self.folder_lineedit)
        self.folder_layout.addWidget(self.folder_button)

        self.filename_lineeit = MLineEdit().small()
        self.filename_lineeit.setMaximumWidth(350)
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.addRow(MLabel(u'文件名:'), self.filename_lineeit)
        self.form_layout.addRow(MLabel(u'输出路径:'), self.folder_layout)


        self.run_btn = MPushButton(u'拍屏')

        self.model_editor_widget = self.create_model_widget()
        self.model_editor_widget.setParent(self)
        self.model_editor_widget.setObjectName("model_editor_widget")
        self.fix_size(self.model_editor_widget)

        self.model_editor_layout = QtWidgets.QHBoxLayout()
        self.model_editor_layout.addStretch()
        self.model_editor_layout.addWidget(self.model_editor_widget)
        self.model_editor_layout.addStretch()

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(self.model_editor_layout)
        main_lay.addWidget(self.slider)
        main_lay.addWidget(MDivider(u"设置水印信息"))
        main_lay.addWidget(self.collapse)
        main_lay.addWidget(MDivider(""))
        # main_lay.addWidget(self.create_cam_checkbox)
        main_lay.addLayout(self.show_lay)
        main_lay.addLayout(self.selected_lay)
        main_lay.addWidget(MDivider(""))
        main_lay.addLayout(self.form_layout)
        # main_lay.addWidget(self.cam_btn)
        main_lay.addWidget(self.run_btn)

        self.setLayout(main_lay)

    def _init_ui_data(self):
        # 初始化信息的时候，应该是获取工程里面现有信息，填写到界面，目的是方便用户不用反复填写默认信息。
        # 后面会根据界面的修改，再修改水印信息，支持用户自定义。

        # 获取首尾帧
        start, end = self.get_playbackOptions()
        # 获取文件名和路径名。
        path_, self.name_ = self.get_project_path()

        self.slider.setRange(start, end)
        current_time1 = int(cmds.currentTime(q=1))
        self.slider.setValue(current_time1)
        self.frame_start_line.setText(str(start))
        self.frame_end_line.setText(str(end))

        self.filename_lineeit.setText(self.name_)
        self.folder_lineedit.setText(path_)

        for shape in cmds.ls(cameras=True):
            trans = cmds.listRelatives(shape, p=True)[0]
            self.cam_combobox.addItem(trans, shape)
        # 字号
        self.font_size_spinbox.setValue(1)
        # 初始化水印信息
        self.set_mask_text()

    def set_mask_text(self):
        # 水印信息的初始化问题
        # 日期
        tct_txt = u"{}".format(datetime.now().strftime("%Y/%m/%d"))
        start, end = self.get_playbackOptions()
        frame = '-'.join([str(start), str(end)])
        frame_info = frame
        uer = getpass.getuser()
        current_frame = int(cmds.currentTime(query=True))

        cmds.setAttr("{}.topLeftText".format(self._zshotmask), str(self.name_), typ="string")
        cmds.setAttr("{}.topCenterText".format(self._zshotmask), u"", typ="string")
        cmds.setAttr("{}.topRightText".format(self._zshotmask), uer, typ="string")
        cmds.setAttr("{}.bottomLeftText".format(self._zshotmask), frame_info, typ="string")
        cmds.setAttr("{}.bottomCenterText".format(self._zshotmask), tct_txt, typ="string")
        cmds.setAttr("{}.bottomRightText".format(self._zshotmask), current_frame, typ="string")

        # 添加遮幅描述的信号
        for row, row_ls in enumerate(self.font_edit):
            for index, font_edit in enumerate(row_ls):
                text = cmds.getAttr("{}.{}".format(self._zshotmask, font_edit))
                edit = getattr(self, font_edit)
                # print(type(text), text.encode('ascii', 'ignore').decode('ascii'))
                edit.setText(text.encode('ascii', 'ignore').decode('ascii'))

    def bind_function(self):
        # format_combobox信息的修改
        self.size_menu._action_group.triggered.connect(
            lambda action: self.select_config(action, self.size_combobox))
        self.color_menu._action_group.triggered.connect(
            lambda action: self.select_config(action, self.color_combobox))
        self.format_menu._action_group.triggered.connect(
            lambda action: self.select_config(action, self.format_combobox))

        # 文件夹按钮选择文件夹，会将文件夹信息写到line_edit中
        self.folder_button.sig_folder_changed.connect(self.folder_lineedit.setText)
        # 滑块
        self.slider.valueChanged.connect(self.change_time)
        # 相机
        self.cam_combobox.currentIndexChanged.connect(self.change_camera)
        # 字号
        self.font_size_spinbox.valueChanged.connect(self.change_font_size)
        # 抗锯齿
        self.smooth_check_box.stateChanged.connect(self.change_anti_aliasing)
        # 灯光
        self.light_check_box.stateChanged.connect(self.change_lighting)
        # 贴图
        self.srf_check_box.stateChanged.connect(self.change_texture)

        # 修改首尾帧设置同时修改UI中的滑块
        self.frame_start_line.returnPressed.connect(self.set_start_frame_text)
        # self.frame_start_line.textChanged.connect(self.change_slider_range)
        self.frame_end_line.returnPressed.connect(self.set_end_frame_text)
        # self.frame_end_line.textChanged.connect(self.change_slider_range)

        # 创建相机命令
        self.cam_btn.clicked.connect(self.create_360_cam)
        # 拍屏命令
        self.run_btn.clicked.connect(self.play_blast)

    def select_config(self, action, combobox):
        if action.isChecked():
            combobox._set_value(action.text())

    def create_collapse(self):
        mask_widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(mask_widget)
        for row, row_ls in enumerate(self.font_edit):
            for index, font_edit in enumerate(row_ls):
                edit = MLineEdit()
                edit.textChanged.connect(partial(self.change_mask_text, font_edit))
                setattr(self, font_edit, edit)
                layout.addWidget(getattr(self, font_edit), row, index)
        return mask_widget

    def set_start_frame_text(self):
        # # 设置播放范围的最小值
        start_1 = self.frame_start_line.text()
        print(start_1)
        pm.playbackOptions(min=int(start_1))
        self.slider.setMinimum(int(start_1))

    def set_end_frame_text(self, *args):
        end_1 = self.frame_end_line.text()
        print(end_1)
        pm.playbackOptions(max=int(end_1))
        self.slider.setMaximum(int(end_1))

    def create_360_cam(self):
        cam = make_suitable_camera()

        # 设置相机360度动画
        start_time = self.frame_start_line.text()
        end_time = self.frame_end_line.text()
        cmds.currentTime(start_time, edit=True)
        cmds.setKeyframe("{}.rx".format(cam), "{}.ry".format(cam), "{}.rz".format(cam))
        cmds.currentTime(end_time, edit=True)
        cmds.setAttr("{}.rotateY".format(cam), 360)
        cmds.setKeyframe("{}.rx".format(cam), "{}.ry".format(cam), "{}.rz".format(cam))
        # self.cam_combobox.clear()
        # for shape in cmds.ls(cameras=True):
        #     trans = cmds.listRelatives(shape, p=True)[0]
        #     self.cam_combobox.addItem(trans, shape)

        # 进入相机视角
        # cmds.lookThru("{}".format(cam))
        # 创建以后就要刷新上面的相机
        # 此处还需要修改上面的相机设置
        # self.cam_combobox.set_value('scene_name1')

        cmds.modelEditor(self._model_editor, edit=True, camera='scene_name1')

    def fix_size(self, widget):
        w, h = get_desk_resolution()
        if 2560 < w < 3840:
            weight = 1022

        elif w >= 3840:
            weight = 1534

        else:
            weight = 766

        height = int(weight / float("%.4f" % get_dar()))
        widget.setFixedWidth(weight)
        widget.setFixedHeight(height)

    def get_project_path(self):
        # 得到当前的工程名字还有路径
        porj_path, file_name = os.path.split(cmds.file(q=True, sn=True))
        porj_name = file_name.split('.')[0]
        return porj_path, porj_name

    def get_playbackOptions(self):
        # 获取当前maya间滑块的起始时间还有结束时间
        start = int(cmds.playbackOptions(minTime=1, q=1))
        end = int(cmds.playbackOptions(maxTime=1, q=1))
        return start, end

    def get_cam(self):
        # 得到当前工程内的所有相机
        all_cam = cmds.ls(cameras=True, )
        cam_list = []
        for shape in all_cam:
            trans = cmds.listRelatives(shape, p=True)[0]
            cam_list.append(trans)
        return cam_list

    def create_model_widget(self):
        if cmds.window("ModelEditor", exists=True):
            cmds.deleteUI("ModelEditor")

        window1 = cmds.window('ModelEditor')
        form = cmds.formLayout()
        # 创建一个新的模型编辑器
        self._model_editor = cmds.modelEditor()

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

    def change_time(self, value):
        """
        设置滑块控制视口,还有屏幕内显示得帧速率
        """
        cmds.currentTime(value)
        padding = 5 if value < 0 else 4
        current_time = "{}".format(value).zfill(padding)
        cmds.setAttr("{}.bottomRightText".format(self._zshotmask), current_time, typ="string")

        # start, end = self.get_playbackOptions()
        # start_time = int(self.frame_start_line.text())
        # end_time = int(self.frame_end_line.text())
        # frame = '-'.join([str(start_time), str(end_time)])
        #
        # padding = 5 if value < 0 else 4
        # current_time = "{}".format(value).zfill(padding)
        # frame_info = frame + '/' + current_time
        # cmds.setAttr("{}.bottomLeftText".format(self._zshotmask), frame_info, typ="string")

    def change_font_size(self, value):
        """
        改变字体
        :param value: [int]
        """
        cmds.setAttr("{}.fontScale".format(self._zshotmask), value)

    @classmethod
    def change_anti_aliasing(cls, value):
        v = True if value == 2 else False
        cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", v)

    def change_lighting(self, value):
        v = "all" if value == 2 else "default"
        cmds.modelEditor(self._model_editor, edit=True, displayLights=v)

    def change_camera(self, index):

        """
        Set model editor's camera.

        :param index: [QtCore.QIndex]
        """
        camera_shape = self.cam_combobox.itemData(index)
        cmds.modelEditor(self._model_editor, edit=True, camera=camera_shape)

    def change_texture(self, value):
        """
        Shot model editor's texture.
        :param value: [int]
        """
        v = True if value == 2 else False
        cmds.modelEditor(self._model_editor, edit=True, displayTextures=v)

    def change_mask_text(self, index, text):
        """
        Change the text of mask by index.

        :param index: [str] The attributes to change.
        :param text: [str] To display.
        """
        cmds.setAttr("{}.{}".format(self._zshotmask, index), text, typ="string")

    def create_360_cam(self):
        cam = make_suitable_camera()
        # 设置相机360度动画
        start_time = self.frame_start_line.text()
        end_time = self.frame_end_line.text()
        cmds.currentTime(start_time, edit=True)
        cmds.setKeyframe("{}.rx".format(cam), "{}.ry".format(cam), "{}.rz".format(cam))
        cmds.currentTime(end_time, edit=True)
        cmds.setAttr("{}.rotateY".format(cam), 360)
        cmds.setKeyframe("{}.rx".format(cam), "{}.ry".format(cam), "{}.rz".format(cam))

        cmds.modelEditor(self._model_editor, edit=True, camera='scene_name1')

        self.cam_combobox.clear()
        for shape in cmds.ls(cameras=True):
            trans = cmds.listRelatives(shape, p=True)[0]
            self.cam_combobox.addItem(trans, shape)

        # 进入相机视角
        # cmds.lookThru("{}".format(cam))
        # 创建以后就要刷新上面的相机
        # 此处还需要修改上面的相机设置
        self.cam_combobox.set_value('scene_name1')

    def play_blast(self):
        """
        Playblast with some tags.

        :returns:[str] The sequence if the video type is "mov", such as "D:\temp\PPP\images\EP02_SC07_Ani.####.tif".

        """
        # Check if filling the output folder or file name.
        # 没有路径和文件名直接报个窗口,此处不写也行作为优化项
        output_folder = self.folder_lineedit.text()
        file_name = self.filename_lineeit.text()
        if not output_folder or not file_name:
            return
        # 组成一个文件路径
        video_type = self.format_combobox.currentText()
        if video_type == 'mov':
            fmt = "qt"
            compression = "Video"
        else:
            fmt = "avi"
            compression = ""

        ouput_path = os.path.join(output_folder, file_name + '.' + video_type)

        # Get play blast tags from ui.
        start_time = int(self.frame_start_line.text())
        end_time = int(self.frame_end_line.text())

        if self.size_combobox.currentText() == u"full":
            resolution = get_resolution()
        else:
            resolution = get_resolution(half=True)

        pm.playblast(editorPanelName=self._model_editor, startTime=start_time, endTime=end_time, filename=ouput_path,
                     forceOverwrite=True, viewer=False, format=fmt, percent=100, quality=100,
                     clearCache=False, widthHeight=resolution, compression=compression)

    def closeEvent(self, *args):
        # Delete widget.
        if cmds.window(self._model_editor, exists=True):
            cmds.deleteUI(self._model_editor)
        delete_shotmask()
        # 此处删除掉创建的360相机
        cameras = cmds.ls(type='camera')
        for camera in cameras:
            transform = cmds.listRelatives(camera, parent=True)[0]
            if 'scene_name' in transform:
                transform = cmds.listRelatives(camera, parent=True)[0]
                cmds.delete(transform)


def main():
    node = create_shot_mask()
    init_shot_mask(node)

    maya_window = maya_main_window()
    win = MaskWindow(node, parent=maya_window)
    dayu_theme.apply(win)
    win.show()



if __name__ == "__main__":
    main()