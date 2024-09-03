#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'YangZhuo'

from collections import Iterable
from app_DAYU.qc_base import MQCBase
import pymel.core as pm


class CheckDoubleName(MQCBase):
    # 因为没有可以import config 的地方, 暂时把配置拷贝过来
    _config_root = ('|ASSET', '|SCENE')
    _config = ('HIG', 'LOW', 'CLOTH', 'XGEN', 'YETI', 'ZIVA', 'LIGHTS', 'CHR', 'ENV', 'PRP',
               'VEH', 'CUSTOM', 'MM', 'ANI', 'FX', 'LGT', 'CMP', 'BDS', 'MM', 'ANI', 'FX', 'LGT', 'CMP')
    _check_step = ('mdl', 'ani', 'lay', 'mm')

    name = 'Mesh Double Name'
    usage = u'检查大纲下是否有非法名字的mesh'
    error_list = None
    error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in self._check_step:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        # 判断 get 所有 mesh 节点获得名字, 得到 transform节点并且判断其父级是否和其名字一致并且判断名字是否在非法列表里
        _mesh = [pm.ls(x, dag=True, type='mesh') for x in self._config_root if pm.objExists(x)]
        mesh_list = [pm.listRelatives(x, parent=True)[0] for x in self.flatten(_mesh)]
        self.error_list = [i for i in mesh_list
                           if i.fullPath().split('|')[-1] == i.fullPath().split('|')[-2]
                           and i.fullPath().split('|')[-1] in self._config]
        return False if self.error_list else True

    def repair(self, *args, **kwargs):
        pm.select(self.error_list)

    @classmethod
    def flatten(cls, items, ignore_types=(str, bytes)):
        for x in items:
            if isinstance(x, Iterable) and not isinstance(x, ignore_types):
                for i in cls.flatten(x):
                    yield i
            else:
                yield x


def get_qc():
    return CheckDoubleName()
