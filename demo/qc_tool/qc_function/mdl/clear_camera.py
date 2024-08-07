# -*- coding: utf-8 -*-

import os

current_dir = os.path.abspath('.')
parent_dir = os.path.dirname(current_dir)

class ClearCamera():
    name = 'Clear Camera'

    def __init__(self):
        super().__init__()
        
    def get_all(self, *args, **kwargs):
        import pymel.core as pm
        default_cameras = ['frontShape', 'perspShape', 'sideShape', 'topShape']
        return [cam for cam in pm.ls(cameras=1) if cam.name() not in default_cameras]
        
    def run(self):
        self.extra_data = self.get_all()
        print(self.extra_data)
        self.error_message = ''
        if self.extra_data:
            # self.error_message += u'{}<br/>'.format(cam.name())
            print(self.extra_data)
            # return False
        else:
            self.error_message = ''
            # return True
        return self.error_message
        
    def repair(self, *args, **kwargs):
        import pymel.core as pm
        import app._maya.util as util
        if not self.extra_data:
            print('There are no extra cameras available')
        else:
            for cam in self.extra_data:
                camera_transform = pm.PyNode(cam).getParent()
                pm.delete(camera_transform)
            print('Remove excess cameras')


def get_qc():
    return ClearCamera()
    

    
