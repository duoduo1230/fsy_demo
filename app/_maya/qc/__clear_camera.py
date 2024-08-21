#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'

from app.qc_base import MQCBase


class ClearCamera(MQCBase):
    name = 'Clear camera'
    usage = u'检查多余相机'

    def __init__(self, parent=None):
        super(ClearCamera, self).__init__(parent)

    def validate(self, options):
        if options.get('type_group') in ['type_group'] and options.get('type') in ['mdl', 'rig']:
            return True
        else:
            return False

    def get_all(self):
        import pymel.core as pm
        default_cameras = ['frontShape', 'perspShape', 'sideShape', 'topShape']

        return [cam for cam in pm.ls(cameras=1) if cam.name() not in default_cameras]

    def run(self, *args, **kwargs):
        self.extra_data = self.get_all()
        self.error_message = ''
        if self.extra_data:
            self.error_message = u'场景中多余的相机：<br/>'
            for cam in self.extra_data:
                self.error_message += u'{}<br/>'.format(cam.name())
            return False
        else:
            self.error_message = ''
            return True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        import app._maya.util as util
        if not self.extra_data:
            util.message(u'没有可修复的数据', dialog=True)
        else:
            pm.delete(self.extra_data)


def get_qc():
    return ClearCamera()
