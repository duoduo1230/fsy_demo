# -*- coding: utf-8 -*-
__author__ = 'yang zhuo'
from _app.qc_base import MQCBase
import pymel.core as pm


class CheckLight(MQCBase):
    name = 'Validate Light'
    usage = u'校验灯光'
    error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['lgt']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        if pm.objExists('|SCENE|LIGHTS') or pm.objExists('|ASSET|SRF|LIGHTS'):
            return True
        else:
            self.error_message = u'当前场景中得LIGHTS层级被删除了， 点击修复可自动帮你创建'
            return False

    def repair(self, *args, **kwargs):
        if pm.objExists('|SCENE'):
            pm.group(em=True, name='LIGHTS', parent='|SCENE')
        if pm.objExists('|ASSET'):
            pm.group(em=True, name='LIGHTS', parent='|ASSET|SRF')


def get_qc():
    return CheckLight()
