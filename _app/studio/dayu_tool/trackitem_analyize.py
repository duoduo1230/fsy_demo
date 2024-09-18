#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/9 18:45

__author__ = 'pengyuxuan'

import hiero.ui as hui
import hiero.core as hcore
from ui_center.qt import *


def trackitem_analyize():
    timeline = hui.activeView()
    if not isinstance(timeline, hui.TimelineEditor):
        return None

    trackitems = timeline.selection()
    framerate = hui.activeSequence().framerate().toFloat()

    if trackitems:
        total_clips = 0
        total_frames = 0

        for item in trackitems:
            if isinstance(item, hcore.TrackItem):
                total_clips += 1
                current_duration = item.sourceOut() - item.sourceIn() + 1
                total_frames += current_duration

        second, frame = int(total_frames / framerate), int(total_frames % framerate)

        total_time = '{m}:{s}:{f}'.format(m=str(int(second / 60)).zfill(2), s=str((second % 60)).zfill(2),
                                          f=str(frame).zfill(2))
        return total_clips, total_frames, total_time

    return None, None, None


class TrackItemAnalyizeDialog(QDialog):

    def __init__(self, parent=None):
        super(TrackItemAnalyizeDialog, self).__init__(parent)

        self.items = QLabel('0')
        self.frames = QLabel('0')
        self.time = QLabel('0')
        lay = QFormLayout()
        lay.addRow('Selected Items Count: ', self.items)
        lay.addRow('Selected Frame Count: ', self.frames)
        lay.addRow('Selected Total Time: ', self.time)
        lay.setLabelAlignment(Qt.AlignLeft)
        self.setLayout(lay)
        self.analyize()

    def analyize(self):
        items_count, frames_count, total_time = trackitem_analyize()

        if items_count and frames_count:
            self.items.setText(str(items_count))
            self.frames.setText(str(frames_count))
            self.time.setText(str(total_time))
