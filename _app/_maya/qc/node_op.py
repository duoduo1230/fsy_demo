#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/3 13:49
# @Author  : pengyuxuan
# @File    : node_op.py

from _app.qc_base import MQCBase


class NodeOpExist(MQCBase):
    name = 'node op is exist'
    usage = u'OP节点是否存在'

    def __init__(self, parent=None):
        super(NodeOpExist, self).__init__(parent)
        self.node_list = []

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['srf']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        self.node_list = []
        import pymel.core as pm
        import _app._maya.util as util
        self.error_message = ''

        current_orm = util.current_workfile_orm()
        asset_name = current_orm.find_meaning('asset').name.replace('-', '_')

        match_list = [asset_name + '_material_export',
                      asset_name + '_material_set',
                      asset_name + '_user_set']

        self.node_list.extend(pm.ls(match_list, type=['aiCollection', 'aiMerge', 'aiMaterialx', 'aiSetParameter',
                                                      'aiSetParameter', 'aiSwitchOperator', 'aiDisable',
                                                      'aiSetTransform']))

        if self.node_list:
            self.error_message = str(self.node_list) + u'存在node op,请删除'
            return False
        else:

            return True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        pm.delete(self.node_list)
        self.error_message = ''


def get_qc():
    return NodeOpExist()
