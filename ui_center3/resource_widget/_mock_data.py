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
        "label": "Project",
        "key": "project",
        "checkable": False,
        "searchable": False,
        "width": 400,
        "font": lambda x, y: {"underline": False},
        "icon": "app-batch_create_element_wizard.png",
    },
]
data_list = [
    {
        "project": "ep01_0010_comp_master_v0001",
    },
    {
        "project": "ep01_0010_comp_pcomp_v0003",
    },
    {
        "project": "New Resource",
    },
]

config_list = ["MZH_slate", "WYD_slate", "QZSD_slate", "TDTEST_slate"]

comment_preset = '过程版\n修改反馈:\n1-\n2-\n3-\n还要修改:\n1-\n2-\n3-\n使用Lightning-Publish版本:\nv000\n使用Effects-Publish版本:\nv000\n使用MattePainting-Publish版本:\nv000'


def result_color(result, y):
    """
    修改 tabel view 的颜色
    """
    if result == 'PASSED':
        return dayu_theme.success_color
    elif result == "FAILED":
        return dayu_theme.error_color
    return dayu_theme.info_color


qc_header_list = [
    {
        "label": "QC Item",
        "key": "item",
        "width": 700,
    },
    {
        "label": "Result",
        "key": "result",
        "width": 300,
        "bg_color": result_color,
    },
]
qc_data_list = [
    {
        "item": "prevent from publishing pcomp without ren",
        "result": "IDLE",
    },
    {
        "item": "Validate File Node path",
        "result": "PASSED",
    },
    {
        "item": "Validate File Node path",
        "result": "FAILED",
    },
]

houdini_node_header_list = [
    {
        "label": "Name",
        "key": "name",
        "width": 200,
        "font": lambda x, y: {"underline": True},
    },
]

houdini_node_data_list = [
    {
        "name": "Node1",
    },
]

render_resource_header_list = [
    {
        "label": "File Name",
        "key": "file name",
        "checkable": True,
        "searchable": True,
        "width": 300,
    },
    {
        "label": "Engine",
        "key": "engine",
        "searchable": True,
        "width": 40,
    },
    {
        "label": "Layer",
        "key": "layer",
        "searchable": True,
        "width": 40,
    },
    {
        "label": "Pass",
        "key": "pass",
        "searchable": True,
        "width": 60,
    },
    {
        "label": "Folder",
        "key": "folder",
        "searchable": True,
        "width": 200,
    },
    {
        "label": "Frame Range",
        "key": "frame range",
        "searchable": True,
        "width": 80,
    },
    {
        "label": "Frame Count",
        "key": "frame count",
        "searchable": True,
        "width": 40,
    },
    ]

