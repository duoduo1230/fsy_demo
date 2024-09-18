#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import nuke


def remapping_platform_path():
    import itertools
    import db.util
    import net_log

    all_mappings = []
    for s in db.util.get_all_storage_configs():
        for k, v in s.items():
            win32 = v.get('win32', '')
            darwin = v.get('darwin', '')
            linux2 = v.get('linux2', '')
            if (win32, darwin, linux2) not in all_mappings:
                all_mappings.append((win32, darwin, linux2))

    mapping_string = ';'.join(itertools.chain(*list(all_mappings)))
    mapping_string += ';y:/td/aces_1.0.3;/Volumes/pipeline/td/aces_1.0.3;/mnt/publish;'

    preference_node = nuke.toNode('preferences')
    preference_node['platformPathRemaps'].fromScript(mapping_string)

    net_log.get_logger().debug('hiero platform path remaps completed')


def set_abc_read_method():
    preference_node = nuke.toNode('preferences')
    preference_node['DfltAbcAlwaysCreateAllInOne'].setValue(True)


def set_ocio(version='1.0.3'):
    def callback():
        root_node = nuke.root()
        root_node['colorManagement'].setValue('OCIO')
        root_node['OCIO_config'].setValue('aces_{}'.format(version))

    nuke.addOnCreate(callback, nodeClass="Root")
