#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'

from _app.qc_base import MQCBase
import traceback


class CheckNullRefer(MQCBase):
    name = 'Check Null reference'
    usage = u'检查 空reference节点'

    def __init__(self, parent=None):
        super(CheckNullRefer, self).__init__(parent)
        self.extra_data = []
        self.error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mm', 'ani']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        self.extra_data = []
        self.error_message = ''
        ref_nodes = pm.ls(rf=1)
        result = True
        if ref_nodes:
            self.error_message = u'场景中的空reference节点：<br/>'

            for ref_node in ref_nodes:
                #  某些情况refNode 会出现 ref_node.isLoaded() 错误
                try:
                    ref_statu = ref_node.isLoaded()
                except:
                    ref_statu = False
                if not ref_statu:
                    self.extra_data.append(ref_node)
                    self.error_message += u'{}<br/>'.format(ref_node)

        if self.extra_data:
            self.error_message = ''

        return True if not self.extra_data else False

    def repair(self, *args, **kwargs):
        import _app._maya.util as util
        import pymel.core as pm
        if not self.extra_data:
            util.message(u'没有可修复的数据', dialog=True)
        else:
            for refer_node in self.extra_data:
                #  某些情况refNode 会出现 ref_node.parentReference() 错误
                try:
                    parent_ref = refer_node.parentReference()
                except:
                    traceback.print_exc()
                    parent_ref = True
                if not parent_ref:
                    import pymel.core as pm
                    pm.FileReference(refer_node).remove()
                if pm.objExists(refer_node):
                    refer_node.unlock()
                    pm.delete(refer_node)

def get_qc():
    return CheckNullRefer()
