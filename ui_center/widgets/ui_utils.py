#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2018.5
# Email : muyanru345@163.com
###################################################################

import collections
import datetime as dt
import functools
import os
import net_log
from singledispatch import singledispatch

from app import DAYU
from ui_center.qt import *

MenuEvent = collections.namedtuple('MenuEvent', ['view', 'selection', 'extra'])

IMAGE_PATH = DAYU.request('/static/image')

default_qss_file = DAYU.request('/static/qss/main.qss')
with open(default_qss_file, 'r') as f:
    default_qss = f.read().replace('url(', 'url(%s/' % default_qss_file.parent.replace('\\', '/'))


def dayu_css(css_content=None):
    def wrapper1(func):
        def new_init(*args, **kwargs):
            result = func(*args, **kwargs)
            instance = args[0]
            instance.setStyleSheet(css_content if css_content else default_qss)
            return result

        return new_init

    return wrapper1


HELP_URL_MAP = DAYU.request('/static/ui_config/help_config')


def dayu_user_state():
    def read_settings(self):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'Phenom-Films', 'DAYU')
        if settings.value('{}/geometry'.format(self.objectName())):
            self.restoreGeometry(settings.value('{}/geometry'.format(self.objectName())))
        if isinstance(self, QMainWindow) and settings.value('{}/windowState'.format(self.objectName())):
            self.restoreState(settings.value('{}/windowState'.format(self.objectName())))

    def closeEvent(self, event):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'Phenom-Films', 'DAYU')
        settings.setValue('{}/geometry'.format(self.objectName()), self.saveGeometry())
        if isinstance(self, QMainWindow):
            settings.setValue('{}/windowState'.format(self.objectName()), self.saveState())
        event.accept()

    def wrapper1(func):
        def new_init(*args, **kwargs):
            result = func(*args, **kwargs)
            instance = args[0]
            instance.read_settings = functools.partial(read_settings, instance)
            instance.closeEvent = functools.partial(closeEvent, instance)
            instance.read_settings()
            return result

        return new_init

    return wrapper1


@Slot()
def open_web_url(self):
    import webbrowser
    key = self.objectName()
    if key not in HELP_URL_MAP.keys():
        HELP_URL_MAP.get('404')
    else:
        webbrowser.open(HELP_URL_MAP.get(key))


def help_action():
    def wrapper1(func):
        def new_init(*args, **kwargs):
            result = func(*args, **kwargs)
            instance = args[0]
            action = QAction(MIcon(IMAGE_PATH.child('icon-help.png')), 'Help', instance)
            instance.addAction(action)
            if not instance.objectName():
                instance.setObjectName(instance.__class__.__name__)
            instance.setContextMenuPolicy(Qt.ActionsContextMenu)
            action.triggered.connect(functools.partial(open_web_url, instance))
            return result

        return new_init

    return wrapper1


def show_loading():
    def wrapper1(waste_time_func):
        def new_init(*args, **kwargs):
            from MLoadingWidget import MLoadingWidget, MLoadingThread
            instance = args[0]
            loading_widget = MLoadingWidget(instance)
            print(instance.pos(), instance.mapFromParent(instance.pos()), instance.mapToGlobal(instance.pos()))
            start_point = instance.pos()  # instance.mapToGlobal(instance.pos())
            loading_widget.setGeometry(start_point.x(), start_point.y(), instance.width(), instance.height())
            loading_widget.show()
            th = MLoadingThread(instance)
            th.set_func(waste_time_func, *args, **kwargs)
            th.sig_finished.connect(getattr(instance, waste_time_func.__name__ + '_finished'))
            th.finished.connect(loading_widget.close)
            th.start()
            return

        return new_init

    return wrapper1


