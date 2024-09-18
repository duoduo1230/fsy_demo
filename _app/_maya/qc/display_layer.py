#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'

from _app.qc_base import MQCBase


class ClearDisplayLayer(MQCBase):
    name = 'Clear DisplayLayer'
    usage = u'检查 显示层'

    def __init__(self, parent=None):
        super(ClearDisplayLayer, self).__init__(parent)
        self.extra_data = []
        self.error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['workfile'] and options.get('type') in ['mdl', 'srf']:  # remove rig
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        self.error_message = ''
        self.extra_data = [layer for layer in pm.ls(type='displayLayer') if layer.name() != 'defaultLayer']
        if self.extra_data:
            self.error_message = u'多余的显示图层：<br/>'
            for layer in self.extra_data:
                self.error_message += '{}<br/>'.format(layer.name())
        return False if self.extra_data else True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        import _app._maya.util as util
        if not self.extra_data:
            util.message(u'没有可修复的数据', dialog=True)
        else:
            for layer in self.extra_data:
                if layer.isLocked():
                    layer.unlock()
                pm.delete(layer)


def get_qc():
    return ClearDisplayLayer()
