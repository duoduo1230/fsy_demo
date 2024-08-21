#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'Wenfeng Zhang'


from app.qc_base import MQCBase
from db.disk_path import DiskPath


class CheckPathSpace(MQCBase):
    name = 'Check the path for spaces.'
    usage = u'检查贴图路径中是否存在空格，使其符合云渲染路径格式'

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['srf', 'mdl', 'acfx']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        self.error_nodes = []
        self.error_message = ''

        image_node_list = pm.ls(typ=['file', 'aiImage'])
        if not image_node_list:
            return True
        for image_node in image_node_list:
            attr_name = 'filename' if image_node.type() == 'aiImage' else 'fileTextureName'
            if image_node.getAttr(attr_name) and ' ' in image_node.getAttr(attr_name):
                self.error_nodes.append(image_node)

        if self.error_nodes:
            msg = u'以下贴图节点的路径中存在空格，需要手动修改， 点击repair帮你选中节点<br/>'
            self.error_message = msg + '<br/>'.join([x.name() for x in set(self.error_nodes)])
            return False
        return True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        pm.select(self.error_nodes)


def get_qc():
    return CheckPathSpace()

