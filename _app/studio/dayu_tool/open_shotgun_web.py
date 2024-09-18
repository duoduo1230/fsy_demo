#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'

import wrap_shotgun as ws


def open_shotgun_web(project, shot):
    """
    :param project: yys
    :param shot:    s0010
    :return:
    """
    import net_log
    import webbrowser
    sg = ws.MyShotgun()
    url_template = 'http://192.168.9.210/page/19418#Shot_{shot_id}'

    project_ = sg.find_one('Project', [['name', 'is', project]])
    shot_ = sg.find_one('Shot', [['project', 'is', project_], ['code', 'is', shot]])
    if shot_:
        print url_template.format(shot_id=shot_.get('id'))
        webbrowser.open(url_template.format(shot_id=shot_.get('id')))
    else:
        net_log.get_logger().warning('current shot {} do not exist!'.format(shot))


if __name__ == '__main__':
    open_shotgun_web('punk', 'ala_0020')

