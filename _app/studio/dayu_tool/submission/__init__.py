#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import hiero.core
import ffmpeg_submission
import oiio_submission

hiero.core.taskRegistry.addSubmission("FFmpeg Render", ffmpeg_submission.FFmpegSubmission)
hiero.core.taskRegistry.addSubmission('Oiio Render', oiio_submission.OiioSubmission)