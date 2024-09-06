# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

# Import built-in modules
import os
import sys
import getpass
import subprocess
import shutil
import tempfile
from functools import partial
from datetime import datetime
import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

try:
    from shiboken import wrapInstance
except ImportError:
    from shiboken2 import wrapInstance

# Import third-party modules
from Qt import QtWidgets, QtCore, QtGui
from dayu_widgets.slider import MSlider
from dayu_widgets.label import MLabel
from dayu_widgets.spin_box import MDoubleSpinBox
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.collapse import MCollapse
from dayu_widgets import dayu_theme

FFMPEG = os.path.join(os.path.dirname(__file__), "ffmpeg.exe")


def maya_main_window(typ=QtWidgets.QWidget):
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), typ)


def window_to_qt(window):
    ptr = omui.MQtUtil.findControl(window)
    return wrapInstance(long(ptr), QtWidgets.QWidget)


def get_cameras():
    return cmds.ls(cameras=True)


def create_shot_mask():
    delete_shotmask()
    plugin = "zshotmask.py"
    if not cmds.pluginInfo(plugin, q=True, loaded=True):
        cmds.loadPlugin(plugin)

    return cmds.createNode("zshotmask")


def change_time(value):
    """
    Change time slider.
    :param value: [int]
    """
    cmds.currentTime(value)


def change_fps(node):
    t = int(cmds.currentTime(q=True))
    cmds.setAttr("{}.bottomRightText".format(node), "{0}".format(t).zfill(4), typ="string")


def init_shot_mask(node):
    cmds.setAttr("{}.borderAlpha".format(node), 0.3)
    cmds.setAttr("{}.fontScale".format(node), 0.63)
    cmds.setAttr("{}.fontColorR".format(node), 1)
    cmds.setAttr("{}.fontColorG".format(node), 0.647)
    cmds.setAttr("{}.fontColorB".format(node), 0)


def get_resolution(half=False):
    res_x = pm.general.getAttr('defaultResolution.width')
    res_y = pm.general.getAttr('defaultResolution.height')
    if half:
        return res_x / 2, res_y / 2
    else:
        return res_x, res_y


def get_dar():
    dar = pm.general.getAttr('defaultResolution.deviceAspectRatio')
    return float("%.4f" % dar)


def get_active_camera():
    activeCamera = om.MDagPath()
    omui.M3dView().active3dView().getCamera(activeCamera)
    return activeCamera.fullPathName()


def make_dirs(directory):
    result = True
    try:
        os.makedirs(directory)
    except Exception, e:
        pm.confirmDialog(message=u"无法创建文件夹: " + directory + '\n' + str(e))
        result = False

    return result


def add_script_job(func, event="timeChanged"):
    _id = cmds.scriptJob(event=[event, func])
    return _id


def imgs_to_videos(images, output, start_number=0, fps=30):
    """
    Convert images to videos by ffmpeg.

    :param images: [str] Such as "D:/aa.####.jpg"
    :param output: [str] The file path to output.
    :param start_number: [int] From which frame to Convert the video.
    :param fps: [str] Frame rate of the video

    :return: [bool] Return True if successful, otherwise False.
    """
    if os.path.exists(output):
        os.remove(output)

    cmd_str = '{ffmpeg} -framerate {fps} -start_number {start_number} -f image2 -i {images} -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" {output}'
    cmd = cmd_str.format(ffmpeg=FFMPEG, fps=fps, images=images, output=output, start_number=start_number)
    print(cmd)

    sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = sp.communicate()
    if err:
        from pprint import pprint
        pprint(err)


def delete_shotmask():
    """
    Delete all shotmask nodes.
    """
    shot_mask_nodes = cmds.ls("zshotmask*")
    for i in shot_mask_nodes:
        trf = cmds.listRelatives(i, p=1)
        cmds.delete(trf)


def get_desk_resolution(typ=QtWidgets.QApplication):
    app = maya_main_window(typ)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    return width, height


def check_exists(object_name="MyMaskWindow"):
    for obj in maya_main_window().children():
        if obj.objectName() == object_name:
            obj.setParent(None)
            obj.deleteLater()


