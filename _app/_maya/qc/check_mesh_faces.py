#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'Wenfeng Zhang'


from _app.qc_base import MQCBase
from db.disk_path import DiskPath


class CheckMeshFaces(MQCBase):
    name = 'Check faces above four sides and Nonmanifold geometry'
    usage = u'检查几何体中是否存在有4个以上边的面或者多面共线的非流形体'

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        self.error_nodes = []
        self.error_message = ''

        nodes = pm.mel.eval(
            'polyCleanupArgList 4 { "1","2","1","0","1","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","2","0","0" }')
        if not nodes:
            pm.select(cl=True)
            return True
        pm.select(nodes)
        self.error_nodes = nodes
        msg = u'几何体中存在有4个以上边的面或者多面共线的非流形体 点击repair帮你选中<br/>'
        self.error_message = msg + '<br/>'.join([x for x in set(self.error_nodes)])
        return False

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        pm.select(self.error_nodes)


# def get_qc():
#     return CheckMeshFaces()

