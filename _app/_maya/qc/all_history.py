#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'

from _app.qc_base import MQCBase
import ui_center.widgets.MAppContext as MAppContext


class ClearAllHistory(MQCBase):
    name = 'Clear Polygon History'
    usage = u'检查模型历史'

    def __init__(self, parent=None):
        super(ClearAllHistory, self).__init__(parent)
        self.extra_data = []
        self.error_message = ''

    def validate(self, options):
        # md项目某个资产暂时不QC
        asset = str(MAppContext.MAppContext().entity_orm.name)
        project = str(MAppContext.MAppContext().entity_orm.find_meaning('PROJECT').name)
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl', 'srf']\
                and asset not in ['env_building-01'] and project not in ['md']:
            return True
        else:
            return False

    def get_all(self):
        import pymel.core as pm
        base_paths = ['|ASSET']
        for base_path in pm.ls(base_paths, type='mesh', dag=1):
            yield base_path

    def run(self, *args, **kwargs):
        intermediateObjects = 1
        self.error_message = ''
        self.history_nodes = []
        self.intermediate_object = []
        result = True
        for shape in self.get_all():
            if shape.intermediateObject.get():
                self.error_message += u'IntermediateObject shape：<br/>'
                self.error_message += u'{}<br/>'.format(shape.fullPath())

                self.intermediate_object.append(shape)
                result = False
                continue

            if shape.inputs():
                self.error_message += u'带历史的节点：<br/>'
                self.error_message += u'{}<br/>'.format(shape.fullPath())

                self.history_nodes.append(shape)
                result = False


        return result

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        import _app._maya.util as util

        error_nodes = []

        for shape in self.history_nodes:
            try:
                pm.delete(shape, ch=1)
                for attr_tuple in shape.inputs(c=1, p=1):
                    pm.disconnectAttr(attr_tuple[1], attr_tuple[0])
            except:
                error_nodes.append(shape)

        for intermediate_shape in self.intermediate_object:
            try:
                if intermediate_shape.isLocked():
                    intermediate_shape.unlock()
                pm.delete(intermediate_shape)
            except:
                error_nodes.append(intermediate_shape)

        if error_nodes:

            util.message(u'无法修复的模型,需要您亲自排查', dialog=True)


def get_qc():
    return ClearAllHistory()
