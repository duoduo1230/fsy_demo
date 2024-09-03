#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/25 17:58
# @Author  : pengyuxuan
# @File    : hig_level.py

from app_DAYU.qc_base import MQCBase


class CheckHIGLevel(MQCBase):
    name = ' Is HIG level have mesh '
    usage = u'HIG层级下是否有mesh'

    def __init__(self, parent=None):
        super(CheckHIGLevel, self).__init__(parent)

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl', 'srf']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import maya.cmds as cmds
        import pymel.core as pm
        path = '|ASSET|GEO|HIG'
        if not pm.ls(path):
            self.error_message = u'场景中没有大纲结构'
            return False
        hig_children = cmds.listRelatives(path, ad=1, f=1)
        if hig_children:
            for i in hig_children:
                if cmds.listRelatives(i, s=1):
                    return True
        else:
            return False

    def repair(self, *args, **kwargs):
        pass


def get_qc():
    return CheckHIGLevel()
