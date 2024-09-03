# -*- coding: utf-8 -*-
import sys
sys.path.append(r"D:\My_code\fsy_demo\demo")
sys.path.append(r'D:\My_code\fsy_demo\demo\qc_tool\qc_widget')
sys.path.append(r'D:\My_code\fsy_demo\third_package\win32')
sys.path.append(r'D:\My_code\fsy_demo\demo\retarget')
sys.path.append(r'D:\My_code\fsy_demo\demo\retarget\packages')

import maya.cmds as cmds
import maya.mel as mel
import maya.utils as m_utils


# 定义一个检查菜单栏是否存在的函数，存在删除，不存pass
def delete_menu(menu_name, menu_label):
    try:
        if cmds.menu(menu_name, l=menu_label, p='MayaWindow') != 0:
            cmds.deleteUI(cmds.menu(menu_name, l=menu_label, e=1, dai=1))
            cmds.deleteUI(menu_name)
    except:
        pass

    cmds.refresh()

def init_menu():

    print(u">>>>>>>>>>>>>>>创建菜单栏<<<<<<<<<<<<<<<<<")
    menu_name = "Tool"

    # 检查菜单是否存在
    delete_menu(menu_name, menu_name)

    # get maya main window 获取maya主菜单
    gMainWindow = mel.eval('$tmpVar=$gMainWindow')

    # 创建 menu
    toolkit_menu = cmds.menu(menu_name, label=menu_name, tearOff=True, parent=gMainWindow) # tearOff=True 可以弹出

    # 创建 QC
    cmds.menuItem(label="QC Manager", parent=toolkit_menu, command="import QC_widget;reload(QC_widget);QC_widget.main()")

    # 创建分割线
    cmds.menuItem(divider=True)

    # 创建 Human IK
    cmds.menuItem(label="Create Human IK", parent=toolkit_menu,
                  command="from create_human_ik import create_humanIK_widget;reload(create_humanIK_widget);create_humanIK_widget.main()")

    # 创建retarget
    cmds.menuItem(label="Retarget Tool", parent=toolkit_menu,
                  command="from retarget import ani_retarget_widget;reload(ani_retarget_widget);ani_retarget_widget.main()")

    # 创建分割线
    cmds.menuItem(divider=True)

    # 创建拍屏
    cmds.menuItem(label="Playblast", parent=toolkit_menu,
                  command="import pb_with_shotmask;from pb_with_shotmask import playblast_mask_UI;reload(playblast_mask_UI);playblast_mask_UI.main()")

# 延迟执行函数
m_utils.executeDeferred(init_menu)