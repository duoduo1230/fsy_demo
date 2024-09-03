import sys

import importlib
from importlib import reload

sys.path.append(r'K:\Trash\fanshiyuan\maya_to_ue')

import maya_export
reload(maya_export)

maya_export.main()
