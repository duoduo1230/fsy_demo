#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from hiero.exporters.FnShotProcessor import ShotProcessorPreset
import dayu_publish_path_solver
import dayu_version_name_solver
import dayu_di_name_solver


def dayu_add_user_resolver(self, resolver):
    resolver.addResolver('{dayu_publish_path}', 'generate dayu pipline publish path',
                         lambda keyword, task: dayu_publish_path_solver.publish_path_solver(task))

    resolver.addResolver('{dayu_di_filename}', 'revert to DI filenames',
                         lambda keyword, task: dayu_di_name_solver.di_filename_solver(task))

    resolver.addResolver('{dayu_version_name}', 'get lastest version name',
                         lambda keyword, task: dayu_version_name_solver.dayu_version_name_solver(task))


ShotProcessorPreset.addUserResolveEntries = dayu_add_user_resolver
