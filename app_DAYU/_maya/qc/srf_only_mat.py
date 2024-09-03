#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'yangzhuo'

from app_DAYU.qc_base import MQCBase
import ui_center.widgets.MAppContext as MAppContext


class CheckSurface(MQCBase):
    name = 'Mesh only shade'
    usage = u'检查Mesh是否只有一个shade'
    error_message = ''
    result = []

    def validate(self, options):
        # TODO 和平精英项目不过这个QC
        project = str(MAppContext.MAppContext().entity_orm.find_meaning('PROJECT').name)
        if options.get('type_group') in ['element'] and options.get('type') in ['srf'] and project not in ['hpjy', 'md']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        mesh_list = [x for x in pm.ls('|ASSET', dag=True, type='mesh') if len(x.shadingGroups()) != 1]
        if mesh_list:
            self.error_message = 'current scene mesh has more than one shade..'
            self.result = mesh_list
            return False
        else:
            return True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        pm.select(self.result)


def get_qc():
    return CheckSurface()
