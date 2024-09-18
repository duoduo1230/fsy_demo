#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import importlib

__author__ = 'andyguo'

import hiero.core as hcore
import hiero.ui as hui
import db
import db.util
import config.sub_level

CREATE_PRIORITY = {'seq': ('.exr', '.dpx', '.tiff', '.tif', '.jpg', '.png'),
                   'mov': ('.mov', '.mp4')}


def create(current_step, id, create=True):
    session = db.get_session()
    orm = session.query(db.util.get_class('file')).get(id)
    if not orm:
        return None

    decision_tree = ['hiero', current_step, orm.type_group_name, orm.type_name, 'create']

    api_version = orm.debug_data.get('api', None)

    try:
        pipeline_module = importlib.import_module(
                'app._hiero.api.{step}_{type_group}_{type}_{api}'.format(step=current_step,
                                                                         type_group=orm.type_group_name,
                                                                         type=orm.type_name,
                                                                         api=api_version))
    except Exception as e:
        pipeline_config = db.util.get_cascading_info(orm,
                                                     'pipeline_config_info', debug=True)['all_info'].get('pipeline', {})
        temp = pipeline_config
        # 这里相信GUI 在pipeline config 配置的时候，实现py 文件一定都是存在的
        for des in decision_tree:
            temp = temp.get(des, {})

        if not temp:
            decision_tree[1] = 'default'
            current_step = 'default'
            api_version = 'a0001'

        elif temp.get('default', False):
            decision_tree[1] = 'default'
            current_step = 'default'
            api_version = temp.get('api', 'a0001')

        pipeline_module = importlib.import_module(
                'app._nuke.api.{step}_{type_group}_{type}_{api}'.format(step=current_step,
                                                                        type_group=orm.type_group_name,
                                                                        type=orm.type_name,
                                                                        api=api_version))

    decision_tree.append(api_version)
    ops = config.sub_level.get_sub_level_op('.'.join(decision_tree), orm)
    op_api_func = getattr(pipeline_module, 'create_api_version')
    result = []
    for x in ops:
        op_func = op_api_func(x[1])
        if op_func:
            result.append({'do': True,  # 对应前端UI，用户是否需要导入这条？
                           'op_func': op_func,  # 操作的func 对象
                           'args': (x[0], orm),  # op_func 对象需要使用的参数，调用是使用func(*args) 即可
                           'options': None})  # 如果需要更多的参数传递给UI，可以在这里
    return result


def parse(selection=True):
    result = [{'trackitem_name_checked': 2,
               'trackitem': x,
               'trackitem_name': x.name(),
               'selected_version_name': None,
               'current_version_name': x.currentVersion().name(),
               'current_version': x.currentVersion(),
               'all_versions': [],
               'selected_sub_level': None,
               'current_sub_level': None,
               'all_sub_levels': {},
               'need_update': 0,
               'children': []} for x in hui.activeView().selection() if x.mediaType().name == 'kVideo']
    return result


def check_update(nested_list):
    pass


def do_update(nested_list):
    pass


def current_file():
    try:
        active_timeline = hui.activeSequence()
        return active_timeline.project().path()
    except Exception as e:
        print e
        return None


def is_legal():
    return True


def new_file():
    if not hcore.projects():
        return hcore.newProject()

    import nuke

    p = nuke.Panel('New Script')
    p.addBooleanCheckBox('Do you want to save current work file?', True)
    p.addButton('Cancel')
    p.addButton('Yes')
    p.addButton('No')

    ret = p.show()

    if ret == 0:
        return None
    if ret == 1:
        save()
    if ret == 2:
        print 'no'
        hcore.closeAllProjects()

    return hcore.newProject()


def open(filename):
    if not hcore.projects():
        return hcore.openProject(filename)

    import nuke

    p = nuke.Panel('New Script')
    p.addBooleanCheckBox('Do you want to save current work file?', True)
    p.addButton('Cancel')
    p.addButton('Yes')
    p.addButton('No')

    ret = p.show()

    if ret == 0:
        return None
    if ret == 1:
        save()
    if ret == 2:
        print 'no'
        hcore.closeAllProjects()

    hcore.openProject(filename)


def save():
    for x in hcore.projects():
        x.save()
    else:
        return True

    return False


def save_as(filename, overwrite=True):
    active_sequence = hui.activeSequence()
    try:
        active_sequence.project().saveAs(filename)
    except Exception as e:
        raise e


def get_main_window():
    return hui.mainWindow()


def show_widget(widget_class, single=False, **kwargs):
    dialog = widget_class(parent=get_main_window(), **kwargs)
    if hasattr(dialog, 'setup_data'):
        dialog.setup_data()
    hui.windowManager().popupWindow(dialog)
