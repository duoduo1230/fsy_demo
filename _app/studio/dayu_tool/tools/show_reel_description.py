#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'yangzhuo'

import sys
import nuke
import hiero.ui as hui
from dayu_widgets.qt import *
from dayu_widgets import dayu_theme
from dayu_widgets.label import MLabel
from dayu_widgets.spin_box import MSpinBox
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.message import MMessage
from dayu_widgets.push_button import MPushButton
from dayu_widgets.browser import MClickBrowserFileToolButton


class BatchCreateInfoDialog(QDialog):
    def __init__(self, parent=None):
        super(BatchCreateInfoDialog, self).__init__(parent)
        self.resize(700, 120)
        self.setWindowTitle('DAYU Show Description')

        # box
        self.x_box = MSpinBox()
        self.y_box = MSpinBox()
        self.r_box = MSpinBox()
        self.t_box = MSpinBox()
        self.x_box.setMaximum(99999)
        self.y_box.setMaximum(99999)
        self.r_box.setMaximum(99999)
        self.t_box.setMaximum(99999)

        self.pos_lay = QHBoxLayout()
        self.pos_lay.addWidget(MLabel('x'))
        self.pos_lay.addWidget(self.x_box)
        self.pos_lay.addWidget(MLabel('y'))
        self.pos_lay.addWidget(self.y_box)
        self.pos_lay.addWidget(MLabel('r'))
        self.pos_lay.addWidget(self.r_box)
        self.pos_lay.addWidget(MLabel('t'))
        self.pos_lay.addWidget(self.t_box)
        self.pos_lay.addStretch()

        # Justify
        self.justify_x = MComboBox()
        self.justify_y = MComboBox()
        self.justify_x.addItems(['left', 'center', 'right', 'justify'])
        self.justify_y.addItems(['left', 'center', 'right', 'justify'])

        self.just_lay = QHBoxLayout()
        self.just_lay.addWidget(self.justify_x)
        self.just_lay.addWidget(self.justify_y)
        self.just_lay.addStretch()

        # font
        self.select_font = MComboBox()
        self.select_font.addItems(
            ['KaiTi', 'FangSong', 'SimHei', 'Microsoft YaHei', 'Adobe Song Std', 'Adobe Heiti Std',
             'Adobe Fangsong Std', 'Adobe Kaiti Std'])
        self.font_lay = QHBoxLayout()
        self.font_lay.addWidget(self.select_font)
        self.font_lay.addStretch()

        # csv
        self.csv_browser = MClickBrowserFileToolButton()
        self.csv_browser.setMaximumWidth(20)
        self.csv_browser.set_dayu_filters('.csv')
        self.csv_label = MLabel()
        self.csv_label.setMinimumWidth(400)

        self.csv_lay = QHBoxLayout()
        self.csv_lay.addWidget(self.csv_browser)
        self.csv_lay.addWidget(self.csv_label)

        # 上面的四层重新规划一下
        setting_lay = QFormLayout()
        setting_lay.addRow(self.tr('Box:'), self.pos_lay)
        setting_lay.addRow(self.tr('Justify:'), self.just_lay)
        setting_lay.addRow(self.tr('Select Font:'), self.font_lay)
        setting_lay.addRow(self.tr('CSV File:'), self.csv_lay)

        # button
        run_btn = MPushButton('Run')
        tk_run_btn = MPushButton('Ten Run')
        shot_name_btn = MPushButton('Shot Name')

        btn_lay = QHBoxLayout()
        btn_lay.addWidget(run_btn)
        btn_lay.addWidget(tk_run_btn)
        btn_lay.addWidget(shot_name_btn)

        main_lay = QVBoxLayout()
        main_lay.addLayout(setting_lay)
        main_lay.addLayout(btn_lay)
        self.setLayout(main_lay)

        run_btn.clicked.connect(self.slot_run)
        tk_run_btn.clicked.connect(self.tk_slot_run)
        shot_name_btn.clicked.connect(self.shot_name_run)
        self.csv_label.set_elide_mode(Qt.ElideRight)
        self.csv_browser.sig_file_changed.connect(self.csv_label.setText)

    def slot_run(self):
        import csv
        import hiero.ui as hui
        import hiero.core as hcore
        csv_file = self.csv_browser.get_dayu_path()
        if not csv_file:
            message = "Please upload a CSV file"
            nuke.alert(message)
            return
        active_seq = hui.activeSequence()
        active_tl = hui.getTimelineEditor(active_seq)
        track_item_list = active_tl.selection()

        x, y, r, t = self.x_box.value(), self.y_box.value(), self.r_box.value(), self.t_box.value()
        justify_x, justify_y = self.justify_x.currentText(), self.justify_y.currentText()
        font = str(self.select_font.currentText())
        if not track_item_list:
            return

        data = None
        with open(csv_file) as rf:
            data = list(csv.reader(rf))

        for item in track_item_list:

            if isinstance(item, hcore.TrackItem):
                item_name = item.name().split('_')[0]
                for index, row in enumerate(data):
                    if row:
                        reel_name = '%s%s' % (row[0], row[1])
                        if reel_name == item_name:

                            text_item = item.parent().createEffect(effectType='Text2', trackItem=item)
                            text_node = text_item.node()
                            text_node['message'].setValue(row[2])
                            text_node['global_font_scale'].setValue(0.5)
                            try:
                                text_node['font'].setValue(font, 'Regular')
                            except:
                                text_node['font'].setValue('Utopia', 'Regular')

                            if int(x) != 0 and x and y and r and t:
                                text_node['xjustify'].setValue(justify_x)
                                text_node['yjustify'].setValue(justify_y)
                                text_node['box'].setValue([int(x), int(y), int(r), int(t)])
                            else:
                                text_node['xjustify'].setValue('left')
                                text_node['yjustify'].setValue('top')
                                text_node['box'].setValue([700, 1000, 1400, 1000])

        MMessage.success('success!', parent=self, closable=True)

    def tk_slot_run(self):
        import csv
        import hiero.ui as hui
        import hiero.core as hcore
        csv_file = self.csv_browser.get_dayu_path()
        if not csv_file:
            message = "Please upload a CSV file"
            nuke.alert(message)
            return
        active_seq = hui.activeSequence()
        active_tl = hui.getTimelineEditor(active_seq)
        track_item_list = active_tl.selection()

        x, y, r, t = self.x_box.value(), self.y_box.value(), self.r_box.value(), self.t_box.value()
        justify_x, justify_y = self.justify_x.currentText(), self.justify_y.currentText()
        font = str(self.select_font.currentText())

        if not track_item_list:
            return

        data = None
        with open(csv_file) as rf:
            data = list(csv.reader(rf))

        for item in track_item_list:

            if not isinstance(item, hcore.TrackItem):
                continue

            item_name = item.name()[:10]
            for index, row in enumerate(data):
                if not row:
                    continue
                reel_name = '%s' % (row[0])
                if reel_name == item_name:
                    text_item = item.parent().createEffect(effectType='Text2', trackItem=item)
                    text_node = text_item.node()
                    text_node['message'].setValue(row[1])
                    text_node['global_font_scale'].setValue(0.5)
                    text_node['font'].setValue(font, 'Regular')

                    if int(x) != 0 and x and y and r and t:
                        text_node['xjustify'].setValue(justify_x)
                        text_node['yjustify'].setValue(justify_y)
                        text_node['box'].setValue([int(x), int(y), int(r), int(t)])
                    else:
                        text_node['xjustify'].setValue('left')
                        text_node['yjustify'].setValue('top')
                        text_node['box'].setValue([700, 1000, 1400, 1000])

        MMessage.success('success!', parent=self, closable=True)

    def shot_name_run(self):
        import csv
        import hiero.ui as hui
        import hiero.core as hcore
        csv_file = self.csv_browser.get_dayu_path()
        if not csv_file:
            message = "Please upload a CSV file"
            nuke.alert(message)
            return
        active_seq = hui.activeSequence()
        active_tl = hui.getTimelineEditor(active_seq)
        track_item_list = active_tl.selection()

        x, y, r, t = self.x_box.value(), self.y_box.value(), self.r_box.value(), self.t_box.value()
        justify_x, justify_y = self.justify_x.currentText(), self.justify_y.currentText()
        font = str(self.select_font.currentText())

        if not track_item_list:
            return

        data = None
        with open(csv_file) as rf:
            data = list(csv.reader(rf))

        for item in track_item_list:

            if not isinstance(item, hcore.TrackItem):
                continue

            item_name = item.name()
            for index, row in enumerate(data):
                if not row:
                    continue
                reel_name = '%s' % (row[0])
                if reel_name == item_name:
                    text_item = item.parent().createEffect(effectType='Text2', trackItem=item)
                    text_node = text_item.node()
                    text_node['message'].setValue(row[1])
                    text_node['global_font_scale'].setValue(0.5)
                    text_node['font'].setValue(font, 'Regular')

                    if int(x) != 0 and x and y and r and t:
                        text_node['xjustify'].setValue(justify_x)
                        text_node['yjustify'].setValue(justify_y)
                        text_node['box'].setValue([int(x), int(y), int(r), int(t)])
                    else:
                        text_node['xjustify'].setValue('left')
                        text_node['yjustify'].setValue('top')
                        text_node['box'].setValue([700, 1000, 1400, 1000])

        MMessage.success('success!', parent=self, closable=True)


def run():
    window = BatchCreateInfoDialog(hui.mainWindow())
    window.setWindowFlags(Qt.Window)
    window.exec_()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    test = BatchCreateInfoDialog()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())




