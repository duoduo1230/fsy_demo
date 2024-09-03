#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'


from app_DAYU.qc_base import MQCBase
from db.disk_path import DiskPath


class CheckTexture(MQCBase):
    name = 'check yeti texture'
    usage = u'检查yeti节点得texture路径是否存在'
    error_message = ''
    error_list = []

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['acfx']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        self.error_message = ''
        self.error_list = []
        import pymel.core as pm
        yeti_list = pm.ls(type='pgYetiMaya')
        for yeti_node in yeti_list:
            texture_path = yeti_node.imageSearchPath.get()
            if texture_path and not DiskPath(texture_path).exists():
                self.error_list.append(yeti_node)

        if self.error_list:
            msg = u'以下yeti节点的texture路径不存在， 点击repair帮你选中<br/>'
            self.error_message = msg + '<br/>'.join([x.name() for x in self.error_list])
            return False

        return True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        pm.select(self.error_list)


def get_qc():
    return CheckTexture()

