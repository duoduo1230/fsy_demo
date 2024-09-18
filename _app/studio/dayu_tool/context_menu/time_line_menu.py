#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'

import functools
import hiero.ui  as hui
import hiero.core as hcore

from ui_center.qt import *
from app._hiero.open_shotgun_web import open_shotgun_web
from ui_center.build_track_dialog import MBuildTrackDialog
from ui_center.update_track_dialog import MUpdateTrackDialog
from ui_center.io_export_dialog import MIOExportDialog
from ui_center.add_to_bookmark_dialog import MAddToBookmarkDialog
from app._hiero.trackitem_analyize import TrackItemAnalyizeDialog


def time_line_event_handler(event):
    if not hasattr(event.sender, 'selection'):
        return

    s = event.sender.selection()
    if not s:
        return

    track_item_selection = [item for item in s if isinstance(item, hcore.TrackItem)]
    track_selection = [item for item in s if isinstance(item, hcore.VideoTrack)]

    if len(track_item_selection) >= 1 and len(track_selection) >= 1:
        hcore.log.debug('Selection must either be a Shot selection or a Track Selection')
        return

    if len(track_item_selection) >= 1:
        trackitem_analyize_action = QAction("trackitem_analyize", hui.mainWindow())
        trackitem_analyize_action.triggered.connect(slot_trackitem_analyize)
        hui.insertMenuAction(trackitem_analyize_action, event.menu)

        auto_sorted_timeline_action = QAction("DaYu Delete Gap", hui.mainWindow())
        auto_sorted_timeline_action.triggered.connect(slot_auto_sorted_timeline)
        hui.insertMenuAction(auto_sorted_timeline_action, event.menu)

        delete_red_timeline_action = QAction("DaYu Delete Red", hui.mainWindow())
        delete_red_timeline_action.triggered.connect(slot_auto_delete_red)
        hui.insertMenuAction(delete_red_timeline_action, event.menu)

        add_to_bookmark_action = QAction("DaYu Add to Bookmark", hui.mainWindow())
        add_to_bookmark_action.triggered.connect(functools.partial(slot_add_to_bookmark, track_item_selection))
        hui.insertMenuAction(add_to_bookmark_action, event.menu)

        open_shotgun_web_action = QAction("DaYu Open Shotgun Web", hui.mainWindow())
        open_shotgun_web_action.triggered.connect(functools.partial(slot_open_shotgun_web, track_item_selection))
        hui.insertMenuAction(open_shotgun_web_action, event.menu)

        create_playlist_action = QAction("DaYu Create SG Playlist", hui.mainWindow())
        create_playlist_action.triggered.connect(functools.partial(slot_create_playlist, track_item_selection))
        hui.insertMenuAction(create_playlist_action, event.menu)

        build_track_from_bookmark_action = QAction("DaYu Build Track From Bookmark", hui.mainWindow())
        build_track_from_bookmark_action.triggered.connect(functools.partial(slot_build_bookmark, track_item_selection))
        hui.insertMenuAction(build_track_from_bookmark_action, event.menu)

        build_track_from_bookmark_action = QAction("DaYu Build Track From Folder", hui.mainWindow())
        build_track_from_bookmark_action.triggered.connect(functools.partial(slot_build_bookmark_from_folder,
                                                                             track_item_selection))
        hui.insertMenuAction(build_track_from_bookmark_action, event.menu)

        build_track_action = QAction("DaYu Build Track", hui.mainWindow())
        build_track_action.triggered.connect(functools.partial(slot_build_track, track_item_selection))
        hui.insertMenuAction(build_track_action, event.menu)

        show_shot_status_action = QAction("DaYu Show Shot Status", hui.mainWindow())
        show_shot_status_action.triggered.connect(functools.partial(slot_show_shot_status, track_item_selection))
        hui.insertMenuAction(show_shot_status_action, event.menu)

        show_shot_status_action2 = QAction("DaYu Show Shot Status2", hui.mainWindow())
        show_shot_status_action2.triggered.connect(functools.partial(slot_show_shot_status2, track_item_selection))
        hui.insertMenuAction(show_shot_status_action2, event.menu)

        show_version_status_action = QAction("DaYu Show Version Status", hui.mainWindow())
        show_version_status_action.triggered.connect(functools.partial(slot_show_version_status, track_item_selection))
        hui.insertMenuAction(show_version_status_action, event.menu)

        show_description_action = QAction("DaYu Show Description", hui.mainWindow())
        show_description_action.triggered.connect(functools.partial(slot_show_description, track_item_selection))
        hui.insertMenuAction(show_description_action, event.menu)

        check_update_action = QAction("DaYu Check Update TimeLine", hui.mainWindow())
        check_update_action.triggered.connect(functools.partial(slot_show_check_update, track_item_selection))
        hui.insertMenuAction(check_update_action, event.menu)

        update_track_action = QAction("DaYu Update Track", hui.mainWindow())
        update_track_action.triggered.connect(functools.partial(slot_update_track, track_item_selection))
        hui.insertMenuAction(update_track_action, event.menu)

        upload_plate_action = QAction("DaYu Upload Plate", hui.mainWindow())
        upload_plate_action.triggered.connect(functools.partial(slot_upload_plate, track_item_selection))
        hui.insertMenuAction(upload_plate_action, event.menu)

        upload_edit_action = QAction('DaYu Upload Edit', hui.mainWindow())
        upload_edit_action.triggered.connect(functools.partial(slot_upload_edit, track_item_selection))
        hui.insertMenuAction(upload_edit_action, event.menu)

        return

    if len(track_selection) >= 1:
        track = track_selection[0]

        trackitem_analyize_action = QAction("trackitem_analyize", hui.mainWindow())
        trackitem_analyize_action.triggered.connect(slot_trackitem_analyize)
        hui.insertMenuAction(trackitem_analyize_action, event.menu)

        add_to_bookmark_action = QAction("DaYu Add to Bookmark", hui.mainWindow())
        add_to_bookmark_action.triggered.connect(functools.partial(slot_add_to_bookmark, track.items()))
        hui.insertMenuAction(add_to_bookmark_action, event.menu)

        build_track_action = QAction('DaYu Build Track', hui.mainWindow())
        build_track_action.triggered.connect(functools.partial(slot_build_track, track.items()))
        hui.insertMenuAction(build_track_action, event.menu)

        update_track_action = QAction('DaYu Update Track', hui.mainWindow())
        update_track_action.triggered.connect(functools.partial(slot_update_track, track.items()))
        hui.insertMenuAction(update_track_action, event.menu)

        upload_plate_action = QAction('DaYu Upload Plate', hui.mainWindow())
        upload_plate_action.triggered.connect(functools.partial(slot_upload_plate, track.items()))
        hui.insertMenuAction(upload_plate_action, event.menu)

        upload_edit_action = QAction('DaYu Upload Edit', hui.mainWindow())
        upload_edit_action.triggered.connect(functools.partial(slot_upload_edit, track.items()))
        hui.insertMenuAction(upload_edit_action, event.menu)

        return


