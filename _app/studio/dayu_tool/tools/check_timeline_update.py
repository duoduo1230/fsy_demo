#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'yangzhuo'

import nuke
import hiero.ui as hui
import hiero.core as hcore
from hiero.core import Timecode
from functools import partial
from dayu_widgets.qt import *
from dayu_widgets import dayu_theme
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.item_view_set import MItemViewSet
from dayu_widgets.push_button import MPushButton


def status_color(result, y):
    result_ = y.get('status')
    if result_ == 'new':
        return dayu_theme.success_color
    elif result_ == 'change':
        return dayu_theme.warning_color
    elif result_ == 'delete':
        return dayu_theme.error_color
    else:
        return 'transparent'


class CheckUpdateTimeLine(QDialog):
    def __init__(self, parent=None):
        super(CheckUpdateTimeLine, self).__init__(parent)

        self.base_result = []
        self.new_result = []

        self.data_type = MComboBox()
        self.data_type.addItems(['all', 'delete', 'new', 'change'])
        self.data_type.setMaximumWidth(100)
        self.data_type.currentTextChanged.connect(self.slot_reset_data)

        btn_lay = QHBoxLayout()
        base_btn = MPushButton('get base data')
        new_btn = MPushButton('get new data')
        base_btn.clicked.connect(partial(self.slot_get_data, 'base'))
        new_btn.clicked.connect(partial(self.slot_get_data, 'new'))
        btn_lay.addWidget(base_btn)
        btn_lay.addWidget(new_btn)

        header_list = [{'label': 'Reel Name', 'key': 'reel_name'},
                       {'label': 'Status', 'key': 'status', 'color': status_color},
                       {'label': 'Start Frame', 'key': 'src_start'},
                       {'label': 'End Frame', 'key': 'src_end'},
                       {'label': 'Duration', 'key': 'duration'},
                       {'label': 'TimeLine In', 'key': 'timeline_in'},
                       {'label': 'TimeLine Out', 'key': 'timeline_out'},
                       {'label': 'Source TimeLine In', 'key': 'src_in'},
                       {'label': 'Source TimeLine Out', 'key': 'src_out'}]

        self.base_view = MItemViewSet()
        self.base_view.set_header_list(header_list)

        self.new_view = MItemViewSet()
        self.new_view.set_header_list(header_list)

        view_lay = QHBoxLayout()
        view_lay.addWidget(self.base_view)
        view_lay.addWidget(self.new_view)

        run_lay = QHBoxLayout()
        run_ui_btn = MPushButton('Run To Ui')
        run_ui_btn.clicked.connect(self.slot_run_ui)
        run_btn = MPushButton('Export CSV')
        run_btn.clicked.connect(self.slot_run)
        run_lay.addWidget(run_ui_btn)
        run_lay.addWidget(run_btn)

        main_lay = QVBoxLayout()
        main_lay.addWidget(self.data_type)
        main_lay.addLayout(btn_lay)
        main_lay.addLayout(view_lay)
        main_lay.addLayout(run_lay)

        self.setLayout(main_lay)
        self.resize(1000, 700)

    def slot_run_ui(self):
        base_result = self.base_result
        new_result = self.new_result

        from zam import ZAM_EDL_Compare
        reload(ZAM_EDL_Compare)
        testclass = ZAM_EDL_Compare.ZAM_EDL_Compare("", "", 24)
        testclass.compareEDLs(base_result, new_result, conformCLue='reel')
        add_list = testclass.getAllAddEvents()
        delete_list = testclass.getAllDeletedEvents()

        trim_old_change, trim_dict = testclass.getAllTrimEvents()

        ex_old_change, expand_dict = testclass.getAllExpandEvents()

        # 1. 删除
        change_list = trim_old_change + ex_old_change
        new_base_result = []
        for base_obj in base_result:
            str_ = '%s_%s' % (base_obj.get('event'), base_obj.get('sourcein'))
            if str_ in delete_list:
                base_obj.update({'status': 'delete'})
            if str_ in change_list:
                base_obj.update({'status': 'change'})

            new_base_result.append(base_obj)
        self.base_view.setup_data(new_base_result)

        # 2. 新增 + 变速
        new_new_result = []
        for new_obj in new_result:
            str_ = '%s_%s' % (new_obj.get('event'), new_obj.get('sourcein'))
            if str_ in add_list:
                new_obj.update({'status': 'new'})
            if str_ in trim_dict.keys():
                new_obj.update({'status': 'change', 'frame_change': trim_dict.get(str_)})

            if str_ in expand_dict.keys():
                new_obj.update({'status': 'change', 'frame_change': expand_dict.get(str_)})

            new_new_result.append(new_obj)
        self.new_view.setup_data(new_new_result)

        nuke.message("Success")

    def slot_run(self):
        base_result = self.base_view.get_data()
        new_result = self.new_view.get_data()
        base_reel_list = [br.get('reel_str') for br in base_result]
        new_reel_list = [nr.get('reel_str') for nr in new_result]

        # 新增
        new_list = [n for n in new_reel_list if n not in base_reel_list]

        # 删除
        delete_list = [d for d in base_reel_list if d not in new_reel_list]

        # 修改
        edit_list = []
        change_list = []
        base_dict = {base.get('reel_name'): [int(base.get('src_start')), int(base.get('src_end')), int(base.get('duration'))] for base in base_result}
        new_dict = {new.get('reel_name'): [int(new.get('src_start')), int(new.get('src_end')), int(new.get('duration'))] for new in new_result}
        for k, base_value in base_dict.items():
            new_value = new_dict.get(k)
            if new_value:
                if base_value and base_value != new_value:
                    change_list.append([k, base_value[-1], new_value[-1]])
                    edit_list.append(k)

        result = [['type', 'Reel', 'Start Frame', 'End Frame', 'Frame Change', 'TimeLine In',
                   'TimeLine Out', 'Source TimeLine In', 'Source TimeLine Out']]

        for rn_name in new_list:
            rn = next((rl for rl in new_result if rl.get('reel_str') == rn_name), None)
            if rn:
                result.append(['new add', rn.get('reel_name'), rn.get('src_start'), rn.get('src_end'),
                               '', rn.get('timeline_in'), rn.get('timeline_out'),
                               rn.get('src_in'), rn.get('src_out')])

        for dn_name in delete_list:
            dn = next((dl for dl in base_result if dl.get('reel_str') == dn_name), None)
            if dn:
                result.append(['delete', dn.get('reel_name'), dn.get('src_start'), dn.get('src_end'),
                               '', dn.get('timeline_in'), dn.get('timeline_out'),
                               dn.get('src_in'), dn.get('src_out')
                               ])

        for cn_list in change_list:
            cn_name, base_dr, new_dr = cn_list
            cn = next((cl for cl in new_result if cl.get('reel_name') == cn_name), None)
            if cn:
                change_value = new_dr - base_dr
                result.append(['change', cn.get('reel_name'), cn.get('src_start'), cn.get('src_end'),
                               change_value,
                               cn.get('timeline_in'), cn.get('timeline_out'),
                               cn.get('src_in'), cn.get('src_out')
                               ])

        import csv
        file_path, flag = QFileDialog.getSaveFileName(self, 'Save CSV File', filter='CSV File(*.csv)')
        if flag and file_path:
            with open(file_path, 'wb') as w:
                writer = csv.writer(w)
                writer.writerows(result)

            nuke.message("Success")

    @staticmethod
    def time_code_pref_check():
        return int(hcore.ApplicationSettings().boolValue('useVideoEDLTimecodes'))

    @staticmethod
    def get_src_in(track_item):
        fps = track_item.parent().parent().framerate()
        clip = track_item.source()
        clip_start_time_code = clip.timecodeStart()
        src_in = Timecode.timeToString(clip_start_time_code + track_item.sourceIn(), fps, Timecode.kDisplayTimecode)
        return src_in

    def get_src_out(self, track_item):
        fps = track_item.parent().parent().framerate()
        clip = track_item.source()
        clip_start_time_code = clip.timecodeStart()
        src_out = Timecode.timeToString(clip_start_time_code + track_item.sourceOut() + self.time_code_pref_check(),
                                        fps,
                                        Timecode.kDisplayTimecode)
        return src_out

    @staticmethod
    def get_dst_in(track_item):
        seq = track_item.parent().parent()
        t_start = seq.timecodeStart()
        fps = seq.framerate()
        dst_in = Timecode.timeToString(t_start + track_item.timelineIn(), fps, Timecode.kDisplayTimecode)
        return dst_in

    def get_dst_out(self, track_item):
        seq = track_item.parent().parent()
        t_start = seq.timecodeStart()
        fps = seq.framerate()
        dst_out = Timecode.timeToString(t_start + track_item.timelineOut() + self.time_code_pref_check(),
                                        fps,
                                        Timecode.kDisplayTimecode)
        return dst_out

    def slot_get_data(self, type_='base'):
        active_seq = hui.activeSequence()
        active_tl = hui.getTimelineEditor(active_seq)
        track_item_list = active_tl.selection()

        result = []
        for index, item in enumerate(track_item_list):
            if isinstance(item, hcore.TrackItem):
                media_source = item.source().mediaSource()
                reel_id = media_source.metadata().value('foundry.source.reelID')
                item_data = {
                    'reel_name': reel_id,
                    'reel_id': reel_id,
                    'reel': reel_id,
                    'reel_str': '%s_%d' % (reel_id, int(item.sourceIn())),
                    'src_start': item.sourceIn(),
                    'src_end': item.sourceOut(),
                    'duration': item.duration(),
                    'timeline_in': self.get_dst_in(item),
                    'timeline_out': self.get_dst_out(item),
                    'src_in': self.get_src_in(item),
                    'src_out': self.get_src_out(item),
                    'index': index + 1,
                    'media': '',
                    'cut': '',
                    'event': '%03d' % (index + 1),
                    'sourcein': self.get_src_in(item),
                    'sourceout': self.get_src_out(item),
                    'targetin': self.get_dst_in(item),
                    'targetout': self.get_dst_out(item),
                }
                result.append(item_data)

        item_view = self.base_view if type_ == 'base' else self.new_view
        item_view.setup_data(result)
        if type_ == 'base':
            self.base_result = result
        else:
            self.new_result = result

    def slot_reset_data(self, data_type):
        if data_type == 'all':
            self.base_view.setup_data(self.base_result)
            self.new_view.setup_data(self.new_result)
        else:
            if data_type == 'delete':
                result = [d for d in self.base_result if d.get('status') == data_type]
                self.base_view.setup_data(result)
            elif data_type == 'change':
                result = [d for d in self.base_result if d.get('status') == data_type]
                new_result = [d for d in self.new_result if d.get('status') == data_type]
                self.base_view.setup_data(result)
                self.new_view.setup_data(new_result)
            else:
                result = [d for d in self.new_result if d.get('status') == data_type]
                self.new_view.setup_data(result)


def run():
    window = CheckUpdateTimeLine(hui.mainWindow())
    window.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    test = CheckUpdateTimeLine()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())




