#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

__doc__ = \
    '''
        这里是整个nuke 相关的路由函数中心。
        主要是前端的router 方式，分别有不同的函数进行处理。

        ========= 对于export 的流程 =========
        1. 前端UI 通过路由，调用到相应的处理函数 handle_export()
        2. 继续跳转到app._hiero.util.export 函数中
        3. 在app._hiero.util.export 函数中，继续分发，根据不同的条件，动态加载app._hiero.api 中的对应module
        4. 在对应的module 中，找到实际完成处理的export 函数，并返回这个函数自身
        3. 前端UI 根据用户在界面上的选择，将所有的数据打包为dict，作为参数传给 export 的处理函数


        ========= 对于create 的流程 ===========
        1. 前端UI 通过路由，调用到相应的处理函数 handle_create()
        2. 继续跳转到app._hiero.util.create 函数中
        3. 这个函数会根据 sub_level config 以及数据库中记录的api 版本，返回每个文件需要使用的函数
        4. 前端得到这个list，通过用户的选择，进行实际的调用

    '''

from app.center import Center

hiero_app = Center('hiero')


@hiero_app.register('/prepare_track')
def prepare_track():
    import app._hiero.track_tool
    return app._hiero.track_tool.prepare_build_track


@hiero_app.register('/build_track')
def build_track():
    import app._hiero.track_tool
    return app._hiero.track_tool.build_track


@hiero_app.register('/check_update')
def handle_check_update():
    import app._hiero.track_tool
    return app._hiero.track_tool.check_update_track


@hiero_app.register('/track_item_to_version')
def track_item_to_version():
    import app._hiero.track_tool
    return app._hiero.track_tool.track_item_to_version


@hiero_app.register('/do_update')
def handle_do_update():
    import app._hiero.track_tool
    return app._hiero.track_tool.do_update


@hiero_app.register('/parse_shot_db')
def parse_shot():
    import app._hiero.track_tool
    return app._hiero.track_tool.parse_shot_db


@hiero_app.register('/ui/show')
def handle_ui():
    import app._hiero.util
    return app._hiero.util.show_widget


@hiero_app.register('/ui/main_window')
def get_main_window():
    import app._hiero.util
    return app._hiero.util.get_main_window


@hiero_app.register('/render_farm/list')
def render_farm_list():
    return []


@hiero_app.register('/section_list')
def get_section_list():
    return []
