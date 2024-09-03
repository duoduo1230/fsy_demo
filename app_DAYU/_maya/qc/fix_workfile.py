#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'

import net_log
from app_DAYU.qc_base import MQCBase


class FixWorkFile(MQCBase):
    name = 'Fix Work File'
    usage = u'修复当前工程文件未知错误'

    def __init__(self, parent=None):
        super(FixWorkFile, self).__init__(parent)
        self.extra_data = []
        self.error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['workfile', 'element']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        self.fix_outliner_bug()
        try:
            self.delete_unknown_node()
        except:
            self.delete_unknown_node()
            from app_DAYU._maya import util as mutil
            mutil.message('remove unknown node error',level='warning')

        try:
            self.fix_unknown_plugin()
        except:
            self.fix_unknown_plugin()
            from app_DAYU._maya import util as mutil
            mutil.message('remove unknown plug error',level='warning')

        try:
            self.delete_model_event()
        except:
            self.delete_model_event()
            from app_DAYU._maya import util as mutil
            mutil.message('remove model event error',level='warning')

        try:
            if pm.objExists('TurtleDefaultBakeLayer'):
                pm.PyNode('TurtleDefaultBakeLayer').unlock()
                pm.delete('TurtleDefaultBakeLayer')
        except:
            pass
        try:
            if pm.objExists('TurtleBakeLayerManager'):
                pm.PyNode('TurtleBakeLayerManager').unlock()
                pm.delete('TurtleBakeLayerManager')
        except:
            pass
        try:
            if pm.objExists('TurtleRenderOptions'):
                pm.PyNode('TurtleRenderOptions').unlock()
                pm.delete('TurtleRenderOptions')
        except:
            pass
        try:
            if pm.objExists('TurtleUIOptions'):
                pm.PyNode('TurtleUIOptions').unlock()
                pm.delete('TurtleUIOptions')
        except:
            pass

        if pm.pluginInfo('Turtle.mll', q=True, l=True):
            pm.unloadPlugin("Turtle.mll", f=True)

        # 删除之前常出现的 sharereferenceNode
        if pm.objExists('sharereferenceNode'):
            try:
                nd = pm.PyNode('sharereferenceNode')
                nd.unlock()
                pm.delete(nd)
            except:
                print 'remove sharereferenceNode failure.'

        return True

    def repair(self, *args, **kwargs):
        self.run(*args, **kwargs)

    def fix_outliner_bug(self):
        import pymel.core as pm
        outliner_ui_list = []
        panels = pm.getPanel(all=True)
        for pannel in panels:
            if pannel.type() == 'ToutlinerEditor':
                outliner_ui_list.append(pannel.name())

        for ui in outliner_ui_list:
            try:
                if pm.outlinerEditor(ui, query=True, selectCommand=True):
                    pm.outlinerEditor(ui, edit=True, selectCommand='print ""')
                if pm.outlinerEditor(ui + 'Slave', query=True, selectCommand=True):
                    pm.outlinerEditor(ui + 'Slave', edit=True, selectCommand='print ""')
            except:
                continue


    @staticmethod
    def delete_unknown_node():
        import pymel.core as pm
        unknown_list = pm.ls(type=['unknown','unknownDag'])
        for node in unknown_list:
            if pm.objExists(node) and not node.isReferenced():
                is_lock = node.isLocked()
                node.unlock() if is_lock else None
                pm.delete(node)

    @staticmethod
    def fix_unknown_plugin():
        import pymel.core as pm
        # 外包文件 发现有不断出现 未知插件加载错误 把错误给移除掉
        plugs = pm.unknownPlugin(q=True, list=True)
        if plugs:
            for plug in plugs:
                pm.unknownPlugin(plug, remove=True)

    def delete_model_event(self):
        # 外包文件打开后 不断加载 onModelChange3dc 移除掉
        import pymel.core as pm
        for item in pm.lsUI(editors=True):
            if isinstance(item, pm.ui.ModelEditor) and pm.modelEditor(item, q=True, editorChanged=True):
                pm.modelEditor(item, edit=True, editorChanged="")


def get_qc():
    return FixWorkFile()
