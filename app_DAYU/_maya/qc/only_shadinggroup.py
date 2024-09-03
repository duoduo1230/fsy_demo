#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wqj'
import pymel.core as pm
from app_DAYU.qc_base import MQCBase


class ShaderMatchShadingGroup(MQCBase):
    name = 'Shader Only ShadingGroup'
    usage = u'材质是否对应单个ShadingGroup'

    def __init__(self, parent=None):
        super(ShaderMatchShadingGroup, self).__init__(parent)
        pass


    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['srf']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        self.error_shaders = []
        self.error_message = ''
        asset_group = pm.PyNode('|ASSET|GEO|HIG')
        meshs = pm.ls(asset_group, dag=True, type='mesh')
        for mesh in meshs:
            if not mesh.shadingGroups():
                self.error_shaders.append(mesh)
                self.error_message += u'{} 模型没有 shandingGroup 存在。<br>'.format(mesh.name())
                continue
            sg = mesh.shadingGroups()[0]
            shader = pm.connectionInfo(sg.attr('surfaceShader'), sfd=True).split('.')[0]
            if not shader:
                continue
            shader = pm.PyNode(shader)
            connect_nodes = [pm.PyNode(connect.split('.')[0]) for connect in
                             pm.connectionInfo(shader.outColor, dfs=True)]
            [connect_nodes.remove(nd) for nd in connect_nodes if nd.type() != 'shadingEngine']
            if len(connect_nodes) != 1:
                self.error_shaders.append(shader)
                self.error_message += u'{} 材质发现有多个 shandingGroup 存在。\n'.format(shader.name())
            continue
        if self.error_shaders:

            return False
        else:
            return True

    def repair(self, *args, **kwargs):
        pm.select(self.error_shaders)


def get_qc():
    return ShaderMatchShadingGroup()
