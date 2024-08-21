from Qt import QtWidgets, QtCore
from dayu_widgets import dayu_theme
from dayu_widgets.label import MLabel
from dayu_widgets.browser import MDragFolderButton
from dayu_widgets.divider import MDivider
from dayu_widgets.item_model import MSortFilterModel
from dayu_widgets.item_model import MTableModel
from dayu_widgets.item_view import MTableView
from dayu_widgets.menu import MMenu
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.slider import MSlider
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.push_button import MPushButton
from dayu_widgets.spin_box import MSpinBox
from dayu_widgets.browser import MClickBrowserFolderToolButton
from ui_center.resource_widget.warning_dialod import MErrorMessageBox, MSuccessMessageBox
import os
import tempfile

class MaskWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MaskWindow, self).__init__(parent)
        self.setWindowTitle(self.tr(u'拍屏工具'))
        self.resize(950, 750)
        self._init_ui()
        self.bind_function()
    def _init_ui(self):


        # 给进度条
        self.slider = MSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(1, 100)

        # 设置水印的label
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
                font-size: 20px; /* 设置标题的字号 */
            }
        """

        self.check_item_groupBox = QtWidgets.QGroupBox(u'设置水印')
        self.check_item_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.check_item_groupBox.setMaximumHeight(100)
        self.check_item_groupBox.setStyleSheet(grp_style_sheet)
        self.check_item_groupBox.setLayout(self.line_edit_lay)

        # 显示信息
        self.light_check_box = MCheckBox(u"灯光")
        self.srf_check_box = MCheckBox(u"贴图")
        self.curve_check_box = MCheckBox(u"曲线")
        self.smooth_check_box = MCheckBox(u"抗锯齿")

        self.show_lay = QtWidgets.QHBoxLayout()
        self.show_lay.addWidget(self.light_check_box)
        self.show_lay.addStretch()
        self.show_lay.addWidget(self.srf_check_box)
        self.show_lay.addStretch()
        self.show_lay.addWidget(self.curve_check_box)
        self.show_lay.addStretch()
        self.show_lay.addWidget(self.smooth_check_box)

        # 第二层
        self.font_size_lab = MLabel(u"字号：")
        self.mask_lab = MLabel(u"遮幅：")
        self.size_lab = MLabel(u"尺寸：")

        self.font_size_spinbox = MSpinBox().small()

        self.mask_menu = MMenu(exclusive=False, parent=self)
        self.mask_menu.set_data(['2.39', '2.35'])
        self.mask_combobox = MComboBox().small()
        self.mask_combobox.setMaximumWidth(150)
        self.mask_combobox._root_menu = self.mask_menu

        self.size_menu = MMenu(exclusive=False, parent=self)
        self.size_menu.set_data(['full', 'half'])
        self.size_combobox = MComboBox().small()
        self.size_combobox.setMaximumWidth(150)
        self.size_combobox._root_menu = self.size_menu

        self.mask_lay = QtWidgets.QHBoxLayout()
        self.mask_lay.addWidget(self.size_lab)
        self.mask_lay.addWidget(self.size_combobox)
        self.mask_lay.addStretch()
        self.mask_lay.addWidget(self.mask_lab)
        self.mask_lay.addWidget(self.mask_combobox)
        self.mask_lay.addStretch()
        self.mask_lay.addWidget(self.font_size_lab)
        self.mask_lay.addWidget(self.font_size_spinbox)


        # ______________________________________

        self.color_lab = MLabel(u"色彩空间：")
        self.format_lab = MLabel(u"格式：")
        self.sequence_check_box = MCheckBox(u"序列")

        self.color_menu = MMenu(exclusive=False, parent=self)
        self.color_menu.set_data(["sRGB gamma", "Raw"])
        self.color_combobox = MComboBox().small()
        self.color_combobox.setMaximumWidth(150)
        self.color_combobox._root_menu = self.color_menu

        self.format_menu = MMenu(exclusive=False, parent=self)
        self.format_menu.set_data(["mov", "avi"])
        self.format_combobox = MComboBox().small()
        self.format_combobox.setMaximumWidth(150)
        self.format_combobox._root_menu = self.format_menu


        self.out_lay = QtWidgets.QHBoxLayout()
        self.out_lay.addWidget(self.format_lab)
        self.out_lay.addWidget(self.format_combobox)
        self.out_lay.addStretch()
        self.out_lay.addWidget(self.color_lab)
        self.out_lay.addWidget(self.color_combobox)
        self.out_lay.addStretch()
        self.out_lay.addWidget(self.sequence_check_box)




        # 第三层
        self.frame_range = MLabel(u"帧范围：")
        self.camera = MLabel(u"摄像机：")

        self.cam_menu = MMenu(exclusive=False, parent=self)
        self.cam_menu.set_data(['pesp', 'top'])
        self.cam_combobox = MComboBox().small()
        self.cam_combobox.setMaximumWidth(150)
        self.cam_combobox._root_menu = self.cam_menu
        self.mask_lab = MLabel(u"遮幅：")


        # 组成第三层
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(self.slider)

        main_lay.addWidget(self.check_item_groupBox)
        main_lay.addWidget(MDivider(""))
        main_lay.addLayout(self.show_lay)
        main_lay.addWidget(MDivider(""))
        main_lay.addLayout(self.mask_lay)
        main_lay.addLayout(self.out_lay)

        self.setLayout(main_lay)
    def bind_function(self):
        self.mask_menu._action_group.triggered.connect(
            lambda action: self.select_config(action, self.mask_combobox))
        self.cam_menu._action_group.triggered.connect(
            lambda action: self.select_config(action, self.cam_combobox))
        self.size_menu._action_group.triggered.connect(
            lambda action: self.select_config(action, self.size_combobox))

    def select_config(self, action, combobox):
        if action.isChecked():
            combobox._set_value(action.text())

def main():
    from dayu_widgets.qt import application

    with application() as app:
        test = MaskWindow()
        dayu_theme.apply(test)
        test.show()


if __name__ == "__main__":
    main()