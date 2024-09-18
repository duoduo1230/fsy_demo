#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re

__author__ = 'andyguo'

from ui_center.qt import *

import hiero.core as hcore
from hiero.exporters import FnExternalRender, FnExternalRenderUI
from app._hiero.submission import oiio_submission
import copy
from cas_combobox import DYCascadingEnumerationComboBox


class OiioExportTask(FnExternalRender.ExternalRenderTask):
    def __init__(self, initDict):
        super(OiioExportTask, self).__init__(initDict)

        self._renderTask = None
        self._submission = oiio_submission.OiioSubmission()
        self._fps = self._item.source().framerate().toFloat()
        if self._submission is not None:
            # Pass the frame range through to the submission.  This is useful for rendering through the frame
            # server, otherwise it would have to evaluate the script to determine it.
            start, end = self.outputRange()
            submissionDict = copy.copy(initDict)
            submissionDict["startFrame"] = start
            submissionDict["endFrame"] = end

            # Create a job on our submission to do the actual rendering.
            self._renderTask = self._submission.addJob(oiio_submission.OiioSubmission.kRender,
                                                       submissionDict)

    def preShot(self):
        super(OiioExportTask, self).preShot()
        if not self._preset.properties()['connect_db']:
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
        super(OiioExportTask, self).postShot()
        if not self._preset.properties()['connect_db']:
            return

        import db
        session = db.get_session()
        self.version_orm.rescan(confirm=True)
        session.commit()

    def startTask(self):
        super(OiioExportTask, self).startTask()
        self._renderTask.startTask()

    def taskStep(self):
        result = self._renderTask.taskStep()
        return result

    def progress(self):
        return self._renderTask.progress()

    def forcedAbort(self):
        self._renderTask.forceAbort()


class OiioExportPreset(FnExternalRender.ExternalRenderPreset):
    def __init__(self, name, properties):
        super(OiioExportPreset, self).__init__(name, properties)
        self._parentType = OiioExportTask
        self._properties.update(properties)

    def supportedItems(self):
        return hcore.TaskPresetBase.kTrackItem


class OiioExportUI(FnExternalRenderUI.ExternalRenderTaskUI):
    def __init__(self, preset):
        super(OiioExportUI, self).__init__(preset)
        self._displayName = 'oiio transcode'
        self._taskType = OiioExportTask
        self.widget = None

    def populateUI(self, widget, exportTemplate):
        super(OiioExportUI, self).populateUI(widget, exportTemplate)
        self.widget = widget
        resolution_layout = widget.layout()
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        if isinstance(resolution_layout, QFormLayout):
            resolution_layout.addRow('', form_layout)
        else:
            resolution_layout.addLayout(form_layout)

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
        db_check_box.setChecked(False)
        db_check_box.stateChanged.connect(self.slot_db_check_changed)
        db_check_box.setChecked(self._preset.properties().get('connect_db', False))
        db_lay.addWidget(db_check_box)

        self.width_spin_box = QSpinBox()
        self.width_spin_box.setRange(0, 99999)
        self.width_spin_box.valueChanged.connect(self.slot_width_changed)
        self.width_spin_box.setValue(self._preset.properties().get('width', 2048))
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
        form_layout.addRow('Resolution:', resolution_layout)
        form_layout.addRow('Connect DB:', db_lay)

    def slot_db_check_changed(self, state):
        self._preset.properties()['connect_db'] = (state == Qt.Checked)

    def slot_browser_file(self):
        f, flag = QFileDialog.getOpenFileName(self.widget, 'OCIO Config', '', 'OCIO(*.ocio)')
        if flag and f:
            self.line_edit.setText(f)
            self._preset.properties()['ocio_config_path'] = f
            self.color_space_combo_box.setup_menu(self.get_cascading_value())

    def slot_color_space_changed(self, index):
        new_color_space = self.color_space_combo_box.itemText(index)
        self._preset.properties()['output_colorspace'] = new_color_space

    def slot_width_changed(self, value):
        self._preset.properties()['width'] = value

    def slot_height_changed(self, value):
        self._preset.properties()['height'] = value

    def get_cascading_value(self):
        ocio_file = self._preset.properties().get('ocio_config_path', None)
        if ocio_file:
            with open(ocio_file, 'r') as yf:
                import yaml
                string = '\n'.join(yf.readlines())
                string = re.sub(r'!<.*>', '', string)
                data = yaml.load(string)
                return [x['family'] + '/' + x['name'] for x in data['colorspaces']]
        return ['None']
