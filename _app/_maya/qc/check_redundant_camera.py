#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Author: he sen
# Date  : 2023/9/14 16:38
# Email : h_s0325@sina.com
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from _app.qc_base import MQCBase


class CheckRedundantCameras(MQCBase):
    name = 'Validate redundant cameras'
    usage = u'校验|ASSET|层级内是否存在冗余相机。'

    special_level = '|ASSET|'

    error_message = u'|ASSET|层级下包含冗余相机'

    def __init__(self):
        super(CheckRedundantCameras, self).__init__()
        self.user_cameras = []

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['rig']:
            return True
        else:
            return False


    def run(self, *args, **kwargs):
        import pymel.core as pm
        flag = bool
        hierarchy_transform = pm.PyNode(self.special_level)
        cameras = [cam.getParent() for cam in pm.listRelatives(hierarchy_transform, ad=True, type="camera")]

        if cameras:
            pm.select(cameras)
            flag = False
        else:
            flag = True
        if flag:
            self.error_message = ""
            return True
        else:
            return False


def get_qc():
    return CheckRedundantCameras()