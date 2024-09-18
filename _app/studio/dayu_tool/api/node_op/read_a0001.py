#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import hiero.core as hcore
import hiero.ui as hui
from db.disk_path import DiskPath


def create(*args, **kwargs):
    seq_file, orm, current_sub = args
    create = kwargs.get('create', True)

    # 得到当前打开时间线对应的工程
    current_project = hui.activeSequence().project()

    # 查找需要的bin，如果没有bin，就创建一个
    bin_name = '{}_imported_clip'.format(orm.top.name)
    new_bin = next((x for x in current_project.clipsBin().bins()
                    if x.name() == bin_name), None)
    if not new_bin:
        new_bin = hcore.Bin(bin_name)
        if create:
            current_project.clipsBin().addItem(new_bin)

    # 内部维护一个identity dict，保证不会重复导入素材
    already_in_clip_dict = {'{res}_{type_group}_{type}_{sub}_{ext}'.format(
        res='_'.join(DiskPath(x.activeItem().mediaSource().fileinfos()[0].filename()).stem.split('_')[:-1]),
        type_group=orm.type_group_name,
        type=orm.type_name,
        sub='/'.join(
            x.activeItem().mediaSource().fileinfos()[0].filename().replace(orm.disk_path(), '').split('/')[:-1]),
        ext=DiskPath(x.activeItem().mediaSource().fileinfos()[0].filename()).ext[1:]): x for x in new_bin.clips()}

    # 查找准备导入的素材是否已经存在于内部的identity dict 中
    import_clip_key = '{res}_{type_group}_{type}_{sub}_{ext}'.format(
        res='_'.join(seq_file.filename.stem.split('_')[:-1]),
        type_group=orm.type_group_name,
        type=orm.type_name,
        sub=current_sub,
        ext=seq_file.filename.ext[1:])

    print import_clip_key, 'key!!!!!!!!!!!!!!!!!!!!!'
    if import_clip_key in already_in_clip_dict:
        # 如果已经存在，那么返回相同的素材
        print 'already in !!!'
        new_binitem = already_in_clip_dict.get(import_clip_key, None)
    else:
        # 如果没有找到，那么新建这个素材的 BinItem 对象
        new_mediasource = hcore.MediaSource(seq_file.filename)
        new_clip = hcore.Clip(new_mediasource)
        new_clip.setFramerate(hui.activeSequence().framerate() if hui.activeSequence() else hcore.TimeBase(24.0))
        new_binitem = hcore.BinItem(new_clip)
        already_in_clip_dict.update({import_clip_key: new_binitem})
        if create:
            new_bin.addItem(new_binitem)

    return new_binitem
