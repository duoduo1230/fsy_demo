# -*- coding: utf-8 -*-
from PySide2 import QtCore
from PySide2 import QtWidgets
import sys
from maya import cmds
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.push_button import MPushButton
from dayu_widgets.label import MLabel
from dayu_widgets.message import MMessage
from dayu_widgets import dayu_theme


class FixModelInfo(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(FixModelInfo, self).__init__(parent)
        self.setWindowTitle("Fix Medol Paint")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        
        self.resize(500, 300)
        self.set_ui()
        self.bind_function()
        dayu_theme.apply(self)
        

    def set_ui(self):
        self.model1_line_edit = QtWidgets.QLineEdit()
        self.model1_line_edit.setPlaceholderText("Select repair model")
        self.nodel1_Button = MPushButton("Input")

        self.model1_layout = QtWidgets.QHBoxLayout()
        self.model1_layout.addWidget(self.model1_line_edit)
        self.model1_layout.addWidget(self.nodel1_Button)

        self.model2_line_edit = QtWidgets.QLineEdit()
        self.model2_line_edit.setPlaceholderText("Select template model")
        self.nodel2_Button = MPushButton("Input")

        self.model2_layout = QtWidgets.QHBoxLayout()
        self.model2_layout.addWidget(self.model2_line_edit)
        self.model2_layout.addWidget(self.nodel2_Button)

        self.run_button = MPushButton("Run")
        
        self.progress = MProgressBar()
        self.progress.setValue(0)

        self.master_Lay = QtWidgets.QVBoxLayout()
        self.master_Lay.addLayout(self.model1_layout)
        self.master_Lay.addLayout(self.model2_layout)
        self.master_Lay.addWidget(self.progress)
        self.master_Lay.addWidget(self.run_button)

        self.setLayout(self.master_Lay)

    def bind_function(self):
        self.nodel1_Button.clicked.connect(self.set_input1)
        self.nodel2_Button.clicked.connect(self.set_input2)
        self.run_button.clicked.connect(self.fix_model_info)

    def set_input1(self):
        sel_1 = cmds.ls(selection=True)
        self.model1_line_edit.setText(sel_1[0])

    def set_input2(self):
        sel_1 = cmds.ls(selection=True)
        self.model2_line_edit.setText(sel_1[0])

    def get_all_vertices(self, mesh_name):
        """
        获取顶点坐标
        """
        selection_list = om.MSelectionList()
        selection_list.add(mesh_name)
        dag_path = selection_list.getDagPath(0)
        vertex_iter = om.MItMeshVertex(dag_path)
        vertices = []
        while not vertex_iter.isDone():
            point = vertex_iter.position()
            vertices.append((point.x, point.y, point.z))
            vertex_iter.next()

        return vertices

    def match_vertex_positions(self, model_A, model_B, point_count):

        selection_list_A = om.MSelectionList()
        selection_list_A.add(model_A)
        dag_path_A = selection_list_A.getDagPath(0)

        selection_list_B = om.MSelectionList()
        selection_list_B.add(model_B)
        dag_path_B = selection_list_B.getDagPath(0)

        vertex_iter_B = om.MItMeshVertex(dag_path_B)
        vertex_iter_A = om.MItMeshVertex(dag_path_A)

        index = 1
        while not vertex_iter_B.isDone():
            point_B = vertex_iter_B.position()
            point_A = vertex_iter_A.position()
            if point_A != point_B:
                vertex_iter_A.setPosition(point_B)
            vertex_iter_A.next()
            percent = int(index * 100 / float(point_count))
            self.progress.setValue(percent)
            index += 1
            vertex_iter_B.next()


    def fix_model_info(self):
        self.progress.setValue(0)
        model_A_name = self.model1_line_edit.text()
        model_B_name = self.model2_line_edit.text()
        tel_vertices = self.get_all_vertices(model_B_name)
        fix_vertices = self.get_all_vertices(model_A_name)

        if len(tel_vertices) == len(fix_vertices):
            self.match_vertex_positions(model_A_name, model_B_name, len(tel_vertices))
            self.progress.setValue(100)
            MMessage.success('successful!!!', self, duration=4, closable=True)
        else:
            cmds.confirmDialog(t="Warning!!!", m="Unable to modify")


if __name__ == "__main__":
    window1 = FixModelInfo()
    window1.show()
