# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
#
# __author__ = 'Wenfeng Zhang'
#
# from app.qc_base import MQCBase
#
#
# class CheckCameraParentIsDefault(MQCBase):
#     name = 'Check camera parent transform'
#     usage = u'检查像机的父层级是否有key帧或者修改数据'
#
#     def __init__(self, parent=None):
#         super(CheckCameraParentIsDefault, self).__init__(parent)
#
#     def validate(self, options):
#         if options.get('type_group') in ['element'] and options.get('type') in ['cam', 'ani']:
#             return True
#         else:
#             return False
#
#     def run(self, *args, **kwargs):
#         import pymel.core as pm
#         self.error_nodes = []
#         self.error_message = ''
#
#         default_camera = ['frontShape', 'perspShape', 'sideShape', 'topShape']
#         cam_list = filter(lambda x: x not in default_camera, pm.ls(type='camera'))
#         check_attr_list = ['translate', 'rotate', 'scale', 'shear', 'rotateAxis', 'rotatePivot', 'scalePivot',
#                            'rotatePivotTranslate', 'scalePivotTranslate']
#         if not cam_list:
#             return True
#         for cam in cam_list:
#             cam_transf = cam.getTransform()
#             cam_parent = cam_transf.getParent()
#             if cam_parent:
#                 if pm.keyframe(cam_parent, query=True):
#                     self.error_nodes.append(cam_parent.fullPath())
#                     continue
#                 for attr in check_attr_list:
#                     new_values = list(cam_parent.getAttr(attr))
#                     default_values = pm.attributeQuery(attr, node=cam_parent, listDefault=True)
#                     if new_values != default_values:
#                         self.error_nodes.append(cam_parent.fullPath())
#                         break
#
#         if self.error_nodes:
#             msg = u'以下节点是像机的父层级，带有动画或者修改过默认数值，需要用户自己修改。<br/>'
#             self.error_message = msg + '<br/>'.join([x for x in set(self.error_nodes)])
#             return False
#         return True
#
#     def repair(self, *args, **kwargs):
#         import pymel.core as pm
#         pm.select(self.error_nodes)
#         self.error_message = ''
#
#
# def get_qc():
#     return CheckCameraParentIsDefault()
#
