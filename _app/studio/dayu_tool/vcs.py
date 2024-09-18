#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import const
import hiero.core as hcore


def add_secret_info(node, orm, **kwargs):
    tag = next((x for x in node.tags() if x.name() == const.DAYU_SECRET), None)
    if tag is None:
        tag = hcore.Tag(const.DAYU_SECRET)
        node.addTag(tag)

    meta = tag.metadata()
    meta.setValue('tag.id', str(orm.id))
    meta.setValue('tag.table', str(orm.__table__))
    for key in kwargs:
        meta.setValue('tag.{}'.format(key), str(kwargs[key]))

    tag.setVisible(False)


def get_secret_info(node):
    tag = next((x for x in node.tags() if x.name() == const.DAYU_SECRET), None)
    if tag is None:
        return {}

    return {key.replace('tag.', ''): value for key, value in tag.metadata().dict().items()}
