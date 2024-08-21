# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
#
# __author__ = 'yangzhuo'
#
#
# from app.qc_base import MQCBase
#
#
# class PolyCleanupArgList(MQCBase):
#     name = 'polyCleanupArgList'
#     usage = u'清理非流体模型'
#
#     def __init__(self, parent=None):
#         super(PolyCleanupArgList, self).__init__(parent)
#
#     def validate(self, options):
#         if options.get('type_group') in ['element'] and options.get('type') in ['mdl']:
#             return True
#         else:
#             return False
#
#     def run(self, *args, **kwargs):
#         import pymel.core as pm
#         try:
#             pm.mel.eval('polyCleanupArgList 4 { "0","1","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","2","0","0" };')
#             return True
#         except Exception as e:
#             print e
#             return False
#
#
# def get_qc():
#     return PolyCleanupArgList()
#
#
