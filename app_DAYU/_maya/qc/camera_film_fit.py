#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Author: he sen
# Date  : 2023/4/23 16:58
# Email : h_s0325@sina.com
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from app_DAYU.qc_base import MQCBase


class CheckCameraFilmFit(MQCBase):
    name = 'Validate Camera Fit Resolution Gate'
    usage = u'校验相机Fit Resolution Gate属性，是否设置为Horizontal。'
    DEFAULT_CAMERAS = ('frontShape', 'perspShape', 'sideShape', 'topShape')
    special_level = '|SCENE|CAMERAS|'
    check_camera_attr = ['filmFit']
    error_message = ''

    def __init__(self):
        super(CheckCameraFilmFit, self).__init__()
        self.user_cameras = []

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['ani']:
            return True
        else:
            return False

    # def check_film_fit(self, camera_list):
    #     import pymel.core as pm
    #     for c in camera_list:
    #         for attr in self.check_camera_attr:
    #             check = pm.getAttr('{name}.{attr}'.format(name=c, attr=attr))
    #             if check != 1:
    #                 return False
    #             else:
    #                 return True

    def run(self, *args, **kwargs):
        import pymel.core as pm
        flag = bool
        camera_list = pm.ls(type='camera')
        self.user_cameras = [cam for cam in camera_list if cam.name() not in self.DEFAULT_CAMERAS]
        for c in self.user_cameras:
            for attr in self.check_camera_attr:
                check = pm.getAttr('{name}.{attr}'.format(name=c, attr=attr))
                if check != 1:
                    flag = False
        if flag:
            return True
        else:
#            self.error_message = u'Fit Resolution Gate error...'
            return False

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        if self.user_cameras:
            for cam in self.user_cameras:
                for attr in self.check_camera_attr:
                    is_lock = getattr(cam, attr).isLocked()
                    getattr(cam, attr).unlock() if is_lock else None
                    pm.setAttr('{name}.{attr}'.format(name=cam, attr=attr), 1)
                    getattr(cam, attr).lock() if is_lock else None


def get_qc():
    return CheckCameraFilmFit()
