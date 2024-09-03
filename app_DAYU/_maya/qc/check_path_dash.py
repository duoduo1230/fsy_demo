#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'Wenfeng Zhang'


from app_DAYU.qc_base import MQCBase
from db.disk_path import DiskPath


class CheckPathDash(MQCBase):
    name = 'Check the dash in the path'
    usage = u'检查file路径中的序列化字符，"_1001","_UDIM"这种序列化字符前的下横杠不符合规范'

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['srf', 'mdl', 'acfx']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import re
        import pymel.core as pm
        self.error_nodes = []
        self.error_message = ''

        image_node_list = pm.ls(typ=['file', 'aiImage'])
        if not image_node_list:
            return True
        for image_node in image_node_list:
            attr_name = 'filename' if image_node.type() == 'aiImage' else 'fileTextureName'
            file_name = image_node.getAttr(attr_name)
            if not file_name or (image_node.type() == 'file' and image_node.getAttr('uvTilingMode') != 3):
                continue
            pattern_regex = re.compile(r'(.*?)(_\d+\.|_<UDIM>)(.*)', re.IGNORECASE)
            filename = DiskPath(file_name)
            basename = filename.name
            if pattern_regex.search(basename):
                if all(pattern_regex.search(basename).groups()):
                    self.error_nodes.append(image_node)

        if self.error_nodes:
            msg = u'以下贴图节点的路径中序列化字符非法，存在"_1001","_UDIM"这种情况，需要手动改文件名重新指定， 点击repair帮你选中节点<br/>'
            self.error_message = msg + '<br/>'.join([x.name() for x in set(self.error_nodes)])
            return False
        return True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        pm.select(self.error_nodes)


def get_qc():
    return CheckPathDash()

