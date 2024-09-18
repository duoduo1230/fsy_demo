#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'YangZhuo'
from _app.qc_base import MQCBase


class CheckCamera(MQCBase):
    name = 'Validate Mesh'
    usage = u'检查模型是否只有一个mesh'
    error_message = ''
    result = []

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        layers = ['|ASSET|GEO|HIG', '|ASSET|GEO|LOW', '|ASSET|GEO|MID', '|ASSET|GEO|XLOW']
        mesh_list = []
        for l in layers:
            mesh_list += [x for x in pm.ls(l, dag=True, type='mesh') if x.intermediateObject.get()]

        if mesh_list:
            self.result = mesh_list
            self.error_message = 'current scene have more than one mesh.. \n {}'.format(str(self.result))
            return False
        else:
            return True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        [pm.delete(i) for i in self.result]


def get_qc():
    return CheckCamera()
