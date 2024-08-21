# -*- coding: utf-8 -*-

import os
import pathlib
from functools import partial
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


class MyRunnable(QtCore.QRunnable):
    def __init__(self, widget, path, index):
        super(MyRunnable, self).__init__()
        self.widget = widget
        self.index = index
        self.path = path
        self.setAutoDelete(True)

    def run(self):
        message = u"正在重定向 {}" + u" --> 进度 {}/" + str(len(self.widget.animation_file_list))
        new_message = message.format(self.path, self.index)
        self.widget.progress_label.setText(new_message)


class BatchFbxWidget(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(BatchFbxWidget, self).__init__(parent)
        self.setWindowTitle(u"批量重定向工具")
        self.resize(700, 200)
        self.character_info = ""

        self.pool = QtCore.QThreadPool()
        self.pool.setMaxThreadCount(1)

        self._init_ui()
        self.set_data()
        self.bind_func()

    def _init_ui(self):
        self.tip_label = QtWidgets.QLabel()
        self.tip_label.setVisible(False)
        self.source_edit = QtWidgets.QLineEdit()
        self.folder_btn1 = QtWidgets.QPushButton("...")
        lay1 = QtWidgets.QHBoxLayout()
        lay1.addWidget(self.source_edit)
        lay1.addWidget(self.folder_btn1)
        self.target_edit = QtWidgets.QLineEdit()
        self.folder_btn2 = QtWidgets.QPushButton("...")
        lay2 = QtWidgets.QHBoxLayout()
        lay2.addWidget(self.target_edit)
        lay2.addWidget(self.folder_btn2)
        self.animation_edit = QtWidgets.QLineEdit()
        self.folder_btn3 = QtWidgets.QPushButton("...")
        lay3 = QtWidgets.QHBoxLayout()
        lay3.addWidget(self.animation_edit)
        lay3.addWidget(self.folder_btn3)
        self.output_edit = QtWidgets.QLineEdit()
        self.folder_btn4 = QtWidgets.QPushButton("...")
        lay4 = QtWidgets.QHBoxLayout()
        lay4.addWidget(self.output_edit)
        lay4.addWidget(self.folder_btn4)
        self.skip_check = QtWidgets.QCheckBox("跳过已存在的重定向")
        self.fps_combo_box = QtWidgets.QComboBox()

        form_lay = QtWidgets.QFormLayout()
        form_lay.addRow(u"源角色：", lay1)
        form_lay.addRow(u"目标角色：", lay2)
        form_lay.addRow(u"动画FBX文件夹：", lay3)
        form_lay.addRow(u"输出目录：", lay4)
        form_lay.addRow(u"帧率:", self.fps_combo_box)
        form_lay.addWidget(self.skip_check)

        self.progress_label = QtWidgets.QLabel(parent=self)
        self.progress_label.setStyleSheet("font-size: 25px; color: #ffd737;")

        self.run_btn = QtWidgets.QPushButton(u"开始转换")
        self.run_btn.setMinimumWidth(200)

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(self.tip_label, alignment=QtCore.Qt.AlignCenter)
        main_lay.addLayout(form_lay)
        main_lay.addWidget(self.progress_label)
        main_lay.addWidget(self.run_btn, alignment=QtCore.Qt.AlignRight)
        self.setLayout(main_lay)

    def set_data(self):
        self.tip_label.setVisible(False)
        self.fps_combo_box.addItems(["60", "50", "48", "30", "25", "24", "15"])

    def bind_func(self):
        self.folder_btn1.clicked.connect(partial(self.select_file, self.source_edit))
        self.folder_btn2.clicked.connect(partial(self.select_file, self.target_edit))
        self.folder_btn3.clicked.connect(partial(self.select_folder, self.animation_edit))
        self.folder_btn4.clicked.connect(partial(self.select_folder, self.output_edit))
        self.run_btn.clicked.connect(self.run)

    def select_file(self, line_edit):
        dialog = QtWidgets.QFileDialog.getOpenFileName(self, u'请选择ma文件')
        if not dialog:
            return
        line_edit.setText(dialog[0])

    def select_folder(self, line_edit):
        dialog = QtWidgets.QFileDialog.getExistingDirectory(self, u'请选择文件夹')
        if not dialog:
            return
        line_edit.setText(dialog)

    def create(self):
        error_list = {}
        character = self.target_edit.text()
        source = self.source_edit.text()

        fps = int(self.fps_combo_box.currentText())
        # 此处得anim 应该改为 anim_fbx
        for index, anim in enumerate(self.animation_file_list):
            anim = anim.replace("\\", "/")
            # 此处是运行的进程
            runnable = MyRunnable(self, anim.decode('gbk'), index + 1)
            self.pool.start(runnable)

            # 是否跳过文件
            fbx_path = '{}/us_{}.fbx'.format(self.output_folder, pathlib.Path(anim).stem)
            if self.is_skip and os.path.exists(fbx_path):
                continue

            # 重定向
            result = retarget.batch_retarget(
                character,
                source,
                anim,
                self.output_folder,
                fps
            )
            if result[0]:
                error_list[anim] = result[1]

        return error_list

    def show_result(self, error_result):
        if error_result:
            text = ""
            for f, i in error_result.items():
                text += "{}\n{}\n\n".format(f, i)
            with open(os.path.join(self.output_folder, "ErrorOutput.txt"), "w") as f:
                f.write(text)
            QtWidgets.QMessageBox.warning(self, "Tip", u"输出有问题，请打开输出目录查看txt文档")
        else:
            QtWidgets.QMessageBox.information(self, "Tip", u"批量转换完成")

    def run(self):
        self.animation_folder = self.animation_edit.text()   # fbx
        self.output_folder = self.output_edit.text()         # 输出文件夹
        self.is_skip = self.skip_check.checkState()          # 是否跳过存在得重定向

        if not self.animation_folder and not self.output_folder:
            QtWidgets.QMessageBox.warning(self, "Tip", u"请选择动画FBX文件夹和输出文件夹")
            return
        # 获取self.animation_folder该路径下得所有fbx文件
        self.animation_file_list = retarget.list_fbx_file(self.animation_folder)
        if not self.animation_file_list:
            QtWidgets.QMessageBox.warning(self, "Tip", u"未找到FBX文件，请重新选择动画文件夹")
            return

        # self.worker_object.start()
        result = self.create()
        self.show_result(result)


def main():
    maya_main_wid = getMainWindow()
    main_window = BatchFbxWidget(parent=maya_main_wid)
    main_window.show()


if __name__ == "__main__":
    main()