@Slot(list)
def slot_build_track(track_item_list):
    window = MBuildTrackDialog(hui.mainWindow())
    window.setWindowFlags(Qt.Window)
    window.set_item_list(track_item_list)
    window.show()


@Slot(list)
def slot_update_track(track_item_list):
    window = MUpdateTrackDialog(hui.mainWindow())
    window.setWindowFlags(Qt.Window)
    window.set_item_list(track_item_list)
    window.exec_()


@Slot(list)
def slot_add_to_bookmark(track_item_list):
    window = MAddToBookmarkDialog(hui.mainWindow())
    window.setWindowFlags(Qt.Window)
    window.set_item_list(track_item_list)
    window.exec_()


@Slot(list)
def slot_open_shotgun_web(track_item_list):
    import net_log
    if len(track_item_list) > 10:
        net_log.get_logger().warning('you should select less than 10 item!')
        return
    for t in track_item_list:
        project, shot = t.project().name(), t.name()
        if project and shot:
            open_shotgun_web(project, shot)


@Slot(list)
def slot_create_playlist(track_item_list):
    from app._hiero.create_playlist import CreatePlaylistWidget
    win = CreatePlaylistWidget(hui.mainWindow())
    win.setup_data(track_item_list)
    win.show()
    win.exec_()


@Slot(list)
def slot_build_bookmark(track_item_list):
    from ui_center.minecraft import Minecraft
    widget = Minecraft(parent=hui.mainWindow())
    setattr(widget, 'track_item_list', track_item_list)
    widget.show()


@Slot(list)
def slot_build_bookmark_from_folder(track_item_list):
    from app._hiero.build_track_from_folder import BuildFolderWidget
    win = BuildFolderWidget(hui.mainWindow())
    win.set_item_list(track_item_list)
    win.setWindowFlags(Qt.Window)
    win.exec_()


@Slot(list)
def slot_show_shot_status(track_item_list):
    import sys
    import wrap_shotgun as ws
    sg = ws.MyShotgun()
    project_name = track_item_list[0].project().name()
    for item in track_item_list:
        project = sg.find_one('Project', [['name', 'is', project_name]])
        shot_split = item.name().split('_')[0:2]
        shot_name = '_'.join(shot_split)
        shot = sg.find_one('Shot', [['project', 'is', project], ['code', 'is', shot_name]], ['sg_status_list'])
        text_item = item.parent().createEffect(effectType='Text2', trackItem=item)
        text_node = text_item.node()
        if sys.platform == 'win32':
            text_node['font'].setValue('Consolas', 'Regular')
        text_node['message'].setValue(shot.get('sg_status_list'))
        text_node['xjustify'].setValue('left')
        text_node['yjustify'].setValue('bottom')
        text_node['box'].setValue([0.0, 0.0, 0.0, 0.0])


