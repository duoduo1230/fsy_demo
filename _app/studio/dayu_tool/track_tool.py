#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import app

__author__ = 'andyguo'

import wrap_shotgun as ws
import hiero.core as hcore
import hiero.ui as hui
import db
import db.util
from db.disk_path import DiskPath
import itertools
import app._hiero.api.node_op.read_a0001 as h_read_a0001
import app._hiero.callbacks
import hiero.core.VersionScanner
import vcs
import re

sg = ws.MyShotgun()
# hiero 的version scanner 变量，里面的doScan() 已经被callback 里面重载了
hiero_version_scanner = hiero.core.VersionScanner.VersionScanner()

VERSION_REGEX = re.compile(r'.*([vV]\d+).*')


def prepare_build_track(track_items, type_group_name, type_name, format_name):
    '''
    在build track 之前，需要调用这个函数，作为准备工作。
    返回的数据给GUI 作为显示。

    返回的数据结构如下：
    [
     {'do': True,
      'trackitem': TrackItem('pl_0010')},
      'trackitem_name': 'pl_0010',
      'resource': <FOLDER>(1098670944521084178, pl_0010_plt_bga, ELEMENT_RESOURCE),
      'resource_name': 'pl_0010_plt_bga',
      'all_versions': [<FILE>(1098670944567217892, pl_0010_plt_bga_v0001, VERSION),
                       <FILE>(1116439460565389949, pl_0010_plt_bga_v0002, VERSION)],
      'all_version_names': [u'pl_0010_plt_bga_v0001', u'pl_0010_plt_bga_v0002'],
      'type_group_name': 'element',
      'type_name': 'plt',
      'format_name': 'exr',
      'selected_version_name': u'pl_0010_plt_bga_v0002',
      'legal': True,
      {...}
    ]

    do: 表示是否需要执行这条
    trackitem：记录hiero 中的trackitem 对象。（GUI 不用理睬）
    trackitem_name：hiero trackitem 对象的名字，用于GUI 显示
    resource：数据中查询到的对应的resource。如果存在多个对应的resource，会返回多个数据结构
    resource_name：resource orm 的名字，用于GUI 显示
    all_versions：list，存放resource 下所有的version 或者是dailies
    all_version_names：list，所有version、dailies 的名字，方便GUI 显示
    type_group_name：str
    type_name: str
    format_name：str
    selected_version_name: str, GUI 可以修改这个字段，表示用户选择的版本。默认值为最新版本的版本名称
    legal：是否为合法的trackitem？ 目前都是true，因为非法的不会被解析

    （由于hiero 的限制，如果一个素材之前读取的是mov，通过代码强行更换成为sequence 序列帧的话，会造成黑屏、崩溃等问题
    因此，强制要求用户指定需要导入的素材类型，而且一旦导入，那么后续的更新操作等，都需要是相同的文件格式）

    :param track_items: list of hiero trackitems。名字需要提前在hiero 中修改为对应的shotcode 才有可能解析成功
    :param type_group_name: str，类似 element、dailies 这样的
    :param type_name: str，类似 plt、ani、cmp 这样的类型名称
    :param format_name: str，类似exr, tiff, jpg, mov 这样的素材类型名称。
    :return: list of dict
    '''
    import db
    result = []
    db_table = db.util.get_class('folder')
    session = db.get_session()

    for x in track_items:
        project = x.project().name()
        shot = x.name()

        # sql 语句，进行查询
        orm = session.query(db_table). \
            filter(db_table.active == True). \
            filter(db_table.name.like('{}%'.format(shot))). \
            filter(db_table.type_group_name == type_group_name). \
            filter(db_table.type_name == type_name). \
            filter(db_table.top.has(db_table.name == project)). \
            all()
        # track item 对应的 version orm在dayu数据库不存在， 可能是外包上传的mov
        # 处理方法: 查询shotgun 对应的version是否存在，如果存在把mov下载到publish区对应的mov层级下
        if not orm and type_group_name == 'dailies':
            data_list = sync_sg_to_publish(x, project, shot, type_group_name, type_name, format_name)
            result.extend(data_list) if data_list else None

        # 如果orm存在 先查找是否有 master 命名的dailies element,
        # 找到后 对比 db 与 sg 的version number， 若 sg>db, 则更新下载sg version mov
        if orm and type_group_name == 'dailies':
            master_resource = next((x for x in orm if '_master' in x.name), None)
            version_orm = list(master_resource.children)[-1] if master_resource else None
            if version_orm:
                db_version = get_version_num(version_orm.name)
                version_list = get_sg_version_list(project, shot, type_name)
                sg_ver_num = get_version_num(version_list[-1]['code']) if version_list else '0'
                if int(sg_ver_num.replace('v',  '')) > int(db_version.replace('v', '')):
                    sync_sg_to_publish(x, project, shot, type_group_name, type_name, format_name)

        for res in orm:
            all_versions = res.sub_files.all()

            if not all_versions:
                continue

            lastest_version = all_versions[-1]
            for s in lastest_version.flatten():
                if s['file'].filename.ext != format_name:
                    continue

                temp = dict()
                temp['trackitem'] = x
                temp['trackitem_name'] = x.name()
                temp['resource'] = res
                temp['resource_name'] = str(res.name)
                temp['current_sub_level'] = str(s['sub_level'])
                temp['current_version'] = s['orm']
                temp['current_file_path'] = s['file']
                temp['type_group_name'] = type_group_name
                temp['type_name'] = type_name
                temp['format_name'] = format_name
                temp['legal'] = True
                temp['trackitem_name_checked'] = 2
                temp['created_time'] = lastest_version.created_time
                result.append(temp)

    return result


