#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan Shiyuan
# Date  : 2023.12.12


# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from collections import Counter

# task 窗口
header_list = [
    {
        "label": "Project",
        "key": "project",
        "searchable": True,
        "width": 80,
    },
    {
        "label": "Shot/Asset",
        "key": "shot asset",
        "searchable": True,
        "width": 100,
    },
    {
        "label": "Task Name",
        "key": "task name",
        "searchable": True,
        "width": 100,
    },
    {
        "label": "Pipeline Step",
        "key": "pipeline step",
        "searchable": True,
        "width": 80,
    },
    {
        "label": "Status",
        "key": "status",
        "searchable": True,
        "width": 60,
    },
    {
        "label": "Assigned To",
        "key": "assigned to",
        "searchable": True,
        "width": 100,
    },
    {
        "label": "Start",
        "key": "start",
        "searchable": True,
        "width": 100,
    },
    {
        "label": "End",
        "key": "end",
        "searchable": True,
        "width": 100,
    },
    {
        "label": "First Look",
        "key": "first look",
        "searchable": True,
        "width": 80,
    },
    {
        "label": "Bid",
        "key": "bid",
        "searchable": True,
        "width": 80,
    },
    {
        "label": "Time Logged",
        "key": "time logged",
        "searchable": True,
        "width": 80,
    },
    {
        "label": "VFX Node",
        "key": "vfx node",
        "searchable": True,
        "width": 80,
    },
    {
        "label": "Retake Bid",
        "key": "retake bid",
        "searchable": True,
        "width": 80,
    },
    {
        "label": "Artist Note",
        "key": "artist note",
        "searchable": True,
        "width": 100,
    },

]
data_list = [
    {
        "project": "wyd",
        "shot asset": "klww",
        "task name": "mod",
        "pipeline step": "Modeling",
        "status": "ip",
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
        "shot asset": "yu",
        "task name": "sfr",
        "pipeline step": "Modeling",
        "status": "ip",
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
        "shot asset": "test_0020",
        "task name": "comp",
        "pipeline step": "comp",
        "status": "omt",
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
        "shot asset": "test_0020",
        "task name": "pcomp",
        "pipeline step": "pcomp",
        "status": "omt",
        "assigned to": "duoduo",
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
        "shot asset": "test_0020",
        "task name": "ani",
        "pipeline step": "ani",
        "status": "omt",
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
    {
        "project": "tdtest",
        "shot asset": "ep_0020",
        "task name": "ani",
        "pipeline step": "ani",
        "status": "pub",
        "assigned to": "rrfz",
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
        "shot asset": "sc_0030",
        "task name": "rig",
        "pipeline step": "rig",
        "status": "hld",
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
    {
        "project": "qaz",
        "shot asset": "ep_0040",
        "task name": "comp",
        "pipeline step": "comp",
        "status": "fin",
        "assigned to": "mm",
        "start": "2023-04-01",
        "end": "2023-11-01",
        "first look": "4.00 hrs",
        "bid": "6.00 hrs",
        "time logged": "6.00 hrs",
        "vfx node": "",
        "retake bid": "7.00 hrs",
        "artist note": "note"
    },
    {
        "project": "edc",
        "shot asset": "ep_0020",
        "task name": "ani",
        "pipeline step": "ani",
        "status": "pub",
        "assigned to": "rrfz",
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
        "project": "yhg",
        "shot asset": "ep_0020",
        "task name": "ani",
        "pipeline step": "ani",
        "status": "pub",
        "assigned to": "rrfz",
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
        "project": "wsx",
        "shot asset": "ep_0070",
        "task name": "mm",
        "pipeline step": "mm",
        "status": "rdy",
        "assigned to": "fanshiyuan",
        "start": "2023-03-01",
        "end": "2023-10-01",
        "first look": "1.00 hrs",
        "bid": "6.00 hrs",
        "time logged": "3.00 hrs",
        "vfx node": "",
        "retake bid": "5.00 hrs",
        "artist note": "note"
    },
    {
        "project": "edc",
        "shot asset": "ep_0050",
        "task name": "efx",
        "pipeline step": "efx",
        "status": "wtg",
        "assigned to": "fanshiyuan",
        "start": "2023-02-01",
        "end": "2023-09-01",
        "first look": "6.00 hrs",
        "bid": "2.00 hrs",
        "time logged": "9.00 hrs",
        "vfx node": "",
        "retake bid": "8.00 hrs",
        "artist note": "note"
    },
]

# tab 窗口
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
work_version_data_list = [
]

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
    filter_head_list, filter_data_list = filter_data_create("project", data_list)
    # print(filter_head_list)
    print(filter_data_list)