#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/16/2018 5:04 PM

__author__ = 'pengyuxuan'

from hiero.exporters import FnTranscodeExporter, FnTranscodeExporterUI
from hiero.exporters import FnExternalRenderUI, FnExternalRender
import hiero


class DaYuTransCode(FnTranscodeExporter.TranscodeExporter):
    def __init__(self, init_dict):
        super(DaYuTransCode, self).__init__(init_dict)
        self.version_orm = None

    def preShot(self):
        super(DaYuTransCode, self).preShot()
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
        super(DaYuTransCode, self).postShot()
        import db
        from db.disk_path import DiskPath
        export_path = DiskPath(self.resolvedExportPath())
        version_orm = export_path.orm()
        version_orm.rescan(confirm=True)
        db.get_session().commit()
        print 'rescan done!'


class DaYuTransCodePreset(FnTranscodeExporter.TranscodePreset):

    def __init__(self, name, properties):
        hiero.core.RenderTaskPreset.__init__(self, DaYuTransCode, name, properties)
        self.properties()["keepNukeScript"] = False
        self.properties()["readAllLinesForExport"] = self._defaultReadAllLinesForCodec()
        self.properties()["useSingleSocket"] = False
        self.properties()["burninDataEnabled"] = False
        self.properties()["burninData"] = dict(
            (datadict["knobName"], None) for datadict in FnExternalRender.NukeRenderTask.burninPropertyData)
        self.properties()["additionalNodesEnabled"] = False
        self.properties()["additionalNodesData"] = []
        self.properties()["method"] = "Blend"
        self.properties()["includeEffects"] = True
        self.properties()["includeAudio"] = False
        self.properties()["deleteAudio"] = True

        # Give the Write node a name, so it can be referenced elsewhere
        if "writeNodeName" not in self.properties():
            self.properties()["writeNodeName"] = "Write_{ext}"

        self.properties().update(properties)


class DaYuTransCodeUI(FnTranscodeExporterUI.TranscodeExporterUI):

    def __init__(self, preset):
        FnExternalRenderUI.NukeRenderTaskUI.__init__(self, preset, DaYuTransCode,
                                                     "dayu transcode ")
        self._tags = []
