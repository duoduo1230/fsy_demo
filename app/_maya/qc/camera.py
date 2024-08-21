# -*- coding: utf-8 -*-
__author__ = 'chenghh'
from app.qc_base import MQCBase
import ui_center.widgets.MAppContext as MAppContext


class CheckCamera(MQCBase):
    name = 'Validate Camera'
    usage = u'校验相机是否存在, 相机缩放值是否为1'
    DEFAULT_CAMERAS = ('frontShape', 'perspShape', 'sideShape', 'topShape')
    special_level = '|SCENE|CAMERAS|'
    check_camera_attr = ('scaleX', 'scaleY', 'scaleZ')
    error_message = ''

    def __init__(self):
        super(CheckCamera, self).__init__()
        self.scale_value_not_1 = None

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['cam']:
            return True
        else:
            return False

    def check_scale_legal(self, camera_list):
        import pymel.core as pm
        for c in camera_list:
            for attr in self.check_camera_attr:
                scale = pm.getAttr('{name}.{attr}'.format(name=c.getTransform().name(),
                                                          attr=attr))
                if round(scale, 2) != 1.0:
                    yield c.getTransform()

    def run(self, *args, **kwargs):
        import pymel.core as pm
        self.error_message = ''
        camera_list = pm.ls(type='camera')
        # mp的环节情况特殊是Asset层级，需要区别对待不按Shot层级来判断
        current_step = str(MAppContext.MAppContext().current_step)
        if current_step == 'mp':
            user_cameras = [cam for cam in camera_list if cam.name() not in self.DEFAULT_CAMERAS]
        else:
            user_cameras = [cam for cam in camera_list
                            if cam.name() not in self.DEFAULT_CAMERAS
                            and self.special_level in cam.fullPath()]
        self.scale_value_not_1 = set(self.check_scale_legal(user_cameras))

        if self.scale_value_not_1:
            self.error_message = 'camera scale value is not 1, you can click repair button to set scale value to 1'
            return False
        elif not user_cameras:
            self.error_message = 'camera is null'
            return False
        else:
            return True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        if self.scale_value_not_1:
            for cam in self.scale_value_not_1:
                for attr in self.check_camera_attr:
                    is_lock = getattr(cam, attr).isLocked()
                    getattr(cam, attr).unlock() if is_lock else None
                    pm.setAttr('{name}.{attr}'.format(name=cam.name(), attr=attr), 1)
                    getattr(cam, attr).lock() if is_lock else None


def get_qc():
    return CheckCamera()
