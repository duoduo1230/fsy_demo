#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from _app.qc_base import MQCBase
import maya.cmds as cmds

try:
    import pymel.core as pm
except:
    pass


class CheckAssetAttr(MQCBase):
    name = 'Check mdl attr'
    usage = u'检查transform节点属性是否K帧.'
    error_message = ''

    def __init__(self, parent=None):
        super(CheckAssetAttr, self).__init__(parent)
        self.extra_data = []
        self.error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        self.error_message = ''
        self.extra_data = []
        k_frame = self.check_objects_keyframes()
        print(k_frame)

        if k_frame:
            self.error_message += u'此处未写修复项，需手动修改 <br/>'
            self.error_message += u'K帧: {} <br/>'.format(", ".join(k_frame))
            self.extra_data.extend(k_frame)

        if not self.extra_data:
            self.error_message = ''
            return True
        else:
            return False

    def check_objects_keyframes(self):
        objects_keyframes = []
        transform_list = cmds.ls(type="transform")

        for obj in transform_list:
            if cmds.keyframe(obj, query=True, keyframeCount=True):
                objects_keyframes.append(obj)

        return objects_keyframes

    def select_callback(self, parent_widget=None):
        if self.extra_data:
            import pymel.core as pm
            pm.select(self.extra_data)


def get_qc():
    return CheckAssetAttr()
