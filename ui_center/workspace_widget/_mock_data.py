#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan Shiyuan
# Date  : 2023.12.12


# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from collections import Counter
from dayu_widgets import dayu_theme
import datetime

# 获取当前日期
today = datetime.date.today()


def score_color(time, y):
    expect = datetime.date.fromisoformat(time)
    if expect < today:
        return dayu_theme.error_color

    return dayu_theme.info_color


# task 窗口
header_list = [
    {
        "label": "Project",
        "key": "project",
        "searchable": True,
        "width": 20,
    },
    {
        "label": "Sequence Type",
        "key": "sequence type",
        "searchable": True,
        "width": 20,
    },
    {
        "label": "Shot/Asset",
        "key": "shot asset",
        "searchable": True,
        "width": 40,
    },
    {
        "label": "Pipeline Step",
        "key": "pipeline step",
        "searchable": True,
        "width": 20,
    },
    {
        "label": "State",
        "key": "state",
        "searchable": True,
        "icon": lambda x, y: (
            "{}_{}.png".format("state", x.lower()),
            getattr(dayu_theme, x.lower() + "_color"),
        ),
        "width": 20,
    },
    {
        "label": "Assigned To",
        "key": "assigned to",
        "searchable": True,
        "width": 80,
    },
    {
        "label": "Start",
        "key": "start",
        "searchable": True,
        "width": 40,
    },
    {
        "label": "End",
        "key": "end",
        "searchable": True,
        "width": 40,
        "bg_color": score_color,
        "color": "#fff"
    },
    {
        "label": "First Look",
        "key": "first look",
        "searchable": True,
        "width": 30,
    },
    {
        "label": "Bid",
        "key": "bid",
        "searchable": True,
        "width": 30,
    },
    {
        "label": "Time Logged",
        "key": "time logged",
        "searchable": True,
        "width": 30,
    },
    {
        "label": "VFX Node",
        "key": "vfx node",
        "searchable": True,
        "width": 30,
    },
    {
        "label": "Retake Bid",
        "key": "retake bid",
        "searchable": True,
        "width": 30,
    },
    {
        "label": "Artist Note",
        "key": "artist note",
        "searchable": True,
        "width": 30,
    },

]
data_list = [
    {
        "project": "wyd",
        "sequence type": "chr",
        "shot asset": "chr_klww",
        "pipeline step": "Mod",
        "state": "ip",
        "assigned to": "fanshiyuan",
        "start": "2023-05-01",
        "end": "2023-10-01",
        "first look": "8.00 hrs",
        "bid": "8.00 hrs",
        "time logged":"4.00 hrs",
        "vfx node": "",
        "retake bid": "0.00 hrs",
        "artist note": "note"
    },
    {
        "project": "wyd",
        "sequence type": "chr",
        "shot asset": "chr_yu",
        "pipeline step": "Mod",
        "state": "ip",
        "assigned to": "fanshiyuan",
        "start": "2023-05-01",
        "end": "2023-10-01",
        "first look": "8.00 hrs",
        "bid": "8.00 hrs",
        "time logged": "4.00 hrs",
        "vfx node": "",
        "retake bid": "0.00 hrs",
        "artist note": "note"
    },
    {
        "project": "wyd",
        "sequence type": "ep01",
        "shot asset": "ep01_0080",
        "pipeline step": "Ani",
        "state": "ip",
        "assigned to": "fanshiyuan",
        "start": "2023-05-01",
        "end": "2023-10-01",
        "first look": "8.00 hrs",
        "bid": "8.00 hrs",
        "time logged": "4.00 hrs",
        "vfx node": "",
        "retake bid": "0.00 hrs",
        "artist note": "note"
    },
    {
        "project": "tdtest",
        "sequence type": "test",
        "shot asset": "test_0020",
        "pipeline step": "Comp",
        "state": "omt",
        "assigned to": "fanshiyuan, duoudo",
        "start": "2023-06-01",
        "end": "2023-08-01",
        "first look": "6.00 hrs",
        "bid": "6.00 hrs",
        "time logged": "2.00 hrs",
        "vfx node": "",
        "retake bid": "2.00 hrs",
        "artist note": "note"
    },
    {
        "project": "tdtest",
        "sequence type": "ep02",
        "shot asset": "ep02_0010",
        "pipeline step": "Pcomp",
        "state": "omt",
        "assigned to": "fanshiyuan",
        "start": "2023-06-01",
        "end": "2023-08-01",
        "first look": "6.00 hrs",
        "bid": "6.00 hrs",
        "time logged": "2.00 hrs",
        "vfx node": "",
        "retake bid": "2.00 hrs",
        "artist note": "note"
    },
    {
        "project": "tdtest",
        "sequence type": "ep02",
        "shot asset": "ep02_0020",
        "pipeline step": "Ani",
        "state": "omt",
        "assigned to": "fanshiyuan, huahua",
        "start": "2023-06-01",
        "end": "2023-08-01",
        "first look": "6.00 hrs",
        "bid": "6.00 hrs",
        "time logged": "2.00 hrs",
        "vfx node": "",
        "retake bid": "2.00 hrs",
        "artist note": "note"
    },
    {
        "project": "tdtest",
        "sequence type": "ep01",
        "shot asset": "ep01_0040",
        "pipeline step": "Ani",
        "state": "fin",
        "assigned to": "fanshiyuan, duoudo",
        "start": "2023-06-01",
        "end": "2023-08-01",
        "first look": "6.00 hrs",
        "bid": "6.00 hrs",
        "time logged": "2.00 hrs",
        "vfx node": "",
        "retake bid": "2.00 hrs",
        "artist note": "note"
    },
    {
        "project": "tdtest",
        "sequence type": "ep01",
        "shot asset": "ep01_0030",
        "pipeline step": "Lgt",
        "state": "hld",
        "assigned to": "huahua",
        "start": "2023-06-01",
        "end": "2023-08-01",
        "first look": "6.00 hrs",
        "bid": "6.00 hrs",
        "time logged": "2.00 hrs",
        "vfx node": "",
        "retake bid": "2.00 hrs",
        "artist note": "note"
    },
]

