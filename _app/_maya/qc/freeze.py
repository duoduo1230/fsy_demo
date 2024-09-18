#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'
import pymel.core as pm
from _app.qc_base import MQCBase


class Freeze(MQCBase):
    name = 'Validate Freeze'
    usage = u'是否冻结'

    def __init__(self, parent=None):
        super(Freeze, self).__init__(parent)

    def validate(self, options):
        if options.get('orm').top.name in ['pepsi2020']:
            return False
        self.step_type = options.get('type')
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl', 'rig', 'srf']:
            return True
        else:
            return False

    def get_all(self):
        base_paths = ['|ASSET|GEO|HIG', '|ASSET|GEO|MID', '|ASSET|GEO|LOW', '|ASSET|GEO|XLOW']
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
        self.error_message = u'以下模型没有冻结<br/>'
        connections = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY',
                       'scaleZ']
        self.step_type = 'rig'
        for tranform in self.get_all():
            # 用于排除 rig环节加的约束问题  如果加过约束则跳过 该transform检查
            # 如果模型的话 不被允许 如果是rig 允许该操作
            if self.step_type == 'mdl':
                for attr in connections:
                    pm.setAttr('{}.{}'.format(tranform, attr), lock=False)
                    pm.makeIdentity(tranform, apply=True, t=1, r=1, s=1)
                continue

            if self.step_type == 'rig':
                attribute_connect_statu = False
                for connect in connections:
                    if getattr(tranform, connect).connections():
                        attribute_connect_statu = True
                if attribute_connect_statu:
                    continue

            nonidentity = pm.xform(tranform, q=True, translation=True) \
                          + pm.xform(tranform, q=True, rotation=True) + \
                          pm.xform(tranform, q=True, scale=True)
            freeze_value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            1.0, 1.0, 1.0]
            nonidentity = [round(x, 7) for x in nonidentity]
            if nonidentity != freeze_value:
                self.error_message += '{}<br/>'.format(tranform.fullPath())
                self.extra_data['freeze'].append(tranform.fullPath())
                result = False

        if result:
            self.error_message = ''
        return result

    def repair(self, *args, **kwargs):
        import _app._maya.util as util
        if not self.extra_data['freeze']:
            util.message(u'没有可修复的数据', dialog=True)
        else:
            # self._freeze(self.extra_data['freeze'])
            try:
                for attr_name in self.extra_data['lock']:
                    pm.setAttr(attr_name, lock=False)
                [pm.makeIdentity(trans_node, apply=True) for trans_node in self.extra_data['freeze']]
                for attr_name in self.extra_data['lock']:
                    pm.setAttr(attr_name, lock=True)
            except:
                import _app._maya.util as util
                util.add_select(self.extra_data['freeze'])

    def _freeze(self, transform_nodes):
        list_with_length = ((x, len(x.strip('|').split('|'))) for x in transform_nodes)
        sort_with_length = sorted(list_with_length, key=lambda item: item[1])
        result = [x[0] for x in sort_with_length]
        result.reverse()
        for trs in result:
            node = pm.PyNode(trs)
            attr_list = ['translate', 'rotate', 'scale', ]
            for attr in attr_list:
                parm_attr = getattr(node, attr)
                lock_statu = False
                if parm_attr.isLocked():
                    lock_statu = True
                    parm_attr.unlock()
                children_attr = parm_attr.getChildren()
                # identity_statu = False
                attribute_quene = []
                for child in children_attr:
                    connect_attr = pm.connectionInfo(child, sfd=True)
                    # attr_tup = []
                    if connect_attr:
                        pm.disconnectAttr(connect_attr, child)
                        # identity_statu = True
                        attribute_quene.append((connect_attr, child))

                if attr == 'translate':
                    pm.makeIdentity(node, apply=True, t=True)

                elif attr == 'rotate':
                    pm.makeIdentity(node, apply=True, r=True)

                elif attr == 'scale':
                    pm.makeIdentity(node, apply=True, s=True)

                # if identity_statu:
                for attr_que in attribute_quene:
                    pm.connectAttr(attr_que[0], attr_que[1], f=True)

                if lock_statu:
                    parm_attr.lock()

    def _select(self):
        if self.extra_data['freeze']:
            pm.select(self.extra_data['freeze'])


def get_qc():
    return Freeze()
