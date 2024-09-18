#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import importlib

api_dict = {'read': 'a0001'}


def create_api_version(op_name, use_func=True):
    if not use_func:
        return api_dict.get(op_name, 'a0001')

    # 动态加载node_op 的对应模块
    module_obj = importlib.import_module('app._hiero.api.node_op.{node}_{api}'.format(node=op_name,
                                                                                      api=api_dict.get(op_name,
                                                                                                       'a0001')))
    # 返回实际的处理create 函数
    return getattr(module_obj, 'create')
