#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'


def di_filename_solver(task):
    task._preset.properties()['dayu_di_filename'] = 'di_filename'
    return task._preset.properties()['dayu_di_filename']
