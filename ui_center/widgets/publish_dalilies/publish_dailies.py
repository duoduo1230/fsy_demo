# -*- coding:utf-8 -*-

import sys

from dayu_widgets.qt import QtWidgets, QtCore
from dayu_widgets.label import MLabel
from dayu_widgets.browser import MDragFileButton
from widget.comment import CommentWidget
from widget.drag_file import FileWidget


class PublishWidget(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(PublishWidget, self).__init__(parent)

        self.setObjectName("PublishWidget")
        self.setWindowTitle(u"Publish Dailies")

        self.resize(870, 680)

        self.init_ui()
        self.bind_func()

    def init_ui(self):
        self.browserert_btn = MDragFileButton(text="Click or drag file here", multiple=False)
        self.browserert_btn.sig_file_changed.connect(self.add_item)
        self.file_widget = FileWidget(self)

        form_lay = QtWidgets.QFormLayout()
        form_lay.addRow(MLabel("Give File:").h4(), self.browserert_btn)
        form_lay.addRow(MLabel("File Result:").h4(), self.file_widget)
        # 包了边框
        self.file_grp_box = QtWidgets.QGroupBox("Drag File")
        self.file_grp_box.setAlignment(QtCore.Qt.AlignHCenter)
        self.file_grp_box.setLayout(form_lay)

        self.comment_widget = CommentWidget(self)
        self.comment_grp_box = QtWidgets.QGroupBox("Comment")
        self.comment_grp_box.setEnabled(False)
        self.comment_grp_box.setAlignment(QtCore.Qt.AlignHCenter)
        self.comment_grp_box.setLayout(self.comment_widget.layout())

        main_lay = QtWidgets.QVBoxLayout(self)
        main_lay.addWidget(self.file_grp_box)
        main_lay.addWidget(self.comment_grp_box)
    
    def bind_func(self):
        self.comment_widget.commit_btn.clicked.connect(self.comment)
        self.file_widget.has_file.connect(self.comment_grp_box.setEnabled)

    def add_item(self, folder):
        if not folder:
            return

        self.file_widget.add_folder(folder)
        self.comment_grp_box.setEnabled(True)
        
    def get_file(self):
        return self.file_widget.folder_list

    def comment(self):
        print(self.get_file())


if __name__ == "__main__":
    app = QtWidgets.QApplication([""])
    win = PublishWidget()
    win.show()
    sys.exit(app.exec_())
