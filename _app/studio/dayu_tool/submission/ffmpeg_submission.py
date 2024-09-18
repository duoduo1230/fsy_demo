#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import hiero
from hiero.exporters import FnSubmission
import subprocess
from bin.ffmpeg.stream import *
import timecode
import re
import sys
import os
from db.disk_path import DiskPath
from config.const import OUTPUT_FORMAT_DICT

frame_regex = re.compile(r'.*frame=\W+(\d+).*')
OCIO_LUT_FOLDER = {'win32' : 'y:\\td\\ocio_luts',
                   'darwin': '/Volumes/pipeline/td/ocio_luts',
                   'linux2': ''}


class FFmpegRenderTask(hiero.core.TaskBase):

    def __init__(self, init_dict):
        print 'ffmpeg render task init!'
        super(FFmpegRenderTask, self).__init__(init_dict)
        self.input_file = self._fileinfo.filename()
        self.input_range = (int(self._item.sourceIn()), int(self._item.sourceOut()) + 1)
        self.output_file = self.resolvedExportPath()
        self._input_colorspace = self._item.source().sourceMediaColourTransform()
        self._output_colorspace = init_dict.get('preset')._properties.get('output_colorspace')
        self._ocio_config = init_dict.get('preset')._properties.get('ocio_config_path')
        self.output_format = init_dict.get('preset')._properties.get('output_format')
        self.width = init_dict.get('preset')._properties.get('width')
        self.height = init_dict.get('preset')._properties.get('height')
        self.output_range = (init_dict.get('startFrame'), init_dict.get('endFrame'))
        self.fps = self._item.source().framerate().toFloat()
        self._progress = 0.0
        self._frame = 0
        self._finished = False
        self._returncode = None
        self.shell = None

    def startTask(self):
        _output_path = DiskPath(self.output_file)

        # 色彩空间转换的处理，如果输入和输出的色彩空间相同，那么根本不转换。需要转换的话，去查找对应的bake lut
        if self._input_colorspace == self._output_colorspace:
            lut_file = None
        else:
            lut_file = os.sep.join((OCIO_LUT_FOLDER.get(sys.platform),
                                    '{}----{}.cube'.format(self._input_colorspace,
                                                           self._output_colorspace)))
            assert os.path.exists(lut_file)

        # 记录下原始素材的起始timecode
        start_tc = timecode.Timecode(self._item.source().mediaSource().timecodeStart() + self.input_range[0], self.fps)

        # 如果输入的素材是mov 类型
        import config.const
        if self.input_file.endswith(tuple(config.const.EXT_SINGLE_MEDIA.keys())):
            cmd = FFmpeg() + Overwrite() + \
                  Input(self.input_file, sequence=False, fps=self.fps,
                        trim_in=self.input_range[0], trim_out=self.input_range[1])
        else:
            cmd = FFmpeg() + Overwrite() + \
                  Input(self.input_file, sequence=True, start=self._fileinfo.startFrame(), fps=self.fps,
                        trim_in=self.input_range[0], trim_out=self.input_range[1])

        cmd = cmd if (self.width == 0 and self.height == 0) else (cmd + Scale(self.width, self.height) + AspectRatio())
        cmd = (cmd + Lut3d(lut_file)) if lut_file else cmd

        if _output_path.ext in ('.mov',):
            cmd = cmd + WriteTimecode(start_tc.timecode())

        # 读取相应的输出编码
        codec_format = OUTPUT_FORMAT_DICT.get(self.output_format, None)
        if codec_format is None:
            raise Exception('there is no codec for {}'.format(self.output_format))

        cmd = cmd + PixelFormat(pixel_format=codec_format.get('pixel_format', None),
                                profile=codec_format.get('profile', None))
        cmd = cmd + Codec(video=codec_format.get('codec', None))
        cmd = cmd + Quality(qscale=codec_format.get('quality', None))

        # 如果输出的是序列帧
        if _output_path.pattern:
            cmd = cmd + Output(_output_path.to_pattern(), fps=self.fps, sequence=True, start=self.output_range[0])
        else:
            cmd = cmd + Output(self.output_file, fps=self.fps, sequence=False)

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

        duration = self.input_range[1] - self.input_range[0]
        if self.shell.poll() is None:
            string = self.shell.stderr.readline()
            # print string
            match = frame_regex.match(string)
            if match:
                self._progress = \
                    float(match.groups()[0]) / duration if duration != 0 else int(
                            match.groups()[0])
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


class FFmpegSubmission(FnSubmission.Submission):
    kRender = 'ffmpeg'
    kCommandLine = 'commandline'

    def __init__(self):
        super(FFmpegSubmission, self).__init__()

    def addJob(self, jobType, initDict):
        if jobType == FFmpegSubmission.kRender:
            return FFmpegRenderTask(initDict)
