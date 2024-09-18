#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import hiero.core as hcore
import hiero.ui as  hui

# import custom_exporter
import ffmpeg_exporter
import oiio_exporter
import cloud_sync_exporter
import dayu_copy_exporter
import dayu_transcode
import cloud_sync_edit_exporter

# hcore.taskRegistry.registerTask(custom_exporter.Exporter_PLT_Preset, custom_exporter.Exporter_PLT)
# hui.taskUIRegistry.registerTaskUI(custom_exporter.Exporter_PLT_Preset, custom_exporter.Exporter_PLT_UI)

hcore.taskRegistry.registerTask(cloud_sync_exporter.CloudSyncExportPreset, cloud_sync_exporter.CloudSyncExportTask)
hui.taskUIRegistry.registerTaskUI(cloud_sync_exporter.CloudSyncExportPreset, cloud_sync_exporter.SyncCloudExportUI)

hcore.taskRegistry.registerTask(cloud_sync_edit_exporter.EditSyncExportPreset,
                                cloud_sync_edit_exporter.EditSyncExportTask)
hui.taskUIRegistry.registerTaskUI(cloud_sync_edit_exporter.EditSyncExportPreset,
                                  cloud_sync_edit_exporter.EditCloudExportUI)

hcore.taskRegistry.registerTask(ffmpeg_exporter.FFmpegExportPreset, ffmpeg_exporter.FFmpegExportTask)
hui.taskUIRegistry.registerTaskUI(ffmpeg_exporter.FFmpegExportPreset, ffmpeg_exporter.FFmpegExportUI)

hcore.taskRegistry.registerTask(oiio_exporter.OiioExportPreset, oiio_exporter.OiioExportTask)
hui.taskUIRegistry.registerTaskUI(oiio_exporter.OiioExportPreset, oiio_exporter.OiioExportUI)

hcore.taskRegistry.registerTask(dayu_copy_exporter.DaYuCopyPreset, dayu_copy_exporter.DaYuCopyExporter)
hui.taskUIRegistry.registerTaskUI(dayu_copy_exporter.DaYuCopyPreset, dayu_copy_exporter.DaYuCopyExporterUI)

hcore.taskRegistry.registerTask(dayu_transcode.DaYuTransCodePreset, dayu_transcode.DaYuTransCode)
hui.taskUIRegistry.registerTaskUI(dayu_transcode.DaYuTransCodePreset, dayu_transcode.DaYuTransCodeUI)
