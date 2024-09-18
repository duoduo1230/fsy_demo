#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import hiero
from hiero.exporters import FnSubmission
import subprocess
from bin.oiio.stream import *
import re
import sys
import time

frame_regex = re.compile(r'.*[^\dvV](\d{2,})[\D]*.*')
pattern_regex = re.compile(r'.*?(#+).*')


class OiioRenderTask(hiero.core.TaskBase):

    def __init__(self, init_dict):
        print 'ffmpeg render task init!'
        print init_dict
        super(OiioRenderTask, self).__init__(init_dict)
        self.input_file = self._fileinfo.filename()
        self.input_range = (int(self._item.sourceIn()), int(self._item.sourceOut()))
        match = pattern_regex.match(self.resolvedExportPath())
        self.output_file = self.resolvedExportPath()
        if match:
            pp = match.groups()[0]
            self.output_file = self.resolvedExportPath().replace(pp, '%0{}d'.format(len(pp)))
        self._input_colorspace = self._item.source().sourceMediaColourTransform()
        print init_dict.get('preset')._properties
        self._output_colorspace = init_dict.get('preset')._properties.get('output_colorspace')
        self._ocio_config = init_dict.get('preset')._properties.get('ocio_config_path')
        self.output_width = init_dict.get('preset')._properties.get('width')
        self.output_height = init_dict.get('preset')._properties.get('height')
        print self._input_colorspace
        print self._output_colorspace
        print self._ocio_config
        self.fps = self._item.source().framerate().toFloat()
        self._progress = 0.0
        self._frame = 0
        self._finished = False
        self._returncode = None
        self.shell = None

    def startTask(self):
        assert not self.output_file.endswith(('.mov', '.mp4'))
        assert not self.input_file.endswith(('.mov', '.mp4'))

        cmd = OIIO() + \
              Input(self.input_file, self._fileinfo.startFrame() + self.input_range[0],
                    self._fileinfo.startFrame() + self.input_range[1]) + \
              Resize(width=self.output_width, height=self.output_height) + \
              ColorConvert(self._input_colorspace,
                           self._output_colorspace,
                           ocio=self._ocio_config) + \
              Output(self.output_file, start=self._startFrame,
                     end=self._startFrame + self.input_range[1] - self.input_range[0])

        shell_cmd = cmd.cmd()
        print shell_cmd
        self.shell = subprocess.Popen(shell_cmd,
                                      shell=True,
                                      stderr=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      universal_newlines=True)

    def taskStep(self):
        self._frame += 1
        if self._frame % 10 != 0:
            return (self._finished == False)

        # todo: oiiotools 不能夠得到stdout，暂时只能够作假进度条
        duration = self.input_range[1] - self.input_range[0] + 1
        if self.shell.poll() is None:
            self._progress += 0.01
            self._progress = min(self._progress, 0.99)
            time.sleep(0.5)
            # string = self.shell.stdout.readline()
            # print string
            # match = frame_regex.match(string)
            # if match:kes
            #     self._progress = \
            #         (float(match.groups()[0]) - self.input_range[0]) / duration if duration != 0 else int(
            #                 match.groups()[0])
        else:
            self._finished = True

        return (self._finished == False)

    def forceAbort(self):
        if self.shell is not None:
            returncode = self.shell.poll()
            if returncode is None:
                try:
                    if sys.platform == "win32":
                        # subprocess.Popen.terminate only kills the top level process, child processes are not killed.
                        # On Windows launching a single socket export creates several processes, the last of which is Nuke.
                        # Killing the parent does not kill Nuke, so we need to explicitly kill the whole tree.
                        subprocess.call(["taskkill", "/F", "/T", "/PID", str(self.shell.pid)])
                    else:
                        self._nukeProcess.terminate()

                    self._nukeProcess.wait()

                except Exception as e:
                    self.setError(str(e))

    def progress(self):
        if self._finished:
            return 1.0
        return float(self._progress)


class OiioSubmission(FnSubmission.Submission):
    kRender = 'oiio'
    kCommandLine = 'commandline'

    def __init__(self):
        super(OiioSubmission, self).__init__()

    def addJob(self, jobType, initDict):
        if jobType == OiioSubmission.kRender:
            return OiioRenderTask(initDict)
