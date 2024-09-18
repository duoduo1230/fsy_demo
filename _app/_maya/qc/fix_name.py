#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'
import pymel.core as pm
from _app.qc_base import MQCBase


class ClearPastedName(MQCBase):
    name = 'Clear pasted name'
    usage = u'检查文件节点名称'

    def __init__(self, parent=None):
        super(ClearPastedName, self).__init__(parent)
        self.self_different = []
        self.other_same = []
        self.error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl', 'srf']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        sels = pm.ls()
        statu = True
        for s in sels:
            if 'pasted__' in s.name() and not s.isReferenced():
                try:
                    s.rename(s.name().replace('pasted__', ''))
                except:
                    statu = False
                    self.error_message += '{} rename error\n'.format(s.name())
        return statu

    def repair(self, *args, **kwargs):
        pass

def get_qc():
    return ClearPastedName()
