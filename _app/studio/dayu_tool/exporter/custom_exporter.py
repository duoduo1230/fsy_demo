#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import hiero.core as hcore
import hiero.ui as hui
from hiero.exporters import FnTranscodeExporter, FnTranscodeExporterUI
import db
from db.disk_path import DiskPath
import db.util


class Exporter_PLT(FnTranscodeExporter.TranscodeExporter):
    def __init__(self, init_dict):
        print init_dict
        super(Exporter_PLT, self).__init__(init_dict)
        print  '---------------'
        print self.resolvedExportPath()
        print self.inputRange()
        print self.outputRange()

    def _before_render(self):
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

    def startTask(self):
        self._before_render()
        super(Exporter_PLT, self).startTask()

    def _after_render(self):
        self.version_orm.rescan(confirm=True)
        db.get_session().commit()

    def finishTask(self):
        super(Exporter_PLT, self).finishTask()
        self._after_render()
        return


class Exporter_PLT_Preset(FnTranscodeExporter.TranscodePreset):
    def __init__(self, name, properties):
        super(Exporter_PLT_Preset, self).__init__(name, properties)
        self._parentType = Exporter_PLT
        self._properties.update(properties)

    def supportedItems(self):
        return hcore.TaskPresetBase.kTrackItem


class Exporter_PLT_UI(FnTranscodeExporterUI.TranscodeExporterUI):
    def __init__(self, preset):
        super(Exporter_PLT_UI, self).__init__(preset)
        self._displayName = 'PLT Transcode'
        self._taskType = Exporter_PLT

    def populateUI(self, widget, exportTemplate):
        super(Exporter_PLT_UI, self).populateUI(widget, exportTemplate)
