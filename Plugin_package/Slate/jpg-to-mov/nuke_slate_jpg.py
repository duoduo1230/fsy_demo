# -*- coding: utf-8 -*
import argparse
import os.path
import nuke

# 将jpg序列帧 批量加水印导出mov
# 提交设置好工程文件
SLATE_FILE = r"D:\slate_jpg\output_mzh_mov.nk"
source_folder = r"D:\temp\231213\pcomp_jpg"
target_folder = r"D:\temp\231213\pcomp_mov"


# def get_fix_filename(filename):
#     """
#     @filename: "ep04_1190_ani_prz-audit_v0000"
#
#     @return:
#         ep04_1190_ani_prz-audit_v0000.mov
#     """
#     # filename:
#     import re
#     to_del = filename.split("_")[3]
#     filename = filename.replace(to_del, "")
#     filename = filename.replace('v0', 'v')
#     filename = filename.replace('__', '_')
#
#     return filename
# def get_fix_filename(filename):
#     """
#     @filename: "ep04_1190_ani_ani_v0000"
#
#     @return:
#         ep04_1190_ani_v0000.mov
#     """
#     # filename:
#     import re
#     # to_del = filename.split("_")[3]
#     # filename = filename.replace(to_del, "")
#     filename = filename.replace('v0', 'v')
#     filename = filename.replace("_prz_", '_')
#
#     return filename
# print(filename)


def get_fix_filename(filename):
    """
    @filename: "ep04_1190_ani_ani_v0000"

    @return:
        ep04_1190
    """
    import re
    ep_ = filename.split('_')[0]
    name_ = filename.split('_')[1]
    filename = ep_ + "_" + name_

    return filename


def open_file(nk_file):
    nuke.scriptReadFile(nk_file)


def get_jpg_path(path_):
    """
    ['D:/20230829/aniprz/ep25_2120_ani_prz_v0001/ep25_2120_ani_prz_v0001.%04d.jpg',
    'D:/20230829/aniprz/ep25_3200_ani_prz_v0002/ep25_3200_ani_prz_v0002.%04d.jpg']
    :param path_:
    :return:
    """
    file_list = os.listdir(path_)
    jpg_list = []
    folder_list = []
    for file_name in file_list:
        full_path = os.path.join(path_, file_name)
        folder_list.append(full_path)

    for jpg in folder_list:
        # jpg_path = jpg + "\jpg"
        # first = os.listdir(jpg_path)[0]
        first = os.listdir(jpg)[0]
        file_list02 = first.replace(".1001.jpg", ".%04d.jpg")
        full_path = os.path.join(jpg, file_list02)
        full_jpg_path = full_path.replace("\\", "/")
        jpg_list.append(full_jpg_path)

    return jpg_list


def get_mov_path(jpg_path):
    output_path = os.path.basename(jpg_path)
    # output_path = jpg_path.split("jpg/")[1]
    mov_path = output_path.replace(".%04d.jpg", ".mov")
    mov_full_path = os.path.join(target_folder, mov_path)
    mov_full_path = mov_full_path.replace("\\", "/")
    print("++++++++++++++++++++++++++++++++++++++++++++++++")
    print(mov_full_path)

    file_name = mov_full_path.split("/")[-1]
    old_name_, ss = os.path.splitext(file_name)
    folder_name = old_name_.replace("ep", "EP").replace("v000", "V0")

    # 输出文件夹
    ep = folder_name.split("_")[0]
    sc = folder_name.split("_")[1]
    rf = folder_name.split("_")[4]
    str_list = ["Sp", ep, sc, "TG", rf, "231212"]
    new_folder_name = "_".join(str_list)

    # 输出文件名
    a = old_name_.split("_")[0]
    b = old_name_.split("_")[1]
    new_name_list = [a, b, ]
    new_file_name = "_".join(new_name_list)
    new_file_name = new_file_name + '.mov'

    # 输出路径
    q = mov_full_path.split("/")[0]
    o = mov_full_path.split("/")[1]
    out_put_list = [q, o, new_folder_name, new_file_name]
    mov_output = "/".join(out_put_list)
    print(mov_output)

    return mov_output


def run(input_file, output):
    # jpg_folder = input_file.split('jpg')[0] + "jpg"
    jpg_folder = os.path.dirname(input_file)
    first = os.listdir(jpg_folder)[0]

    first_number = first.split('.')[1]
    print(first_number)

    last = os.listdir(jpg_folder)[-1]
    last_number = last.split('.')[1]
    print(last_number)

    read_node = nuke.toNode('Read_Input')
    read_node["file"].fromUserText(input_file)

    first_frame_knob = read_node.knob('first')
    first_frame_knob.setValue(int(first_number))

    last_frame_knob = read_node.knob('last')
    last_frame_knob.setValue(int(last_number))

    # file_name = get_fix_filename(os.path.basename(input_file))
    # filename_node = nuke.toNode('filename')
    # filename_node["message"].setValue(file_name.split(".")[0])

    write_node = nuke.toNode("Output")
    write_node["file"].setValue(output)

    nuke.execute(write_node, int(first_number), int(last_number))


def main():
    jpg_list = get_jpg_path(source_folder)
    open_file(SLATE_FILE)
    for name in jpg_list:
        output = get_mov_path(name)
        run(name, output)

    nuke.scriptClose()


if __name__ == "__main__":
    main()

# "C:\Program Files\nuke11.2v2\Nuke11.2.exe" -t "D:\slate_jpg\nuke_slate_jpg.py"