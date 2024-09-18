#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import os

import hiero.ui

from ui_center.qt import *

SOFT_EFFECT_PATH = os.path.join(os.path.dirname(__file__), 'icon')


def example_soft_effect():
    effect_name = 'easy_slate'
    icon_path = SOFT_EFFECT_PATH + effect_name + '.png'
    if not os.path.exists(icon_path):
        icon_path = SOFT_EFFECT_PATH + 'default.png'
    action = QAction(QIcon(icon_path), effect_name, None)
    action.setObjectName('foundry.timeline.effect.{}'.format(effect_name))
    action.setToolTip('')
    action.setData(effect_name)
    hiero.ui.registerAction(action)


example_soft_effect()
