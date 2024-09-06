__author__ = 'yangzhuo'

import os
from rv import rvtypes, commands
import PyOpenColorIO as OCIO


default_config = "D:/temp/rv/YZ/OpenColorIO-Config-ACES-1.2/aces_1.2/config.ocio"

class SetRec(rvtypes.MinorMode):

    @staticmethod
    def set_rec709(event):
        print("Log: aaaaaaaaaa")
        print(event)
        event.reject()

    @staticmethod
    def set_en(event):
        print("Log: bbbbbbbbbbbbb")
        print(event)
        event.reject()

        config = OCIO.Config()
        config=config.CreateFromFile(default_config)
        OCIO.SetCurrentConfig(config)
        commands.defineModeMenu("OCIO Source Setup", self.buildOCIOMenu(), True)

    @staticmethod
    def set_re(event):
        print("Log: ccccccccccccc")
        print(event)
        event.reject()

    @staticmethod
    def set_ec(event):
        print("Log: eeeeeeeeeeeeeeeee")
        print(event)
        event.reject()

    def __init__(self):
        rvtypes.MinorMode.__init__(self)

        print("llllllllllllll")

        self.init("set-rec",
                  [
                      ("source-modified", self.set_rec709, ""),
                      ("play-start", self.set_re, ""),
                      ("media-relocated", self.set_ec, ""),
                      ("after-progressive-loading", self.set_en, "")
                  ],
                  None)


def createMode():
    return SetRec()


