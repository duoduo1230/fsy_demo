#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'

from app_DAYU.qc_base import MQCBase


class CheckNormal(MQCBase):
    name = 'Clear Uv Normal'
    usage = u'检查 UV法线'

    def __init__(self, parent=None):
        super(CheckNormal, self).__init__(parent)
        self.extra_data = []
        self.error_message = ''
        self.lock_normal = []
        self.error_normal = []
        self.overlay_uv = []

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl', 'srf']:
            return True
        else:
            return False

    def get_all(self):
        import pymel.core as pm
        base_paths = ['|ASSET', '|SCENE']
        return pm.ls(base_paths, type='mesh', dag=1)
        # yield shape_node.parent(0)

    def run(self, *args, **kwargs):
        import maya
        import pymel.core as pm
        self.error_message = ''
        try:
            pm.refresh(suspend=True)
            all_nodes = self.get_all()
            pm.select(all_nodes)
            pm.polyNormalPerVertex(ufn=1)
            pm.mel.eval('DeleteHistory')
            pm.refresh(suspend=False)
            return True
        except Exception as e:
            print e
            self.error_message += u'有点法线锁定，请手动修复'
            return False

        # if len(transform_node.vtx[0])<1:
        #     continue
        # pm.select(transform_node.vtx[0], r=True)
        #
        # if pm.polyNormalPerVertex(q=1, allLocked=True)[0]:
        #
        #     self.lock_normal.append(transform_node)
        # todo uv check wait
        # pm.select(transform_node)
        # maya.mel.eval('ConvertSelectionToFaces')
        # overlay_uv = maya.mel.eval('polyUVOverlap -oc')
        #
        # if overlay_uv:
        #     self.overlay_uv.append(transform_node)

        # if self.lock_normal:
        #     self.error_message += u'点法线锁定：<br/>'
        #     for lock_node in self.lock_normal:
        #         self.error_message += u'{}<br/>'.format(lock_node.name())
        #     result = False
        # if self.overlay_uv:
        #     self.error_message += u'UV重叠：<br/>'
        #     for overlay_node in self.overlay_uv:
        #         self.error_message += u'{}<br/>'.format(overlay_node.name())
        #     result = False

    def repair(self, *args, **kwargs):
        pass


def get_qc():
    return CheckNormal()
