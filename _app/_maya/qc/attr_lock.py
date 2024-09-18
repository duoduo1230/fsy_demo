#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'

from _app.qc_base import MQCBase


class AttrLock(MQCBase):
    name = 'Validate Attr Lock'
    usage = u'属性是否锁定'

    def __init__(self, parent=None):
        super(AttrLock, self).__init__(parent)

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl','srf']:
            return True
        else:
            return False

    def get_all(self):
        import pymel.core as pm
        base_paths = ['|ASSET|GEO|HIG', '|ASSET|GEO|MID','|ASSET|GEO|LOW', '|ASSET|GEO|XLOW']
        for base_path in pm.ls(base_paths, type='transform', dag=1, l=1):
            if base_path.fullPath() not in base_paths:
                yield base_path

    def run(self, *args, **kwargs):
        self.error_message = ''

        self.error_edges_face = {}
        self.error_vertexs = {}
        self.extra_data = {}
        self.extra_data['freeze'] = []
        self.extra_data['lock'] = []

        result = True

        for tranform in self.get_all():
            lock_attrs = tranform.listAttr(l=1)
            if lock_attrs:
                self.error_message += u'被锁属性为<br/>{}<br/>'.format(lock_attrs)

                self.extra_data['lock'] += lock_attrs
                result = False

        if result:
            self.error_message = ''
        return result

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        import _app._maya.util as util
        if not self.extra_data:
            util.message(u'没有可修复的数据', dialog=True)
        else:
            [pm.setAttr(attr_name, lock=False) for attr_name in self.extra_data['lock']]


def get_qc():
    return AttrLock()
