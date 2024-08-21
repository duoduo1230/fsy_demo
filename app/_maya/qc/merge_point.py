#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'

from app.qc_base import MQCBase


class CheckNormal(MQCBase):
    name = 'Clear unuse point'
    usage = u'检查 浮离点'

    def __init__(self, parent=None):
        super(CheckNormal, self).__init__(parent)
        self.extra_data = []
        self.error_message = ''

    def validate(self, options):
        # if options.get('type_group') in ['element'] and options.get('type') in ['mdl']:
        #
        #     return True
        # else:
        return False

    def run(self, *args, **kwargs):

        import pymel.core as pm
        if pm.objExists('|ASSET'):
            pm.select('|ASSET')
            mesh_list = pm.ls('|ASSET', dag=True, type='mesh')
            for mesh in mesh_list:
                faces = pm.polyEvaluate(mesh, f=True)
                if not faces:
                    self.extra_data.append(mesh)
                    continue
                pm.select(mesh)
                pm.mel.eval('polyMergeVertex -d 0.0000001')
                pm.select(mesh)
                pm.mel.eval('DeleteHistory')
        self.error_message = ','.join(self.extra_data) + u'   的点有问题，请手动修复选中他们'
        return True

    def repair(self, *args, **kwargs):
        import pymel.coe as pm
        pm.select(self.extra_data)

def get_qc():
    return CheckNormal()