def db_op(error=True, success=True):
    def wrapper1(func):
        def wrapper2(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                import traceback
                import db
                error_detail = traceback.format_exc()
                db.get_session().rollback()
                net_log.get_logger().error(u'Database rollback. Error:{}'.format(error_detail))
                if error:
                    from message_box import MErrorMessageBox
                    msg = MErrorMessageBox(str(e), detail=error_detail, parent=args[0])
                    msg.exec_()
                return None
            else:
                if success:
                    from message_box import MSuccessMessageBox
                    msg = MSuccessMessageBox('Success!', parent=args[0])
                    msg.exec_()
                return result

        return wrapper2

    return wrapper1


@Slot(object)
def slot_item_view_context_menu(self, extra, get_actions_callback, finish_callback, event):
    import db.util
    event.extra.update(extra() if callable(extra) else extra)
    action_list = get_actions_callback()
    current_permission = db.util.get_current_user().authorization_name
    menu = QMenu(self)
    for sub_action_list in action_list:
        for get_action in sub_action_list:
            action_data = get_action()
            if current_permission in action_data.authorization and action_data.validate(event):
                if action_data.cls_type == 'action':
                    action = menu.addAction(action_data.name)
                else:
                    action = menu.addMenu(action_data.name)
                    event.extra.update({'parent_menu': action})
                if action_data.icon:
                    action.setIcon(MIcon(action_data.icon if os.path.isfile(action_data.icon) else
                                         IMAGE_PATH.child((action_data.icon))))
                self.connect(action, SIGNAL(action_data.signal), functools.partial(action_data.run, event))
                if finish_callback:
                    action_data.sig_finished.connect(finish_callback)

        menu.addSeparator()

    menu.exec_(QCursor.pos())


def create_item_view(header_list_url, setup_data_url, context_menu_url):
    def _make_widget(parent):
        from MItemViewFilterSetWidget import MItemViewFilterSetWidget
        page = MItemViewFilterSetWidget(parent=parent)
        page.enable_search()
        page.enable_filter()
        header_list = DAYU.request(header_list_url).get('header_list')
        page.set_header_list(header_list)
        page.setup_data(DAYU.request(setup_data_url))
        page.slot_show_context = slot_item_view_context_menu
        page.sig_context_menu.connect(
            functools.partial(page.slot_show_context,
                              {},
                              lambda: DAYU.request(context_menu_url),
                              lambda: page.setup_data(DAYU.request(setup_data_url))))
        return page

    return _make_widget


def get_obj_value(data_obj, attr, default=None):
    if isinstance(data_obj, dict):
        return data_obj.get(attr, default)
    else:
        return getattr(data_obj, attr, default)


def set_obj_value(data_obj, attr, value):
    if isinstance(data_obj, dict):
        return data_obj.update({attr: value})
    else:
        return setattr(data_obj, attr, value)


def has_obj_value(data_obj, attr):
    if isinstance(data_obj, dict):
        return attr in data_obj.keys()
    else:
        return hasattr(data_obj, attr)


def apply_formatter(obj, *args, **kwargs):
    if obj is None:  # 压根就没有配置
        return args[0]
    elif isinstance(obj, dict):  # 字典选项型配置
        return obj.get(args[0], None)
    elif callable(obj):  # 回调函数型配置
        return obj(*args, **kwargs)
    else:  # 直接值型配置
        return obj


@singledispatch
def default_formatter(obj):
    return obj


@default_formatter.register(dict)
def _(obj):
    if 'name' in obj.keys():
        return default_formatter(obj.get('name'))
    elif 'code' in obj.keys():
        return default_formatter(obj.get('code'))
    else:
        return str(dict)


@default_formatter.register(list)
def _(obj):
    result = []
    for i in obj:
        result.append(default_formatter(i))
    return ','.join(result)


@default_formatter.register(str)
def _(obj):
    return obj.decode('utf-8')


@default_formatter.register(unicode)
def _(obj):
    return obj


@default_formatter.register(type(None))
def _(obj):
    return '--'


@default_formatter.register(object)
def _(obj):
    if hasattr(obj, 'name'):
        return default_formatter(getattr(obj, 'name'))
    if hasattr(obj, 'code'):
        return default_formatter(getattr(obj, 'code'))
    return str(obj)


@default_formatter.register(dt.datetime)
def _(obj):
    return obj.strftime('%Y-%m-%d %H:%M:%S')


def get_font(underline=False, bold=False):
    _font = QFont()
    _font.setUnderline(underline)
    _font.setBold(bold)
    return _font


@singledispatch
def icon_formatter(obj, cls=MIcon):
    return obj


@icon_formatter.register(dict)
def _(data_obj, cls=MIcon):
    setting_list = [('icon', '{}')]
    for attr, formatter in setting_list:
        path = get_obj_value(data_obj, attr)
        if path:
            return icon_formatter(formatter.format(path), cls)
    return icon_formatter('icon-unknown.png', cls)


@icon_formatter.register(object)
def _(data_obj, cls=MIcon):
    setting_list = [('icon', '{}'),
                    ('thumbnail_path', '{}'),
                    ('cloud_id', '{}'),
                    ('children_shots', 'icon-rank1.png'),
                    ('meaning', 'icon-{}.png'),
                    ('__tablename__', 'icon-{}.png')]

    for attr, formatter in setting_list:
        path = get_obj_value(data_obj, attr)
        if not path:
            continue
        if attr == 'cloud_id':
            cloud_table = get_obj_value(data_obj, 'cloud_table')
            if cloud_table and (not get_obj_value(data_obj, '_bad', False)) \
                    and cloud_table in ['Version']:
                path = DAYU.request('/pm/download_thumbnail')(cloud_table, path)
                if path:
                    return cls(path)
                else:
                    set_obj_value(data_obj, '_bad', True)
        else:
            if attr == 'children_shots':
                path = list(path)
            if path:
                return icon_formatter(formatter.format(path), cls)
    return icon_formatter('icon-unknown.png', cls)


@icon_formatter.register(basestring)
def _(path, cls=MIcon):
    if path.count('/') or path.count('\\'):
        if os.path.isfile(path):
            return cls(path)
        else:
            return cls(IMAGE_PATH.child('icon-unknown.png'))
    else:
        path = IMAGE_PATH.child(path.lower())
        if os.path.isfile(path):
            return cls(path)
        else:
            return cls(IMAGE_PATH.child('icon-unknown.png'))


@singledispatch
def real_model(source_model):
    """
    Get the source model whenever user give a source index or proxy index or proxy model.
    """
    return source_model


@real_model.register(QSortFilterProxyModel)
def _(proxy_model):
    return proxy_model.sourceModel()


@real_model.register(QModelIndex)
def _(index):
    return real_model(index.model())


def real_index(index):
    """
    Get the source index whenever user give a source index or proxy index.
    """
    model = index.model()
    if isinstance(model, QSortFilterProxyModel):
        return model.mapToSource(index)
    return index
