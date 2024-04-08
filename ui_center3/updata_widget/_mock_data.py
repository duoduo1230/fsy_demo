#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Fan Shiyuan
# Date  : 2023.12.12

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from dayu_widgets import dayu_theme


header_list = [
    {
        "label": "Node Name",
        "key": "node name",
        "checkable": True,
        "searchable": True,
        "width": 180,
    },
    {
        "label": "Current Versior",
        "key": "current version",
        "searchable": True,
        "width": 180,
    },
    {
        "label": "Step",
        "key": "step",
        "width": 50,
        "searchable": True,
        "icon": lambda x, y: (
            "{}-{}.png".format("step", x.lower()),
            getattr(dayu_theme, x.lower() + "_color"),
        ),

    },
    {
        "label": "Current Level",
        "key": "current level",
        "searchable": True,
        "width": 100,
    },
    {
        "label": "Target Version",
        "key": "target version",
        "searchable": True,
        "width": 180,
    },
    {
        "label": "Target Level",
        "key": "target level",
        "searchable": True,
        "width": 100,
    },
    {
        "label": "Target Version Comment",
        "key": "target version comment",
        "searchable": True,
        "width": 300,
    },

]

tree_data_list = [
    {
        "node name": "ep06_0750_ani_layout",
        "current version": "ep06_0750_ani_layout_v0002",
        "step": "ani",
        "current level": "scene/psne",
        "target version": "ep06_0750_ani_layout_v0003",
        "target level": "scene/psne",
        "target version comment": "镜头描述",
        "children": [
            {
                "node name": "prp_luoshen_srf",
                "current version": "prp_luoshen_srf_v0002",
                "step": "srf",
                "current level": "mat/mb",
                "target version": "prp_luoshen_srf_v0003",
                "target level": "mat/mb",
                "target version comment": "描述描述",
            },
            {
                "node name": "prp_ice_srf",
                "current version": "prp_ice_srf_v0002",
                "step": "srf",
                "current level": "mat/mb",
                "target version": "prp_ice_srf_v0003",
                "target level": "mat/mb",
                "target version comment": "描述描述",
            },
        ],
    },
    {
        "node name": "ep06_0750_ani_layout",
        "current version": "ep06_0750_ani_layout_v0002",
        "step": "ani",
        "current level": "scene/psne",
        "target version": "ep06_0750_ani_layout_v0003",
        "target level": "scene/psne",
        "target version comment": "镜头描述",
    },
]