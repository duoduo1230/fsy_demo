# -*- coding: utf-8 -*-

import sys
sys.path.append(r"D:\FSY\maya\out_materials")
sys.path.append(r"D:\FSY\maya\add_materials")

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

    menu_name = "dayu2.0"

    # 检查菜单是否存在
    delete_menu(menu_name, menu_name)

    # get maya main window 获取maya主菜单
    get_main_window = mel.eval('$tmpVar=$gMainWindow') 

    # create menu
    toolkit_menu = cmds.menu(menu_name, label=menu_name, tearOff=True, parent=get_main_window) # tearOff=True 可以弹出

    # create Import Material
    cmds.menuItem(label="Import Material", parent=toolkit_menu, command="import add_materials;reload(add_materials);win = add_materials.Window1();win.show()") #parent=toolkit_menu 写入toolkit_menu下

    # create divider 分割线
    cmds.menuItem(divider=True)

    # create Export Material
    cmds.menuItem(label="Export Material", parent=toolkit_menu, command="import out_materials;reload(out_materials);win = out_materials.Window1();win.show()")

    # 创建子菜单
    sub_menu = cmds.menuItem("publish_to", label="publish_to", subMenu=True, tearOff=True, parent=toolkit_menu)
    cmds.menuItem(label="check", parent=sub_menu, command="print('publish')")


# 延迟执行函数
m_utils.executeDeferred(init_menu)