class MaskWindow(QtWidgets.QDialog):

    def __init__(self, zshotmask, parent=None):
        super(MaskWindow, self).__init__(parent)

        # Set class properties.
        self._zshotmask = zshotmask
        self.model_editor_widget = ""
        self._model_editor = ""
        self.font_edit = [
            ["topLeftText", "topCenterText", "topRightText"],
            ["bottomLeftText", "bottomCenterText", "bottomRightText"]
        ]
        self.settings = os.path.join(cmds.internalVar(usd=True), "mf_playblast.ini")

        # Set widget attributes.
        self.setWindowTitle(u"魔术师拍屏霸王")
        self.setObjectName("MyMaskWindow")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Execute functions.
        self._init_ui()
        self.bind_func()
        self._init_ui_data()

    def _init_ui(self):
        self.model_editor_widget = self.create_model_widget()
        self.model_editor_widget.setParent(self)
        self.model_editor_widget.setObjectName("model_editor_widget")
        self.fix_size(self.model_editor_widget)

        self.slider = MSlider(QtCore.Qt.Horizontal)

        self.collapse = self.create_collapse(expand=False)

        font_size_lab = MLabel(u"字体大小：")
        self.font_size_spinbox = QtWidgets.QDoubleSpinBox()
        self.font_size_spinbox.setRange(0.01, 2)
        self.font_size_spinbox.setSingleStep(0.02)
        self.font_size_spinbox.setMinimumWidth(80)
        proj_lab = MLabel(u"项目名称：")
        self.proj_line = MLineEdit().large()
        h_lay1 = QtWidgets.QHBoxLayout()
        h_lay1.addWidget(font_size_lab)
        h_lay1.addWidget(self.font_size_spinbox)
        h_lay1.addWidget(proj_lab)
        h_lay1.addWidget(self.proj_line)

        seq_size_lab = MLabel(u"场次名：")
        self.seq_line = MLineEdit(u"第一场")
        shot_size_lab = MLabel(u"镜头名：")
        self.shot_line = MLineEdit(u"第一镜")
        h_lay2 = QtWidgets.QHBoxLayout()
        h_lay2.addWidget(seq_size_lab)
        h_lay2.addWidget(self.seq_line)
        h_lay2.addWidget(shot_size_lab)
        h_lay2.addWidget(self.shot_line)

        fame_lab = MLabel(u"帧范围：")
        self.frame_start_line = MLineEdit()
        _lab = MLabel("- ")
        self.frame_end_line = MLineEdit()
        cam_lab = MLabel(u"摄像机：")
        self.cam_comb = MComboBox()
        h_lay3 = QtWidgets.QHBoxLayout()
        h_lay3.addWidget(fame_lab)
        h_lay3.addWidget(self.frame_start_line)
        h_lay3.addWidget(_lab)
        h_lay3.addWidget(self.frame_end_line)
        h_lay3.addWidget(cam_lab)
        h_lay3.addWidget(self.cam_comb)

        size_lab = MLabel(u"尺寸：")
        self.size_comb = MComboBox()
        colorspace_lab = MLabel(u"色彩空间：")
        self.color_comb = MComboBox()
        type_lab = MLabel(u"视频格式：")
        self.type_comb = MComboBox()
        self.anti_aliasing = MCheckBox(u"抗锯齿")
        self.lighting = MCheckBox(u"照明")
        self.texture = MCheckBox(u"贴图")
        self.curve = MCheckBox(u"曲线")
        h_lay4 = QtWidgets.QHBoxLayout()
        h_lay4.addWidget(size_lab)
        h_lay4.addWidget(self.size_comb)
        h_lay4.addWidget(colorspace_lab)
        h_lay4.addWidget(self.color_comb)
        h_lay4.addWidget(type_lab)
        h_lay4.addWidget(self.type_comb)
        h_lay4.addWidget(self.anti_aliasing)
        h_lay4.addWidget(self.lighting)
        h_lay4.addWidget(self.texture)
        h_lay4.addWidget(self.curve)

        output_lab = MLabel(u"输出路径：")
        self.output_line = MLineEdit().folder().large()
        self.create_folder = MCheckBox(u"创建文件夹")
        self.create_folder.setChecked(True)
        self.gen_images = MCheckBox(u"生成序列图")
        h_lay5 = QtWidgets.QHBoxLayout()
        h_lay5.addWidget(output_lab)
        h_lay5.addWidget(self.output_line)
        h_lay5.addWidget(self.create_folder)
        h_lay5.addWidget(self.gen_images)

        file_name_lab = MLabel(u"输出文件名：")
        self.file_name_edit = MLineEdit()
        self.file_name_edit.setPlaceholderText(u"文件名，禁止中文")
        h_lay6 = QtWidgets.QHBoxLayout()
        h_lay6.addWidget(file_name_lab)
        h_lay6.addWidget(self.file_name_edit)

        self.play_btn = QtWidgets.QPushButton(u"开始拍屏")
        self.play_btn.setStyleSheet("background-color:#ff9900; color:black")
        self.play_btn.setMinimumHeight(200)
        self.play_btn.setMinimumWidth(200)
        tip_lab = MLabel(u'* 输出路径和文件名禁止包含中文 *')

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addLayout(h_lay1)
        left_layout.addLayout(h_lay2)
        left_layout.addLayout(h_lay3)
        left_layout.addLayout(h_lay4)
        left_layout.addLayout(h_lay5)
        left_layout.addLayout(h_lay6)
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addLayout(left_layout)
        h_layout.addWidget(self.play_btn)

        v_layout = QtWidgets.QVBoxLayout(self)
        v_layout.addWidget(self.model_editor_widget)
        v_layout.addWidget(self.slider)
        v_layout.addWidget(self.collapse)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(tip_lab, alignment=QtCore.Qt.AlignCenter)

        self.load_state()

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

    def _init_ui_data(self):
        """
        Initialize UI data.
        """
        start = int(cmds.playbackOptions(minTime=1, q=1))
        end = int(cmds.playbackOptions(maxTime=1, q=1))

        # Set mask font size.
        self.font_size_spinbox.setValue(0.5)

        # Set slider value.
        self.slider.setRange(start, end)
        current_time = int(cmds.currentTime(q=1))
        self.slider.setValue(current_time)

        # Set output size.
        self.size_comb.addItems([u"完整尺寸", u"一半尺寸"])

        # Set frame range.
        self.frame_start_line.setText(str(start))
        self.frame_end_line.setText(str(end))

        # Set camera.
        for shape in get_cameras():
            trans = cmds.listRelatives(shape, p=True)[0]
            self.cam_comb.addItem(trans, shape)

        # Set color space.
        self.color_comb.addItems(["sRGB gamma", "Raw"])

        # Set video type.
        self.type_comb.addItems(["mov", "avi"])

        # Set file name.
        scene_name = cmds.file(sceneName=True, q=True)
        if scene_name:
            file_name = os.path.basename(scene_name).split(".")[0]
            self.file_name_edit.setText(file_name)

        # NOTE: Set shot mask text.
        self.set_mask_text()

    def bind_func(self):
        """ Bind functions. """
        self.slider.valueChanged.connect(self.change_time)
        self.font_size_spinbox.valueChanged.connect(self.change_mask_size)
        self.proj_line.textChanged.connect(self.set_mask_text)
        self.seq_line.textChanged.connect(self.set_mask_text)
        self.shot_line.textChanged.connect(self.set_mask_text)
        self.frame_start_line.textChanged.connect(self.set_mask_text)
        self.frame_start_line.textChanged.connect(self.change_slider_range)
        self.frame_end_line.textChanged.connect(self.set_mask_text)
        self.frame_end_line.textChanged.connect(self.change_slider_range)
        self.cam_comb.currentIndexChanged.connect(self.change_camera)
        self.color_comb.currentTextChanged.connect(self.change_color_space)
        self.anti_aliasing.stateChanged.connect(self.change_anti_aliasing)
        self.lighting.stateChanged.connect(self.change_lighting)
        self.texture.stateChanged.connect(self.change_texture)
        self.curve.stateChanged.connect(self.change_curve)
        self.play_btn.clicked.connect(self.play_blast)

    def closeEvent(self, *args):
        """ Execute code after close window. """
        # Delete widget.
        if cmds.window(self._model_editor, exists=True):
            cmds.deleteUI(self._model_editor)

        # Delete zshotmask* nodes.
        delete_shotmask()

        # Cache user setting.
        self.save_state()

    def set_mask_text(self):
        """ Set shot mask text one by one, and update line edit. """

        cmds.setAttr("{}.topLeftText".format(self._zshotmask), u"魔方工作室", typ="string")

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

    def create_collapse(self, expand=False):
        """
        Create collapse widget.

        :param expand: [bool] If expanded the collapse

        :returns: The instance of MCollapse.
        """
        mask_widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(mask_widget)
        for row, row_ls in enumerate(self.font_edit):
            for index, font_edit in enumerate(row_ls):
                edit = MLineEdit()
                edit.textChanged.connect(partial(self.change_mask_text, font_edit))
                setattr(self, font_edit, edit)
                layout.addWidget(getattr(self, font_edit), row, index)

        section_list = [
            {"title": "设置水印", "expand": expand, "widget": mask_widget},
        ]

        section_group = MCollapse()
        section_group.add_section_list(section_list)
        return section_group

    def create_model_widget(self, camera="persp"):
        """
         Create model editor and return QtWidget of it.

        :param camera: [str]

        :returns: The instance of ModelEditor.
        """
        if cmds.window("ModelEditor", exists=True):
            cmds.deleteUI("ModelEditor")

        window = cmds.window('ModelEditor')
        form = cmds.formLayout()
        self._model_editor = cmds.modelEditor()
        column = cmds.columnLayout('true')
        cmds.formLayout(form, edit=True,
                        attachForm=[(column, 'top', 0), (column, 'left', 0), (self._model_editor, 'top', 0),
                                    (self._model_editor, 'bottom', 0), (self._model_editor, 'right', 0)],
                        attachNone=[(column, 'bottom'), (column, 'right')],
                        attachControl=(self._model_editor, 'left', 0, column))
        current_cam = camera if camera else cmds.modelEditor("modelPanel4", q=1, av=1, cam=1)
        cam_shape = cmds.listRelatives(current_cam, s=True)[0]
        cmds.setAttr("{}.overscan".format(cam_shape), 1)
        cmds.modelEditor(self._model_editor, edit=True, allObjects=False)
        cmds.modelEditor(self._model_editor, edit=True, camera=current_cam, imagePlane=True,
                         displayAppearance='smoothShaded', hud=0, polymeshes=True)

        return window_to_qt(window)

    def change_time(self, value):
        """
        Change time slider.
        :param value: [int]
        """
        cmds.currentTime(value)

        padding = 5 if value < 0 else 4
        current_time = "{}".format(value).zfill(padding)
        cmds.setAttr("{}.bottomRightText".format(self._zshotmask), current_time, typ="string")

    def change_mask_text(self, index, text):
        """
        Change the text of mask by index.

        :param index: [str] The attributes to change.
        :param text: [str] To display.
        """
        cmds.setAttr("{}.{}".format(self._zshotmask, index), text, typ="string")

    def change_mask_size(self, value):
        """
        Change the size of mask fonts

        :param value: [int]
        """
        cmds.setAttr("{}.fontScale".format(self._zshotmask), value)

    def change_color_space(self, text):
        """
        Change the colorspace

        :param text: [str] "Raw/SRGB gamma".
        """
        cmds.colorManagementPrefs(e=True, viewTransformName=text)

    def change_slider_range(self, *args):
        start_time = self.frame_start_line.text()
        end_time = self.frame_end_line.text()
        if start_time and end_time:
            self.slider.setRange(int(start_time), int(end_time))

    def change_camera(self, index):
        """
        Set model editor's camera.

        :param index: [QtCore.QIndex]
        """
        camera_shape = self.cam_comb.itemData(index)
        cmds.modelEditor(self._model_editor, edit=True, camera=camera_shape)

    def change_lighting(self, value):
        """
        Set model editor light type.

        :param value: [int]
        """
        v = "all" if value == 2 else "default"
        cmds.modelEditor(self._model_editor, edit=True, displayLights=v)

    def change_texture(self, value):
        """
        Shot model editor's texture.

        :param value: [int]
        """
        v = True if value == 2 else False
        cmds.modelEditor(self._model_editor, edit=True, displayTextures=v)

    def change_curve(self, value):
        """
        Shot model editor's curve.

        :param value: [int]
        """
        v = True if value == 2 else False
        cmds.modelEditor(self._model_editor, edit=True, nurbsCurves=v)

    @classmethod
    def change_anti_aliasing(cls, value):
        v = True if value == 2 else False
        cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", v)

    def play_blast(self):
        """
        Playblast with some tags.

        :returns:[str] The sequence if the video type is "mov", such as "D:\temp\PPP\images\EP02_SC07_Ani.####.tif".

        """
        # Check if filling the output folder or file name.
        output_folder = self.output_line.text()
        file_name = self.file_name_edit.text()
        if not output_folder or not file_name:
            return

        # Create folder with file name.
        if self.create_folder.isChecked():
            output_folder = os.path.join(output_folder, file_name)
            if os.path.exists(output_folder):
                shutil.rmtree(output_folder)
            os.makedirs(output_folder)

        # Get play blast tags from ui.
        start_time = self.frame_start_line.text()
        end_time = self.frame_end_line.text()
        if self.size_comb.currentText() == u"完整尺寸":
            resolution = get_resolution()
        else:
            resolution = get_resolution(half=True)
        video_type = self.type_comb.currentText()

        # Playblast by frames.
        compression = "jpg"
        fmt = "image"
        temp_img_dir = os.path.join(tempfile.gettempdir(), "m_pb_images")
        if os.path.exists(temp_img_dir):
            shutil.rmtree(temp_img_dir)
        temp_img_path = os.path.join(temp_img_dir, file_name)
        print('***'*10)
        print('temp_img_path', temp_img_path)
        for frame in range(int(start_time), int(end_time) + 1):
            self.slider.setValue(frame)
            fp = 5 if frame < 0 else 4
            pm.playblast(editorPanelName=self._model_editor, startTime=frame, endTime=frame, filename=temp_img_path,
                         forceOverwrite=True, viewer=False, format=fmt, percent=100, quality=100,
                         clearCache=False, widthHeight=resolution, compression=compression, fp=fp)

        # Convert images to videos.
        img = temp_img_path + ".%04d.jpg"
        video_path = os.path.join(output_folder, "{}.{}".format(file_name, video_type))
        print('video_path', video_path)
        imgs_to_videos(img, video_path, start_number=start_time)
        if os.path.exists(video_path):
            cmd = "start {}".format(video_path)
            subprocess.Popen(cmd, shell=True)

        # Copy images.
        if self.gen_images.isChecked():
            img_dir = os.path.join(output_folder, "images")
            shutil.copytree(temp_img_dir, img_dir)

    def save_state(self):
        settings = QtCore.QSettings(self.settings, QtCore.QSettings.IniFormat)
        settings.beginGroup("Playblast")
        settings.setValue("proj_name", self.proj_line.text())
        settings.endGroup()

    def load_state(self):
        settings = QtCore.QSettings(self.settings, QtCore.QSettings.IniFormat)
        settings.beginGroup("Playblast")
        labels = settings.value("proj_name")
        settings.endGroup()

        if labels:
            self.proj_line.setText(labels)


def main():
    # Create shot mask
    node = create_shot_mask()
    init_shot_mask(node)

    # Set font family
    font_path = os.path.join(os.path.dirname(__file__), "data/Alibaba-PuHuiTi-Medium.ttf")
    _id = QtGui.QFontDatabase.addApplicationFont(font_path)
    dayu_theme.font_family = "Alibaba PuHuiTi M"
    dayu_theme.font_size_base = 18

    # Show window
    check_exists()
    maya_window = maya_main_window()
    win = MaskWindow(node, parent=maya_window)
    dayu_theme.apply(win)
    win.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([""])
    main()
    sys.exit(app.exec_())
