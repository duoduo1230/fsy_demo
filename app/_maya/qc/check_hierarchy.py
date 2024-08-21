#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'

from app.qc_base import MQCBase
import traceback


class CheckNullRefer(MQCBase):
    name = 'Check current hierarchy'
    usage = u'检查 rig hierarchy'

    def __init__(self, parent=None):
        super(CheckNullRefer, self).__init__(parent)
        self.extra_data = []
        self.null_ref = []
        self.error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mm', 'ani', 'lay']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        from app._maya.api.node_op import outliner_a0001 as outa
        from app._maya import util as mutil

        hierarchy_list = outa.get_asset_hierarchy()[:-1]
        refs = pm.ls(type='reference')

        for ref in refs:
            attr = getattr(ref, 'dayu_secret', None)
            if attr:
                version_id = eval(attr.get()).get('id')
                version_orm = mutil.get_orm_from_id(version_id)
                if version_orm.type.name == 'rig':
                    if not ref.referenceFile():
                        continue
                    nd = mutil.get_transform(ref)
                else:
                    continue
                if nd:
                    ns = nd.namespace()
                else:
                    self.null_ref.append(ref)
                    continue
            else:
                continue
            nd_error = True
            for hie in hierarchy_list:
                hie_path = '{}|{}|{}'.format(nd.fullPath(), ns + ':GEO', ns + ':' + hie)
                if not pm.objExists(hie_path):
                    continue
                hierarchy_node = pm.PyNode(hie_path)
                if hierarchy_node and hierarchy_node.getChildren():
                    nd_error = False
                    break

            if nd_error:
                self.extra_data.append(nd)

        if self.extra_data:
            self.error_message = u'当前选中得资产下得层级模型存在问题（GEO/下得HIG|MID|LOW|XLOW），' \
                                 u'请检查是否都为空或者下面任何模型都不显示'
            return False
        elif self.null_ref:
            self.error_message = u'当前场景中有空的reference，请将其移除掉或者勾选上加入场景中'
            return False
        else:
            return True

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        if self.extra_data:
            pm.select(self.extra_data)
            self.error_message = u'当前选中得资产下得层级模型存在问题（GEO/下得HIG|MID|LOW|XLOW），请检查是否都为空或者下面任何模型都不显示'
        if self.null_ref:
            pm.mel.eval('ReferenceEditor;')


def get_qc():
    return CheckNullRefer()
