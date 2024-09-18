#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2018.7
# Email : muyanru345@163.com
###################################################################

import os
import csv
import db.util
import job_center
import db.disk_path
from _app import DAYU
import datetime as dt
import wrap_shotgun as ws
from ui_center.qt import *
from dayu_path import DayuPath
from ui_center.widgets import ui_utils
from ui_center.widgets.MFolderWidget import MFolderWidget
from ui_center.widgets.MItemViewFilterSetWidget import MItemViewFilterSetWidget
from ui_center.widgets.MJobMonitor import MJobMonitor
from ui_center.widgets.message_box import MErrorMessageBox



class MDownloadFilesDialog(QDialog):
    @ui_utils.dayu_css()
    @ui_utils.dayu_user_state()
    @ui_utils.help_action()
    def __init__(self, parent=None):
        super(MDownloadFilesDialog, self).__init__(parent)
        self.remove_info_dict = {}
        self._init_ui()
        self.bind_function()

    def _init_ui(self):
        self._resolver = DAYU.request('/resolver')
        self.setWindowTitle(self.tr('Download RS Files'))
        geo = QApplication.desktop().screenGeometry()
        self.setGeometry(geo.width() / 4, geo.height() / 4, geo.width() / 2, geo.height() / 2)
        self.title_label = QLabel(self.tr('Download RS Files'))
        self.title_label.setObjectName('title')
        self.title_label.setAlignment(Qt.AlignCenter)

        self.folder_widget = MFolderWidget()
        folder_lay = QHBoxLayout()
        folder_lay.addWidget(QLabel(self.tr('Traget Folder:')))
        folder_lay.addWidget(self.folder_widget)

        # self.dependencies_check_box = QCheckBox(self.tr('With Dependencies'))
        self.csv_check_box = QCheckBox(self.tr('Generate CSV File'))
        self.csv_check_box.setChecked(True)
        self.is_remove_sub_level_box = QCheckBox(u'去除多余层级')
        self.use_sg_client_name_check_box = QCheckBox(u'使用shotgun 镜头client字段命名')
        self.use_sg_client_name_check_box.setChecked(False)
        self.bknuse_sg_client_name_check_box = QCheckBox(u'BKN格式命名')
        self.bknuse_sg_client_name_check_box.setChecked(False)

        box_lay = QHBoxLayout()
        box_lay.addWidget(self.csv_check_box)
        # box_lay.addWidget(self.is_remove_sub_level_box)
        box_lay.addWidget(self.use_sg_client_name_check_box)
        box_lay.addWidget(self.bknuse_sg_client_name_check_box)
        box_lay.addStretch()

        self.rename_check_box = QCheckBox(self.tr('Rename:'))
        self.rename_check_box.setChecked(True)
        self.rename_line_edit = QLineEdit()
        self.rename_check_box.setChecked(False)

        resolver_tooltip = "You can rename using the following keyword tokens:<br>" \
                           "eg: yys pl_0010_comp_master_v0003<br>"
        for i in range(0, self._resolver.entry_count()):
            resolver_tooltip += '<b>%s</b> - %s<br>' % (
                self._resolver.entry_name(i), self._resolver.entry_description(i))
        self.rename_line_edit.setToolTip(resolver_tooltip)

        rename_lay = QHBoxLayout()
        rename_lay.addWidget(self.rename_check_box)
        rename_lay.addWidget(self.rename_line_edit)
        rename_lay.setContentsMargins(0, 0, 0, 0)

        self.item_view = MItemViewFilterSetWidget()
        self.item_view.enable_search()
        self.item_view.set_header_list(
            [{'name': 'Version Name', 'attr': 'name', 'searchable': True, 'checkable': True, 'width': 300},
             {'name': 'Sub level', 'attr': 'sub_level', 'searchable': True, 'width': 400},
             {'name': 'Type', 'attr': 'type', 'searchable': False, 'width': 100}])
        self.item_view.table_view.header_view.setStretchLastSection(True)
        self.result_line_edit = QLineEdit()
        self.result_line_edit.setReadOnly(True)
        self.download_button = QPushButton(self.tr('Download Now'))
        self.button_lay = QHBoxLayout()
        self.button_lay.addWidget(self.download_button)

        self.checkbox_lay = QHBoxLayout()

        self.main_lay = QVBoxLayout()
        self.main_lay.addSpacing(10)
        self.main_lay.addWidget(self.title_label)
        self.main_lay.addSpacing(10)
        self.main_lay.addLayout(folder_lay)
        self.main_lay.addLayout(rename_lay)
        self.main_lay.addLayout(box_lay)
        self.main_lay.addLayout(self.checkbox_lay)
        self.main_lay.addWidget(self.item_view)
        self.main_lay.addWidget(self.result_line_edit)
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

        self.setLayout(self.main_lay)

    def bind_function(self):
        self.item_view.sig_left_clicked.connect(self.slot_show_result)
        self.rename_check_box.stateChanged.connect(self.rename_line_edit.setEnabled)
        self.download_button.clicked.connect(self.slot_update)
        self.item_view.table_view.clicked.connect(self.change_checkbox_state)

    def setup_data(self, version_orm_list):
        '''
        更新item数据

        @param version_orm_list:
        '''
        self.result_line_edit.clear()
        DAYU.request('/refresh/all')()
        result_list = []
        for orm in version_orm_list:
            orig_folder = orm.disk_path(disk_type='publish')
            for sub_level in orm.sub_level.walk(collapse=True):
                file_type = sub_level.filename.replace(orig_folder, '').split("/")[1]
                if len(file_type) > 10:
                    file_type = "other"
                result_list.append(
                    {'name': orm.name,
                     'name_checked': 2,
                     'sub_level': sub_level.filename.replace(orig_folder, ''),
                     'type': file_type,
                     'sub_level_obj': sub_level,
                     'orm': orm})
            else:
                self.rename_line_edit.setText(
                    db.util.get_cascading_info(orm, 'cascading_info')['all_info'].get(
                        'output_naming', ''))
        self.item_view.setup_data(result_list)
        self.add_checkbox_btn()

    def get_element_info(self):
        """
        @return: {
                    u'ref': [u'ep01_6570_edt_ref_v0001', u'ep02_6110_edt_ref_v0001'],
                    u'fullres': [u'ep01_6570_plt_bgb_v0001'],
                    u'cloud': [u'ep01_6570_plt_bgb_v0001']
                 }
        """
        element_info_dict = {}
        for item in self.item_view.get_data():
            _type = item.get("type")
            name = item.get("name")
            if len(_type) > 10:
                element_info_dict["other"] = [name]

            else:
                if _type in element_info_dict:
                    element_info_dict[_type].append(name)
                else:
                    element_info_dict[_type] = [name]

        return element_info_dict

    def add_checkbox_btn(self):
        """
        获取checkbox的类型，添加按钮
        @return:
        """
        element_info_dict = self.get_element_info()
        element_type_list = element_info_dict.keys()

        count_index = len(element_type_list)

        for n in range(count_index):
            element_type = QCheckBox(element_type_list[n])
            element_type.setChecked(True)
            element_type.setCheckState(Qt.Checked)
            element_type.stateChanged.connect(self.change_tableview_state)
            self.checkbox_lay.addWidget(element_type)

    def change_tableview_state(self, state):
        """
        Update tableview status.

        @param state: <int>
        """
        text = self.sender().text()
        if state == 0:
            for item in self.item_view.get_data():
                if text == item.get("type"):
                    item["name_checked"] = 0
            self.item_view.setup_data(self.item_view.get_data())
        else:
            for item in self.item_view.get_data():
                if text == item.get("type"):
                    item["name_checked"] = 2
            self.item_view.setup_data(self.item_view.get_data())

    def get_change_checkbox_state(self, type_key):
        checked_list = []
        for item in self.item_view.get_data():
            if item["type"] == type_key:
                checked_list.append(item["name_checked"])
        return checked_list

    def checkbox_state(self, type_key, state):
        for i in range(self.checkbox_lay.count()):
            widget = self.checkbox_lay.itemAt(i).widget()
            if widget.text() == type_key:
                widget.setChecked(state)

    def change_checkbox_state(self, index):
        """
        Update tableview status
        @param index: <QModelIndex>
        """
        row = index.row()
        type_column = 2
        folder_column = 1
        if not index.column() == 0:
            return
        state = self.item_view.table_view.model().index(row, 0).data( )
        _type_key = self.item_view.table_view.model().index(row, type_column).data()
        _type_value = self.item_view.table_view.model().index(row, folder_column).data()

        # 首先判断勾选状态
        if state == 0:
            get_unchecked_list = self.get_change_checkbox_state(_type_key)
            checked_state = not all(num == 0 for num in get_unchecked_list)
            self.checkbox_state(_type_key, checked_state)

        else:
            get_checked_list = self.get_change_checkbox_state(_type_key)
            checked_state = all(num == 2 for num in get_checked_list)
            self.checkbox_state(_type_key, checked_state)

    @Slot()
    def slot_update(self):
        if not self.folder_widget.get_folder():
            msg = MErrorMessageBox(parent=self, msg=self.tr('Please give me the target folder!'))
            msg.exec_()
            self.folder_widget.line_edit.setFocus(Qt.MouseFocusReason)
            return
        if not os.path.isdir(self.folder_widget.get_folder()):
            msg = MErrorMessageBox(parent=self, msg=self.tr('The target folder not exist!'))
            msg.exec_()
            return
        csv_data_dict = {}
        monitor = MJobMonitor(parent=self)
        for data_obj in self.item_view.get_data():
            if not ui_utils.get_obj_value(data_obj, 'name_checked'):
                continue
            orm = ui_utils.get_obj_value(data_obj, 'orm')
            key_name = u'{}-{}'.format(orm.top.name, orm.meaning)
            if key_name not in csv_data_dict.keys():
                reg_obj, header_list = db.util.get_name_pattern(orm.top.name, orm.meaning)
                csv_data_dict[key_name] = [header_list + [u'FOLDER_PATH']]

            # 以上内容是写入csv的数据

            from_list = []
            to_list = []
            sub_level_obj = ui_utils.get_obj_value(data_obj, 'sub_level_obj')
            try:
                new_file_obj = db.disk_path.DiskPath(self._resolve(data_obj))
            except Exception as e:
                import traceback
                msg = MErrorMessageBox(parent=self,
                                       msg=u'重命名失败，请看详细信息',
                                       detail=traceback.format_exc())
                msg.exec_()
                return
            data_list = csv_data_dict.get(key_name)
            header_list = data_list[0]
            data_list.append(
                [orm.find_meaning(meaning).name.split('_')[-1] for meaning in header_list[:-1]] +
                [new_file_obj.parent])

            if sub_level_obj.frames:
                for frame in sub_level_obj.frames:
                    from_list.append(sub_level_obj.filename.restore_pattern(frame))
                    to_list.append(new_file_obj.restore_pattern(frame))
            else:
                from_list.append(sub_level_obj.filename)
                to_list.append(new_file_obj)
            monitor.add_job(
                job_center.util.make_disk_copy_job(from_list=from_list, to_list=to_list))

        if self.csv_check_box.isChecked():
            self._write_to_csv(csv_data_dict)
        monitor.exec_()

    def _resolve(self, data_obj):
        sg = ws.MyShotgun()
        name_conventions = {'comp': 'cmp', 'roto': 'rto', 'paint': 'pnt', 'ldev': 'ldv'}
        orm = ui_utils.get_obj_value(data_obj, 'orm')
        target_obj = self.folder_widget.get_folder()
        sub_level_obj = ui_utils.get_obj_value(data_obj, 'sub_level_obj')

        filename_ = DayuPath(sub_level_obj.filename)
        original_filename = filename_.name.split(".")[0]
        # 修改文件名字和文件夹名字ep01_1270_comp_compositing_v0012 为 ep011270_cmp_rr_v012
        # 此处不涉及资产（但是也写了）
        # 根据sg的信息，根据任务类型修改命名
        sequence_group = orm.find_meaning('SEQUENCE_GROUP').name
        if sequence_group == 'asset':
            asset_id = orm.find_meaning('ASSET').cloud_id
            asset_info = sg.find_one('Asset', [['id', 'is', asset_id]],
                                     ['sg_note_1'])
            footage = original_filename.split('_')
            version_num = footage[4].replace('v0', 'v')

            note_1 = asset_info.get('sg_note_1')
            if not note_1:
                folder_name = '_'.join([footage[1], footage[2], version_num])
            else:
                folder_name = '_'.join([footage[1], footage[2], note_1, version_num])
        else:
            shot_id = orm.find_meaning('SHOT').cloud_id
            shot_info = sg.find_one('Shot', [['id', 'is', shot_id]],
                                    ['sg_lens'])
            len_type = shot_info.get('sg_lens')

            footage = original_filename.split('_')
            shot_name = footage[0] + footage[1]
            if footage[2] in name_conventions:
                step = name_conventions[footage[2]]
            else:
                step = footage[2]
            version_num = footage[4].replace('v0', 'v')
            if not len_type:
                folder_name = '_'.join([shot_name, step, version_num])
            else:
                folder_name = '_'.join([shot_name, step, len_type, version_num])

        result = DayuPath(target_obj).child(folder_name, '{}.%04d{}'.format(folder_name, DayuPath(filename_).ext))

        # 如果勾选了去除额外层级  则删除掉中间多余层级
        if self.is_remove_sub_level_box.isChecked():
            filename_ = DayuPath(sub_level_obj.filename)
            if filename_.ext == '.mov':
                result = DayuPath(target_obj).child(filename_.name)
            else:
                result = DayuPath(target_obj).child(orm.name, filename_.name)

        # 如果用户勾选了使用shotgun shot client字段得命名，则获取shotgun命名进行输出
        if self.use_sg_client_name_check_box.isChecked():
            sg = ws.MyShotgun()
            filename_ = DayuPath(sub_level_obj.filename)
            shot_id = orm.find_meaning('SHOT').cloud_id
            # NOTE: 新增shot的project字段
            shot = sg.find_one('Shot', [['id', 'is', shot_id]], ['sg_client_name', 'project'])

            new_folder_name = shot.get('sg_client_name') + '_{}'.format(orm.name.split('_')[-1])
            client_name = new_folder_name

            if filename_.ext == '.mov':
                result = DayuPath(target_obj).child('{}{}'.format(new_folder_name, DayuPath(filename_).ext))
            else:
                result = DayuPath(target_obj).child(new_folder_name, '{}.%04d{}'.format(client_name, DayuPath(filename_).ext))

        # 如果如果用户勾选了使用bkn命名规则命名，则获取shotgun命名后修改格式进行输出
        if self.bknuse_sg_client_name_check_box.isChecked():
            sg = ws.MyShotgun()
            filename_ = DayuPath(sub_level_obj.filename)
            shot_id = orm.find_meaning('SHOT').cloud_id
            shot = sg.find_one('Shot', [['id', 'is', shot_id]], ['sg_client_name'])
            client_name = shot.get('sg_client_name') + '_{}'.format(orm.name.split('_')[-1])
            step_name = orm.name.split('_')[-3]
            version_str = orm.name.split('_')[-1]
            new_version_str = ''
            for i in range(0, len(version_str)):
                if i != 1:
                    new_version_str = new_version_str + version_str[i]
            new_name = 'BKN_' + shot.get('sg_client_name').replace('E', '').replace('S', '').replace('org', step_name)\
                .replace('_v001', '') + '_{}'.format(new_version_str)
            if filename_.ext == '.mov':
                result = DayuPath(target_obj).child('{}{}'.format(new_name, DayuPath(filename_).ext))
            else:
                result = DayuPath(target_obj).child(new_name, '{}.%04d{}'.format(new_name, DayuPath(filename_).ext))

        if self.rename_check_box.isChecked() and self.rename_line_edit.text():
            new_name = self._resolver.resolve(orm, self.rename_line_edit.text())
            result = result.replace(orm.name, new_name)

        return result

    @Slot(QModelIndex)
    def slot_show_result(self, index):
        data_obj = index.internalPointer()
        try:
            self.result_line_edit.setText(self._resolve(data_obj))
        except Exception as e:
            self.result_line_edit.setText(str(e))

    def _write_to_csv(self, csv_data_dict):
        for key, data_list in csv_data_dict.items():
            file_path = os.path.join(self.folder_widget.get_folder(),
                                     '{}-{}.csv'.format(
                                         dt.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), key))
            with open(file_path, 'wb') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(data_list)


if __name__ == '__main__':
    import sys
    import db
    import db.util
    item_list = [1178336596426887832, 1175872722768632178, 1850969052474706363, 1850969627035634035, 1854500664374138269]
    item_list2 = [1850969052474706363, 1850969627035634035, 1854500664374138269]
    sess = db.get_session()
    app = QApplication(sys.argv)
    test = MDownloadFilesDialog()
    test.setup_data([sess.query(db.util.get_class('file')).get(i)
                     for i in item_list
                     ])
    test.show()
    sys.exit(app.exec_())
