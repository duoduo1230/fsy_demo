#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'

write_dict = {}
config_data = eval(r"{config_data}")
version_data = eval(r"{version_data}")


def create_every_version_node(read_filename, shot_name, file_type, out_path, fps, time_code, description, meta_codec_type):
    import nuke
    root = nuke.Root()
    for attr in config_data.get('root_sorted'):
        root[attr].setValue(config_data.get('root').get(attr))
    root['fps'].setValue(fps)

    read_node = nuke.createNode('Read')
    read_node['raw'].setValue(True)
    read_node.knob('file').fromUserText(read_filename)
    first_frame = read_node['first'].value()
    last_frame = read_node['last'].value()
    frame_range = str(first_frame) + '_' + str(last_frame)

    if file_type == 'asset':
        slate_node = nuke.createNode('rs_ass_slate')
    else:
        slate_node = nuke.createNode('rs_slate')
    slate_node.setInput(1, read_node)

    # 创建 时间 节点
    time_text = nuke.createNode("Text2")
    # frame_text['name'].setValue("Frame_value")
    time_text['message'].setValue(' [date %D] ')
    time_text['global_font_scale'].setValue(0.5)
    time_text['font'].setValue('Bitstream Charter', 'Regular')
    time_text['box'].setValue([240, 733, 560, 780])
    time_text['opacity'].setAnimated()
    time_text['opacity'].setValueAt(1, 1000)
    time_text['opacity'].setValueAt(0, 1001)

    # 创建 Frame_value 节点
    frame_text = nuke.createNode("Text2")
    # frame_text['name'].setValue("Frame_value")
    frame_text['message'].setValue(frame_range)
    frame_text['global_font_scale'].setValue(0.5)
    frame_text['font'].setValue('Bitstream Charter', 'Regular')
    frame_text['box'].setValue([286.0, 655.0, 749.0, 715.0])
    frame_text['opacity'].setAnimated()
    frame_text['opacity'].setValueAt(1, 1000)
    frame_text['opacity'].setValueAt(0, 1001)

    # 创建 镜头名字 节点
    name_text = nuke.createNode("Text2")
    # name_text['name'].setValue("Name_value")
    name_text['message'].setValue(shot_name)
    name_text['global_font_scale'].setValue(0.5)
    name_text['font'].setValue('Bitstream Charter', 'Regular')
    name_text['box'].setValue([389.0, 600.0, 1210.5, 645.0])
    name_text['opacity'].setAnimated()
    name_text['opacity'].setValueAt(1, 1000)
    name_text['opacity'].setValueAt(0, 1001)

    # 创建 描述 节点
    description_text = nuke.createNode("Text2")
    # description_text['name'].setValue("Description_value")
    description_text['message'].setValue(description)
    description_text['global_font_scale'].setValue(0.5)
    description_text['font'].setValue('KaiTi', 'Regular')
    description_text['box'].setValue([408, 332, 1668, 572])
    description_text['opacity'].setAnimated()
    description_text['opacity'].setValueAt(1, 1000)
    description_text['opacity'].setValueAt(0, 1001)

    # 创建 镜头名字 节点
    shot_name_text = nuke.createNode("Text2")
    # shot_name_text['name'].setValue("shot_name")
    shot_name_text['message'].setValue(shot_name)
    shot_name_text['global_font_scale'].setValue(0.2)
    shot_name_text['font'].setValue('Bitstream Charter', 'Regular')
    shot_name_text['box'].setValue([950, 0.1, 1180, 21.1])
    shot_name_text['opacity'].setAnimated()
    shot_name_text['opacity'].setValueAt(0, 1000)
    shot_name_text['opacity'].setValueAt(1, 1001)

    # 创建 时间码 节点
    shot_name_text = nuke.createNode("Text2")
    # shot_name_text['name'].setValue("timecode")
    shot_name_text['message'].setValue(time_code)
    shot_name_text['global_font_scale'].setValue(0.2)
    shot_name_text['font'].setValue('Bitstream Charter', 'Regular')
    shot_name_text['box'].setValue([15, 0, 214, 21.3])
    shot_name_text['opacity'].setAnimated()
    shot_name_text['opacity'].setValueAt(0, 1000)
    shot_name_text['opacity'].setValueAt(1, 1001)

    # 创建输出节点
    write_node = nuke.createNode('Write')
    write_node['file'].setValue(out_path)
    write_node['raw'].setValue(True)
    write_node['file_type'].setValue('mov')
    write_node['mov32_fps'].setValue(fps)
    write_node['meta_codec'].setValue(meta_codec_type)
    write_node['create_directories'].setValue(True)
    if write_node.knob('mov32_write_timecode'):
        write_node.knob('mov32_write_timecode').setValue(True)
    elif write_node.knob('mov64_write_timecode'):
        write_node.knob('mov64_write_timecode').setValue(True)

    write_dict[write_node.name()] = [1000, write_node.lastFrame()]

def start_batch_render():
    import os
    import nuke

    nuke.pluginAddPath(r'Y:/td/dayu_app_fitment/nuke/nodes/phenom_user/gizmos')
    nuke.pluginAddPath(r'Y:/td/dayu_app_fitment/nuke/nodes/all_menu/strilen_kit')
    os.environ['PYTHONPATH'] += r';Y:/td/dayu_python_lib/win32'
    # batch create node
    for _, version_dict in version_data.items():
        create_every_version_node(**version_dict)

    # start batch render
    # nuke.scriptSaveAs(filename='D:/temp/ors2/project/OUT124.nk', overwrite=True)
    for write, frame_range in write_dict.items():
        first_frame, last_frame = frame_range
        nuke.render(write, first_frame, last_frame)


start_batch_render()

