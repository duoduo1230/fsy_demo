#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'

from app.action_base import MActionBase
from app._hiero import vcs
from db.disk_path import SequentialFiles
from db.sub_level import SubLevel


class BuildBookmark(MActionBase):
    def __init__(self, parent=None):
        super(BuildBookmark, self).__init__(parent)
        self.name = self.tr('DaYu Build Track')
        self.icon = 'icon-import-file.png'

    def validate(self, event, **kwargs):
        # 只要选中的 item中有 file 即可
        return event.selection and any(getattr(orm, '__tablename__', '') == 'file' for orm in event.selection)

    def run(self, event, **kwargs):

        import hiero
        import hiero.ui as hui
        import hiero.core as hcore
        import app._hiero.api.node_op.read_a0001 as h_read_a0001

        track_item_list = event.extra.get('parent_menu').parent().parent().parent().parent().parent().parent().parent().track_item_list
        if event.selection and len(event.selection) >= 1:
            hiero_version_scanner = hiero.core.VersionScanner.VersionScanner()
            current_project = hui.activeSequence().project()
            track_item_dict = {x.name(): x for x in track_item_list}
            version_list = event.selection

            version_dict = {}
            for x in version_list:
                type_list = version_dict.setdefault(x.find_meaning('TYPE').name, [])
                type_list.append(x)

            for _, version_list_ in version_dict.items():
                with current_project.beginUndo('build new track'):
                    current_sequence = hui.activeSequence()
                    new_track = hcore.VideoTrack('bookmark track item')
                    current_sequence.addTrack(new_track)

                    for version_orm in version_list_:
                        resource_name = '_'.join(version_orm.name.split('_')[:-3])
                        select_item = track_item_dict.get(resource_name, None)
                        if not select_item:
                            continue
                        if version_orm.type_group_name == 'dailies':
                            sub_file = next((x for x in version_orm.sub_level.walk(collapse=False, relative=True) if 'mov/' in x), None)
                            print '------- build file -------', version_orm.name
                            filename = SubLevel(version_orm.sub_level.disk_path().child(sub_file.split('/')[0], sub_file.split('/')[1]))
                            seq_file = SequentialFiles(filename=filename, frames=[], missing=[])
                            binitem = h_read_a0001.create(seq_file, version_orm, 'mov')
                        elif version_orm.type_group_name == 'element':
                            sub_level_ = next((s for s in version_orm.flatten() if '/mov' in s.get('sub_level')
                                               and s.get('orm').name == version_orm.name), None)

                            if not sub_level_:
                                sub_level_ = next((s for s in version_orm.flatten() if s['file'].filename.ext == '.mov'
                                                   and s.get('orm').name == version_orm.name), None)

                            level_list = ['/exr', '/dpx', '/jpg']
                            ext = ''
                            for level in level_list:
                                temp_level = next((s for s in version_orm.flatten() if level in s.get('sub_level')
                                                   and s.get('orm').name == version_orm.name), None)
                                if temp_level:
                                    sub_level_ = temp_level
                                    ext = level.lstrip('/')
                                    break

                            seq_file = sub_level_.get('file')

                            binitem = h_read_a0001.create(seq_file, version_orm, ext)

                        # 重新扫描所有的hiero version
                        hiero_version_scanner.doScan(binitem.activeVersion())
                        hiero_version = next((x for x in binitem.items() if x.name() == str(version_orm.name)), None)
                        binitem.setActiveVersion(hiero_version)
                        clip = binitem.activeItem()

                        clip.rescan()
                        new_track_item = new_track.createTrackItem(binitem.name())
                        new_track_item.setSource(clip)
                        duration = select_item.duration()
                        new_track_item.setSourceOut(new_track_item.sourceIn() + duration - 1)

                        new_track_item.setTimelineIn(select_item.timelineIn())
                        new_track_item.setTimelineOut(select_item.timelineIn() + duration - 1)
                        vcs.add_secret_info(new_track_item, version_orm.parent)
                        new_track.addItem(new_track_item)


def get_action():
    return BuildBookmark()