# render_resource_data_list = [
#     {'folder': 'D:/11/arnold\\beauty', 'file name': 'ep15_3020_ren_prp_prp_arnold_beauty_v0001.%04d.exr',
#      'engine': 'arnold', 'layer': 'beauty', 'pass': 'v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}},
#     {'folder': 'D:/11/arnold\\crypto_asset', 'file name': 'ep15_3020_ren_prp_prp_arnold_crypto_asset_v0001.%04d.exr',
#      'engine': 'arnold', 'layer': 'crypto', 'pass': 'asset_v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}}, {'folder': 'D:/11/arnold\\crypto_material',
#                                                        'file name': 'ep15_3020_ren_prp_prp_arnold_crypto_material_v0001.%04d.exr',
#                                                        'engine': 'arnold', 'layer': 'crypto', 'pass': 'material_v0001',
#                                                        'frame range': '1001_1030', 'frame count': 30,
#                                                        '_parent': {'name': 'root', 'children': [...]}},
#     {'folder': 'D:/11/arnold\\crypto_object', 'file name': 'ep15_3020_ren_prp_prp_arnold_crypto_object_v0001.%04d.exr',
#      'engine': 'arnold', 'layer': 'crypto', 'pass': 'object_v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}}, {'folder': 'D:/11/arnold\\diffuse_albedo',
#                                                        'file name': 'ep15_3020_ren_prp_prp_arnold_diffuse_albedo_v0001.%04d.exr',
#                                                        'engine': 'arnold', 'layer': 'diffuse', 'pass': 'albedo_v0001',
#                                                        'frame range': '1001_1030', 'frame count': 30,
#                                                        '_parent': {'name': 'root', 'children': [...]}},
#     {'folder': 'D:/11/arnold\\diffuse_direct',
#      'file name': 'ep15_3020_ren_prp_prp_arnold_diffuse_direct_v0001.%04d.exr', 'engine': 'arnold', 'layer': 'diffuse',
#      'pass': 'direct_v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}}, {'folder': 'D:/11/arnold\\diffuse_indirect',
#                                                        'file name': 'ep15_3020_ren_prp_prp_arnold_diffuse_indirect_v0001.%04d.exr',
#                                                        'engine': 'arnold', 'layer': 'diffuse', 'pass': 'indirect_v0001',
#                                                        'frame range': '1001_1030', 'frame count': 30,
#                                                        '_parent': {'name': 'root', 'children': [...]}},
#     {'folder': 'D:/11/arnold\\motionvector', 'file name': 'ep15_3020_ren_prp_prp_arnold_motionvector_v0001.%04d.exr',
#      'engine': 'arnold', 'layer': 'motionvector', 'pass': 'v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}},
#     {'folder': 'D:/11/arnold\\N', 'file name': 'ep15_3020_ren_prp_prp_arnold_N_v0001.%04d.exr', 'engine': 'arnold',
#      'layer': 'N', 'pass': 'v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}},
#     {'folder': 'D:/11/arnold\\P', 'file name': 'ep15_3020_ren_prp_prp_arnold_P_v0001.%04d.exr', 'engine': 'arnold',
#      'layer': 'P', 'pass': 'v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}}, {'folder': 'D:/11/arnold\\specular_albedo',
#                                                        'file name': 'ep15_3020_ren_prp_prp_arnold_specular_albedo_v0001.%04d.exr',
#                                                        'engine': 'arnold', 'layer': 'specular', 'pass': 'albedo_v0001',
#                                                        'frame range': '1001_1030', 'frame count': 30,
#                                                        '_parent': {'name': 'root', 'children': [...]}},
#     {'folder': 'D:/11/arnold\\specular_direct',
#      'file name': 'ep15_3020_ren_prp_prp_arnold_specular_direct_v0001.%04d.exr', 'engine': 'arnold',
#      'layer': 'specular', 'pass': 'direct_v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}}, {'folder': 'D:/11/arnold\\specular_indirect',
#                                                        'file name': 'ep15_3020_ren_prp_prp_arnold_specular_indirect_v0001.%04d.exr',
#                                                        'engine': 'arnold', 'layer': 'specular',
#                                                        'pass': 'indirect_v0001', 'frame range': '1001_1030',
#                                                        'frame count': 30,
#                                                        '_parent': {'name': 'root', 'children': [...]}},
#     {'folder': 'D:/11/arnold\\sss_albedo', 'file name': 'ep15_3020_ren_prp_prp_arnold_sss_albedo_v0001.%04d.exr',
#      'engine': 'arnold', 'layer': 'sss', 'pass': 'albedo_v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}},
#     {'folder': 'D:/11/arnold\\sss_direct', 'file name': 'ep15_3020_ren_prp_prp_arnold_sss_direct_v0001.%04d.exr',
#      'engine': 'arnold', 'layer': 'sss', 'pass': 'direct_v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}},
#     {'folder': 'D:/11/arnold\\sss_indirect', 'file name': 'ep15_3020_ren_prp_prp_arnold_sss_indirect_v0001.%04d.exr',
#      'engine': 'arnold', 'layer': 'sss', 'pass': 'indirect_v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}}, {'folder': 'D:/11/arnold\\transmission_albedo',
#                                                        'file name': 'ep15_3020_ren_prp_prp_arnold_transmission_albedo_v0001.%04d.exr',
#                                                        'engine': 'arnold', 'layer': 'transmission',
#                                                        'pass': 'albedo_v0001', 'frame range': '1001_1030',
#                                                        'frame count': 30,
#                                                        '_parent': {'name': 'root', 'children': [...]}},
#     {'folder': 'D:/11/arnold\\transmission_direct',
#      'file name': 'ep15_3020_ren_prp_prp_arnold_transmission_direct_v0001.%04d.exr', 'engine': 'arnold',
#      'layer': 'transmission', 'pass': 'direct_v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}}, {'folder': 'D:/11/arnold\\transmission_indirect',
#                                                        'file name': 'ep15_3020_ren_prp_prp_arnold_transmission_indirect_v0001.%04d.exr',
#                                                        'engine': 'arnold', 'layer': 'transmission',
#                                                        'pass': 'indirect_v0001', 'frame range': '1001_1030',
#                                                        'frame count': 30,
#                                                        '_parent': {'name': 'root', 'children': [...]}},
#     {'folder': 'D:/11/arnold\\volume_albedo', 'file name': 'ep15_3020_ren_prp_prp_arnold_volume_albedo_v0001.%04d.exr',
#      'engine': 'arnold', 'layer': 'volume', 'pass': 'albedo_v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}},
#     {'folder': 'D:/11/arnold\\volume_direct', 'file name': 'ep15_3020_ren_prp_prp_arnold_volume_direct_v0001.%04d.exr',
#      'engine': 'arnold', 'layer': 'volume', 'pass': 'direct_v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}}, {'folder': 'D:/11/arnold\\volume_indirect',
#                                                        'file name': 'ep15_3020_ren_prp_prp_arnold_volume_indirect_v0001.%04d.exr',
#                                                        'engine': 'arnold', 'layer': 'volume', 'pass': 'indirect_v0001',
#                                                        'frame range': '1001_1030', 'frame count': 30,
#                                                        '_parent': {'name': 'root', 'children': [...]}},
#     {'folder': 'D:/11/arnold\\Z', 'file name': 'ep15_3020_ren_prp_prp_arnold_Z_v0001.%04d.exr', 'engine': 'arnold',
#      'layer': 'Z', 'pass': 'v0001', 'frame range': '1001_1030', 'frame count': 30,
#      '_parent': {'name': 'root', 'children': [...]}}]
