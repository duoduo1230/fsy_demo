#!/usr/bin/pythont
# -*- coding: utf-8 -*-

import re
import os
import glob
import pathlib
import traceback
from xml.dom.minidom import parse
import maya.cmds as cmds
import pymel.core as pm
from maya import mel

import FBX_Scene
import humanIK_api

reload(FBX_Scene)
reload(humanIK_api)


def sub_ascii(string):
    """
    替换字符串中的ASCII码，例如 "FBXASC049nrt00T0FBXASC032Trall" -> "1nrt00T0Trall"
    :param string: <list>
    """

    def replace_ascii(match):
        ascii_code = int(match.group(1))
        return chr(ascii_code)

    new_name = re.sub(r'FBXASC(\d{3})', replace_ascii, string)
    return new_name


def sub_fbx_node_name(fbx):
    """
    处理FBX的节点名称不带空格和数字开头。例如'1nrt00T0 L foot bone03' -> 'Lfootbone03'
    """
    fbx = FBX_Scene.FBX_Class(fbx)
    nodes = fbx.get_scene_nodes()
    for node in nodes:
        orig_name = node.GetName()  # 1nrt00T0 L foot bone03
        if " " not in orig_name:
            continue
        new_name = "".join(orig_name.split(" ")[1:])
        node.SetName(new_name)
    fbx.save()


def parse_definition_xml(xml_path):
    """
    解析XML文件，获取XML中的节点信息
    :param xml_path:
    :return:
    """
    result = {}
    dom_tree = parse(xml_path)
    root_node = dom_tree.documentElement
    items = root_node.getElementsByTagName("item")
    for index, item in enumerate(items):
        value = item.getAttribute("value")
        if value:
            key = item.getAttribute("key")
            result[key] = {
                "bone": value,
                "hikid": index
            }
    return result


def remove_import_nodes():
    default_node = ['persp', 'top', 'front', 'side']
    for i in cmds.ls(assemblies=1):
        if cmds.referenceQuery(i, isNodeReferenced=True):
            continue
        elif i in default_node:  # without namespace
            continue
        cmds.delete(i)


def bake(objects, start, end):
    # Bake Animation
    cmds.bakeResults(
        objects,
        simulation=False,
        t=(start, end),
        sampleBy=1,
        oversamplingRate=1,
        disableImplicitControl=True,
        preserveOutsideKeys=False,
        sparseAnimCurveBake=False,
        removeBakedAttributeFromLayer=False,
        bakeOnOverrideLayer=False,
        minimizeRotation=True
    )


def fbx_parameter():
    """设置输出fbx预设"""
    if not pm.pluginInfo("fbxmaya", q=True, loaded=True):
        pm.loadPlugin("fbxmaya")
    pm.mel.eval("FBXResetExport")  # ----------------------------------- 重置设置
    pm.mel.eval("FBXExportFileVersion -v FBX201600")  # ---------------- FBX版本
    pm.mel.eval("FBXExportInAscii -v false")  # ------------------------ 使用Binary编码导出
    # pm.mel.eval("FBXExportInAscii -v %s" % str(self.debug).lower())  # - 使用Ascii|Binary编码导出
    pm.mel.eval("FBXExportScaleFactor 1.0")  # ------------------------- 使用缩放比，不要在输出的时候改变比例，关闭
    pm.mel.eval("FBXExportUpAxis y")  # -------------------------------- y 轴向上
    pm.mel.eval("FBXExportIncludeChildren -v false")  # ---------------- 导出子对象即使它未选中，仅导出选中，关闭
    pm.mel.eval("FBXExportLights -v false")  # ------------------------- 导出灯光， 默认不需要
    pm.mel.eval("FBXExportCameras -v true")  # ------------------------- 导出摄像机
    pm.mel.eval("FBXExportSmoothingGroups -v false")  # ---------------- 软硬边转换为光滑组，保持软硬边信息，关闭
    pm.mel.eval("FBXExportSmoothMesh -v false")  # --------------------- 导出细分信息，需导出原始模型，关闭
    pm.mel.eval("FBXExportTriangulate -v true")  # --------------------- 以三角面导出Mesh, 为保持maya计算结果，开启
    pm.mel.eval("FBXExportEmbeddedTextures -v false")  # --------------- 导出FBX嵌入贴图，关闭
    pm.mel.eval("FBXExportShapes -v true")  # - 导出 blendshape 混合变形
    pm.mel.eval("FBXExportConstraints -v false")  # -------------------- 导出约束关系，输出前都会bake, 关闭
    pm.mel.eval("FBXExportSkins -v false")  # -------------------------- 导出蒙皮信息，关闭
    pm.mel.eval("FBXExportBakeResampleAnimation -v true")  # ---------- 导出时bake动画， 提前bake过，关闭
    pm.mel.eval("FBXExportInputConnections -v false")  # ----------------避免控制器被导出 关闭
    pm.mel.eval("FBXExportUseSceneName -v false")  # -------------------- 默认动画会使用 Take 001, 开启则使用文件名