def get_version_num(version):
    match = VERSION_REGEX.match(version)
    return match.group(1) if match else 0


def get_sg_version_list(project, shot, type_name):
    version = sg.find('Version', [['project.Project.name', 'is', project],
                                  ['entity.Shot.code', 'is', shot],
                                  ['code', 'contains', '{}_{}'.format(shot, type_name)]], ['sg_uploaded_movie', 'code'])
    return version


def sync_sg_to_publish(track_item, project, shot, type_group_name, type_name, format_name):
    import db
    session = db.get_session()
    version = get_sg_version_list(project, shot, type_name)
    if version and version[-1]['sg_uploaded_movie']:
        import db.db_path
        import db.util

        sequence_, shot_ = shot.split('_')
        project_db_path = db.db_path.DBPath('/{}'.format(project))
        root_list = ['sequence', sequence_, shot_, type_group_name, type_name, 'master']
        resource = project_db_path.create(*root_list)
        resource_orm = resource.orm()
        file_table = db.util.get_class('file')
        version_orm = file_table(parent=resource_orm)
        session.flush()
        target_path = version_orm.disk_path(disk_type='publish')
        mov_path = DiskPath(target_path).child('mov', '{}.mov'.format(version_orm.name))
        mov_path.parent.mkdir(parents=True)
        sg.download_attachment(attachment_id=version[-1]["sg_uploaded_movie"]['id'], file_path=mov_path)
        version_orm.rescan(confirm=True)
        session.commit()
        result = []
        for s in version_orm.flatten():
            if s['file'].filename.ext != format_name:
                continue

            temp = dict()
            temp['trackitem'] = track_item
            temp['trackitem_name'] = track_item.name()
            temp['resource'] = resource_orm
            temp['resource_name'] = str(resource_orm.name)
            temp['current_sub_level'] = str(s['sub_level'])
            temp['current_version'] = s['orm']
            temp['current_file_path'] = s['file']
            temp['type_group_name'] = type_group_name
            temp['type_name'] = type_name
            temp['format_name'] = format_name
            temp['legal'] = True
            temp['trackitem_name_checked'] = 2
            temp['created_time'] = version_orm.created_time
            result.append(temp)

        return result


