#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'

from app.qc_base import MQCBase


class ClearUnknown(MQCBase):
    name = 'Clear Unknown Node'
    usage = u'检查 未知节点'

    def __init__(self, parent=None):
        super(ClearUnknown, self).__init__(parent)
        self.extra_data = []
        self.error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['workfile','element'] and options.get('type') in ['mdl', 'srf', 'rig']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        self.error_message = ''
        self.extra_data = pm.ls(type=('unknown', 'unknownDag', 'unknownTransform'))
        if self.extra_data:
            self.error_message = u'未知节点：<br/>'
            for unknown_node in self.extra_data:
                self.error_message += '{}<br/>'.format(unknown_node.name())
            return False
        else:
            return True

    def repair(self, *args, **kwargs):
        import app._maya.util as util
        import pymel.core as pm
        if not self.extra_data:
            util.message(u'没有可修复的数据', dialog=True)
        else:
            for node in self.extra_data:
                node = pm.PyNode(node)
                if node.isLocked():
                    node.unlock()
                pm.delete(node)


def get_qc():
    return ClearUnknown()