def export_fbx(sel, in_path):
    fbx_parameter()
    pm.select(sel, r=1)
    print('FBXExport -f "{0}" -s'.format(str(in_path).replace("\\", "/")))
    mel.eval('FBXExport -f "{0}" -s'.format(str(in_path).replace("\\", "/")))


def remove_namespace(self):
    """
    Remove all namespaces from all nodes
    This is not an ideal method but
    """
    self.get_scene_nodes()
    for node in self.scene_nodes:
        orig_name = node.GetName()
        split_by_colon = orig_name.split(':')
        if len(split_by_colon) > 1:
            new_name = split_by_colon[-1:][0]
            node.SetName(new_name)
    return True


def clear_skeletal():
    """
    清理骨骼名称，删除关键，初始化T-pose
    """
    nodes = cmds.ls(type=("joint"))
    # 删除关键帧
    cmds.cutKey(nodes, clear=True)
    # 替换ascii码
    for node in nodes:
        new_name = sub_ascii(node)
        if " " not in new_name:
            continue
        new_name = "".join(new_name.split(" ")[1:])
        cmds.rename(node, new_name)
    # T-pose
    for i in ["LUpperArm", "RUpperArm"]:
        arm = cmds.ls("*{}".format(i))
        if not arm:
            continue
        for r in ["rx", "ry", "rz"]:
            cmds.setAttr("{}.{}".format(arm[0], r), 0)


def get_frame_range():
    """
    从所有骨骼上获取所有动画帧，取最小和最大为第一帧和最后一帧
    :return: <tuple>
    """
    start, end = 0, 0
    joints = cmds.ls(long=True, type="joint")
    cmds.select(joints)
    all_keys = sorted(cmds.keyframe(joints, q=True) or [])
    if all_keys:
        start = int(all_keys[0])
        end = int(all_keys[-1])
    return start, end


def create_custom_humanik(template_file):
    # 清理骨骼
    # clear_skeletal()
    #
    humanIK_api.hik_initialize()
    # 获取template模板信息
    result = parse_definition_xml(template_file)

    # 此处得到的root是None
    root = result.get("Hips").get("bone")
    # 选中骨骼
    cmds.select(root)
    # 设置骨骼定义
    humanIK_api.set_definition("Character1", result)
    try:
        humanIK_api.lock_definition()
    except:
        pass
    humanIK_api.hik_update_tool()


