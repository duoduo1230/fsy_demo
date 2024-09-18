#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'pengyuxuan'

import os
import shutil
import hiero.core
from hiero.core import util
from hiero.exporters import FnFrameExporter
from ui_center.qt import *


class DaYuCopyExporter(FnFrameExporter.FrameExporter):
    def __init__(self, initDict):
        """Initialize"""
        FnFrameExporter.FrameExporter.__init__(self, initDict)
        self.version_orm = None
        if self.nothingToDo():
            return

    def startTask(self):
        # FrameExporter 重载 startTask 的时候直接覆盖了 shotTask的 startTask的方法(没有使用super),
        # 导致preShot 不会运行，所以必须重载一次startTask 手动调用preShot
        super(DaYuCopyExporter, self).startTask()
        self.preShot()

    def preShot(self):
        # 往数据库写入 di_full_path
        super(DaYuCopyExporter, self).preShot()
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
        super(DaYuCopyExporter, self).postShot()
        import db
        self.version_orm.rescan(confirm=True)
        db.get_session().commit()
        print 'rescan done!'

    def _try_copy(self, src, dst):

        overwrite = self._preset.properties()['overwrite']

        def __compare_size_and_copy(source, target):
            if os.path.exists(target):
                if os.path.getsize(source) != os.path.getsize(target):
                    shutil.copy2(source, target)
            else:
                shutil.copy2(source, target)

        try:
            if overwrite:
                shutil.copy2(util.asUnicode(src), util.asUnicode(dst))
            else:
                __compare_size_and_copy(util.asUnicode(src), util.asUnicode(dst))

        except shutil.Error, e:
            # Dont need to report this as an error
            if e.message.endswith("are the same file"):
                pass
            else:
                self.setError("Unable to copy file. %s" % e.message)
        except OSError as err:
            if err.errno == 45:  # ENOTSUP
                pass
            else:
                raise

    def doFrame(self, src, dst):
        dstdir = os.path.dirname(dst)
        util.filesystem.makeDirs(dstdir)
        self._try_copy(src, dst)

    def taskStep(self):
        ret = FnFrameExporter.FrameExporter.taskStep(self)
        # print 'run %s' % self._frame
        return ret and not self._singleFile


class DaYuCopyPreset(hiero.core.TaskPresetBase):
    def __init__(self, name, properties):
        hiero.core.TaskPresetBase.__init__(self, DaYuCopyExporter, name)
        self.properties().update(properties)

    def supportedItems(self):
        return hiero.core.TaskPresetBase.kTrackItem


class DaYuCopyExporterUI(hiero.ui.TaskUIBase):
    def __init__(self, preset):
        """Initialize"""
        hiero.ui.TaskUIBase.__init__(self, DaYuCopyExporter, preset, "dayu copy ")
        self.widget = None

    def populateUI(self, widget, exportTemplate):
        super(DaYuCopyExporterUI, self).populateUI(widget, exportTemplate)
        self.widget = widget
        lay = self.widget.layout()
        formlay = QFormLayout()
        lay.addLayout(formlay)
        over_write_box = QCheckBox()
        formlay.addRow('Over Write', over_write_box)

        self._preset.properties()['overwrite'] = 0
        over_write_box.stateChanged.connect(self.slot_overwrite_changed)

    def slot_overwrite_changed(self, data):
        self._preset.properties()['overwrite'] = data
