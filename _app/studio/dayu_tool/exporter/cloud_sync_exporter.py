#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re

__author__ = 'andyguo'

from ui_center.qt import *

import hiero.core as hcore
from hiero.exporters import FnExternalRender, FnExternalRenderUI
import copy
import time


class CloudSyncExportTask(FnExternalRender.ExternalRenderTask):
    def __init__(self, initDict):
        super(CloudSyncExportTask, self).__init__(initDict)

        self._renderTask = None
        self._fps = self._item.source().framerate().toFloat()
        self._frame = 0
        self._progress = 0.0
        self._finished = False

    def preShot(self):
        super(CloudSyncExportTask, self).preShot()

        from db.disk_path import DiskPath

        export_path = DiskPath(self.resolvedExportPath())
        self.version_orm = export_path.orm()
        if not self.version_orm:
            raise Exception('no orm for path: {}'.format(export_path))

    def startTask(self):
        super(CloudSyncExportTask, self).startTask()

    def taskStep(self):
        self._frame += 1
        if self._frame % 10 != 0:
            return (self._finished == False)

        import app
        import app._shotgun
        import app.utils

        coin = app.DAYU.request('/pm/publish_dailies')(self.version_orm)
        app._shotgun.shotgun_sync_version(coin, None)
        self._progress = 1.0
        self._finished = True

        return (self._finished == False)

    def progress(self):
        return self._progress

    def forcedAbort(self):
        super(CloudSyncExportTask, self).forcedAbort()


class CloudSyncExportPreset(FnExternalRender.ExternalRenderPreset):
    def __init__(self, name, properties):
        super(CloudSyncExportPreset, self).__init__(name, properties)
        self._parentType = CloudSyncExportTask
        self._properties.update(properties)

    def supportedItems(self):
        return hcore.TaskPresetBase.kTrackItem


class SyncCloudExportUI(FnExternalRenderUI.ExternalRenderTaskUI):
    def __init__(self, preset):
        super(SyncCloudExportUI, self).__init__(preset)
        self._displayName = 'Sync Cloud'
        self._taskType = CloudSyncExportTask
        self.widget = None

    def populateUI(self, widget, exportTemplate):
        super(SyncCloudExportUI, self).populateUI(widget, exportTemplate)
