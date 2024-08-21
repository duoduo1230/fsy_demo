#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'

from app.qc_base import MQCBase


class CheckUnit(MQCBase):
    name = 'Check Unit'
    usage = u'检查maya场景单位设置'

    def __init__(self, parent=None):
        super(CheckUnit, self).__init__(parent)
        self.extra_data = []
        self.error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type_group') in ['workfile']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        import app._maya.util as util
        from db.disk_path import DiskPath
        file_path = util.current_file()
        file_orm = DiskPath(file_path).orm(disk_type='work')
        maya_unit = file_orm.cascading_info.get('maya_unit') if file_orm else 'cm'

        self.error_message = ''
        if pm.currentUnit(q=1) != maya_unit:
            self.error_message = u'场景比例不对'
            return False
        else:
            self.error_message = ''
            return True


def get_qc():
    return CheckUnit()
