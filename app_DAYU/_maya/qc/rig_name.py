# # -*- coding: utf-8 -*-
# __author__ = 'chenghh'
#
# from app.qc_base import MQCBase
#
#
# class ClearRigName(MQCBase):
#     name = 'Clear Rig Name'
#     usage = u'检查绑定命名规范'
#
#     def __init__(self, parent=None):
#         super(ClearRigName, self).__init__(parent)
#         self.extra_data = []
#         self.error_message = ''
#
#     def validate(self, options):
#         if options.get('type_group') in ['element'] and options.get('type') in ['rig']:
#             # orm = options.get('orm')
#             # if orm and orm.top.name == 'yys':
#             #     return False
#             return True
#         else:
#             return False
#
#     def get_all(self):
#         import pymel.core as pm
#         base_paths = ['|ASSET|RIG']
#         for trans in pm.ls(base_paths, type='transform', dag=1):
#             if trans.name() not in ['RIG', 'Group']:
#                 yield trans
#
#     def run(self, *args, **kwargs):
#         self.error_message = ''
#         self.extra_data = {}
#
#         self.extra_data['other_same'] = []
#         self.extra_data['outline_error'] = []
#         self.extra_data['main_null'] = []
#         result = True
#
#         for node in self.get_all():
#
#             if '|' in node.name():
#                 self.extra_data['other_same'].append(node)
#             try:
#                 if node.fullPath().split('|')[:5] == [u'', u'ASSET', u'RIG', u'Group',u'Main']:
#                     self.extra_data['main_null'].append(node)
#                 elif node.fullPath().split('|')[:4] != [u'', u'ASSET', u'RIG', u'Group']:
#                     self.extra_data['outline_error'].append(node)
#                 else:
#                     pass
#
#             except:
#                 pass
#
#         if self.extra_data['other_same']:
#             self.error_message += u'transform 节点重名：<br/>'
#             for node in self.extra_data['other_same']:
#                 self.error_message += '{}<br/>'.format(node.fullPath())
#             result = False
#
#         if not self.extra_data['main_null']:
#             self.error_message += u'控制器Group|Main 为空：<br/>'
#             result = False
#         elif self.extra_data['outline_error']:
#             self.error_message += u'大纲 命名不正确：<br/>'
#             for node in self.extra_data['outline_error']:
#                 self.error_message += '{}<br/>'.format(node.fullPath())
#             result = False
#         else:
#             pass
#
#         print self.extra_data
#         return result
#
#
#     def select_callback(self, parent_widget=None):
#         import pymel.core as pm
#         if self.extra_data['other_same']:
#             for transform_error_nodes in self.extra_data['other_same']:
#                 pm.select()
#                 pm.select(transform_error_nodes, add=1)
#         if self.extra_data['outline_error']:
#             import app._maya.util as util
#             util.message('OutLine should be RIG/Group/Main')
#
#
# def get_qc():


#     return ClearRigName()
