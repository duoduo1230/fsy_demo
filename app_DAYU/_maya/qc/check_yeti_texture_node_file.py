#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'Wenfeng Zhang'

import os
from app_DAYU.qc_base import MQCBase
from app_DAYU._maya.tools import yeti_util as yutil
import pymel.core as pm

class CheckTextureFile(MQCBase):
    '''
    检查yeti Graph Editor里的texture类节点路径，使其符合ali云端渲染格式，如果无法用 Repair It修复，请到yeti Graph Editor里查看texture
    类节点的File，是否存在有贴图名和有贴图完整路径两种格式，这种需要手动重新设置。例如 ：
            ‘joydog_fur_daliubody1.tif’
            ‘P:/xxxfur/joydog_fur_scatter_01.tif’
    '''
    name = 'check yeti Graph Editor texture'
    usage = u'检查yeti Graph Editor里的texture类节点路径，使其符合ali云端渲染格式.'
    error_message = ''
    error_list = []

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['acfx', 'scfx']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        self.error_message = ''
        self.error_list_isfile = []
        self.error_list_image_Search_Path = []
        texture_list = []

        nodes = pm.ls(typ='pgYetiMaya')
        if not nodes:
            return True
        for node in nodes:
            image_search_path = node.getAttr('imageSearchPath')
            texture = yutil.get_graph_node_from_yeti(node, 'texture')
            if not texture:
                texture_list.append(False)
                continue
            texture_list.append(True)
            for i in texture:
                yeti_node = i.name
                file = str(i.file_name.get())
                if file:
                    file = file.replace('\\', '/')
                    if os.path.isfile(file):
                        self.error_list_isfile.append(node.name()+'.'+yeti_node)
                    if not os.path.isfile(file) and not image_search_path:
                        self.error_list_image_Search_Path.append(node.name())

        #如果texture_list都为False，则any(texture_list)返回false，这就代表yeti Graph Editor里没有texture类节点，直接返回Ture
        if not any(texture_list):
            return True

        if self.error_list_isfile:
            msg = u'yeti Graph Editor里的texture类节点路径不是标准的路径格式,如果无法用 Repair It修复，' \
            u'请到yeti Graph Editor里查看texture类节点的File，是否存在‘xxxx.tif’和‘p:/xxx/xxx/xxxx.tif’两种路径格式，这种需要手动重新设置<br/>'
            self.error_message = msg + '<br/>'.join([x for x in self.error_list_isfile])
            return False
        if self.error_list_image_Search_Path:
            msg = u'yeti的Image Search Path路径不存在<br/>'
            self.error_message = msg + '<br/>'.join([x for x in self.error_list_image_Search_Path])
            return False
        return True

    def repair(self, *args, **kwargs):
        if self.error_list_isfile:
            yeti_nodes = list(set([str(node.split('.')[0]) for node in self.error_list_isfile]))
            yeti_attr_list = self.get_yeti_attr_value(yeti_nodes)
            self.set_yeti_attr_value(yeti_attr_list)
        if self.error_list_image_Search_Path:
            pm.select(self.error_list_image_Search_Path)

    def commonprefix(self, l):
        '''
        替代py2.7里的 os.path.commonprefix，2.7里的是以字符串来判断公共最大的，而不是路径
        :param l: 路径列表
        :return: 返回最大的公共路径
        '''
        cp = []
        ls = [p.split('/') for p in l]
        ml = min(len(p) for p in ls)
        for i in range(ml):
            s = set(p[i] for p in ls)
            if len(s) != 1:
                break
            cp.append(s.pop())
        return '/'.join(cp)

    def get_yeti_attr_value(self, yeti_nodes):
        '''
        返回yeti Graph Editor里的texture节点和file路径的列表，类似于：
                                        {'yeti_joy_bodyShape01':{'texture0'      :'xx1.tif', 节点名和文件名
                                                                 'texture1'      :'xx2.tif',
                                                                 '_commonprefix' :'P:/phenom/xxxx/fur' 固定_commonprefix所有的公共路径
                                                                }
                                        'yeti_joy_bodyShape02':{'texture_1'      :'yy1.tif',
                                                                'texture_2'      :'yy2.tif',
                                                                '_commonprefix'  :'P:/phenom/yyyy/fur'
                                                                }
                                        }
        :param yeti_nodes: yeti的节点列表
        :return: yeti的节点和路径字典
        '''
        nodes = yeti_nodes[:]
        attr_dict = dict()
        for node in nodes:
            node = pm.PyNode(node)
            texture = yutil.get_graph_node_from_yeti(node, 'texture')
            if not texture:
                continue
            attr_dict[node.name()] = {}
            for i in texture:
                yeti_node = i.name
                file = str(i.file_name.get())
                print file
                if file:
                    file = file.replace('\\', '/')
                    attr_dict[node.name()].update({yeti_node: file})
        print attr_dict
        attr_dict_ = dict()
        for yeti_name, yeti_node_dict in attr_dict.items():
            if len(yeti_node_dict.values()) == 1:
                file_c = os.path.dirname(yeti_node_dict.values()[0])
            else:
                file_c = self.commonprefix(yeti_node_dict.values())
            attr_dict_[str(yeti_name)] = {'_commonprefix': file_c}
            for yeti_tex_name, tex_file in yeti_node_dict.items():
                base_tex_file = tex_file.split(file_c)[-1].lstrip('/')
                attr_dict_[str(yeti_name)].update({str(yeti_tex_name): base_tex_file})
        return attr_dict_

    def set_yeti_attr_value(self, value_dict):
        '''
        根据yeti的节点和路径字典设置路径
        :param value_dict: yeti的节点和路径字典
        :return:
        '''
        if not value_dict:
            return
        for node, values in value_dict.items():
            for yeti_name, filename in values.items():
                if yeti_name != '_commonprefix':
                    texture = yutil.YetiNode(yeti_name, 'texture', pm.PyNode(node))
                    texture.file_name.set(filename)
            path = values['_commonprefix']
            pm.PyNode(node).setAttr('imageSearchPath', path.lower())

def get_qc():
    return CheckTextureFile()
