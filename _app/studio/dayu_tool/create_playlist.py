#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'yangzhuo'

import wrap_shotgun as ws
from ui_center.qt import *
from ui_center.widgets import ui_utils
from ui_center.widgets.message_box import MSuccessMessageBox


class CreatePlaylistWidget(QDialog):
    @ui_utils.dayu_css()
    def __init__(self, parent=None):
        super(CreatePlaylistWidget, self).__init__(parent=parent)
        self.playlist_name = QLineEdit()
        self.playlist_name.setPlaceholderText(u'请不要输入中文')
        self.playlist_name.textChanged.connect(self.enable_button)
        lay = QFormLayout()
        lay.addRow(QLabel('Playlist Name: '), self.playlist_name)
        self.create_btn = QPushButton('Create Playlist', clicked=self.create)
        self.create_btn.setEnabled(False)
        main_lay = QVBoxLayout()
        main_lay.addStretch()
        main_lay.addLayout(lay)
        main_lay.addStretch()
        main_lay.addWidget(self.create_btn)
        self.setLayout(main_lay)
        self.resize(300, 100)

    def enable_button(self):
        self.create_btn.setEnabled(True)

    def setup_data(self, item_list):
        setattr(self, 'track_item_list', item_list)

    def create(self):
        sg = ws.MyShotgun()
        sg_version_list = []
        project_name = None

        for x in self.track_item_list:
            project_name = x.project().name()
            sg_project = sg.find_one('Project', [['name', 'is', project_name]])
            version = sg.find_one('Version', [['code', 'is', x.currentVersion().name()],
                                              ['project', 'is', sg_project]], ['id'])
            if not version:
                continue
            sg_version_list.append(version.get('id'))

        project = sg.find_one('Project', [['name', 'is', project_name]])
        play_list = sg.create('Playlist', {'code': self.playlist_name.text(), 'project': project})
        version = sg.find('Version', [['id', 'in', sg_version_list]])
        sg.update('Playlist', play_list['id'], {'versions': version})
        MSuccessMessageBox('Create Playlist Success!').exec_()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    test = CreatePlaylistWidget()
    test.show()
    sys.exit(app.exec_())
