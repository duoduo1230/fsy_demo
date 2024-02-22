from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from dayu_widgets import dayu_theme


header_list = [
    {
        "label": "Project",
        "key": "project",
        "checkable": False,
        "searchable": False,
        "width": 400,
        "font": lambda x, y: {"underline": False},
        "icon": "app-batch_create_element_wizard.png",
    },
    ]
data_list = [
    {
        "project": "ep01_0010_comp_master_v0001",
    },
    {
        "project": "ep01_0010_comp_pcomp_v0003",
    },
    {
        "project": "New Resource",
    },
    ]
