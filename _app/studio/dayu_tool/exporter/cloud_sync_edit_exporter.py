#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/4 13:49

__author__ = 'pengyuxuan'

from ui_center.qt import *
import hiero.core as hcore
from hiero.exporters import FnExternalRender, FnExternalRenderUI
import copy
import time


class EditSyncExportTask(FnExternalRender.ExternalRenderTask):
    def __init__(self, initDict):
        super(EditSyncExportTask, self).__init__(initDict)

        self._renderTask = None
        self._fps = self._item.source().framerate().toFloat()
        self._frame = 0
        self._progress = 0.0
        self._finished = False

    def preShot(self):
        super(EditSyncExportTask, self).preShot()

        from db.disk_path import DiskPath

        export_path = DiskPath(self.resolvedExportPath())
        self.version_orm = export_path.orm()
        if not self.version_orm:
            raise Exception('no orm for path: {}'.format(export_path))

    def startTask(self):
        super(EditSyncExportTask, self).startTask()

    def taskStep(self):
        self._frame += 1
        if self._frame % 10 != 0:
            return (self._finished == False)

        import app
        import app._shotgun
        import app.utils

        coin = app.DAYU.request('/pm/publish_dailies')(self.version_orm)
        app._shotgun.shotgun_sync_edit_version(coin, None)
        self._progress = 1.0
        self._finished = True

        return (self._finished == False)

    def progress(self):
        return self._progress

    def forcedAbort(self):
        super(EditSyncExportTask, self).forcedAbort()


class EditSyncExportPreset(FnExternalRender.ExternalRenderPreset):
    def __init__(self, name, properties):
        super(EditSyncExportPreset, self).__init__(name, properties)
        self._parentType = EditSyncExportTask
        self._properties.update(properties)

    def supportedItems(self):
        return hcore.TaskPresetBase.kTrackItem


class EditCloudExportUI(FnExternalRenderUI.ExternalRenderTaskUI):
    def __init__(self, preset):
        super(EditCloudExportUI, self).__init__(preset)
        self._displayName = 'Sync Edit'
        self._taskType = EditSyncExportTask
        self.widget = None

    def populateUI(self, widget, exportTemplate):
        super(EditCloudExportUI, self).populateUI(widget, exportTemplate)
