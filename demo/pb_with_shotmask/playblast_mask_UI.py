# -*- coding: utf-8 -*-
from Qt import QtWidgets, QtCore
from dayu_widgets import dayu_theme
from dayu_widgets.label import MLabel
from dayu_widgets.divider import MDivider
from dayu_widgets.menu import MMenu
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.slider import MSlider
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.push_button import MPushButton
from dayu_widgets.spin_box import MSpinBox
from dayu_widgets.browser import MClickBrowserFolderToolButton
# from ui_center.resource_widget.warning_dialod import MErrorMessageBox, MSuccessMessageBox
from shiboken2 import wrapInstance
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import pymel.core as pm
import maya.OpenMaya as om


def maya_main_window(typ=QtWidgets.QWidget):
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), typ)

def window_to_qt(window):
    ptr = omui.MQtUtil.findControl(window)
    return wrapInstance(int(ptr), QtWidgets.QWidget)

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


class MaskWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MaskWindow, self).__init__(parent)
        self.setWindowTitle(self.tr(u'拍屏工具'))
        self.resize(950, 750)
        self._init_ui()
        self.bind_function()
        self._init_ui_data()
    def _init_ui(self):
        # 给进度条
        self.slider = MSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(1, 100)

        # 设置水印的 lineedit
        self.line_edit_lay = QtWidgets.QGridLayout()
        l_s = MLineEdit().small()
        l_x = MLineEdit().small()
        m_s = MLineEdit().small()
        m_x = MLineEdit().small()
        r_s = MLineEdit().small()
        r_x = MLineEdit().small()
        self.line_edit_lay.addWidget(l_s, 1, 1)
        self.line_edit_lay.addWidget(l_x, 1, 2)
        self.line_edit_lay.addWidget(m_s, 1, 3)
        self.line_edit_lay.addWidget(m_x, 2, 1)
        self.line_edit_lay.addWidget(r_s, 2, 2)
        self.line_edit_lay.addWidget(r_x, 2, 3)

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
                font-size: 10px; /* 设置标题的字号 */
            }
        """

        self.check_item_groupBox = QtWidgets.QGroupBox(u'设置水印')
        self.check_item_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.check_item_groupBox.setMaximumHeight(100)
        self.check_item_groupBox.setStyleSheet(grp_style_sheet)
        self.check_item_groupBox.setLayout(self.line_edit_lay)

        # 显示信息的checkbox
        self.light_check_box = MCheckBox(u"灯光")
        self.srf_check_box = MCheckBox(u"贴图")
        self.curve_check_box = MCheckBox(u"曲线")
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

        self.font_size_lab = MLabel(u"字号：")
        self.font_size_spinbox = MSpinBox().small()
        self.font_size_spinbox.setValue(1)
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

        self.camera = MLabel(u"摄像机：")
        self.cam_menu = MMenu(exclusive=False, parent=self)
        self.cam_combobox = MComboBox().small()
        self.cam_combobox.setMinimumWidth(118)
        self.cam_combobox._root_menu = self.cam_menu
        self.cam_lay = QtWidgets.QHBoxLayout()
        self.cam_lay.addWidget(self.camera)
        self.cam_lay.addWidget(self.cam_combobox)
        self.cam_lay.addStretch()

        self.frame_range = MLabel(u"帧范围：")
        self.start = MLineEdit().small()
        self.start.setMaximumWidth(45)
        self.end = MLineEdit().small()
        self.end.setMaximumWidth(45)
        _lab = MLabel("-")

        self.frame_lay = QtWidgets.QHBoxLayout()
        self.frame_lay.addWidget(self.frame_range)
        self.frame_lay.addWidget(self.start)
        self.frame_lay.addWidget(_lab)
        self.frame_lay.addWidget(self.end)
        self.frame_lay.addStretch()

        self.selected_lay = QtWidgets.QGridLayout()
        self.selected_lay.addLayout(self.size_lay, 1, 1)
        self.selected_lay.addLayout(self.out_lay, 1, 2)
        self.selected_lay.addLayout(self.frame_lay, 1, 3)
        self.selected_lay.addLayout(self.cam_lay, 2, 1)
        self.selected_lay.addLayout(self.color_lay, 2, 2)
        self.selected_lay.addLayout(self.font_lay, 2, 3)

        self.folder_button = MClickBrowserFolderToolButton().huge()
        self.folder_lineedit = MLineEdit().small()
        self.folder_layout = QtWidgets.QHBoxLayout()
        self.folder_layout.addWidget(self.folder_lineedit)
        self.folder_layout.addWidget(self.folder_button)

        self.file_name = MLineEdit().small()
        self.file_name.setMaximumWidth(350)
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.addRow(MLabel(u'文件名:').h4(), self.file_name)
        self.form_layout.addRow(MLabel(u'输出路径:').h4(), self.folder_layout)

        self.run_btn = MPushButton(u'拍屏')

        self.model_editor_widget = self.create_model_widget()
        self.model_editor_widget.setParent(self)
        self.model_editor_widget.setObjectName("model_editor_widget")
        self.fix_size(self.model_editor_widget)

        self.model_editor_layout = QtWidgets.QHBoxLayout()
        self.model_editor_layout.addStretch()
        self.model_editor_layout.addWidget(self.model_editor_widget)
        self.model_editor_layout.addStretch()

        # 给进度条
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addLayout(self.model_editor_layout)
        main_lay.addWidget(self.slider)
        main_lay.addWidget(self.check_item_groupBox)
        main_lay.addLayout(self.show_lay)
        main_lay.addWidget(MDivider(""))
        main_lay.addLayout(self.selected_lay)
        main_lay.addWidget(MDivider(""))
        main_lay.addLayout(self.form_layout)
        main_lay.addWidget(self.run_btn)

        self.setLayout(main_lay)

    def _init_ui_data(self):
        start, end = self.get_playbackOptions()
        cam_list = self.get_cam()
        path_, name_ = self.get_project_path()

        if start and end:
            self.slider.setRange(start, end)
            current_time = int(cmds.currentTime(q=1))
            self.slider.setValue(current_time)
            print(123)
            self.start.setText(str(start))
            self.end.setText(str(end))
            print(345)
        if path_ and name_:
            self.file_name.setText(name_)
            self.folder_lineedit.setText(path_)
        if cam_list:
            self.cam_menu.set_data(cam_list)
            self.cam_combobox._set_value(cam_list[1])

    def bind_function(self):
        self.cam_menu._action_group.triggered.connect(
            lambda action: self.select_config(action, self.cam_combobox))
        self.size_menu._action_group.triggered.connect(
            lambda action: self.select_config(action, self.size_combobox))
        self.color_menu._action_group.triggered.connect(
            lambda action: self.select_config(action, self.color_combobox))
        self.format_menu._action_group.triggered.connect(
            lambda action: self.select_config(action, self.format_combobox))
        self.folder_button.sig_folder_changed.connect(self.folder_lineedit.setText)

        # 滑块
        self.slider.valueChanged.connect(self.change_time)
        # 抗锯齿
        self.smooth_check_box.stateChanged.connect(self.change_anti_aliasing)
        # 灯光
        self.light_check_box.stateChanged.connect(self.change_lighting)
        # 贴图
        self.srf_check_box.stateChanged.connect(self.change_texture)

    def select_config(self, action, combobox):
        if action.isChecked():
            combobox._set_value(action.text())

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

    def change_time(self, value):
        """
        设置滑块控制视口
        """
        cmds.currentTime(value)

        # padding = 5 if value < 0 else 4
        # current_time = "{}".format(value).zfill(padding)
        # cmds.setAttr("{}.bottomRightText".format(self._zshotmask), current_time, typ="string")

    def get_project_path(self):
        import os
        porj_path, file_name = os.path.split(cmds.file(q=True, sn=True))
        porj_name = file_name.split('.')[0]
        return porj_path, porj_name

    def get_playbackOptions(self):
        # 获取当前maya间滑块的起始时间还有结束时间
        start = int(cmds.playbackOptions(minTime=1, q=1))
        end = int(cmds.playbackOptions(maxTime=1, q=1))
        return start, end

    def get_cam(self):
        all_cam = cmds.ls(cameras=True, )
        cam_list = []
        for shape in all_cam:
            trans = cmds.listRelatives(shape, p=True)[0]
            cam_list.append(trans)
        return cam_list

    def create_model_widget(self, camera="persp"):
        """
         Create model editor and return QtWidget of it.

        :param camera: [str]

        :returns: The instance of ModelEditor.
        """
        if cmds.window("ModelEditor", exists=True):
            cmds.deleteUI("ModelEditor")

        window1 = cmds.window('ModelEditor')
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

        ptr = omui.MQtUtil.findControl(window1)
        return wrapInstance(int(ptr), QtWidgets.QWidget)

    @classmethod
    def change_anti_aliasing(cls, value):
        v = True if value == 2 else False
        cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", v)

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


def main():
    from dayu_widgets.qt import application

    with application() as app:
        test = MaskWindow()
        dayu_theme.apply(test)
        test.show()


if __name__ == "__main__":
    main()