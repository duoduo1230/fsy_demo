#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wenfeng'
import pymel.core as pm
from _app.qc_base import MQCBase
import ui_center.widgets.MAppContext as MAppContext


class checkGroupId(MQCBase):
    name = 'Check groupId'
    usage = u'检查 模型有groupId节点'

    def __init__(self, parent=None):
        super(checkGroupId, self).__init__(parent)
        self.self_different = []
        self.error_message = ''

    def validate(self, options):
        project = str(MAppContext.MAppContext().entity_orm.find_meaning('PROJECT').name)
        if options.get('type_group') in ['element'] and options.get('type') in ['srf'] and project not in ['md']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        objects_Selected = pm.ls('|ASSET|GEO', dag=True, type='mesh') if pm.objExists('|ASSET|GEO') else []
        if not objects_Selected:
            return True
        groupId_List = pm.listHistory(objects_Selected, allConnections=True, type='groupId')
        if groupId_List:
            self.error_message = 'There are nodes of type groupid.'
            self.self_different = groupId_List
            return False
        else:
            return True


    def repair(self, *args, **kwargs):
        import pymel.core as pm
        if self.self_different:
            try:
                pm.delete(self.self_different)
            except:
                pass


def get_qc():
    return checkGroupId()

