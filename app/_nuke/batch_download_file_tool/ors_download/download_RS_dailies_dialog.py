#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'

import os
import csv
import time
from datetime import datetime, timedelta
import db.util
from app import DAYU
import datetime as dt
import wrap_shotgun as ws
from ui_center.qt import *
from dayu_path import DayuPath
from db.util import get_cascading_info
from ui_center.widgets import ui_utils
from config.const import OUTPUT_FORMAT_DICT
from ui_center.widgets.MFolderWidget import MFolderWidget
from ui_center.widgets.MItemViewFilterSetWidget import MItemViewFilterSetWidget
from ui_center.widgets.message_box import MErrorMessageBox, MSuccessMessageBox
from app._public.context_menu.folder_file.download_dailies.attr_config import COLOR_SPACE_CONFIG, META_CODEC_DICT


class DownloadDailiesDialog(QDialog):
    @ui_utils.dayu_css()
    @ui_utils.dayu_user_state()
    @ui_utils.help_action()
    def __init__(self, parent=None):
        super(DownloadDailiesDialog, self).__init__(parent)
        self.setWindowTitle(self.tr('Download RS Dailies'))
        self.project = None
        geo = QApplication.desktop().screenGeometry()
        self.setGeometry(geo.width() / 4, geo.height() / 4, geo.width() / 2, geo.height() / 2)
        self.title_label = QLabel(self.tr('Download RS Dailies'))
        self.title_label.setObjectName('title')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.folder_widget = MFolderWidget()

        folder_lay = QHBoxLayout()
        folder_lay.addWidget(QLabel(self.tr('Target Folder:')))
        folder_lay.addWidget(self.folder_widget)

        self.rename_check_box = QCheckBox(self.tr('Rename:'))
        self.rename_check_box.setChecked(True)
        self.rename_line_edit = QLineEdit()
        self.rename_check_box.stateChanged.connect(self.rename_line_edit.setEnabled)
        self.rename_check_box.setChecked(False)

        # self.folder_rename_check_box = QCheckBox(self.tr('Folder Name:'))
        # self.rename_check_box.setChecked(True)
        # self.folder_rename_line_edit = QLineEdit()

        rename_lay = QHBoxLayout()
        rename_lay.addWidget(self.rename_check_box)
        rename_lay.addWidget(self.rename_line_edit)
        rename_lay.setContentsMargins(0, 0, 0, 0)

        # folder_rename_lay = QHBoxLayout()
        # folder_rename_lay.addWidget(self.folder_rename_check_box)
        # folder_rename_lay.addWidget(self.folder_rename_line_edit)
        # folder_rename_lay.setContentsMargins(0, 0, 0, 0)

        self._resolver = DAYU.request('/resolver')
        resolver_tooltip = "You can rename using the following keyword tokens:<br>" \
                           "eg: yys pl_0010_comp_master_v0003<br>"
        for i in range(0, self._resolver.entry_count()):
            resolver_tooltip += '<b>%s</b> - %s<br>' % (
                self._resolver.entry_name(i), self._resolver.entry_description(i))
        self.rename_line_edit.setToolTip(resolver_tooltip)

        self.choose_grp = QGroupBox(u'选择mov转码所需要的编码器')
        self.codec_check_box = QCheckBox(self.tr('Transcode With Codec'))
        self.add_lut_name_check_box = QCheckBox(self.tr('Add Lut Name'))
        self.lut_check_box = QCheckBox(self.tr('Transcode With Lut'))
        self.csv_check_box = QCheckBox(self.tr('Generate CSV File'))
        self.sequence_check_box = QCheckBox(self.tr('Sequence'))
        self.csv_check_box.setChecked(True)

        self.use_sg_client_name_check_box = QCheckBox(u'使用shotgun 镜头client字段命名')
        self.use_sg_client_name_check_box.setChecked(False)

        self.use_time_check_box = QCheckBox(u'日期')
        self.use_time_check_box.setChecked(False)

        self.codec_com_box = QComboBox()
        self.codec_com_box.setEnabled(False)
        self.codec_com_box.addItems(
            sorted([key for key in OUTPUT_FORMAT_DICT.keys() if key not in ['tiff', 'jpg']])
        )
        self.codec_com_box.setCurrentIndex(3)

        self.ext_label = QLabel(self.tr('Transcode With Ext'))
        self.ext_com_box = QComboBox()
        self.ext_com_box.addItems(['.mov', '.jpg', '.exr', '.dpx'])
        self.ext_com_box.activated[str].connect(self.slot_ext_changed)
        self.codec_check_box.stateChanged.connect(self.slot_is_codec)

        choose_lay = QHBoxLayout()
        choose_lay.addWidget(self.codec_check_box)
        choose_lay.addWidget(self.codec_com_box)
        choose_lay.addStretch()
        choose_lay.addWidget(self.ext_label)
        choose_lay.addWidget(self.ext_com_box)
        choose_lay.addStretch()
        choose_lay.addWidget(self.lut_check_box)
        choose_lay.addStretch()
        choose_lay.addWidget(self.csv_check_box)
        choose_lay.addStretch()
        choose_lay.addWidget(self.sequence_check_box)
        choose_lay.addStretch()
        choose_lay.addWidget(self.use_sg_client_name_check_box)
        choose_lay.addWidget(self.use_time_check_box)
        choose_lay.addStretch()

        self.choose_grp.setLayout(choose_lay)

        self.item_view = MItemViewFilterSetWidget()
        self.item_view.enable_search()
        self.item_view.set_header_list(
            [{'name': 'Version Name', 'attr': 'name', 'searchable': True, 'checkable': True,
              'width': 250},
             {'name': 'Sub level', 'attr': 'sub_level', 'searchable': True}])
        self.item_view.table_view.header_view.setStretchLastSection(True)
        self.download_button = QPushButton(self.tr('Download Dailies'))
        self.download_button.clicked.connect(self.slot_download)
        button_lay = QHBoxLayout()
        button_lay.addWidget(self.download_button)

        main_lay = QVBoxLayout()
        main_lay.addSpacing(10)
        main_lay.addWidget(self.title_label)
        main_lay.addSpacing(10)
        main_lay.addWidget(self.choose_grp)
        main_lay.addSpacing(20)
        main_lay.addLayout(folder_lay)
        main_lay.addLayout(rename_lay)
        # main_lay.addLayout(folder_rename_lay)
        main_lay.addWidget(self.item_view)
        main_lay.addLayout(button_lay)

        self.setLayout(main_lay)

    def setup_data(self, version_orm_list):
        result_list = []
        DAYU.request('/refresh/all')()
        for orm in version_orm_list:
            orig_folder = orm.disk_path(disk_type='publish')
            for sub_level in orm.sub_level.walk(collapse=True):
                if '/jpg/' in sub_level.filename.replace(orig_folder, ''):
                    result_list.append({
                            'name': orm.name,
                            'name_checked': 2,
                            'sub_level': sub_level.filename.replace(orig_folder, ''),
                            'sequence_file': sub_level,
                            'ext': sub_level.filename.ext,
                            'orm': orm}
                    )
            else:
                variable = db.util.get_cascading_info(orm, 'cascading_info')['all_info'].get('output_naming', '')
                self.rename_line_edit.setText(variable)
                # self.folder_rename_line_edit.setText(variable)

        self.item_view.setup_data(result_list)

    @Slot()
    def slot_is_codec(self):
        if self.codec_check_box.isChecked():
            self.codec_com_box.setEnabled(True)
        else:
            self.codec_com_box.setEnabled(False)

    @Slot()
    def slot_ext_changed(self, ext):
        filter_data = [x for x in self.orig_data if x.get('ext') == ext]
        self.item_view.setup_data(filter_data)

    def milliseconds_to_tc(self, milliseconds):
        frames_per_second = 25
        time_delta = timedelta(milliseconds=milliseconds)
        hours, remainder = divmod(time_delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        frames = (milliseconds % 1000) * frames_per_second // 1000
        timecode = "{:02d}:{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds, frames)

        return timecode

    @Slot()
    def slot_download(self):
        """
        核心逻辑: nuke.exe temp.py
        temp.py 里面创建所有需要渲染的节点，然后批量执行渲染
        :return:
        """
        sg = ws.MyShotgun()
        if not self.folder_widget.get_folder():
            msg = MErrorMessageBox(parent=self, msg=self.tr('Please give me the target folder!'))
            msg.exec_()
            self.folder_widget.line_edit.setFocus(Qt.MouseFocusReason)
            return
        if not os.path.isdir(self.folder_widget.get_folder()):
            msg = MErrorMessageBox(parent=self, msg=self.tr('The target folder not exist!'))
            msg.exec_()
            return

        version_dict = {}
        csv_data_dict = {}

        name_conventions = {'comp': 'cmp', 'roto': 'rto', 'paint': 'pnt', 'ldev': 'ldv'}
        for data_obj in self.item_view.get_data():
            if not ui_utils.get_obj_value(data_obj, 'name_checked'):
                continue
            orm = ui_utils.get_obj_value(data_obj, 'orm')
            self.project = orm.top.name
            version_id = orm.cloud_id
            version_info = sg.find_one('Version', [['id', 'is', version_id]], ['sg_version_folder_win'])
            description = version_info.get('sg_version_folder_win')
            key_name = u'{}-{}'.format(orm.top.name, orm.meaning)
            if key_name not in csv_data_dict.keys():
                reg_obj, header_list = db.util.get_name_pattern(orm.top.name, orm.meaning)
                csv_data_dict[key_name] = [header_list + [u'FOLDER_PATH', u'has lut']]
            data_list = csv_data_dict.get(key_name)
            header_list = data_list[0]
            data_list.append([orm.find_meaning(meaning).name.split('_')[-1] for meaning in header_list[:-2]] +
                             [os.path.join(self.folder_widget.get_folder(), orm.name)])

            target_obj = self.folder_widget.get_folder()
            sequence_file = ui_utils.get_obj_value(data_obj, 'sequence_file')
            frame_range = [sequence_file.frames[0], sequence_file.frames[-1]] if sequence_file.frames else ['', '']
            read_filename = '{} {}-{}'.format(sequence_file.filename, frame_range[0], frame_range[-1])

            # 修改文件名字和文件夹名字ep01_1270_comp_compositing_v0012 为 ep011270_cmp_rr_v012
            # 修改文件名字和文件夹名字chr_cat_mdl_master_v012 为 cat_mdl_hi_v012/cat_mdl_v012
            # 根据sg的信息，根据任务类型修改命名
            new_name = self._resolver.resolve(orm, self.rename_line_edit.text())
            sequence_group = read_filename.split('/')[4]
            if sequence_group == 'asset':
                file_type = 'asset'
                asset_id = orm.find_meaning('ASSET').cloud_id
                asset_info = sg.find_one('Asset', [['id', 'is', asset_id]],
                                        ['sg_note_1'])
                footage = new_name.split('_')
                version_num = footage[4].replace('v0', 'v')
                file_timecode = ''

                note_1 = asset_info.get('sg_note_1')
                if not note_1:
                    customer_name = '_'.join([footage[1], footage[2], version_num])
                else:
                    customer_name = '_'.join([footage[1], footage[2], note_1,  version_num])
            else:
                file_type = 'shot'
                shot_id = orm.find_meaning('SHOT').cloud_id
                shot_info = sg.find_one('Shot', [['id', 'is', shot_id]],
                                        ['sg_lens', 'sg_phenom_cut_in_'])
                tame_code = shot_info.get('sg_phenom_cut_in_')
                if not tame_code:
                    file_timecode = ''
                else:
                    trans_timecode = self.milliseconds_to_tc(tame_code)
                    file_timecode = '[make_timecode {} 24 1001]'.format(trans_timecode)
                len_type = shot_info.get('sg_lens')
                footage = new_name.split('_')
                shot_name = footage[0] + footage[1]
                if footage[2]in name_conventions:
                    step = name_conventions[footage[2]]
                else:
                    step = footage[2]
                version_num = footage[4].replace('v0', 'v')
                if not len_type:
                    customer_name = '_'.join([shot_name, step, version_num])
                else:
                    customer_name = '_'.join([shot_name, step, len_type, version_num])

            # 输出路径
            out_path = DayuPath(target_obj).child('{}.mov'.format(customer_name))
            cas_info = get_cascading_info(orm.top, 'cascading_info')
            fps = float(cas_info['all_info'].get('fps', 24.0))

            meta_codec_type = META_CODEC_DICT[self.codec_com_box.currentText()] \
                if self.codec_check_box.isChecked() else 'apcn'

            version_dict.setdefault(orm.name, {
                'read_filename': read_filename,
                'shot_name': customer_name,
                'file_type': file_type,
                'out_path': str(out_path),
                'fps': fps,
                'time_code': file_timecode,
                'description': description,
                'meta_codec_type': meta_codec_type,
            })

        # 渲染并判断是否成功
        if not self.nuke_render(version_dict):
            msg = MSuccessMessageBox(parent=self, msg=self.tr('Finished rendering.'))
            msg.exec_()
            return
        else:
            msg = MErrorMessageBox(parent=self, msg=self.tr('Rendering error.'))
            msg.exec_()
            return

    def nuke_render(self, version_dict):
        """
        cmd: nuke.exe temp.py
        获取模版, 替换对应参数， 执行render
        :param version_dict: {'version_name': {'read_filename': '', ...}}
        :return: 如果渲染成功返回0，否则返回1
        """
        template_py = DayuPath(__file__).parent.child('rs_template_script.py')
        with open(template_py, 'r') as r:
            template_code = r.read()
        config_data = COLOR_SPACE_CONFIG.get(self.project, '') or COLOR_SPACE_CONFIG.get('default')
        print(config_data)
        result = template_code.format('{}', config_data=config_data, version_data=version_dict)

        scripts_path = DayuPath(os.path.expanduser('~')).child('download_RS_dailies_dialog.py')
        with open(scripts_path, 'w') as f:
            f.write(result)

        if DayuPath(scripts_path).exists():
            cmd = r'"C:\Program Files\Nuke11.2v2\Nuke11.2.exe" --nukex -i --tg {}'.format(scripts_path)
            render_result = os.system(cmd)
            return render_result


if __name__ == '__main__':
    import sys
    import db
    import db.util

    # sess = db.get_session()
    # app = QApplication(sys.argv)
    # test = DownloadDailiesDialog()

    import os
    for k, v in {
            'colorManagement': 'OCIO',
            'OCIO_config': 'aces_1.0.3',
            'customOCIOConfigPath': 'y:/td/aces_1.0.3/config.ocio',
            'workingSpaceLUT': 'ACES - ACEScg',
            'monitorLut': 'ACES/Rec.709',
            'int8Lut': 'Utility - sRGB - Texture',
            'int16Lut': 'ACES - ACEScc',
            'logLut': 'Input - ADX - ADX10',
            'floatLut': 'ACES - ACEScg'}.items():
        print k, v
