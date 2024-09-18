#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'

import db
import db.util
import os
from dayu_widgets.qt import *
from functools import partial
from dayu_path import DayuPath
from db.sub_level import SubLevel
from dayu_widgets.label import MLabel
from db.disk_path import SequentialFiles
from dayu_widgets.divider import MDivider
from dayu_widgets.message import MMessage
from dayu_widgets.progress_bar import MProgressBar
from dayu_widgets.browser import MDragFolderButton
from dayu_widgets import dayu_theme, MItemViewFullSet, MPushButton


class BuildFolderWidget(QDialog):
    def __init__(self, parent=None):
        super(BuildFolderWidget, self).__init__(parent=parent)

        self.track_item_list = []

        drag_folder_button = MDragFolderButton()
        drag_folder_button.set_dayu_svg('attachment_line.svg')
        drag_folder_button.sig_folder_changed.connect(self.slot_folder_change)
        drag_folder_button.setMaximumHeight(160)

        drag_lay = QHBoxLayout()
        drag_lay.addWidget(drag_folder_button)

        select_lay = QHBoxLayout()
        select_cloud_mov = MPushButton('Select cloud/*.mov')
        select_mov_mov = MPushButton('Select mov/*.mov')
        select_exr = MPushButton('Select exr')
        select_jpg = MPushButton('Select jpg')

        select_cloud_mov.clicked.connect(partial(self.filter_ext, ['/cloud/', '.mov']))
        select_mov_mov.clicked.connect(partial(self.filter_ext, ['/mov/', '.mov']))
        select_exr.clicked.connect(partial(self.filter_ext, ['/exr/', '.exr']))
        select_jpg.clicked.connect(partial(self.filter_ext, ['/jpg/', '.jpg']))

        select_lay.addWidget(select_cloud_mov)
        select_lay.addWidget(select_mov_mov)
        select_lay.addWidget(select_exr)
        select_lay.addWidget(select_jpg)

        header_list = [
            {"key": "filename", "label": "File Name", 'searchable': True, 'checkable': True},
            {"key": "sub_level", "label": "Sub Level", 'searchable': True}
        ]

        self.item_view = MItemViewFullSet()
        self.item_view.set_header_list(header_list)

        self.progress = MProgressBar()
        self.progress.setValue(0)
        progress_lay = QHBoxLayout()
        progress_lay.addWidget(MLabel('Build Track Progress: ').warning().strong())
        progress_lay.addWidget(self.progress)

        self.build_btn = MPushButton('Build Track', MIcon('cloud_line.svg'))
        self.input_btn = MPushButton('folder Build Track', MIcon('cloud_line.svg'))
        self.input_mul_btn = MPushButton('Build Multiple Track', MIcon('cloud_line.svg'))
        button_lay = QHBoxLayout()
        self.build_btn.clicked.connect(self.build_bookmark)
        self.input_btn.clicked.connect(self.input_file)
        self.input_mul_btn.clicked.connect(self.input_multiple_file)
        button_lay.addWidget(self.build_btn)
        button_lay.addWidget(self.input_btn)
        button_lay.addWidget(self.input_mul_btn)

        main_lay = QVBoxLayout()
        main_lay.addLayout(drag_lay)
        main_lay.addWidget(MDivider('Build Track Widget'))
        main_lay.addLayout(select_lay)
        main_lay.addWidget(self.item_view)
        main_lay.addLayout(progress_lay)
        main_lay.addLayout(button_lay)
        self.resize(999, 666)
        self.setLayout(main_lay)
        dayu_theme.apply(self)

    def slot_folder_change(self, folder):
        mov_list = DayuPath(folder).scan(recursive=True, ext_filters='.mov')
        exr_list = DayuPath(folder).scan(recursive=True, ext_filters='.exr')
        jpg_list = DayuPath(folder).scan(recursive=True, ext_filters='.jpg')
        result_list = list(mov_list) + list(exr_list) + list(jpg_list)
        data = [{'filename': x.name, 'full_path': x, 'filename_checked': 2, 'sub_level': x.ancestor(2).name}
                for x in result_list]
        self.item_view.setup_data(data)
        self.item_view.table_view.header_view.resizeSections(QHeaderView.ResizeToContents)

    def filter_ext(self, filter_):
        sub_level, ext = filter_
        result = []
        for obj in self.item_view.get_data():
            file_path = obj.get('full_path')
            if sub_level in file_path and file_path.endswith(ext):
                obj['filename_checked'] = 2
            else:
                obj['filename_checked'] = 0
            result.append(obj)
        self.item_view.setup_data(result)

    def set_item_list(self, track_item_list):
        self.track_item_list = track_item_list

    def build_bookmark(self):
        """
        核心逻辑为：判断路径是否存在，如不存在，则创建
        :return:
        """
        import hiero.ui as hui
        import hiero.core as hcore
        import app._hiero.api.node_op.read_a0001 as h_read_a0001

        # create project bin
        project = hui.activeSequence().project()
        bin_name = '{}_clip'.format(project.name())
        new_bin = next((x for x in project.clipsBin().bins() if x.name() == bin_name), None)
        if not new_bin:
            new_bin = hcore.Bin(bin_name)
            project.clipsBin().addItem(new_bin)

        with project.beginUndo('build new track'):
            current_sequence = hui.activeSequence()
            new_track = hcore.VideoTrack('bookmark track item')
            current_sequence.addTrack(new_track)

            progress_index = 0
            all_num = len([x for x in self.item_view.get_data() if x.get('filename_checked')])
            image_list = [x.get('full_path') for x in self.item_view.get_data() if x.get('filename_checked')]

            for select_item in self.track_item_list:
                file_path = next((i for i in image_list if select_item.name() in DayuPath(i).stem), None)
                if not file_path:
                    continue
                already_bin_dict = {x.name(): x for x in new_bin.clips()}
                # create bin item and set media source
                import_clip_key = '{}'.format(DayuPath(file_path).name)
                if import_clip_key in already_bin_dict:
                    new_bin_item = already_bin_dict.get(import_clip_key, None)
                else:
                    new_media_source = hcore.MediaSource(file_path)
                    new_clip = hcore.Clip(new_media_source)
                    new_clip.setFramerate(
                        hui.activeSequence().framerate() if hui.activeSequence() else hcore.TimeBase(24.0))
                    new_bin_item = hcore.BinItem(new_clip)
                    already_bin_dict.update({import_clip_key: new_bin_item})
                    new_bin.addItem(new_bin_item)

                clip = new_bin_item.activeItem()
                clip.rescan()
                new_track_item = new_track.createTrackItem(new_bin_item.name())
                new_track_item.setSource(clip)
                duration = select_item.duration()
                new_track_item.setSourceOut(new_track_item.sourceIn() + duration - 1)

                new_track_item.setTimelineIn(select_item.timelineIn())
                new_track_item.setTimelineOut(select_item.timelineIn() + duration - 1)
                new_track.addItem(new_track_item)

                progress_index += 1
                percent = int(progress_index * 100 / float(all_num))
                self.progress.setValue(percent)

        MMessage.success('build success!', duration=6, parent=self, closable=True)

    def input_file(self):

        import re
        import hiero.ui as hui
        import hiero.core as hcore
        import app._hiero.api.node_op.read_a0001 as h_read_a0001

        # create project bin
        project = hui.activeSequence().project()
        bin_name = '{}_clip'.format(project.name())
        new_bin = next((x for x in project.clipsBin().bins() if x.name() == bin_name), None)
        if not new_bin:
            new_bin = hcore.Bin(bin_name)
            project.clipsBin().addItem(new_bin)
        with project.beginUndo('build new track'):
            current_sequence = hui.activeSequence()
            new_track = hcore.VideoTrack('import track item')
            current_sequence.addTrack(new_track)

            progress_index = 0
            all_num = len([x for x in self.item_view.get_data() if x.get('filename_checked')])
            image_list = [x.get('full_path') for x in self.item_view.get_data() if x.get('filename_checked')]
            for select_item in self.track_item_list:
                for file_path in image_list:
                    folder_name = file_path.split("/")[-2]
                    lower_case_name = folder_name.lower()
                    name_parts = lower_case_name.split("_")
                    ep_elements = [item for item in name_parts if "ep" in item]
                    four_digit_elements = [item for item in name_parts if re.match(r"\d{4}$", item)]
                    match_name = "_".join(ep_elements + four_digit_elements)
                    if match_name != select_item.name():
                        continue

                    already_bin_dict = {x.name(): x for x in new_bin.clips()}
                    import_clip_key = '{}'.format(DayuPath(file_path).name)
                    if import_clip_key in already_bin_dict:
                        new_bin_item = already_bin_dict.get(import_clip_key, None)
                    else:
                        new_media_source = hcore.MediaSource(file_path)
                        new_clip = hcore.Clip(new_media_source)

                        new_clip.setFramerate(
                            hui.activeSequence().framerate() if hui.activeSequence() else hcore.TimeBase(24.0))
                        new_bin_item = hcore.BinItem(new_clip)

                        already_bin_dict.update({import_clip_key: new_bin_item})
                        new_bin.addItem(new_bin_item)

                    clip = new_bin_item.activeItem()
                    clip.rescan()
                    new_track_item = new_track.createTrackItem(new_bin_item.name())
                    new_track_item.setSource(clip)
                    duration = select_item.duration()
                    new_track_item.setSourceOut(new_track_item.sourceIn() + duration - 1)

                    new_track_item.setTimelineIn(select_item.timelineIn())
                    new_track_item.setTimelineOut(select_item.timelineIn() + duration - 1)
                    new_track.addItem(new_track_item)

                    progress_index += 1
                    percent = int(progress_index * 100 / float(all_num))
                    self.progress.setValue(percent)

    def input_multiple_file(self):
        """
        核心逻辑为：判断路径是否存在，如不存在，则创建
        :return:
        """
        import hiero.ui as hui
        import hiero.core as hcore
        import app._hiero.api.node_op.read_a0001 as h_read_a0001

        # create project bin
        project = hui.activeSequence().project()
        bin_name = '{}_clip'.format(project.name())
        new_bin = next((x for x in project.clipsBin().bins() if x.name() == bin_name), None)
        if not new_bin:
            new_bin = hcore.Bin(bin_name)
            project.clipsBin().addItem(new_bin)

        with project.beginUndo('build new track'):
            current_sequence = hui.activeSequence()
            new_track_l = hcore.VideoTrack('import S_L item')
            new_track_r = hcore.VideoTrack('import S_R item')
            current_sequence.addTrack(new_track_l)
            current_sequence.addTrack(new_track_r)

            progress_index = 0
            all_num = len([x for x in self.item_view.get_data() if x.get('filename_checked')])

            image_list = [x.get('full_path') for x in self.item_view.get_data() if x.get('filename_checked')]
            # 这里将素材分成两组
            s_l_image_list = []
            s_r_image_list = []
            for item in image_list:
                if item.endswith('S_L.mov'):
                    s_l_image_list.append(item)
                elif item.endswith('S_R.mov'):
                    s_r_image_list.append(item)
            
            iter_data = [
                (s_r_image_list, new_track_r),
                (s_l_image_list, new_track_l)
            ] 
            
            # 下面选了四个
            for select_item in self.track_item_list:
                for _iter in iter_data:
                    image_list, track = _iter[0], _iter[1]
                    print(image_list, track)
                    # 右侧素材轨道这样
                    file_path = next((i for i in image_list if select_item.name() in DayuPath(i).stem), None)
                    if not file_path:
                        continue
                    already_bin_dict = {x.name(): x for x in new_bin.clips()}
                    import_clip_key = '{}'.format(DayuPath(file_path).name)
                    if import_clip_key in already_bin_dict:
                        new_bin_item = already_bin_dict.get(import_clip_key, None)
                    else:
                        new_media_source = hcore.MediaSource(file_path)
                        new_clip = hcore.Clip(new_media_source)
                        new_clip.setFramerate(
                            hui.activeSequence().framerate() if hui.activeSequence() else hcore.TimeBase(24.0))
                        new_bin_item = hcore.BinItem(new_clip)
    
                        already_bin_dict.update({import_clip_key: new_bin_item})
                        new_bin.addItem(new_bin_item)
    
                    clip = new_bin_item.activeItem()
                    clip.rescan()
                    new_track_item = track.createTrackItem(new_bin_item.name())
                    new_track_item.setSource(clip)
                    duration = select_item.duration()
                    new_track_item.setSourceOut(new_track_item.sourceIn() + duration - 1)
    
                    new_track_item.setTimelineIn(select_item.timelineIn())
                    new_track_item.setTimelineOut(select_item.timelineIn() + duration - 1)
                    track.addItem(new_track_item)
    
                    progress_index += 1
                    percent = int(progress_index * 100 / float(all_num/2))
                    self.progress.setValue(percent)

        MMessage.success('build success!', duration=6, parent=self, closable=True)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    test = BuildFolderWidget()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())
