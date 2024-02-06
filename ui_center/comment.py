# -*- coding:utf-8 -*-
import sys

from dayu_widgets.qt import QtWidgets, QtCore
from dayu_widgets.push_button import MPushButton


class CommentWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(CommentWidget, self).__init__(parent)

        self.setObjectName("CommentWidget")

        self.init_ui()

    def init_ui(self):
        self.text_edit = QtWidgets.QPlainTextEdit(self)
        self.text_edit.setPlainText(u"element:\n状态:（渲染序列） \n分辨率信息:(2048x1152) \n帧范围信息:(1001-1071) \n制作内容:(mask) \n对应：dailies_v0000")
        self.commit_btn = MPushButton(u"Publish").medium()
        self.commit_btn.setMaximumWidth(150)

        main_lay = QtWidgets.QVBoxLayout(self)
        main_lay.addWidget(self.text_edit)
        main_lay.addWidget(self.commit_btn, QtCore.Qt.AlignLeft)


if __name__ == "__main__":
    app = QtWidgets.QApplication([""])
    win = CommentWidget()
    win.show()
    sys.exit(app.exec_())
