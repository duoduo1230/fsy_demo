#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Wenfeng Zhang'

from app_DAYU.qc_base import MQCBase
from dayu_path import DayuPath as DiskPath
from app_DAYU.utils import is_ascii


class checkAscii(MQCBase):
    name = 'Check Image Name'
    usage = u'检查 是否存在非法的文件路径名'

    def __init__(self, parent=None):
        super(checkAscii, self).__init__(parent)
        self.self_different = []
        self.error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['srf']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        from app_DAYU.utils import name_format
        self.error_nodes = []
        self.error_message = ''

        image_node_list = pm.ls(typ=['file', 'aiImage'])
        if not image_node_list:
            return True
        for image_node in image_node_list:
            attr_name = 'filename' if image_node.type() == 'aiImage' else 'fileTextureName'
            file_name = DiskPath(image_node.getAttr(attr_name))
            if not is_ascii(file_name) or name_format(file_name).absname.isdigit():
                self.error_nodes.append(image_node)

        if self.error_nodes:
            msg = u'以下贴图节点的路径中包含非法字符，可能的情况： 文件名字完全是数字组成, 有中文或其它全角符号<br/><br/>'
            self.error_message = msg + '<br/>'.join([x.name() for x in set(self.error_nodes)])
            return False
        return True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        pm.select(self.error_nodes)


def get_qc():
    return checkAscii()

