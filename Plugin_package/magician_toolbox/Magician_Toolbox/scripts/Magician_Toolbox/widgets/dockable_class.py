# -*- coding:utf8 -*-
import os
import sys

from Qt import QtGui, QtWidgets, QtCore, QtCompat

try:
    from shiboken import wrapInstance
except ImportError:
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.cmds as cmds


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major>2:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


def maya_api_version():
    return int(cmds.about(api=True))


class MyDockingWindow(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    MAYA2014 = 201400
    MAYA2015 = 201500
    MAYA2016 = 201600
    MAYA2016_5 = 201650
    MAYA2017 = 201700

    def __init__(self, widget, parent=None):

        self.delete_instance()  # remove any instance of this window before starting

        super(MyDockingWindow, self).__init__(parent)

        # 设置属性
        self.setObjectName("MyMainDockingWindow")
        self.setWindowFlags(QtCore.Qt.Tool)

        self.widget = widget
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.widget)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def dockCloseEventTriggered(self):
        """ 停靠窗口关闭时执行该函数 """
        self.delete_instance()

    def hideEvent(self, event):
        self.widget.hideEvent(event)

    def delete_2016(self):
        for obj in maya_main_window().children():
            if str(type(obj)) == "<class 'maya.app.general.mayaMixin.MayaQDockWidget'>":
                if obj.widget().__class__.__name__ == "MyDockingWindow":
                    obj.setParent(None)
                    obj.deleteLater()

    def delete_2017(self):
        for obj in maya_main_window().children():
            if str(type(obj)) == "<class '{}.MyDockingWindow'>".format(os.path.splitext(
                    os.path.basename(__file__)[0])):

                if obj.__class__.__name__ == "MyDockingWindow":
                    obj.setParent(None)
                    obj.deleteLater()

    def run_2016(self):
        self.show(dockable=True, area='right', floating=False)
        self.raise_()
        self.setDockableParameters(width=420)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.setMinimumWidth(420)
        self.setMaximumWidth(600)

    def run_2017(self):
        workspace_control_name = self.objectName() + 'WorkspaceControl'
        self.delete_control(workspace_control_name)
        self.show(dockable=True, area='right', floating=False)
        cmds.workspaceControl(workspace_control_name, e=True, ttc=["AttributeEditor", 0], wp="preferred", mw=350,
                              rs=True)
        self.raise_()

    def delete_instance(self):
        """ 删除该类的实例化 """
        if maya_api_version() < self.__class__.MAYA2017:
            self.delete_2016()
        else:
            self.delete_2017()

    def delete_control(self, control):
        """ 删除 workspace control"""
        if cmds.workspaceControl(control, q=True, exists=True):
            cmds.workspaceControl(control, e=True, close=True)
            cmds.deleteUI(control, control=True)

    def run(self):
        """ 显示具有停靠能力的窗口， 2017以后的停靠和之前版本的停靠不一样 """
        if maya_api_version() < self.__class__.MAYA2017:
            self.run_2016()
        else:
            self.run_2017()