def check_update_track(track_items):
    '''
    批量更新的准备函数，返回的数据用于GUI 的显示。
    （在调用do_update() 函数之前，需要先调用这个函数）

    函数的数据结构：
    [
        {
            'do': False,
            'trackitem': TrackItem('pl_0010_plt_bga')
            'trackitem_name': 'pl_0010_plt_bga',
            'resource': <FILE>(1116439460565389949, pl_0010_plt_bga_v0002, VERSION),
            'resource_name': 'pl_0010_plt_bga_v0002',
            'all_versions': (Version('pl_0010_plt_bga_v0001'), Version('pl_0010_plt_bga_v0002')),
            'all_version_names': ['pl_0010_plt_bga_v0001', 'pl_0010_plt_bga_v0002'],
            'type_group_name': u'element',
            'type_name': u'plt',
            'format_name': u'exr',
            'current_sub_level': 'fullres/exr'
            'current_version_name': 'pl_0010_plt_bga_v0002',
            'selected_version_name': 'pl_0010_plt_bga_v0002',
            'need_update': 'green',
        }
        {...}
    ]

    do: 表示是否要执行操作？
    trackitem：hiero trackitem 的对象
    trackitem_name：str，trackitem 的名称，用于GUI 的显示
    resource：数据库中查询到的orm
    resource_name：str，orm 的名字，用于GUI 显示
    all_versions: list，resource orm 下所有的version 或者dailies 对象
    all_version_names: list，所有version、dailies 的名称，用于GUI 显示
    type_group_name：str
    type_name: str
    format_name: str
    current_version_name：str，trackitem 当前的version 名称，GUI 显示，但是不能够修改
    selected_version_name: str，用户选择的版本。默认值是最新版本
    need_update: str，'green' 表示不需要更新，'red' 表示需要更新


    :param track_items: list of hiero trackitem
    :return: list of dict
    '''
    result = []

    for x in track_items:
        temp = dict()
        path = DiskPath(x.source().mediaSource().fileinfos()[0].filename())
        orm = path.orm().parent if path.orm() else None
        if orm:
            temp['node'] = x
            temp['node_name'] = x.name()
            temp['resource'] = orm
            temp['resource_name'] = str(orm.name)
            # 这里的小技巧，利用重载过后的version scanner，重新扫描，生成新的hiero versions，这样就不需要重复写代码了
            hiero_version_scanner.doScan(x.currentVersion())
            temp['all_versions'] = orm.sub_files.all()
            temp['all_version_names'] = [v.name for v in temp['all_versions']]
            temp['all_hiero_versions'] = x.currentVersion().parent().items()
            temp['all_hiero_version_names'] = [v.name() for v in temp['all_hiero_versions']]
            temp['format_name'] = path.split('.')[-1]
            temp['current_sub_level'] = '/'.join(path.replace(orm.disk_path(), '').strip('/').split('/')[:-1])
            temp['current_version_name'] = x.currentVersion().name()
            temp['current_version'] = x.currentVersion()
            temp['selected_version'] = temp['all_versions'][-1] if temp['all_versions'] else None
            temp['selected_version_name'] = temp['all_hiero_version_names'][-1] \
                if temp['all_hiero_version_names'] else '----'

            temp['type_group_name'] = orm.type_group_name
            temp['type_name'] = orm.type_name
            temp['need_update'] = 'red' if temp['selected_version_name'] > temp['current_version_name'] else 'green'
            temp['node_name_checked'] = 2 if temp['need_update'] == 'red' else 0
            result.append(temp)

    return result


def track_item_to_version(track_items):
    result = []

    for x in track_items:
        temp = dict()
        path = DiskPath(x.source().mediaSource().fileinfos()[0].filename())
        version_orm = path.orm()
        temp['node'] = x
        temp['node_name'] = x.name()
        temp['node_name_checked'] = 0
        temp['version_orm'] = version_orm
        if version_orm:
            temp['version_orm'] = version_orm
            temp['node_name_checked'] = 2
            result.append(temp)

    return result


def do_update(list_of_dicts):
    '''
    执行实际的update 操作。
    （在调用本函数之前，请先调用check_update() 函数）

    :param list_of_dicts: 数据结构就是check_update() 返回的数据
    :return: None
    '''
    current_project = hui.activeSequence().project()
    # undo group
    with current_project.beginUndo('batch update'):
        for x in list_of_dicts:
            if not x['node_name_checked'] or x['need_update'] == 'yellow':
                continue

            selected_version = next((v for v in x['all_hiero_versions']
                                     if v.name() == x['selected_version_name']), None)
            if selected_version:
                x['node'].setCurrentVersion(selected_version)


