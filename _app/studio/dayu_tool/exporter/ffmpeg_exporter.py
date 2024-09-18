#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import copy
import re

import hiero.core as hcore
from hiero.exporters import FnExternalRender, FnExternalRenderUI

from app._hiero.submission import ffmpeg_submission
from cas_combobox import DYCascadingEnumerationComboBox
from ui_center.qt import *


class FFmpegExportTask(FnExternalRender.ExternalRenderTask):
    def __init__(self, initDict):
        super(FFmpegExportTask, self).__init__(initDict)

        self._renderTask = None
        self._submission = ffmpeg_submission.FFmpegSubmission()
        self._fps = self._item.source().framerate().toFloat()
        if self._submission is not None:
            # Pass the frame range through to the submission.  This is useful for rendering through the frame
            # server, otherwise it would have to evaluate the script to determine it.
            start, end = self.outputRange()
            submissionDict = copy.copy(initDict)
            submissionDict["startFrame"] = start
            submissionDict["endFrame"] = end

            # Create a job on our submission to do the actual rendering.
            self._renderTask = self._submission.addJob(ffmpeg_submission.FFmpegSubmission.kRender,
                                                       submissionDict)

    def preShot(self):
        super(FFmpegExportTask, self).preShot()
        if not self._preset.properties().get('connect_db', None):
            return

        import db
        from db.disk_path import DiskPath

        session = db.get_session()
        export_path = DiskPath(self.resolvedExportPath())
        self.version_orm = export_path.orm()
        if not self.version_orm:
            raise Exception('no orm for path: {}'.format(export_path))

        old_dict = dict(self.version_orm.path_data)
        if self._fileext.lower() in ('.mov', '.mp4', '.avi', '.r3d'):
            old_dict.update({'di_full_path_mov': [self._fileinfo.filename()]})
        else:
            _filename = DiskPath(self._fileinfo.filename())
            old_dict.update({'di_full_path_seq':
                                 [_filename.restore_pattern(x)
                                  for x in range(
                                         int(self._fileinfo.startFrame()) + int(self._item.sourceIn()),
                                         int(self._fileinfo.startFrame()) + int(
                                                 self._item.sourceOut()) + 1)] if _filename.pattern else [_filename]})
        self.version_orm.path_data = old_dict
        session.commit()

    def postShot(self):
        super(FFmpegExportTask, self).postShot()
        if self._preset.properties().get('connect_db', None):
            import re
            import db
            from db.disk_path import DiskPath

            camera_name_regex = re.compile(r'^([a-zA-Z]\d+)_*?([a-zA-Z]\d+).*')
            session = db.get_session()
            self.version_orm.rescan(confirm=True)

            _filename = DiskPath(self._fileinfo.filename()).stem
            match = camera_name_regex.match(_filename)
            if match:
                _filename = ''.join(match.groups())

            shot_orm = self.version_orm.find_meaning('SHOT')
            if shot_orm:
                cam_clue = set(shot_orm.cam_clue)
                cam_clue.add(_filename)
                shot_orm.cam_clue = list(cam_clue)

            session.commit()

    def startTask(self):
        super(FFmpegExportTask, self).startTask()
        self._renderTask.startTask()

    def taskStep(self):
        result = self._renderTask.taskStep()
        return result

    def progress(self):
        return self._renderTask.progress()

    def forcedAbort(self):
        self._renderTask.forceAbort()


class FFmpegExportPreset(FnExternalRender.ExternalRenderPreset):
    def __init__(self, name, properties):
        super(FFmpegExportPreset, self).__init__(name, properties)
        self._parentType = FFmpegExportTask
        self._properties.update(properties)

    def supportedItems(self):
        return hcore.TaskPresetBase.kTrackItem


