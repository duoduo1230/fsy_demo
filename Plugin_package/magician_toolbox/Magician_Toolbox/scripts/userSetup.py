# -*- coding: utf-8 -*-
import os
import pymel.core as pm
import maya.cmds as cmds

try:
    from shiboken import wrapInstance
except ImportError:
    from shiboken2 import wrapInstance

from Magician_Toolbox import magician_toolbox


def build_button_magician():
    command = 'from Magician_Toolbox import magician_toolbox;magician_toolbox.main()'

    program_name = 'MF_Toolbox'
    package_path = os.environ["Magician_Toolbox"]
    icon_path = "{}/{}".format(package_path, "icons/morefun.svg")
    if cmds.iconTextButton(program_name, ex=True):
        cmds.deleteUI(program_name)
    cmds.iconTextButton(program_name, i=icon_path,
                        w=150, h=30,
                        c=command, stp='python',
                        p=cmds.iconTextButton('statusFieldButton', q=True, p=True))


if __name__ == "__main__":
    if not cmds.about(batch=True):
        pm.evalDeferred(magician_toolbox.main)
        pm.evalDeferred(build_button_magician)