@Slot(list)
def slot_show_shot_status2(track_item_list):
    import sys
    import wrap_shotgun as ws
    sg = ws.MyShotgun()
    project_name = track_item_list[0].project().name()
    for item in track_item_list:
        project = sg.find_one('Project', [['name', 'is', project_name]])
        shot_split = item.name().split('_')[0:2]
        shot_name = '_'.join(shot_split)
        shot = sg.find_one('Shot', [['project', 'is', project], ['code', 'is', shot_name]], ['sg_status_list'])
        text_item = item.parent().createEffect(effectType='Text2', trackItem=item)
        text_node = text_item.node()
        if sys.platform == 'win32':
            text_node['font'].setValue('Consolas', 'Regular')
        text_node['message'].setValue(shot.get('sg_status_list'))
        text_node['xjustify'].setValue('left')
        text_node['yjustify'].setValue('bottom')
        text_node['box'].setValue([500.0, 0.0, 1300.0, 0.0])


@Slot(list)
def slot_show_version_status(track_item_list):
    import sys
    import wrap_shotgun as ws
    sg = ws.MyShotgun()
    project_name = track_item_list[0].project().name()
    for item in track_item_list:
        project = sg.find_one('Project', [['name', 'is', project_name]])
        version = sg.find_one('Version', [
            ['project', 'is', project], ['code', 'is', item.currentVersion().name()]], ['sg_status_list'])
        text_item = item.parent().createEffect(effectType='Text2', trackItem=item)
        text_node = text_item.node()
        if sys.platform == 'win32':
            text_node['font'].setValue('Consolas', 'Regular')
        text_node['message'].setValue(version.get('sg_status_list'))
        text_node['xjustify'].setValue('left')
        text_node['yjustify'].setValue('bottom')
        text_node['box'].setValue([500.0, 0.0, 1300.0, 0.0])


@Slot(list)
def slot_show_description(track_item_list):
    from app._hiero.tools import show_reel_description
    show_reel_description.run()


@Slot(list)
def slot_show_check_update(track_item_list):
    from app._hiero.tools import check_timeline_update
    check_timeline_update.run()


@Slot(list)
def slot_upload_plate(track_item_list):
    window = MIOExportDialog(hui.mainWindow())
    window.setWindowFlags(Qt.Window)
    window.set_item_list(track_item_list, 'plt')
    if window.exec_():
        items = window.get_legal_items()
        if len(items) > 0:
            seq_obj = items[0].parent().parent()
            time_line_editor = hui.getTimelineEditor(seq_obj)
            time_line_editor.setSelection(items)
            export_action = hui.findMenuAction('Export...')
            export_action.triggered.emit()


@Slot(list)
def slot_upload_edit(track_item_list):
    window = MIOExportDialog(hui.mainWindow())
    window.setWindowFlags(Qt.Window)
    window.set_item_list(track_item_list, 'edt')
    if window.exec_():
        items = window.get_legal_items()
        if len(items) > 0:
            seq_obj = items[0].parent().parent()
            time_line_editor = hui.getTimelineEditor(seq_obj)
            time_line_editor.setSelection(items)
            export_action = hui.findMenuAction('Export...')
            export_action.triggered.emit()


@Slot()
def slot_trackitem_analyize():
    window = TrackItemAnalyizeDialog(hui.mainWindow())
    window.setWindowFlags(Qt.Window)
    window.exec_()


@Slot()
def slot_auto_sorted_timeline():
    import hiero.ui as hui

    timeline = hui.activeView()
    start_time = 0
    track_items = timeline.selection()

    for item in track_items:
        duration = item.duration()
        end_timeline = start_time + duration - 1
        item.setTimelineIn(start_time)
        item.setTimelineOut(end_timeline)
        start_time += duration


@Slot()
def slot_auto_delete_red():
    import hiero.ui as hui

    timeline = hui.activeView()
    track_items = timeline.selection()

    # 创建 新的层级
    new_track = hcore.VideoTrack('red')
    current_sequence = hui.activeSequence()
    current_sequence.addTrack(new_track)

    for item in track_items:
        clip = item.source()
        source_duration = clip.mediaSource().duration()
        new_track_item = new_track.createTrackItem(item.name())
        new_track_item.setSource(clip)
        new_track_item.setSourceOut(new_track_item.sourceIn() + source_duration - 1)

        new_track_item.setTimelineIn(item.timelineIn())
        new_track_item.setTimelineOut(item.timelineIn() + source_duration - 1)
        new_track.addItem(new_track_item)


hcore.events.registerInterest("kShowContextMenu/kTimeline", time_line_event_handler)
hcore.events.registerInterest("kShowContextMenu/kSpreadsheet", time_line_event_handler)
