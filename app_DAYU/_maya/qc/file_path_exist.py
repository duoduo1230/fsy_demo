#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 17:58
# @Author  : pengyuxuan
# @File    : file_path_exist.py

from app_DAYU.qc_base import MQCBase


class FilePathExist(MQCBase):
    name = ' File texture is exist '
    usage = u'贴图是否存在'

    def __init__(self, parent=None):
        super(FilePathExist, self).__init__(parent)
        self.error_nodes = []

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['srf', 'mdl', 'acfx']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        from app_DAYU._maya.const import DAYU_TEXTURE_TYPE
        from app_DAYU._maya.tools import texture_util as texture

        self.error_message = ''
        self.error_nodes = []

        select_list = []
        for node_type in DAYU_TEXTURE_TYPE.keys():
            select_list.extend(pm.ls(type=node_type))

        for i in select_list:
            attr_dict = DAYU_TEXTURE_TYPE[pm.objectType(i)]
            path = i.getAttr(attr_dict.get('texture_path'))
            if not path:
                self.error_message = 'node {} not set texture path.<br> '.format(i)
                self.error_nodes.append(i)
                continue
            if not texture.check_texture_exist(path):
                self.error_message = 'node {} not find any texture.<br> '.format(i)
                self.error_nodes.append(i)
                continue
            if (pm.objectType(i) == 'file' and i.uvTilingMode.get() == 3) or pm.objectType(i) == 'aiImage':
                file_list = texture.get_filelist_from_udim(path)
                if file_list:
                    continue
                else:
                    self.error_message = 'node {} not find any texture.<br> '.format(i)
                    self.error_nodes.append(i)

        if self.error_nodes:
            return False
        return True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        pm.select(self.error_nodes)


def get_qc():
    return FilePathExist()
