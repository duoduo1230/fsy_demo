from PySide2 import QtCore
from PySide2 import QtWidgets
import sys
from maya import cmds
import maya.api.OpenMaya as om


class Window1(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window1, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(u"匹配模型位置")
        self.resize(500, 300)
        self.set_ui()
        self.bind_function()

    def set_ui(self):
        self.model1_line_edit = QtWidgets.QLineEdit()
        self.model1_line_edit.setPlaceholderText(u"选择模板模型")
        self.nodel1_Button = QtWidgets.QPushButton(u"传入")

        self.model1_layout = QtWidgets.QHBoxLayout()
        self.model1_layout.addWidget(self.model1_line_edit)
        self.model1_layout.addWidget(self.nodel1_Button)

        self.model2_line_edit = QtWidgets.QLineEdit()
        self.model2_line_edit.setPlaceholderText(u"选择修复模型")
        self.nodel2_Button = QtWidgets.QPushButton(u"传入")

        self.model2_layout = QtWidgets.QHBoxLayout()
        self.model2_layout.addWidget(self.model2_line_edit)
        self.model2_layout.addWidget(self.nodel2_Button)

        self.run_button = QtWidgets.QPushButton(u"Run")

        self.master_Lay = QtWidgets.QVBoxLayout()
        self.master_Lay.addLayout(self.model1_layout)
        self.master_Lay.addLayout((self.model2_layout))
        self.master_Lay.addWidget((self.run_button))

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

    def match_vertex_positions(self, model_A, model_B):

        selection_list_A = om.MSelectionList()
        selection_list_A.add(model_A)
        dag_path_A = selection_list_A.getDagPath(0)

        selection_list_B = om.MSelectionList()
        selection_list_B.add(model_B)
        dag_path_B = selection_list_B.getDagPath(0)

        vertex_iter_B = om.MItMeshVertex(dag_path_B)
        vertex_positions_B = []
        while not vertex_iter_B.isDone():
            point_B = vertex_iter_B.position()
            vertex_positions_B.append(point_B)
            vertex_iter_B.next()

        vertex_iter_A = om.MItMeshVertex(dag_path_A)
        for i, point_B in enumerate(vertex_positions_B):
            point_A = vertex_iter_A.position()
            if point_A != point_B:
                vertex_iter_A.setPosition(point_B)
            vertex_iter_A.next()

    def fix_model_info(self):
        model_A_name = self.model1_line_edit.text()  # 替换为模型 A 的名称
        model_B_name = self.model2_line_edit.text()  # 替换为模型 B 的名称
        print(model_A_name)
        print(model_B_name)
        tel_vertices = self.get_all_vertices(model_B_name)
        fix_vertices = self.get_all_vertices(model_A_name)

        if len(tel_vertices) == len(fix_vertices):
            self.match_vertex_positions(model_A_name, model_B_name)
            cmds.headsUpMessage(u"成功!!!")
        else:
            cmds.confirmDialog(t="Warning!!!", m=u"顶点数不一致，无法修改本")


win = Window1()
win.show()
