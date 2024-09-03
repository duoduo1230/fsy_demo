import maya.cmds as cmds
import json

path_ = r"D:\temp\ue\ma_json\tst02.json"


def write_json(path, data):
    with open(path, "w") as f:
        temp = json.dumps(data, indent=4)
        f.write(temp)


def main():
    LIST = ["perspShape", "topShape", "frontShape", "sideShape"]
    shape_list = cmds.ls(shapes=True, typ='mesh')
    for i in LIST:
        shape_list.remove(i)

    attr_dict = {}

    for node in shape_list:
        node = str(node)
        shape_parent = cmds.listRelatives(node, parent=True)[0]
        temp = {}
        iter = ["X", "Y", "Z"]
        temp["transform"] = [cmds.getAttr("{}.translate{}".format(shape_parent, i)) for i in iter]
        temp["rotation"] = [cmds.getAttr("{}.rotate{}".format(shape_parent, i)) for i in iter]
        temp["scacle"] = [cmds.getAttr("{}.scale{}".format(shape_parent, i)) for i in iter]

        attr_dict[shape_parent] = temp

    print(attr_dict)

    write_json(path_, attr_dict)










