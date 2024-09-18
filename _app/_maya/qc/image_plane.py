# -*- coding: utf-8 -*-
__author__ = 'chenghh'

import db.util
from _app.qc_base import MQCBase
from db.disk_path import DiskPath
from ui_center.widgets.MAppContext import MAppContext


class CheckPlane(MQCBase):
    def __init__(self, parent=None):
        super(CheckPlane, self).__init__(parent)
        self.name = 'Check Image Plane Node'
        self.usage = u'校验相机背板路径是否合法'
        self.DEFAULT_CAMERAS = [u'frontShape', u'perspShape', u'sideShape', u'topShape']
        self.error_message = ''
        self.extra_data = {}

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['cam']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        import pymel.core as pm
        from db.disk_path import DiskPath
        result = True

        self.extra_data = {}
        self.error_message = u'以下相机背板路径不合法：<br/>'

        # 只有image存在且路径不合法的情况下为False
        image_planes = pm.ls(type='imagePlane')
        for image_plane in image_planes:
            camera = image_plane.message.connections()
            if not camera:
                continue
            image_path = image_plane.imageName.get()

            if not image_path or not DiskPath(image_path).isfile():
                continue
            if not DiskPath(image_path).get_configs(disk_type='publish')[0]:
                self.error_message += '{}<br/>'.format(image_plane.name())
                self.extra_data[image_plane] = image_path
                result = False

        if result:
            self.error_message = ''
        return result

    def repair(self, *args, **kwargs):
        '''
        可选重载
        如果质检没通过，用户点击界面修复按钮，调用该函数执行修复操作
        :param args:
        :param kwargs:
        :return:
        '''
        import pymel.core as pm
        import _app._maya.util as util
        if not self.extra_data:
            util.message(u'没有可修复的数据', dialog=True)
        else:
            app_context = MAppContext()
            shot_orm = app_context.workfile_version_orm.find_meaning('shot')
            pool_path = shot_orm.disk_path('publish').child('pool', db.util.short_uuid())
            new_path = pool_path.child(app_context.workfile_version_orm.name)
            DiskPath(new_path).mkdir(parents=True)
            for node, image_path in self.extra_data.items():
                sequential_files = DiskPath(image_path).scan()
                filename = sequential_files.filename
                for f in sequential_files.frames:
                    old_path = DiskPath(filename.replace('%04d', '{}'.format(f)))
                    old_path.copy(DiskPath(new_path).child(DiskPath(old_path).name))

                pm.select(node)
                node.imageName.set(new_path.child(DiskPath(image_path).name))


def get_qc():
    return CheckPlane()

