# -*- coding: utf-8 -*-

import os

current_dir = os.path.abspath('../mdl')
parent_dir = os.path.dirname(current_dir)

class ClearCamera():

    def __init__(self):
        super().__init__()
        self.description = u'清除冗余相机'
        self.error_message = u''
        self.check_result = ''
        self.extra_data = []
        
    def get_all(self, *args, **kwargs):
        import pymel.core as pm
        default_cameras = ['frontShape', 'perspShape', 'sideShape', 'topShape']
        return [cam for cam in pm.ls(cameras=1) if cam.name() not in default_cameras]
        
    def run(self):
        self.extra_data = self.get_all()

        if self.extra_data:
            cam_list = []
            for cam in self.extra_data:
                cam_list.append(cam.name())

            self.error_message = u'存在冗余相机' + str(cam_list)
            self.check_result = 'FAILED'

        else:
            self.check_result = 'PASSED'

        return self.error_message, self.check_result

        
    def repair(self, *args, **kwargs):
        import pymel.core as pm
        if self.extra_data:
            for cam in self.extra_data:
                camera_transform = pm.PyNode(cam).getParent()
                pm.delete(camera_transform)
            self.error_message = u'相机删除'
            self.check_result = 'PASSED'

        return self.error_message, self.check_result


def get_qc():
    return ClearCamera()
    

    
