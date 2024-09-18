#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'

from _app.qc_base import MQCBase


class CheckNameSpace(MQCBase):
    name = 'Validate Namespace'
    usage = u'清除命名空间'

    def __init__(self, parent=None):
        super(CheckNameSpace, self).__init__(parent)

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl', 'srf', 'rig','cfx']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        namespaces = pm.namespaceInfo(listOnlyNamespaces=True, recurse=True)
        namespaces.remove("UI")
        namespaces.remove("shared")
        namespaces.sort(reverse=True)

        for name_space in namespaces:
            try:
                pm.namespace(moveNamespace=[name_space, ":"], force=True)
                pm.namespace(removeNamespace=name_space)
            except:
                pass

        return True

    def repair(self, *args, **kwargs):
        pass

def get_qc():
    return CheckNameSpace()
