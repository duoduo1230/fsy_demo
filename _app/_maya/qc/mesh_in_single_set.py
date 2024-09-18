# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 11/28/2018 6:57 PM
# from collections import Counter
#
# __author__ = 'pengyuxuan'
# from app.qc_base import MQCBase
#
#
# class MeshSingleSet(MQCBase):
#     name = ' Is mesh in single set '
#     usage = u'单个mesh 只能存在于一个set 中'
#
#     def __init__(self, parent=None):
#         super(MeshSingleSet, self).__init__(parent)
#         self.error_nodes = []
#
#     def validate(self, options):
#         if options.get('type_group') in ['element'] and options.get('type') in ["srf"]:
#             return True
#         else:
#             return False
#
#     def run(self, *args, **kwargs):
#         import pymel.core as pm
#         import maya.mel as mel
#
#         self.error_nodes = []
#         default_set = ['defaultLightSet', 'defaultObjectSet', 'initialParticleSE', 'initialShadingGroup', '<done>']
#         set_nodes = mel.eval('lsType("objectSet")')
#         set_nodes = filter(lambda x: x not in default_set, set_nodes)
#         if not set_nodes:
#             self.error_nodes = pm.ls('|ASSET|GEO',type='mesh',dag=True)
#             self.error_message = u'当前所有shape都没有创建set组'
#             return False
#         set_nodes = [pm.PyNode(i) for i in set_nodes]
#
#         set_node_list = []
#         for single_set in set_nodes:
#             #  先拿到所有set 下的所有节点，如果节点是transform 往下找到mesh, 最后在大列表中筛选出重复元素
#             set_node_list.extend(list({node.getShape() if node.type() == 'transform' else node for node in single_set}))
#         self.error_nodes.extend([k for k, v in Counter(set_node_list).items() if v > 1])
#
#         if self.error_nodes:
#             self.error_message = u'{} 可能存在于多个 set 之中或 shape 和 transform 分别在不同的 set 之中，' \
#                                  u'请检查. 点击 repair 选中这些节点'.format(str(self.error_nodes))
#             return False
#         return True
#
#     def repair(self, *args, **kwargs):
#         import pymel.core as pm
#         set_node = pm.createNode('objectSet')
#
#         set_node.addMembers([node.getTransform() for node in self.error_nodes if node.nodeType() == 'mesh'])
#         pm.select(self.error_nodes)
#
#
#
#
#
#
#
#
# def get_qc():
#     return MeshSingleSet()
