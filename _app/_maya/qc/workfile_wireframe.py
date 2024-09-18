# -*- coding: utf-8 -*-
__author__ = 'zhaoxu'

from _app.qc_base import MQCBase


class CheckWireframe(MQCBase):
    name = 'Validate Workfile Wireframe'
    usage = u'检查文件中视图是否都是线框显示'
    error_message = ''

    def validate(self, options):
        if options.get('type_group') == 'workfile':
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        self.error_message = ''
        import pymel.core as pm

        panels = [v for v in pm.getPanel(vis=True) if
                  v.startswith('modelPanel') and pm.modelEditor(v, q=True, displayAppearance=True) != 'wireframe']
        if panels:
            self.error_message += u'有窗口没有线框显示'
            return False

        return True

    def repair(self, *args, **kwargs):
        self.error_message = ''
        import pymel.core as pm

        [pm.modelEditor(v, e=True, displayAppearance='wireframe') for v in pm.getPanel(vis=True) if
         v.startswith('modelPanel') and pm.modelEditor(v, q=True, displayAppearance=True) != 'wireframe']
        self.error_message = ''


def get_qc():
    return CheckWireframe()


if __name__ == '__main__':
    qc = get_qc()
    print qc.run()
    qc.repair()