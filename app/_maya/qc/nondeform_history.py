#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'

from app.qc_base import MQCBase


class ClearNondeformHistory(MQCBase):
    name = 'Clear Nondeform History'
    usage = u'检查 模型非形变历史'

    def __init__(self, parent=None):
        super(ClearNondeformHistory, self).__init__(parent)
        self.extra_data = []
        self.error_message = ''

    def validate(self, options):
        # todo 暂时关掉 后需要需要更新 40 行 处的 node list
        if options.get('type_group') in ['element'] and options.get('type') in ['riga']:
            return True
        else:
            return False

    def get_all(self):
        import pymel.core as pm
        base_paths = ['|ASSET', '|SCENE']
        for shape_node in pm.ls(base_paths, type='mesh', dag=1, noIntermediate=1):
            yield shape_node

    def run(self, *args, **kwargs):
        import pymel.core as pm
        self.error_message = ''
        self.error_node = []

        result = True
        for shape_node in self.get_all():
            deformers = [n for n in shape_node.listHistory(type='geometryFilter') if pm.nodeType(n) not in ['tweak']]

            history = [i for i in shape_node.inputs() if
                       pm.nodeType(i) not in ['objectSet', 'groupId', 'tweak', 'groupParts', 'shadingEngine'] and i not in deformers]
            if history:
                self.error_node.append(shape_node)
                for i in history:
                    print pm.objectType(i)
                result = False
        if self.error_node:
            self.error_message = u'有非形变历史节点的模型为：<br/>'
            for node in self.error_node:
                self.error_message += '{}<br/>'.format(node.fullPath())
        print result, self.error_node
        return result

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        if self.error_node:
            pm.bakePartialHistory(self.error_node, ppt=1)


def get_qc():
    return ClearNondeformHistory()