def batch_retarget(character, source, animation_fbx, output, fps=60):
    character_path = pathlib.Path(character)
    anim_path = pathlib.Path(animation_fbx)
    namespace = character_path.stem

    # 方法将路径中的反斜杠 \ 转换为正斜杠 /
    # anim_path.as_posix()

    error = False
    error_info = ""
    try:
        # 这里的fbx_file返回的是什么？
        # 这个方法不太明白
        # <batch_retarget.FBX_Scene.FBX_Class object at 0x00000272565774A8>
        # (1, 173)
        fbx_file = FBX_Scene.FBX_Class(anim_path.as_posix())
        print('_______________________________')
        print(fbx_file)
        start, end = fbx_file.get_time_range()
        print(start, end)

        if not start and not end:
            start, end = get_frame_range()
        fbx_file.close()

        # 新建场景
        cmds.file(force=True, new=True)

        # 引用source绑定文件
        print(">>> Reference {}...".format(source))
        cmds.file(source, r=True, options="v=0;", namespace=":")
        current_source = humanIK_api.get_current_hik_character()

        # 导入source绑定的max动画文件
        print(">>> Import {}...".format(anim_path.as_posix()))
        cmds.file(anim_path.as_posix(), i=True)
        cmds.playbackOptions(animationStartTime=start, minTime=start, maxTime=end, animationEndTime=end)

        # 引用character绑定文件并bake control rig
        default_character_list = humanIK_api.get_hik_character_list()
        print(">>> Reference {}...".format(character_path))
        cmds.file(character_path, r=True, namespace=namespace)
        source_list = humanIK_api.get_hik_character_list()
        current_character = list(set(source_list) ^ set(default_character_list))
        humanIK_api.set_hik_char(current_character[0])
        humanIK_api.set_hik_source_char(current_source)
        humanIK_api.bake_skeleton()

        # 设置fps
        set_fps(fps)

        # 移除引用并另存文件
        remove_import_nodes()  # 清理多余节点

        # 清理命名空间
        for rf_node in cmds.ls(rf=1):
            if rf_node == namespace + "RN":
                continue
            cmds.file(removeReference=True, referenceNode=rf_node)
        cmds.file(rename='{}/{}_retarget.ma'.format(output, anim_path.stem))
        cmds.file(force=True, type='mayaAscii', save=True)

        # bake骨骼并导出FBX
        fbx_path = '{}/{}_retarget.fbx'.format(output, anim_path.stem)
        joints = cmds.ls(type="joint")
        bake(joints, start, end)
        export_fbx(joints, fbx_path)

        # 去除FBX的命名空间
        fbx_file = FBX_Scene.FBX_Class(fbx_path.decode('gbk'))
        fbx_file.remove_namespace()
        fbx_file.save(fbx_path.decode('gbk'))

    except Exception as e:
        error = True
        error_info = traceback.format_exc()

    return error, error_info


def create_humanik(ma, template_file, save_path):
    # 新建场景
    cmds.file(force=True, new=True)

    # 导入ma工程文件
    print(">>> Import {}...".format(ma))
    cmds.file(ma, i=True)

    # 创建humanik绑定
    create_custom_humanik(template_file)

    # 保存ma文件
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    cmds.file(rename=save_path)
    cmds.file(force=True, type='mayaAscii', save=True)

    # 修复 nan 值
    clear_file_with_nan(save_path)


def list_fbx_file(path):
    return glob.glob(r"{}\*.fbx".format(path))


def set_fps(fps):
    if fps == 15:
        unit = 'game'
    elif fps == 24:
        unit = 'film'
    elif fps == 25:
        unit = 'pal'
    elif fps == 30:
        unit = 'ntsc'
    elif fps == 48:
        unit = 'show'
    elif fps == 50:
        unit = 'palf'
    elif fps == 60:
        unit = 'ntscf'
    else:
        unit = str(fps) + 'fps'

    cmds.currentUnit(time=unit)
    fps = mel.eval('currentTimeUnitToFPS')
    return fps


def clear_file_with_nan(path):
    """
    清理文件中的 nan
    :param path: <str> MayaAscii文件
    """
    with open(path, "r") as f:
        s = f.read()

    with open(path, 'w') as f:
        s = s.replace("nan(ind)", "0").replace("nan", "0")
        f.write(s)
