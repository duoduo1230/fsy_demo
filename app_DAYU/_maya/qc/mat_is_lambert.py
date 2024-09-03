#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'YangZhuo'

from app_DAYU.qc_base import MQCBase


class CheckAssetMat(MQCBase):
    name = 'Check mesh mat is lambert'
    usage = u'检查mesh是否连接了lambert材质节点 和 材质节点是否连接了initialShadingGroup, initialShadingGroup'
    error_message = ''

    def __init__(self):
        self.error_list = []

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['srf']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        self.error_list = []
        self.error_message = ''
        import pymel.core as pm

        mesh_list = pm.ls('|ASSET|GEO', dag=True, type='mesh')

        for mesh in mesh_list:
            sgs = mesh.shadingGroups()
            for sg in sgs:

                if sg.nodeType() in ['initialParticleSE', 'initialShadingGroup']:
                    self.error_list.append(mesh)
                    self.error_message += u'{}连接了不可修改的 initialParticleSE, initialShadingGroup.<br>'.format(mesh.name())
                    break

                else:
                    material_name = pm.connectionInfo(sg.surfaceShader.name(), sfd=True).split('.')[0]
                    if material_name in [u'lambert1']:
                        self.error_list.append(mesh)
                        self.error_message += u'{}连接了不可修改的 initialParticleSE, initialShadingGroup.<br>'.format(mesh.name())
                        break

        # 查找SG完成 查找材质完成 mesh 还有没有其他操作导致 不对
        return False if self.error_list else True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        if self.error_list:
            pm.select(self.error_list)


def get_qc():
    return CheckAssetMat()


if __name__ == '__main__':
    qc = get_qc()
    qc.repair()