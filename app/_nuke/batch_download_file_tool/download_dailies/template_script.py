#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'

write_dict = {}
config_data = eval(r"{config_data}")
version_data = eval(r"{version_data}")


def create_every_version_node(read_filename, lut_filename, meta_codec_type, cilent_name, out_path, extra_data, fps, time_code,
                              comment, updated_by_name):
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

    time_code_node = nuke.createNode('AddTimeCode')
    time_code_node['startcode'].setValue(time_code)
    if not time_code:
        time_code_node['disable'].setValue(True)

    slate_node = nuke.createNode(config_data.get('slate') or 'xyzs_slate')
    client_file_node = nuke.createNode('Text')
    if config_data.get('slate'):
        slate_node['dayu_orm_version'].setValue(extra_data)
        slate_node['set_info'].execute()
        if slate_node.knob('artist'):
            slate_node.knob('artist').setValue(updated_by_name)
        if slate_node.knob('notes'):
            if comment:
                slate_node.knob('notes').setValue(comment.encode('utf-8'))
    else:
        slate_node['disable'].setValue(True)

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
    write_node.setInput(0, client_file_node)

    read_node.setInput(0, time_code_node)
    color_space_node_input = nuke.createNode('OCIOColorSpace')
    color_space_node_input.setInput(0, time_code_node)
    color_space_input = config_data.get('color_space_input', '')
    if color_space_input:
        color_space_node_input['in_colorspace'].setValue(color_space_input.get('in_colorspace'))
        color_space_node_input['out_colorspace'].setValue(color_space_input.get('out_colorspace'))
    else:
        color_space_node_input['disable'].setValue(True)

    ocio_file_transform_node = nuke.createNode('OCIOFileTransform')
    ocio_file_transform_node.setInput(0, color_space_node_input)
    if lut_filename:
        ocio_file_transform_node['file'].setValue(lut_filename)
        ocio_file_transform_node['working_space'].setValue(config_data.get('working_space', ''))
    else:
        ocio_file_transform_node['disable'].setValue(True)

    color_space_node_out = nuke.createNode('OCIOColorSpace')
    color_space_node_out.setInput(0, ocio_file_transform_node)
    color_space_out = config_data.get('color_space_output', '')
    if color_space_out:
        color_space_node_out['in_colorspace'].setValue(color_space_out.get('in_colorspace'))
        color_space_node_out['out_colorspace'].setValue(color_space_out.get('out_colorspace'))
    else:
        color_space_node_out['disable'].setValue(True)

    slate_node.setInput(1, color_space_node_out)

    if cilent_name and read_filename.split("/")[3] == "mzh":
        client_file_node['message'].setValue(cilent_name)
        client_file_node['scale'].setValue(0.7)
        client_file_node['box'].setValue([-311.0, -411.0, 649.0, 129.0])

    elif cilent_name and read_filename.split("/")[3] == "fc2":
        client_file_node['message'].setValue(cilent_name)
        client_file_node['scale'].setValue(0.7)
        client_file_node['box'].setValue([-280.0, -385.0, 649.0, 129.0])

    else:
        client_file_node['disable'].setValue(True)

    client_file_node.setInput(0, slate_node)

    write_dict[write_node.name()] = [write_node.firstFrame(), write_node.lastFrame()]

    nuke.scriptSaveAs(filename='D:/temp/ors2/project/OUT.nk', overwrite=True)

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
    for write, frame_range in write_dict.items():
        first_frame, last_frame = frame_range
        nuke.render(write, first_frame, last_frame)


start_batch_render()