# tab  work  窗口
work_resources_header_list = [
    {
        "label": "Resources Name",
        "key": "resources name",
        "width": 200,
    },
]
work_resources_data_list = [
]

work_version_header_list = [
    {
        "label": "Version Name",
        "key": "version name",
        "width": 200,
    },
    {
        "label": "Comment",
        "key": "comment",
        "width": 100,
    },
    {
        "label": "Created Data",
        "key": "created data",
        "width": 100,
    },
]
work_version_data_list = [
]

work_snapshots_header_list = [
    {
        "label": "File Name",
        "key": "file name",
        "width": 200,
    },
    {
        "label": "Comment",
        "key": "comment",
        "width": 100,
    },
    {
        "label": "Created Data",
        "key": "created data",
        "width": 100,
    },
]
work_snapshots_data_list = [
]

# tab  cloud file  窗口
resources_file_header_list = [
    {
        "label": "Name",
        "key": "name",
        "width": 200,
    },
    {
        "label": "Comment",
        "key": "comment",
        "width": 100,
    },
    {
        "label": "Created By",
        "key": "created by",
        "width": 100,
    },
    {
        "label": "Created At",
        "key": "created at",
        "width": 200,
    },
]
resources_file_data_list = [
]

version_header_list = [
    {
        "label": "Name",
        "key": "name",
        "width": 200,
    },
    {
        "label": "Comment",
        "key": "comment",
        "width": 100,
    },
    {
        "label": "Created By",
        "key": "created by",
        "width": 100,
    },
    {
        "label": "Created At",
        "key": "created at",
        "width": 200,
    },
]
version_data_list = [
]

# tab  metadata  窗口
metadata_header_list = [
    {
        "label": "Metadata Name",
        "key": "metadata name",
        "width": 300,
    },
    {
        "label": "Metadata Type",
        "key": "metadata type",
        "width": 300,
    },
    {
        "label": "Comment",
        "key": "comment",
        "width": 150,
    },
]
metadata_data_list = [
]

# tab  shot/asset  窗口
name_header_list = [
    {
        "label": "Name",
        "key": "name",
        "searchable": True,
        "width": 80,
    },
]
name_data_list = [
]




# filter 数据获取
filter_list = []
for label in header_list:
    filter_list.append(label.get("key"))

def filter_data_create(filter_name, data):
    filter_head_list = [
    {
        "label": filter_name.title(),
        "key": filter_name,
        "checkable": True,
        "searchable": True,
        "width": 200,
        "font": lambda x, y: {"underline": True},
    },
    {
        "label": "Count",
        "key": "count",
        "searchable": True,
        "selectable": True,

    },
    ]
    pro_list = []
    for data in data:
        pro_list.append(data.get(filter_name))

    filter_data = dict(Counter(pro_list))

    filter_data_list = []

    for key, value in filter_data.items():
        item_dict = {filter_name: key, "count": value}
        filter_data_list.append(item_dict)

    return filter_head_list, filter_data_list


if __name__ == "__main__":
    filter_head_list, filter_data_list = filter_data_create("status", data_list)
    # print(data_list)
    # print(len(data_list))
    # for i in data_list:
    #     print(i)
    # print(filter_head_list)
    print(filter_data_list)