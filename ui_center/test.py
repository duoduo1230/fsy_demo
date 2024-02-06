#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2019.2
# Email : muyanru345@163.com
###################################################################

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import third-party modules
from Qt import QtCore
from Qt import QtWidgets

# Import local modules
from dayu_widgets.browser import MClickBrowserFilePushButton
from dayu_widgets.browser import MClickBrowserFileToolButton
from dayu_widgets.browser import MClickBrowserFolderPushButton
from dayu_widgets.browser import MClickBrowserFolderToolButton
from dayu_widgets.browser import MDragFileButton
from dayu_widgets.browser import MDragFolderButton
from dayu_widgets.divider import MDivider
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.label import MLabel
from dayu_widgets.qt import MIcon


class BrowserExample(QtWidgets.QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(BrowserExample, self).__init__(parent)
        self.setWindowTitle("Examples for MBrowser...")
        self._init_ui()

    def _init_ui(self):
        browser_1 = MClickBrowserFilePushButton(
            text="Browser File PushButton"
        ).primary()
        browser_2 = MClickBrowserFolderPushButton(text="Browser Folder PushButton")
        browser_2.setIcon(MIcon("upload_line.svg"))
        browser_3 = MClickBrowserFilePushButton(
            text="Browser Multi Files", multiple=True
        ).primary()
        lay_1 = QtWidgets.QHBoxLayout()
        lay_1.addWidget(browser_1)
        lay_1.addWidget(browser_2)
        lay_1.addWidget(browser_3)

        browser_4 = MClickBrowserFileToolButton().huge()
        label_4 = MLabel()
        label_4.set_elide_mode(QtCore.Qt.ElideMiddle)
        browser_4.sig_file_changed.connect(label_4.setText)

        browser_5 = MClickBrowserFolderToolButton().huge()
        label_5 = MLabel()
        label_5.set_elide_mode(QtCore.Qt.ElideMiddle)
        browser_5.sig_folder_changed.connect(label_5.setText)

        lay_2 = QtWidgets.QHBoxLayout()
        lay_2.addWidget(label_4)
        lay_2.addWidget(browser_4)
        lay_2.addWidget(label_5)
        lay_2.addWidget(browser_5)

        browser_6 = MDragFileButton(text="Click or drag file here")
        browser_6.set_dayu_svg("attachment_line.svg")
        label_6 = MLabel()
        label_6.set_elide_mode(QtCore.Qt.ElideMiddle)
        browser_6.sig_file_changed.connect(label_6.setText)

        browser_7 = MDragFolderButton()
        label_7 = MLabel()
        label_7.set_elide_mode(QtCore.Qt.ElideRight)
        browser_7.sig_folder_changed.connect(label_7.setText)

        lay_3 = QtWidgets.QGridLayout()
        lay_3.addWidget(browser_6, 2, 0)
        lay_3.addWidget(browser_7, 2, 1)
        lay_3.addWidget(label_6, 3, 0)
        lay_3.addWidget(label_7, 3, 1)

        browser_8 = MDragFileButton(
            text="Click or drag media file here", multiple=False
        )
        browser_8.set_dayu_svg("media_line.svg")
        browser_8.set_dayu_filters([".mov", ".mp4"])
        browser_8_label = MLabel()
        browser_8_label.set_elide_mode(QtCore.Qt.ElideRight)
        self.register_field("current_file", "")
        self.bind("current_file", browser_8, "dayu_path", signal="sig_file_changed")
        self.bind("current_file", browser_8_label, "text")

        main_lay = QtWidgets.QVBoxLayout()
        main_lay.addWidget(MDivider("MClickBrowser*PushButton"))
        main_lay.addLayout(lay_1)
        main_lay.addWidget(MDivider("MClickBrowser*ToolButton"))
        main_lay.addLayout(lay_2)
        main_lay.addWidget(MDivider("MDragBrowser*ToolButton"))
        main_lay.addLayout(lay_3)
        main_lay.addWidget(MDivider("data bind"))
        main_lay.addWidget(browser_8)
        main_lay.addWidget(browser_8_label)
        main_lay.addStretch()
        self.setLayout(main_lay)


if __name__ == "__main__":
    # Import local modules
    from dayu_widgets import dayu_theme
    from dayu_widgets.qt import application

    with application() as app:
        test = BrowserExample()
        dayu_theme.apply(test)
        test.show()

{'project': 'edc', 'sequence type': 'ep03', 'shot asset': 'ep03_0050', 'pipeline step': 'efx', 'status': 'wtg',
 'assigned to': 'fanshiyuan', 'start': '2023-02-01', 'end': '2023-09-01', 'first look': '6.00 hrs', 'bid': '2.00 hrs',
 'time logged': '9.00 hrs', 'vfx node': '', 'retake bid': '8.00 hrs', 'artist note': 'note', '_parent': {'name': 'root',
                                                                                                         'children': [{
                                                                                                                          'project': 'wyd',
                                                                                                                          'sequence type': 'chr',
                                                                                                                          'shot asset': 'chr_klww',
                                                                                                                          'pipeline step': 'Modeling',
                                                                                                                          'status': 'ip',
                                                                                                                          'assigned to': 'fanshiyuan',
                                                                                                                          'start': '2023-05-01',
                                                                                                                          'end': '2023-10-01',
                                                                                                                          'first look': '8.00 hrs',
                                                                                                                          'bid': '8.00 hrs',
                                                                                                                          'time logged': '4.00 hrs',
                                                                                                                          'vfx node': '',
                                                                                                                          'retake bid': '0.00 hrs',
                                                                                                                          'artist note': 'note',
                                                                                                                          '_parent': {
                                                                                                                              ...}},
                                                                                                                      {
                                                                                                                          'project': 'wyd',
                                                                                                                          'sequence type': 'chr',
                                                                                                                          'shot asset': 'chr_yu',
                                                                                                                          'pipeline step': 'Modeling',
                                                                                                                          'status': 'ip',
                                                                                                                          'assigned to': 'fanshiyuan',
                                                                                                                          'start': '2023-05-01',
                                                                                                                          'end': '2023-10-01',
                                                                                                                          'first look': '8.00 hrs',
                                                                                                                          'bid': '8.00 hrs',
                                                                                                                          'time logged': '4.00 hrs',
                                                                                                                          'vfx node': '',
                                                                                                                          'retake bid': '0.00 hrs',
                                                                                                                          'artist note': 'note',
                                                                                                                          '_parent': {
                                                                                                                              ...}},
                                                                                                                      {
                                                                                                                          'project': 'tdtest',
                                                                                                                          'sequence type': 'test',
                                                                                                                          'shot asset': 'test_0020',
                                                                                                                          'pipeline step': 'comp',
                                                                                                                          'status': 'omt',
                                                                                                                          'assigned to': 'fanshiyuan, duoudo',
                                                                                                                          'start': '2023-06-01',
                                                                                                                          'end': '2023-08-01',
                                                                                                                          'first look': '6.00 hrs',
                                                                                                                          'bid': '6.00 hrs',
                                                                                                                          'time logged': '2.00 hrs',
                                                                                                                          'vfx node': '',
                                                                                                                          'retake bid': '2.00 hrs',
                                                                                                                          'artist note': 'note',
                                                                                                                          '_parent': {
                                                                                                                              ...}},
                                                                                                                      {
                                                                                                                          'project': 'tdtest',
                                                                                                                          'sequence type': 'test',
                                                                                                                          'shot asset': 'test_0020',
                                                                                                                          'pipeline step': 'pcomp',
                                                                                                                          'status': 'omt',
                                                                                                                          'assigned to': 'duoduo',
                                                                                                                          'start': '2023-06-01',
                                                                                                                          'end': '2023-08-01',
                                                                                                                          'first look': '6.00 hrs',
                                                                                                                          'bid': '6.00 hrs',
                                                                                                                          'time logged': '2.00 hrs',
                                                                                                                          'vfx node': '',
                                                                                                                          'retake bid': '2.00 hrs',
                                                                                                                          'artist note': 'note',
                                                                                                                          '_parent': {
                                                                                                                              ...}},
                                                                                                                      {
                                                                                                                          'project': 'tdtest',
                                                                                                                          'sequence type': 'test',
                                                                                                                          'shot asset': 'test_0020',
                                                                                                                          'pipeline step': 'ani',
                                                                                                                          'status': 'omt',
                                                                                                                          'assigned to': 'huahua',
                                                                                                                          'start': '2023-06-01',
                                                                                                                          'end': '2023-08-01',
                                                                                                                          'first look': '6.00 hrs',
                                                                                                                          'bid': '6.00 hrs',
                                                                                                                          'time logged': '2.00 hrs',
                                                                                                                          'vfx node': '',
                                                                                                                          'retake bid': '2.00 hrs',
                                                                                                                          'artist note': 'note',
                                                                                                                          '_parent': {
                                                                                                                              ...}},
                                                                                                                      {
                                                                                                                          'project': 'tdtest',
                                                                                                                          'sequence type': 'test',
                                                                                                                          'shot asset': 'ep_0020',
                                                                                                                          'pipeline step': 'ani',
                                                                                                                          'status': 'fin',
                                                                                                                          'assigned to': 'rrfz',
                                                                                                                          'start': '2023-06-01',
                                                                                                                          'end': '2023-08-01',
                                                                                                                          'first look': '6.00 hrs',
                                                                                                                          'bid': '6.00 hrs',
                                                                                                                          'time logged': '2.00 hrs',
                                                                                                                          'vfx node': '',
                                                                                                                          'retake bid': '2.00 hrs',
                                                                                                                          'artist note': 'note',
                                                                                                                          '_parent': {
                                                                                                                              ...}},
                                                                                                                      {
                                                                                                                          'project': 'tdtest',
                                                                                                                          'sequence type': 'sc',
                                                                                                                          'shot asset': 'sc_0030',
                                                                                                                          'pipeline step': 'rig',
                                                                                                                          'status': 'hld',
                                                                                                                          'assigned to': 'huahua',
                                                                                                                          'start': '2023-06-01',
                                                                                                                          'end': '2023-08-01',
                                                                                                                          'first look': '6.00 hrs',
                                                                                                                          'bid': '6.00 hrs',
                                                                                                                          'time logged': '2.00 hrs',
                                                                                                                          'vfx node': '',
                                                                                                                          'retake bid': '2.00 hrs',
                                                                                                                          'artist note': 'note',
                                                                                                                          '_parent': {
                                                                                                                              ...}},
                                                                                                                      {
                                                                                                                          'project': 'qaz',
                                                                                                                          'sequence type': 'ep01',
                                                                                                                          'shot asset': 'ep01_0040',
                                                                                                                          'pipeline step': 'comp',
                                                                                                                          'status': 'fin',
                                                                                                                          'assigned to': 'mm',
                                                                                                                          'start': '2023-04-01',
                                                                                                                          'end': '2023-11-01',
                                                                                                                          'first look': '4.00 hrs',
                                                                                                                          'bid': '6.00 hrs',
                                                                                                                          'time logged': '6.00 hrs',
                                                                                                                          'vfx node': '',
                                                                                                                          'retake bid': '7.00 hrs',
                                                                                                                          'artist note': 'note',
                                                                                                                          '_parent': {
                                                                                                                              ...}},
                                                                                                                      {
                                                                                                                          'project': 'edc',
                                                                                                                          'sequence type': 'ep01',
                                                                                                                          'shot asset': 'ep01_0020',
                                                                                                                          'pipeline step': 'ani',
                                                                                                                          'status': 'rtk',
                                                                                                                          'assigned to': 'rrfz',
                                                                                                                          'start': '2023-06-01',
                                                                                                                          'end': '2023-08-01',
                                                                                                                          'first look': '6.00 hrs',
                                                                                                                          'bid': '6.00 hrs',
                                                                                                                          'time logged': '2.00 hrs',
                                                                                                                          'vfx node': '',
                                                                                                                          'retake bid': '2.00 hrs',
                                                                                                                          'artist note': 'note',
                                                                                                                          '_parent': {
                                                                                                                              ...}},
                                                                                                                      {
                                                                                                                          'project': 'yhg',
                                                                                                                          'sequence type': 'ep02',
                                                                                                                          'shot asset': 'ep02_0020',
                                                                                                                          'pipeline step': 'ani',
                                                                                                                          'status': 'pub',
                                                                                                                          'assigned to': 'rrfz',
                                                                                                                          'start': '2023-06-01',
                                                                                                                          'end': '2023-08-01',
                                                                                                                          'first look': '6.00 hrs',
                                                                                                                          'bid': '6.00 hrs',
                                                                                                                          'time logged': '2.00 hrs',
                                                                                                                          'vfx node': '',
                                                                                                                          'retake bid': '2.00 hrs',
                                                                                                                          'artist note': 'note',
                                                                                                                          '_parent': {
                                                                                                                              ...}},
                                                                                                                      {
                                                                                                                          'project': 'wsx',
                                                                                                                          'sequence type': 'ep02',
                                                                                                                          'shot asset': 'ep02_0070',
                                                                                                                          'pipeline step': 'mm',
                                                                                                                          'status': 'rdy',
                                                                                                                          'assigned to': 'fanshiyuan',
                                                                                                                          'start': '2023-03-01',
                                                                                                                          'end': '2023-10-01',
                                                                                                                          'first look': '1.00 hrs',
                                                                                                                          'bid': '6.00 hrs',
                                                                                                                          'time logged': '3.00 hrs',
                                                                                                                          'vfx node': '',
                                                                                                                          'retake bid': '5.00 hrs',
                                                                                                                          'artist note': 'note',
                                                                                                                          '_parent': {
                                                                                                                              ...}},
                                                                                                                      {
                                                                                                                          ...}]}}
