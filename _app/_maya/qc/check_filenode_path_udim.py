#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'Wenfeng Zhang'


import re
from _app.qc_base import MQCBase
from db.disk_path import DiskPath


class CheckPathUdim(MQCBase):
    name = 'Check the UDIM in the file path.'
    usage = u'检查“file”节点“Image Name”属性里的路径在“UV Tiling Mode”为Off时是否存在“UDIM”这个字符'

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['srf']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        self.error_nodes = []
        self.error_message = ''

        image_node_list = pm.ls(typ=['file'])
        if not image_node_list:
            return True
        for image_node in image_node_list:
            attr_name = 'fileTextureName'
            image_name = image_node.getAttr(attr_name)
            if image_name and '<UDIM>' in image_name and image_node.getAttr('uvTilingMode') == 3:
                self.error_nodes.append(image_node)

        if self.error_nodes:
            msg = u'以下“file”节点的路径在“UV Tiling Mode”属性为Off时存在“UDIM”这个字符，需要是数字，点击repair修改<br/>'
            self.error_message = msg + '<br/>'.join([x.name() for x in set(self.error_nodes)])
            return False
        return True

    def repair(self, *args, **kwargs):
        for node in set(self.error_nodes):
            attr_name = 'fileTextureName'
            node.setAttr('uvTilingMode', 0)
            file_name = DiskPath(node.getAttr(attr_name))
            file_list = file_name.parent.scan(ext=file_name.ext)
            if not file_list:
                raise ValueError('There is no path in the file.')
            flag_ = False
            for file_ in file_list:
                filename = file_.filename
                if flag_:
                    continue
                if self.get_file_name_format(filename) and \
                        self.get_file_name_format(file_name) == self.get_file_name_format(filename):
                    frame_num = file_.frames[0]
                    new_name = file_name.name.replace('<UDIM>', str(frame_num))
                    new_file = file_name.parent.child(new_name)
                    node.setAttr(attr_name, new_file)
                    flag_ = True
            node.setAttr('uvTilingMode', 3)
        self.error_message = ''

    @staticmethod
    def get_file_name_format(filename):
        pattern_regex = re.compile(r'(.*?)(%\d*d|#+|<UDIM>|\$F\d*|\.*\d+\.|u.+_v.+?)(.*)', re.IGNORECASE)
        filename = DiskPath(filename)
        basename = filename.name
        if pattern_regex.search(basename):
            if all(pattern_regex.search(basename).groups()):
                name_list = pattern_regex.search(basename).groups()
                new_name = name_list[0].rstrip('.')
                return new_name
            else:
                return False
        return filename.stem


def get_qc():
    return CheckPathUdim()

