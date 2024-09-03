#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2018.7
# Email : muyanru345@163.com
###################################################################

from app_DAYU.qc_base import MQCBase


class MValidateFileNode(MQCBase):
    name = 'Validate File Node File Path'
    usage = u'校验所有引用外部文件的文件路径是否都在服务器上'

    def __init__(self, parent=None):
        super(MValidateFileNode, self).__init__(parent)

    def validate(self, options):
        if options.get('type_group') in ['workfile']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        return True


def get_qc():
    return MValidateFileNode()
