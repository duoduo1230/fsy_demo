#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'

from app_DAYU.qc_base import MQCBase


class CheckOverlayMesh(MQCBase):
    name = 'Clear overlay mesh'
    usage = u'检查 重叠模型'

    def __init__(self, parent=None):
        super(CheckOverlayMesh, self).__init__(parent)
        self.extra_data = []
        self.error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl', 'srf'] and self.validate_project():
            return True
        else:
            return False

    @staticmethod
    def validate_project():
        import ui_center.widgets.MAppContext as MAppContext
        context = MAppContext.MAppContext()
        project = context.workfile_version_orm.top.name
        return False if project and project == 'joy' else True

    def get_all(self):
        import pymel.core as pm
        re = []
        base_paths = ['|ASSET|GEO|HIG', '|ASSET|GEO|MID', '|ASSET|GEO|LOW', '|ASSET|GEO|XLOW']
        for path in base_paths:
            temp = [shape_node.parent(0) for shape_node in pm.ls(path, type='mesh', dag=1, noIntermediate=1)]
            re.append(temp)
        return re

    def run(self, *args, **kwargs):
        import pymel.core as pm
        self.error_message = ''
        self.extra_data = []

        for level in self.get_all():
            self.overlay_mesh = {}
            self.overlay_mesh['vernum'] = {}
            self.overlay_mesh['verposition'] = {}
            for node in level:
                x, y, z, xx, yy, zz = pm.xform(node, q=1, ws=1, bb=1)
                bb = '%.3f' % x + ',' + '%.3f' % y + ',' + '%.3f' % z + ',' + '%.3f' % xx + ',' + '%.3f' % yy + ',' + '%.3f' % zz
                self.overlay_mesh['vernum'].setdefault((bb, node.numVertices()), []).append(node)

            for tran_num, node_list in self.overlay_mesh['vernum'].items():
                if len(node_list) > 1:
                    ver_num = tran_num[1]
                    import random
                    count = 20 if ver_num > 20 else ver_num
                    random_ver = random.sample(range(ver_num), count)
                    for num_node in node_list:
                        for index in random_ver:
                            num_node_ver = num_node.vtx[index]
                            self.overlay_mesh['verposition'].setdefault(num_node_ver.getPosition().get(), []).append(
                                num_node)

                    result = True
                    for ver_position, same_ver_position in self.overlay_mesh['verposition'].items():
                        if len(same_ver_position) < 2:
                            result = False
                            break
                    if result:
                        self.extra_data.extend(same_ver_position)

        if self.extra_data:
            self.error_message += u'重叠模型：<br/>'
            for overlay_node in self.extra_data:
                self.error_message += u'{}<br/>'.format(overlay_node.fullPath())
            return False
        else:
            self.error_message = ''
            return True

    def select_callback(self, *args, **kwargs):
        if self.extra_data:
            import pymel.core as pm
            pm.select(self.extra_data)


def get_qc():
    return CheckOverlayMesh()
