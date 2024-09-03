#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'


from app_DAYU.qc_base import MQCBase


class ClearUnknownError(MQCBase):
    name = 'Search unknown error'
    usage = u'检查未知错误 '

    def __init__(self, parent=None):
        super(ClearUnknownError, self).__init__(parent)

    def validate(self, options):
        # if options.get('type_group') in ['element'] and options.get('type') in ['acfx']:
        #     return True
        # else:
        return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        for nd in pm.ls(type='unknown'):
            if nd.isLocked():
                nd.unlock()
            pm.delete(nd)

        plugs = pm.unknownPlugin(q=True, list=True)
        if plugs:
            for plug in plugs:
                pm.unknownPlugin(plug, remove=True)
        return True

    def repair(self, *args, **kwargs):
        pass


def get_qc():
    return ClearUnknownError()
