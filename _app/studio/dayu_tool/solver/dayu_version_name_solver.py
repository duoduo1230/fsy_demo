#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'


def dayu_version_name_solver(task):
    import db
    from db.db_path import DBPath
    from db.table import FOLDER, FILE

    # track 名字为 ref 则类型为 edt ，否则当做 plt 上传
    type_name = 'edt' if task._item.parent().name() in ['ref', 'color', 'lut', 'reflut'] else 'plt'

    session = db.get_session()
    project_name = task.projectName()
    project = DBPath('/{}'.format(project_name)).orm()
    if not project:
        return 'dayu_version_name'

    shot_name = task._item.name()
    description_name = task._item.parent().name()

    ver_orm = session.query(FILE) \
        .filter(FILE.active == True) \
        .filter(FILE.meaning.like('%ELEMENT_VERSION')) \
        .filter(FILE.name.like('{}\\_{}\\_{}%'.format(shot_name, type_name, description_name))) \
        .filter(FILE.top_id == project.id).all()
    if ver_orm:
        ver_orm.sort(key=lambda x: x.name)
        ver_orm = [x for x in ver_orm if '_{}_'.format(description_name) in x.name]
        task._preset.properties()['dayu_version_name'] = str(ver_orm[-1].name)
        return task._preset.properties()['dayu_version_name']
    else:
        return 'dayu_version_name'