class FFmpegExportUI(FnExternalRenderUI.ExternalRenderTaskUI):
    def __init__(self, preset):
        super(FFmpegExportUI, self).__init__(preset)
        self._displayName = 'ffmpeg transcode'
        self._taskType = FFmpegExportTask

    def populateUI(self, widget, exportTemplate):
        super(FFmpegExportUI, self).populateUI(widget, exportTemplate)
        self.widget = widget
        layout = widget.layout()
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        if isinstance(layout, QFormLayout):
            layout.addRow('', form_layout)
        else:
            layout.addLayout(form_layout)

        # OCIO config file browser
        file_lay = QHBoxLayout()
        self.line_edit = QLineEdit()
        self.file_button = QPushButton('Browse')
        self.file_button.clicked.connect(self.slot_browser_file)
        self.line_edit.setText(self._preset.properties().get('ocio_config_path', ''))
        file_lay.addWidget(self.line_edit)
        file_lay.addWidget(self.file_button)

        self.color_space_combo_box = DYCascadingEnumerationComboBox()
        self.color_space_combo_box.setFixedWidth(300)
        self.color_space_combo_box.setup_menu(self.get_cascading_value())
        if self._preset.properties().get('output_colorspace', None):
            self.color_space_combo_box.setCurrentIndex(self.color_space_combo_box.findText(
                    self._preset.properties()['output_colorspace']))
        self.color_space_combo_box.currentIndexChanged.connect(self.slot_color_space_changed)

        db_lay = QHBoxLayout()
        db_check_box = QCheckBox('')
        db_check_box.stateChanged.connect(self.slot_db_check_changed)
        db_check_box.setChecked(self._preset.properties().get('connect_db', False))
        db_lay.addWidget(db_check_box)

        self.format_comobo_box = QComboBox()
        self.format_comobo_box.addItems(
                ['prores 422', 'prores 422 lt', 'prores 422 hq', 'prores 4444', 'h264', 'tiff', 'jpg'])
        self.format_comobo_box.currentIndexChanged.connect(self.slot_format_changed)
        index = self.format_comobo_box.findText(self._preset.properties().get('output_format', '__'))
        self.format_comobo_box.setCurrentIndex(index)

        self.width_spin_box = QSpinBox()
        self.width_spin_box.setRange(0, 99999)
        self.width_spin_box.valueChanged.connect(self.slot_width_changed)
        self.width_spin_box.setValue(self._preset.properties().get('width', 0))
        self.height_spin_box = QSpinBox()
        self.height_spin_box.setRange(0, 99999)
        self.height_spin_box.valueChanged.connect(self.slot_height_changed)
        self.height_spin_box.setValue(self._preset.properties().get('height', 0))
        resolution_layout = QHBoxLayout()
        resolution_layout.setContentsMargins(0, 0, 0, 0)
        resolution_layout.addWidget(QLabel('w'))
        resolution_layout.addWidget(self.width_spin_box)
        resolution_layout.addSpacing(20)
        resolution_layout.addWidget(QLabel('h'))
        resolution_layout.addWidget(self.height_spin_box)

        form_layout.addRow('OCIO Config:', file_lay)
        form_layout.addRow("Output Color Space:", self.color_space_combo_box)
        form_layout.addRow('Connect DB:', db_lay)
        form_layout.addRow('Pre-Reformat:', resolution_layout)
        form_layout.addRow('Output Format:', self.format_comobo_box)

    def slot_db_check_changed(self, state):
        self._preset.properties()['connect_db'] = (state == Qt.Checked)

    def slot_format_changed(self, index):
        self._preset.properties()['output_format'] = self.format_comobo_box.itemText(index)

    def slot_width_changed(self, value):
        self._preset.properties()['width'] = value

    def slot_height_changed(self, value):
        self._preset.properties()['height'] = value

    def slot_browser_file(self):
        f, flag = QFileDialog.getOpenFileName(self.widget, 'OCIO Config', '', 'OCIO(*.ocio)')
        if flag and f:
            self.line_edit.setText(f)
            self._preset.properties()['ocio_config_path'] = f
            self.color_space_combo_box.setup_menu(self.get_cascading_value())

    def slot_color_space_changed(self, index):
        new_color_space = self.color_space_combo_box.itemText(index)
        self._preset.properties()['output_colorspace'] = new_color_space
        print 'slot_color_space_changed', self._preset.properties()['output_colorspace']

    def get_cascading_value(self):
        import os
        ocio_file = self._preset.properties().get('ocio_config_path', None)
        if not ocio_file: return ['None']
        if os.path.exists(ocio_file):
            with open(ocio_file, 'r') as yf:
                import yaml
                string = '\n'.join(yf.readlines())
                string = re.sub(r'!<.*>', '', string)
                data = yaml.load(string)
                return [x['family'] + '/' + x['name'] for x in data['colorspaces']]
        return ['None']
