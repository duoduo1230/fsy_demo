# -*- coding: utf-8 -*-

import maya.cmds as cmds
from maya import mel


def create_definition():
    return mel.eval("hikCreateDefinition();")


def set_definition(character, definition_info):
    for hik_name, d_info in definition_info.items():
        bone = d_info.get('bone')
        hikid = d_info.get('hikid')
        mel_str = 'setCharacterObject("{}", "{}", {}, 0)'.format(bone, character, hikid)
        mel.eval(mel_str)


def hik_initialize():
    mel.eval('HIKCharacterControlsTool();')
    create_definition()
    set_hik_char('Character1')
    cmds.refresh()


def get_hik_source_list():
    mel.eval("HIKCharacterControlsTool;")
    _HUMAN_IK_SOURCE_MENU = "hikSourceList"
    _HUMAN_IK_SOURCE_MENU_OPTION = _HUMAN_IK_SOURCE_MENU + "|OptionMenu"
    items = cmds.optionMenuGrp(_HUMAN_IK_SOURCE_MENU, q=True, ill=True)

    hik_list = []
    for i in xrange(0, len(items)):
        label = cmds.menuItem(items[i], q=True, l=True)
        hik_list.append(label)

    return hik_list


def get_hik_character_list():
    mel.eval("HIKCharacterControlsTool;")
    _HUMAN_IK_CHARACTER_MENU = "hikCharacterList"
    _HUMAN_IK_CHARACTER_MENU_OPTION = _HUMAN_IK_CHARACTER_MENU + "|OptionMenu"
    items = cmds.optionMenuGrp(_HUMAN_IK_CHARACTER_MENU, q=True, ill=True)

    hik_list = []
    for i in xrange(0, len(items)):
        label = cmds.menuItem(items[i], q=True, l=True)
        hik_list.append(label)

    return hik_list


def get_current_hik_character():
    """
    ....Get the current active character definition.
    ...."""

    mel.eval("HIKCharacterControlsTool;")
    char = mel.eval("hikGetCurrentCharacter();")
    return char


def get_current_hik_source():
    mel.eval("HIKCharacterControlsTool;")
    char = mel.eval("hikGetCurrentSource();")
    return char


def hik_update_tool():
    melCode = """
        if ( hikIsCharacterizationToolUICmdPluginLoaded() )
        {
            hikUpdateCharacterList();
            hikUpdateCurrentCharacterFromUI();
            hikUpdateContextualUI();
            hikControlRigSelectionChangedCallback;
            hikUpdateSourceList();
            hikUpdateCurrentSourceFromUI();
            hikUpdateContextualUI();
            hikControlRigSelectionChangedCallback;
        }
        """
    try:
        mel.eval(melCode)
    except:
        pass


def set_hik_char(targetChar):
    mel.eval("HIKCharacterControlsTool;")
    mel.eval('hikSetCurrentCharacter("{0}")'.format(targetChar))
    hik_update_tool()


def set_hik_source_char(source):
    _HUMAN_IK_SOURCE_MENU = "hikSourceList"
    _HUMAN_IK_SOURCE_MENU_OPTION = _HUMAN_IK_SOURCE_MENU + "|OptionMenu"
    items = cmds.optionMenuGrp(_HUMAN_IK_SOURCE_MENU, q=True, ill=True)
    for i in xrange(0, len(items)):
        label = cmds.menuItem(items[i], q=True, l=True)
        #  开头有空格，去掉
        if label.lstrip() == source.lstrip():
            cmds.optionMenu(_HUMAN_IK_SOURCE_MENU_OPTION, e=True, sl=i + 1)
            mel.eval("hikUpdateCurrentSourceFromUI()")
            mel.eval("hikUpdateContextualUI()")
            mel.eval("hikControlRigSelectionChangedCallback")
            break


def is_character_definition(char):
    # Check Node Exists
    if not cmds.objExists(char): return False

    # Check Node Type
    if cmds.objectType(char) != 'HIKCharacterNode': return False

    return True


def get_character_nodes(char):
    # Check Node
    if not is_character_definition(char):
        raise Exception(
            'Invalid character definition node! Object "'
            + char
            + '" does not exist or is not a valid HIKCharacterNode!'
        )

    # Get Character Nodes
    charNodes = mel.eval('hikGetSkeletonNodes "' + char + '"')

    # Return Result
    return charNodes


def bake_to_control_rig():
    return mel.eval("hikBakeToControlRig 0;")


def bake_skeleton():
    return mel.eval("hikBakeCharacter 0;")


def lock_definition():
    return mel.eval("hikToggleLockDefinition();")
