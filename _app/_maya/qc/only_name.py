#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenghh'
import pymel.core as pm
from _app.qc_base import MQCBase
import ui_center.widgets.MAppContext as MAppContext


class ClearOnlyName(MQCBase):
    name = 'Clear Only Name'
    usage = u'检查 模型名字是否唯一'

    def __init__(self, parent=None):
        super(ClearOnlyName, self).__init__(parent)
        self.self_different = []
        self.other_same = []
        self.error_message = ''

    def validate(self, options):
        # TODO 和平精英项目不过这个QC
        project = str(MAppContext.MAppContext().entity_orm.find_meaning('PROJECT').name)
        if options.get('type_group') in ['element'] and options.get('type') in ['mdl', 'srf'] and project not in ['hpjy']:
            return True
        else:
            return False

    def get_all(self):
        base_paths = ['|ASSET|GEO|HIG', '|ASSET|GEO|XLOW', '|ASSET|GEO|MID']
        return [pm.ls(level, type='mesh', dag=1) for level in base_paths]

    def run(self, *args, **kwargs):
        from collections import Counter
        self.error_message = ''

        self.self_different = []
        self.other_same = []
        result = True

        for level in self.get_all():
            temp = []
            for node in level:
                trans_name = node.parent(0)
                if trans_name:
                    temp.append((node.name(), node.name().split('|')[-1]))
            temp_short = map(lambda x: x[1], temp)
            count_dict = Counter(temp_short)
            same_list = []
            for key, v in count_dict.items():
                if v > 1:
                    same_list.append(temp_short.index(key))
            if same_list:
                for i in same_list:
                    self.self_different.append(temp[i][0])

            short_name_list = [item.split('|')[-1] for item in level]
            count = Counter(short_name_list)

            for item in level:
                if count.get(item.split('|')[-1]) > 1:
                    self.other_same.append(item)

        if self.self_different:
            self.error_message += u'Shape 重名：<br/>'
            for node in self.self_different:
                self.error_message += '{}<br/>'.format(node)
            result = False

        if self.other_same:
            self.error_message += u'transform 节点重名：<br/>'
            for node in self.other_same:
                self.error_message += '{}<br/>'.format(node.fullPath())
            result = False
        if result:
            self.error_message = ''
        return result

    def repair(self, *args, **kwargs):
        import pymel.core as pm
        if self.self_different:
            try:
                pm.select(self.self_different)
            except:
                pass

    def select_callback(self, parent_widget=None):
        import pymel.core as pm
        if self.other_same:
            pm.select(d=1)
            for transform_error_nodes in self.other_same:
                pm.select(transform_error_nodes, add=1)


def get_qc():
    return ClearOnlyName()
