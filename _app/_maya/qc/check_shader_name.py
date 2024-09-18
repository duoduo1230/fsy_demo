#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'


from _app.qc_base import MQCBase


class CheckShaderName(MQCBase):
    name = 'check shader name is legal'
    usage = u'检验shader名字是否合法'
    error_message = ''

    def __init__(self):
        super(CheckShaderName, self).__init__()
        self.not_legal_list = []

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['srf']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        """
        缘由: 因为shader名字中带有 : 会使代码无法对其进行正确重新命名时
        方案: 检查srf环节的shader名字中是否有 : 非法字符, 重新命名shader
        """
        import pymel.core as pm
        self.not_legal_list = []
        mesh_list = pm.ls('|ASSET', dag=True, type='mesh')
        for mesh in mesh_list:
            if not mesh.shadingGroups():
                continue
            sg = mesh.shadingGroups()[0]
            shader = pm.connectionInfo(sg.surfaceShader, sfd=True).split('.')[0]
            if ':' in shader:
                self.not_legal_list.append(shader)
        return True if not self.not_legal_list else False

    def repair(self, *args, **kwargs):
        """
        因为存在多个mesh共用一个shader的情况，所以需要set()一下shader list
        """
        import pymel.core as pm
        for shader_str in list(set(self.not_legal_list)):
            shader_node = pm.PyNode(shader_str)
            behind = shader_str.split(':')[-1]
            shader_node.setName(behind)


def get_qc():
    return CheckShaderName()

