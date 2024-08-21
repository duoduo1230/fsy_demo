# -*- coding: utf-8 -*-
import os
from functools import partial
import traceback
from pathlib import Path

import maya.OpenMayaUI as apiUI
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

import retarget

reload(retarget)


def getMainWindow():
    pointer = apiUI.MQtUtil.mainWindow()
    if pointer is not None:
        _MainWindow = wrapInstance(long(pointer), QtWidgets.QWidget)
    return _MainWindow


class HumanIkWidget(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(HumanIkWidget, self).__init__(parent)
        self.setWindowTitle(u"HumanIK 绑定生成工具")
        self.resize(600, 180)

        self._init_ui()
        self.bind_func()
        self.set_data()

    def _init_ui(self):
        self.fbx_edit = QtWidgets.QLineEdit()
        self.btn1 = QtWidgets.QPushButton("...")
        lay1 = QtWidgets.QHBoxLayout()
        lay1.addWidget(self.fbx_edit)
        lay1.addWidget(self.btn1)

        self.template_comb = QtWidgets.QComboBox()

        form_lay = QtWidgets.QFormLayout()
        form_lay.addRow(u"选择绑定ma：", lay1)
        form_lay.addRow(u"选择模板：", self.template_comb)

        self.run_btn = QtWidgets.QPushButton(u"开始")
        self.run_btn.setMinimumWidth(200)

        main_lay = QtWidgets.QVBoxLayout(self)
        main_lay.addLayout(form_lay)
        main_lay.addWidget(self.run_btn, alignment=QtCore.Qt.AlignHCenter)

    def bind_func(self):
        self.btn1.clicked.connect(partial(self.select_folder, self.fbx_edit))
        self.run_btn.clicked.connect(self.run)

    def set_data(self):
        template_folder = os.path.join(Path(__file__).parent.as_posix(), "template")
        template_files = os.listdir(template_folder)
        for index, template_file in enumerate(template_files):
            name = os.path.basename(template_file).split(".")[0]
            self.template_comb.addItem(name)
            template_path = os.path.join(template_folder, template_file)
            self.template_comb.setItemData(index, template_path, role=QtCore.Qt.UserRole)

    def select_folder(self, line_edit):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, u"选择ma文件", "", "MA Files (*.ma)")
        if not file_name:
            return
        line_edit.setText(file_name)

    def run(self):
        template_file = self.template_comb.itemData(self.template_comb.currentIndex(), QtCore.Qt.UserRole)
        ma = self.fbx_edit.text()

        if not ma:
            return

        try:
            output_file = os.path.join(os.path.dirname(ma), os.path.basename(ma).replace(".ma", "_humanIK.ma"))
            retarget.create_humanik(ma, template_file, output_file)
            QtWidgets.QMessageBox.information(self, u"成功", "humanIK转换成功")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, u"错误", u"生成失败：{}".format(traceback.format_exc()))


def main():
    maya_main_wid = getMainWindow()
    main_window = HumanIkWidget(parent=maya_main_wid)
    main_window.show()


if __name__ == "__main__":
    main()
