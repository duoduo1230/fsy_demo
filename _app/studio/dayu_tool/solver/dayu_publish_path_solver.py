#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'


def publish_path_solver(task):
    import db
    from db.util import get_root_folder, get_class

    # track 名字为 ref 则类型为 edt ，否则当做 plt 上传
    type_name = 'edt' if task._item.parent().name() in ['ref', 'color', 'lut', 'reflut'] else 'plt'

    session = db.get_session()
    project_name = task.projectName()
    project = get_root_folder()[project_name]
    if not project:
        return 'dayu_publish_path'

    shot_name = task._item.name()
    description_name = task._item.parent().name()

    file_table = get_class('file')
    ver_orm = session.query(file_table) \
        .filter(file_table.active == True) \
        .filter(file_table.meaning.like('%ELEMENT_VERSION')) \
        .filter(file_table.name.like('{}\\_{}\\_{}%'.format(shot_name, type_name, description_name))) \
        .filter(file_table.top_id == project.id).all()
    if ver_orm:
        ver_orm.sort(key=lambda x: x.name)
        ver_orm = [x for x in ver_orm if '_{}_'.format(description_name) in x.name]
        task._preset.properties()['dayu_publish_path'] = str('/'.join(ver_orm[-1].disk_path().get_configs()[-1]))
        return task._preset.properties()['dayu_publish_path']
    else:
        return 'dayu_publish_path'