def build_track(list_of_builditems, track_name=None, match_shot=True):
    '''
    build track 的实际执行函数
    （在执行本函数之前，请先调用perpare_build_track() 函数）

    :param list_of_builditems: 就是prepare_build_track 函数返回的数据结构
    :param track_name: str，创建的video track 的名称
    :param match_shot: bool，True 表示新导入的trackitem 应该放到对应shot 相同的时间线位置，
                             False 表示所有的新建的trackitem 连在一起
    :return: generator
    '''
    current_project = hui.activeSequence().project()
    with current_project.beginUndo('build new track'):
        current_sequence = hui.activeSequence()

        # 这里使用groupby 迭代器，是因为有些shot 可能会对应多个resource，例如 pl_0010 可能存在pl_0010_plt_bga、pl_0010_plt_bgb
        # 两个plt 素材。此时就需要创建多个video track，并且将resource 分别放到对应的轨道上。
        grouped_items = itertools.groupby(list_of_builditems, key=lambda n: n['trackitem_name'])
        track_list = []
        audio_track_list = []
        current_track_num = 0

        for shot in grouped_items:
            current_track_num = 0

            for builditem in shot[1]:
                # 跳过不需要执行的
                if not builditem['trackitem_name_checked']:
                    continue

                # 如果同一个shot，解析到了多个resource，那么需要的 video track 就会增加
                current_track_num += 1

                # # 如果用户的选择不存在all_version 列表？那么跳过
                # version_orm = next((x for x in builditem['all_versions']
                #                     if x.name == builditem['selected_version_name']), None)
                # if not version_orm:
                #     continue

                # # 查找对应version 内部的sub level，严格找到用户提供的format，如果不存在，跳过
                # seq_file = [x for x in version_orm.sub_level.walk(collapse=True)
                #             if builditem['format_name'] in x.filename]
                # if not seq_file:
                #     continue

                # 如果需要创建的轨道数量超过已经创建的，那么创建更多的video track
                if current_track_num > len(track_list):
                    new_track = hcore.VideoTrack('{}_{}_{:02d}'.format(track_name if track_name else 'video',
                                                                       list_of_builditems[0]['format_name'],
                                                                       current_track_num))
                    track_list.append(new_track)
                    current_sequence.addTrack(new_track)

                # 由于hiero 只有read 一种方式导入，因此总是调用默认的read op 操作
                # 如果已经到如果了，不会重复导入素材
                binitem = h_read_a0001.create(builditem['current_file_path'], builditem['current_version'],
                                              builditem['current_sub_level'])

                # 重新扫描所有的hiero version
                hiero_version_scanner.doScan(binitem.activeVersion())
                # print builditem['current_version']
                hiero_version = next((x for x in binitem.items()
                                      if x.name() == str(builditem['current_version'].name)), None)
                # 理论上，这里应该不需要进行None 值防御。因为version scanner 的操作也是查找数据库，二者应该总是得到相同的结果
                # 除非极小概率发生，用户在check_update() 的时候，其他人其实删除了某些version，导致数据不一致。
                binitem.setActiveVersion(hiero_version)
                clip = binitem.activeItem()
                # 注意 ！！rescan() 这一行加入的原因是, herio 自己的版本扫描机制，在给binitem addversion 的时候，
                # 如果这个版本的长度和其他version 不一样，会把所有binitem 中的version 的 frame range 变为所有version中最短
                # 所以某个版本如果 不幸少帧了，那所有的版本帧范围会变小。最后只能在 build 进来的时候，对clip 进行一次 rescan
                clip.rescan()
                # print track_list
                # print current_track_num
                new_track_item = track_list[current_track_num - 1].createTrackItem(binitem.name())
                new_track_item.setSource(clip)

                duration = builditem['trackitem'].duration()
                new_track_item.setSourceOut(new_track_item.sourceIn() + duration - 1)

                # 如果文件中包含声音，则也会自动创建音轨
                audio_num = clip.numAudioTracks()

                for x in range(audio_num):
                    x += 1
                    if x > len(audio_track_list):
                        new_audio_track = hcore.AudioTrack('{}_{}_{:02d}'.format(track_name if track_name else 'audio',
                                                                                 list_of_builditems[0]['format_name'],
                                                                                 x))
                        current_sequence.addTrack(new_audio_track)
                        audio_track_list.append(new_audio_track)

                    new_audio_track = audio_track_list[x - 1]
                    new_audio_track_item = new_audio_track.createTrackItem(binitem.name())
                    new_audio_track_item.setSource(clip)
                    new_audio_track.addItem(new_audio_track_item)
                    if match_shot:
                        # 避免重叠
                        new_audio_track_item.move(builditem['trackitem'].timelineIn())

                    else:
                        if new_audio_track.items():
                            last_trackitem = new_audio_track.items()[-1]
                            new_audio_track_item.setTimelineIn(last_trackitem.timelineOut() + 1)
                            new_audio_track_item.setTimelineOut(last_trackitem.timelineOut() + duration)
                        else:
                            new_audio_track_item.setTimelineIn(0)
                            new_audio_track_item.setTimelineOut(duration - 1)

                # 是否match shot 在时间线上的位置
                if match_shot:
                    new_track_item.setTimelineIn(builditem['trackitem'].timelineIn())
                    new_track_item.setTimelineOut(builditem['trackitem'].timelineIn() + duration - 1)

                else:
                    if track_list[current_track_num - 1].items():
                        last_trackitem = track_list[current_track_num - 1].items()[-1]
                        new_track_item.setTimelineIn(last_trackitem.timelineOut() + 1)
                        new_track_item.setTimelineOut(last_trackitem.timelineOut() + duration)
                    else:
                        new_track_item.setTimelineIn(0)
                        new_track_item.setTimelineOut(duration - 1)

                vcs.add_secret_info(new_track_item, builditem['current_version'].parent)
                track_list[current_track_num - 1].addItem(new_track_item)
                # new_track2.addItem(new_track_item2)
                yield new_track_item


