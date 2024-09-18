#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from _app.qc_base import MQCBase
import maya.cmds as cmds

try:
    import pymel.core as pm
except:
    pass

SHAPE_LIST = ['|persp|perspShape', '|side|sideShape', '|top|topShape', '|front|frontShape']


class CheckAssetName(MQCBase):
    name = 'Check mdl name'
    usage = u'检查shape节点的命名规范'
    error_message = ''

    def __init__(self, parent=None):
        super(CheckAssetName, self).__init__(parent)
        self.extra_data = []
        self.error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        self.error_message = ''

        name_false = self.check_objects_name()
        if name_false:
            self.error_message += u'shape节点命名不规范: {} <br/>'.format(", ".join(name_false))
            for node in name_false:
                self.extra_data.append(node)

        if not self.extra_data:
            self.error_message = ''
            return True
        else:
            return False

    def check_objects_name(self):
        objects_name = []
        shape_list = cmds.ls(shapes=True)

        shape_list = list(set(shape_list) - set(SHAPE_LIST))

        for shape_node in shape_list:

            shape_node = str(shape_node)
            trans = cmds.listRelatives(shape_node, parent=True)[0]
            trans = str(trans)

            new_shape = shape_node.replace("Shape", "")

            if new_shape != trans:
                objects_name.append(trans)

        return objects_name

    def repair(self, *args, **kwargs):
        import _app._maya.util as util
        if not self.extra_data:
            util.message(u'没有可修复的数据', dialog=True)
        else:
            for node in self.extra_data:
                trans_node = cmds.ls(node, long=True)[0]
                shape_node = cmds.listRelatives(trans_node, children=True, fullPath=True)[0]
                if not shape_node:
                    continue

                trans_node_str = str(trans_node)
                shape_node_str = str(shape_node)
                virtual_shape_name = trans_node_str + "|" + trans_node_str.split("|")[-1] + "Shape"
                if shape_node_str != virtual_shape_name:
                    old_shape = shape_node_str.split('|')[-1]
                    new_name = virtual_shape_name.split('|')[-1]
                    cmds.select(shape_node_str)
                    cmds.rename(old_shape, new_name)


def get_qc():
    return CheckAssetName()
