#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wenfeng'
import pymel.core as pm
from app_DAYU.qc_base import MQCBase


class NoMaterial(MQCBase):
    name = 'Is assign material'
    usage = u'检查 模型是否有材质或shading Groups'

    def __init__(self, parent=None):
        super(NoMaterial, self).__init__(parent)
        self.self_different = []
        self.error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl']:
            return True
        else:
            return False


    def run(self, *args, **kwargs):
        mesh_list = []
        objects_Selected = pm.ls('|ASSET|GEO', dag=True, type='mesh') if pm.objExists('|ASSET|GEO') else []
        for mesh in objects_Selected:
            shadingEngine_List = pm.listConnections(mesh, type='shadingEngine')
            if not pm.ls(pm.listConnections(shadingEngine_List), materials=True):
                mesh_list.append(mesh)
        if mesh_list:
            self.error_message = 'There are meshes in the current scene without any materials..'
            self.self_different = mesh_list
            return False
        else:
            return True


    def repair(self, *args, **kwargs):
        import pymel.core as pm
        if self.self_different:
            try:
                pm.select(self.self_different)
            except:
                pass


def get_qc():
    return NoMaterial()