def parse_shot_db(track_item_list, upload_type):
    result_list = []
    session = db.get_session()
    folder_table = db.util.get_class('folder')
    rx = re.compile(r'^[a-z]+[a-z0-9\-]*?\D+$')
    for track_item in track_item_list:
        data_dict = {
            'trackitem_name': track_item.name(),
            'trackitem': track_item,
            'shot_orm': None,
            'resource_orm': None,
            'latest_version_orm': None,
            'latest_comment': None,
            'descriptor': track_item.parent().name(),
            'descriptor_valid': bool(rx.findall(track_item.parent().name())),
            'incoming_version': None,
        }
        shot_orm = session.query(folder_table) \
            .filter(folder_table.active == True) \
            .filter(folder_table.meaning == 'SHOT') \
            .filter(folder_table.name == track_item.name()) \
            .filter(folder_table.top.has(folder_table.name == track_item.project().name())).first()
        if shot_orm:
            resource_orm = session.query(folder_table) \
                .filter(folder_table.active == True) \
                .filter(folder_table.name == '{}_{}_{}'.format(shot_orm.name, upload_type, data_dict['descriptor'])) \
                .filter(folder_table.meaning.like('%ELEMENT_RESOURCE')) \
                .filter(folder_table.top.has(folder_table.name == track_item.project().name())) \
                .first()

            if resource_orm:
                data_dict['resource_orm'] = resource_orm
                all_versions = list(resource_orm.children)
                data_dict['latest_version_orm'] = all_versions[-1] if all_versions else None
                data_dict['latest_comment'] = all_versions[-1].comment if all_versions else None
                data_dict['incoming_version'] = 'v{:04d}'.format(
                    (int(data_dict.get('latest_version_orm').name[-4:])
                     if data_dict.get('latest_version_orm') else 0) + 1)

        data_dict['shot_orm'] = shot_orm
        result_list.append(data_dict)

    return result_list


def parse_shot_edit_db(track_item_list):
    result_list = []
    session = db.get_session()
    folder_table = db.util.get_class('folder')
    rx = re.compile(r'^[a-z]+[a-z0-9\-]*?\D+$')
    for track_item in track_item_list:
        data_dict = {
            'trackitem_name': track_item.name(),
            'trackitem': track_item,
            'shot_orm': None,
            'resource_orm': None,
            'latest_version_orm': None,
            'latest_comment': None,
            'descriptor': track_item.parent().name(),
            'descriptor_valid': bool(rx.findall(track_item.parent().name())),
            'incoming_version': None,
        }
        shot_orm = session.query(folder_table) \
            .filter(folder_table.active == True) \
            .filter(folder_table.meaning == 'SHOT') \
            .filter(folder_table.name == track_item.name()) \
            .filter(folder_table.top.has(folder_table.name == track_item.project().name())).first()
        if shot_orm:
            resource_orm = session.query(folder_table) \
                .filter(folder_table.active == True) \
                .filter(folder_table.name == '{}_edit_{}'.format(shot_orm.name, data_dict['descriptor'])) \
                .filter(folder_table.meaning.like('%ELEMENT_RESOURCE')) \
                .filter(folder_table.top.has(folder_table.name == track_item.project().name())) \
                .first()

            if resource_orm:
                data_dict['resource_orm'] = resource_orm
                all_versions = list(resource_orm.children)
                data_dict['latest_version_orm'] = all_versions[-1] if all_versions else None
                data_dict['latest_comment'] = all_versions[-1].comment if all_versions else None
                data_dict['incoming_version'] = 'v{:04d}'.format(
                    (int(data_dict.get('latest_version_orm').name[-4:])
                     if data_dict.get('latest_version_orm') else 0) + 1)

        data_dict['shot_orm'] = shot_orm
        result_list.append(data_dict)

    return result_list
