# -*- coding: utf-8 -*-

name = "Magician_Toolbox"

uuid = "5c93da6a-9bce-4372-9d01-cc22ae266662"

fp_project = "Magician"
compiler = ['python-2.7']
requires = [
    'magician_Qt',
    'magician_yaml',
    'magician_pathlib',
    'magician_dayu_widgets',
    'magician_pymysql',
    'magician_sql'
]

build_command = "python {root}/build.py {install}"


def commands():
    """Setup environment variables."""
    env.PYTHONPATH.append("{root}/scripts")
    env.MF_MENU_CONFIG.append("{root}/scripts/Magician_Toolbox/config/menu_config.yaml")
    env.Magician_Toolbox = "{root}/scripts/Magician_Toolbox"
    env.XBMLANGPATH = "{root}/scripts/Magician_Toolbox/icons_shelf"


@early()
def version():
    """Get version.

    Returns:
        str: Version of this build.
    """
    import os
    tag = os.getenv("BK_CI_GIT_REPO_REF")
    if tag is not None:
        return tag
    else:
        from pkgm.version_utils import get_dev_version
        return get_dev_version(name)
