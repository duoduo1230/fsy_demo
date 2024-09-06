__author__ = 'yangzhuo'

import os
from rv import rvtypes


class SetRec(rvtypes.MinorMode):

    @staticmethod
    def set_rec709(event):
        event.reject()
        os.environ["RV_OVERRIDE_TRANSFER_MOV"] = "Rec709"

    def __init__(self):
        rvtypes.MinorMode.__init__(self)
        self.init("graph-new-node",  [("graph-new-node", self.set_rec709, "")],  None)


def createMode():
    return SetRec()


