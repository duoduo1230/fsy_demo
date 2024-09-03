#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'


from app_DAYU.qc_base import MQCBase


class ClearRefer(MQCBase):
    name = 'Clear reference'
    usage = u'检查 reference'

    def __init__(self, parent=None):
        super(ClearRefer, self).__init__(parent)
        self.extra_data = []
        self.error_message = ''


    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl', 'srf', 'rig']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        self.error_message = ''
        self.extra_data = pm.ls(rf=1)
        if self.extra_data:
            self.error_message = u'场景中的reference节点：<br/>'
            for ref_node in self.extra_data:
                self.error_message += u'{}<br/>'.format(ref_node)
            return False
        else:
            self.error_message = ''
            return True

    def repair(self, *args, **kwargs):
        import app_DAYU._maya.util as util

        if not self.extra_data:
            util.message(u'没有可修复的数据', dialog=True)
        else:
            for refer_node in self.extra_data:
                if refer_node.referenceFile() == None:
                    refer_node.unlock()
                    pm.delete(refer_node)
                    continue
                if not refer_node.parentReference():
                    import pymel.core as pm
                    pm.FileReference(refer_node).remove()


def get_qc():
    return ClearRefer()





