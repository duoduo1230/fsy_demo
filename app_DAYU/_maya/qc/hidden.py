#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'


from app_DAYU.qc_base import MQCBase



class CheckHidden(MQCBase):
    name = 'Check Hidden'
    usage = u'检查隐藏模型'

    def __init__(self, parent=None):
        super(CheckHidden, self).__init__(parent)
        self.transform_hidden = []
        self.shape_hidden = []

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl','srf']:
            return True
        else:
            return False

    def get_all(self):
        import pymel.core as pm
        base_paths = []
        [base_paths.append(pm.PyNode('|ASSET|GEO'+level)) for level in ['|HIG','|MID','|LOW','|XLOW'] if pm.objExists('|ASSET|GEO'+level)]

        for transform in pm.ls(base_paths, type='transform', dag=True, l=True):
            if transform not in base_paths:
                yield transform

    def run(self, *args, **kwargs):
        import pymel.core as pm
        self.error_message = ''
        self.transform_hidden = []
        self.shape_hidden = []

        result = True

        for transform_node in self.get_all():

            shape_node = next(iter(pm.listRelatives(transform_node, shapes=1)), None)

            if pm.getAttr(transform_node.visibility) == 0:
                self.transform_hidden.append(transform_node.fullPath())

            if shape_node and pm.getAttr(shape_node.visibility) == 0:
                self.shape_hidden.append(shape_node.fullPath())

        if self.transform_hidden or self.shape_hidden:
            self.error_message += u'隐藏的transform:<br/>'
            self.error_message += '<br/>'.join(self.transform_hidden)

            self.error_message += u'隐藏的shape:<br/>'
            self.error_message += '<br/>'.join(self.shape_hidden)

            result = False

        return result



    def repair(self, *args, **kwargs):
        import pymel.core as pm
        import app_DAYU._maya.util as util
        if not self.transform_hidden and not self.shape_hidden:
            util.message(u'没有可修复的数据', dialog=True)
        else:
            for hidden_node in (self.transform_hidden + self.shape_hidden):
                pm.setAttr(pm.PyNode(hidden_node).visibility, 1)


def get_qc():
    return CheckHidden()





