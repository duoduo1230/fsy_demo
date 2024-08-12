import os
import re
import nuke
from pprint import pprint
from dayu_widgets import dayu_theme


def set_version_color(version, y):
    version_file = [path for path in get_read_files() if version in path]
    if not version_file:
        return
    version_file = version_file[0]
    is_new_version = check_latest_version_exists(version_file)
    # 有新版本标为红色
    if is_new_version:
        return dayu_theme.error_color
    # 否则标为绿色
    else:
        return dayu_theme.success_color

header_list = [
    {
        "label": " Node Name",
        "key": "node_name",
        "searchable": True,
        "checkable": True,
        "width": 100,
    },
    {
        "label": "Current Version",
        "key": "current_version",
        "searchable": True,
        "width": 300,
        "bg_color": set_version_color
    },
    {
        "label": "Type",
        "key": "type",
        "width": 30,
        "searchable": True,
    },
    {
        "label": "File Name",
        "key": "file_name",
        "width": 300,
        "searchable": True,
    },
    {
        "label": "File Type",
        "key": "file_type",
        "width": 40,
        "searchable": True,
    },
    {
        "label": "Original Range",
        "key": "original_range",
        "width": 100,
        "searchable": True,
    }
]

def get_node_by_type(node_type="Read"):
    return nuke.allNodes(node_type)

def get_read_files():
    return [i["file"].value() for i in get_node_by_type()]

def get_view_data():
    """
    得到填写到ui的信息
    其中file_path 未在ui中展现
    """
    tree_data_list = []
    read_node_data =  get_node_by_type()
    for rn in read_node_data:
        read_node_name = rn['name'].value()
        file_path = rn['file'].value()
        first_frame = str(rn['origfirst'].value())
        last_frame = str(rn['origlast'].value())
        original_range = "_".join([first_frame, last_frame])
        file_path_split = file_path.split('/')
        _type = file_path_split[6]
        file_name = file_path_split[-1].split('.')[0]
        file_type = file_path_split[-1].split('.')[-1]
        current_version = file_path_split[7]

        read_node_dict = {
            'node_name': read_node_name,
            'current_version': current_version,
            'type': _type,
            'file_name': file_name,
            'file_type': file_type,
            'original_range': original_range,
            'file_path': file_path
        }
        tree_data_list.append(read_node_dict)

    return tree_data_list


def check_latest_version_exists(read_node_file):
    """
    通过nuke中的文件名，得到升级后的版本名字
    返回存在的版本路径
    """
    read_node_file = read_node_file.replace("\\", "/")
    version = re.findall(r"_v(\d{4})/", read_node_file)[0]
    old_version = f"v{int(version):04d}"
    new_version = f"v{int(version) + 1:04d}"
    latest_version_path = read_node_file.replace(old_version, new_version)
    # 判断文件是否存在 存在即为有升级的版本
    if os.path.exists(latest_version_path):
        return latest_version_path


if __name__ == "__main__":
    ROOT_PATH = r'D:/temp/yyy/updata/ep06_1060/element/'
    read_node_path_list = get_read_files()
    upgrade_file_list = check_latest_version_exists(read_node_path_list)
    print(upgrade_file_list)

