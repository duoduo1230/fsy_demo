# -*- coding: utf-8 -*-
__author__ = 'zhaoxu'

from app.qc_base import MQCBase


class CheckAssetLink(MQCBase):
    name = 'Validate Asset Link'
    usage = u'检查资产是否有关联, 在shot环节组装时尤为重要'
    error_message = ''

    def validate(self, options):
        if options.get('type_group') in ['element'] and options.get('type') in ['srfa', 'shda', 'ldva', 'riga']:
            return True
        else:
            return False

    def run(self, *args, **kwargs):
        self.error_message = ''
        import app._maya.util as util

        current_step = util.current_step()
        file_info = util.get_file_info()

        workfile_orm = util.current_workfile_orm()
        asset_orm = workfile_orm.find_meaning('asset')
        if workfile_orm and asset_orm:
            # 考虑到以后资产环节会在shot下工作
            if current_step in ['srf', 'shd', 'ldv']:
                # 必须有mdl信息
                if 'mdl' not in file_info:
                    self.error_message += u'场景文件中没有mdl信息! 可能模型不是通过Resource Manager创建的.'
                    return False
            elif current_step == 'rig':
                # 必须有mdl 或者 srf 信息
                if 'mdl' not in file_info and 'srf' not in file_info:
                    self.error_message += u'场景文件中没有mdl或srf信息! 可能模型不是通过Resource Manager创建的.'
                    return False
        return True

    def repair(self, *args, **kwargs):
        import app._maya.util as util
        from db.db_path import DBPath
        import itertools

        current_step = util.current_step()

        current_orm = util.current_workfile_orm()
        asset_orm = current_orm.find_meaning('asset')

        mdl_type_orm = DBPath(asset_orm.db_path()).child('element', 'mdl').orm()

        res_iter = mdl_type_orm.children
        if current_step == 'rig':
            srf_type_orm = DBPath(asset_orm.db_path()).child('element', 'srf').orm()
            res_iter = itertools.chain(res_iter, srf_type_orm.children)

        self._select_resource(list(res_iter))
        if self.res_orm:
            util.add_file_info(self.res_orm.sub_files[-1])
            self.error_message = ''

    def _select_resource(self, resources):
        if not resources:
            self.res_orm = None
            return

        from ui_center.qt import QDialog, QVBoxLayout, QComboBox, QPushButton, SIGNAL

        self.res_orm = None

        win = QDialog()
        win.setWindowTitle('Select Resource')
        layout = QVBoxLayout()
        win.setLayout(layout)

        win.combo = QComboBox()
        win.combo.addItems([r.name for r in resources])
        layout.addWidget(win.combo)

        ok_btn = QPushButton('OK')
        layout.addWidget(ok_btn)

        clr_btn = QPushButton('Clear')
        layout.addWidget(clr_btn)

        def ok():
            _index = win.combo.currentIndex()
            self.res_orm = resources[_index]
            win.close()

        win.connect(ok_btn, SIGNAL('clicked()'), ok)
        win.connect(clr_btn, SIGNAL('clicked()'), win.close)

        win.exec_()
        return self.res_orm


def get_qc():
    return CheckAssetLink()


if __name__ == '__main__':
    qc = get_qc()
    qc.repair()