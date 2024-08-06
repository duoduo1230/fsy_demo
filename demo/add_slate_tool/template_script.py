#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import nuke

write_dict = {}
version_data = eval(r"{version_data}")

def create_every_version_node(read_filename, meta_codec_type, out_path, fps, slate, reformat):
    print(123456)
    root = nuke.Root()
    root['fps'].setValue(int(fps))

    read_node = nuke.createNode('Read')
    read_node['raw'].setValue(True)
    read_node.knob('file').fromUserText(read_filename)
    # first_frame = read_node['first'].value()
    # last_frame = read_node['last'].value()

    nuke.createNode(slate)

    if reformat == '2K_2048':
        reformat_node = nuke.createNode('Reformat')
        reformat_node['box_width'].setValue(2048)
        reformat_node['box_height'].setValue(1152)
        reformat_node['type'].setValue('to box')
    else:
        reformat_node = nuke.createNode(reformat)

    write_node = nuke.createNode('Write')
    write_node['file'].setValue(out_path)
    write_node['raw'].setValue(True)
    write_node['file_type'].setValue('mov')
    write_node['meta_codec'].setValue(meta_codec_type)
    write_node['create_directories'].setValue(True)

    write_node.setInput(0, reformat_node)
    write_dict[write_node.name()] = [write_node.firstFrame(), write_node.lastFrame()]
    # write_dict[write_node.name()] = [first_frame, last_frame]
    nuke.scriptSaveAs(filename='D:/temp/demo_tool/PY/demo.nk', overwrite=True)

def start_batch_render():
    for name, version_dict in version_data.items():
        create_every_version_node(**version_dict)

    # start batch render
    for write, frame_range in write_dict.items():
        first_frame, last_frame = frame_range
        nuke.render(write, first_frame, last_frame)


start_batch_render()