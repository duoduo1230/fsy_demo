#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'Wenfeng Zhang'


from app_DAYU.qc_base import MQCBase
from db.disk_path import DiskPath


class CheckUdimCapitalized(MQCBase):
    name = 'Check that <UDIM> is capitalized.'
    usage = u'检查贴图路径中的<UDIM>是否是大写的，使其符合云渲染路径格式'

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['srf']:
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
            file_name = DiskPath(image_node.getAttr(attr_name))
            if '<udim>' in file_name.name:
                self.error_nodes.append(image_node)

        if self.error_nodes:
            msg = u'以下贴图节点的路径中<udim>为小写的， 点击repair批量改为大写<br/>'
            self.error_message = msg + '<br/>'.join([x.name() for x in set(self.error_nodes)])
            return False
        return True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        for node in set(self.error_nodes):
            attr_name = 'filename' if node.type() == 'aiImage' else 'fileTextureName'
            file_name = DiskPath(node.getAttr(attr_name))
            new_name = file_name.name.replace('<udim>', '<UDIM>')
            new_file_name = file_name.parent.child(new_name)
            node.setAttr(attr_name, new_file_name)
        self.error_message = ''

def get_qc():
    return CheckUdimCapitalized()

