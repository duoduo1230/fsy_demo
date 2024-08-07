#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from dayu_widgets import dayu_theme
from pprint import pprint


# def test(version, y):
#     print(version)
#     print(y)
#     version = int(version.split("_")[1])
#     if version <= 1010:
#         return dayu_theme.error_color
#     else:
#         return dayu_theme.success_color

def score_color(score, y):
    if score < 60:
        return dayu_theme.error_color
    elif score < 80:
        return dayu_theme.warning_color
    elif score >= 90:
        return dayu_theme.success_color
    return dayu_theme.info_color


header_list = [
    {
        "label": " Node Name",
        "key": "node_name",
        "searchable": True,
        "checkable": True,
        "width": 100,
    },
    {
        "label": "Score",
        "key": "score",
        "width": 60,
        "bg_color": score_color
    },
    {
        "label": "Current Version",
        "key": "current_version",
        "searchable": True,
        "width": 140,
    },
    {
        "label": "Type",
        "key": "type",
        "width": 60,
        "searchable": True,
    },
    {
        "label": "File Name",
        "key": "file_name",
        "width": 200,
        "searchable": True,
    },
    {
        "label": "File Type",
        "key": "file_type",
        "width": 80,
        "searchable": True,
    },
    {
        "label": "Original Range",
        "key": "original_range",
        "width": 120,
        "searchable": True,
    }
]

# UI中填写数据
tree_data_list = [
    {'node_name': 'Read1', 'current_version': 'ep06_1060_lgt_v0001', 'score': 100, 'type': 'lgt', 'file_name': 'ep06_1060_lgt_test_beauty_a_v0001', 'file_type': 'exr', 'original_range': '1001_1010'},
    {'node_name': 'Read2', 'current_version': 'ep06_1060_lgt_v0001', 'score': 100, 'type': 'lgt', 'file_name': 'ep06_1060_lgt_test_beauty_b_v0001', 'file_type': 'exr', 'original_range': '1001_1010'},
    {'node_name': 'Read3', 'current_version': 'ep06_1060_lgt_v0001', 'score': 100, 'type': 'lgt', 'file_name': 'ep06_1060_lgt_test_beauty_c_v0001', 'file_type': 'exr', 'original_range': '1001_1010'},
    {'node_name': 'Read4', 'current_version': 'ep06_1060_lgt_v0001', 'score': 100, 'type': 'lgt', 'file_name': 'ep06_1060_lgt_test_beauty_d_v0001', 'file_type': 'exr', 'original_range': '1001_1010'},
    {'node_name': 'Read5', 'current_version': 'ep06_1010_edt_v0001', 'score': 100, 'type': 'edt', 'file_name': 'ep06_1010_edt_v0001', 'file_type': 'mov', 'original_range': '1_141'},
    {'node_name': 'Read6', 'current_version': 'ep06_1010_plt_v0001', 'score': 100, 'type': 'plt', 'file_name': 'ep06_1010_plt_v0001', 'file_type': 'mov', 'original_range': '1_141'}]


# 工程内部的路径列表
read_node_path_list = [
    'D:/temp/yyy/updata/ep06_1060/element/lgt/ep06_1060_lgt_v0001/beauty_c/ep06_1060_lgt_test_beauty_c_v0001.%04d.exr',
    'D:/temp/yyy/updata/ep06_1060/element/lgt/ep06_1060_lgt_v0001/beauty_d/ep06_1060_lgt_test_beauty_d_v0001.%04d.exr',
    'D:/temp/yyy/updata/ep06_1060/element/lgt/ep06_1060_lgt_v0001/beauty_b/ep06_1060_lgt_test_beauty_b_v0001.%04d.exr',
    'D:/temp/yyy/updata/ep06_1060/element/lgt/ep06_1060_lgt_v0001/beauty_a/ep06_1060_lgt_test_beauty_a_v0001.%04d.exr',
    'D:/temp/yyy/updata/ep06_1060/element/plt/ep06_1010_plt_v0001/ep06_1010_plt_v0001.mov',
    'D:/temp/yyy/updata/ep06_1060/element/edt/ep06_1010_edt_v0001/ep06_1010_edt_v0001.mov']

# 存在的新版本列表
latest_version_list = ['D:/temp/yyy/updata/ep06_1060/element/plt/ep06_1010_plt_v0002/ep06_1010_plt_v0002.mov',
                       'D:/temp/yyy/updata/ep06_1060/element/edt/ep06_1010_edt_v0002/ep06_1010_edt_v0002.mov',]


# 在此处完成了数据颜色的修改
for new_version in latest_version_list:
    file_name = new_version.split('/')[-1].split('_v')[0]
    for read_node in read_node_path_list:
        old_name = read_node.split('/')[-1].split('_v')[0]
        if file_name == old_name:
            print(file_name)
            for info in tree_data_list:
                if file_name in info['file_name']:
                    info['score'] = 0




if __name__ == "__main__":
    pass
    pprint(tree_data_list)
    print(len(tree_data_list))

    import sys
    sys.path.append(r'D:\My_code\fsy_demo\ui_center3\updata_widget')
    sys.path.append(r"D:\My_code\fsy_demo\ui_center3\updata_widget")

    import nuke
    import importlib


    import get_read_node_info
    importlib.reload(get_read_node_info)
    get_read_node_info.main()

    import launch_updata_manager



    ROOT_PATH = r'D:/temp/yyy/updata/ep06_1060/element/'



    tree_data_list = get_read_node_info.get_view_data()

    importlib.reload(launch_updata_manager)
    widget = launch_updata_manager.UpdataManager()

    # UI中填入由get_read_node_info 获取到的信息
    widget.data_tree_widget.set_header_data(get_read_node_info.header_list)
    widget.data_tree_widget.update_data(tree_data_list)
    widget.show()

