#!/usr/bin/env python
#-*- coding: utf-8 -*-
#@Time    : 11/28/2018 6:57 PM

__author__ = 'pengyuxuan'
from _app.qc_base import MQCBase
from _app._maya.const import DAYU_SET_GROUP


class HasDayuGroup(MQCBase):
    name = ' Is mesh has dayuGroup attr '
    usage = u'mesh 有没有dayugroup的属性'

    def __init__(self, parent=None):
        super(HasDayuGroup, self).__init__(parent)
        self.error_nodes = []

    def validate(self, options):
        return False
        # todo 这条QC 暂时关掉 因为目前 做houdini材质的时候 不需要 去pub maya的 element
        # if options.get('type_group') in ['element'] and options.get('type') in ["srf"]:
        #     return True
        # else:
        #     return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        self.error_nodes = []

        all_meshs = pm.ls('ASSET|GEO|HIG', type='mesh', dag=1)
        for mesh in all_meshs:
            has = pm.hasAttr(mesh, DAYU_SET_GROUP)
            if not has:
                self.error_nodes.append(mesh)
        if self.error_nodes:
            self.error_message = '{} do not have attr {}'.format(str(self.error_nodes), DAYU_SET_GROUP)
            return False
        return True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        pm.select(self.error_nodes)


def get_qc():
    return HasDayuGroup()
