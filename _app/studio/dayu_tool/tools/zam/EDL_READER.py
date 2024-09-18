#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'AndyGuo'

import re
import os
import copy
# import app._hiero.tools.zam.ZAM_TIMECODE as TC
import ZAM_TIMECODE as TC


class EDL_READER(object):
    def __init__(self):
        super(EDL_READER, self).__init__()
        self.frameRate = 24.0
        self.edlList = []
        self.resolvedList = []
        self.timecode = TC.ZAM_TIMECODE()
        self.titleRegex = re.compile(r'^TITLE:\s+([\w\s]*)')
        self.fcpRegex = re.compile(r'^FCM:\s+([\w\s]*)')
        self.eventRegex = re.compile(
            r'(\d+)\s+(\w+)\s+([\w\/]+)\s+(\w+)\s+(\d*)\s+(\d{1,2}:\d{1,2}:\d{1,2}[\:\;]\d{1,3})\s+(\d{1,2}:\d{1,2}:\d{1,2}[\:\;]\d{1,3})\s+(\d{1,2}:\d{1,2}:\d{1,2}[\:\;]\d{1,3})\s+(\d{1,2}:\d{1,2}:\d{1,2}[\:\;]\d{1,3})')
        self.auxRegex = re.compile(r'^\*')
        self.effectRegex = re.compile(r'^\* EFFECT NAME:\s+([\w\s]*)')
        self.fromClipNameRegex = re.compile(r'^\* FROM CLIP NAME:\s+([\S ]*)')
        self.stillRegex = re.compile(r'^\* FROM CLIP IS A STILL')
        self.problemRegex = re.compile(r'^\* PROBLEM WITH EDIT:\s+([\w\s]*)')
        self.commentRegex = re.compile(r'^\* COMMENT:\s+([\w\s]*)')
        self.filterRegex = re.compile(r'^\* CLIP FILTER:\s+([\w\s]*)')
        self.toClipNameRegex = re.compile(r'^\* TO CLIP NAME:\s+([\S ]*)')
        self.speedRegex = re.compile(r'M2\s+(\w+)\s+(\-?\d+\.\d+)\s+(\d{1,2}:\d{1,2}:\d{1,2}[\:\;]\d{1,3})')
        self.longReelRegex = re.compile(r'^FINAL CUT PRO REEL:\s+(\w+)\s+REPLACED BY:\s+(\w+)')

    def __repr__(self):
        result = 'index\tevent\treel\tshotcode\tmedia\tcut\ttransition\tsourcein\tsourceout\targetin\ttargetout\tduration\teffect\tclipname\tstill\tprobelem\tcommet\tfilter\tspeed\tlongreel\n'
        for item in self.resolvedList:
            mylist = [item['index'], item['event'], item['reel'], item['shotcode'], item['media'], item['cut'],
                      item['transition'],
                      item['sourcein'], item['sourceout'],
                      item['targetin'], item['targetout'], item['duration'],
                      item['effect'], item['clipname'], item['still'],
                      item['problem'], item['comment'], item['filter'], item['speed'],
                      item['longreel']
                      ]
            for index, xx in enumerate(mylist):
                result += str(xx)
                result += '\t'
            result += '\n'

        return result

    def saveEDL(self, savepath):
        result = 'TITLE: ' + 'XXX\n\n'
        for item in self.resolvedList:
            result += '%04d  ' % item['index']
            result += item['reel'].ljust(9)
            result += item['media'].ljust(6)
            result += item['cut'].ljust(5)
            if item['transition'] != 0:
                result += '%03d ' % item['transition']
            else:
                result += '    '

            result += '%s %s %s %s ' % (item['sourcein'], item['sourceout'], item['targetin'], item['targetout'])
            result += os.linesep

        with open(savepath, 'w') as savefile:
            savefile.write(result)

    def setFrameRate(self, framerate):
        self.frameRate = framerate

    def resolveTransition(self):
        for index, item in enumerate(self.resolvedList):
            if item['cut'] == 'D':
                self.resolvedList[index - 1]['sourceout'] = self.timecode.addTimecode(
                    self.resolvedList[index - 1]['sourceout'],
                    self.timecode.framesToTimecode(self.resolvedList[index]['transition'], self.frameRate),
                    self.frameRate)
                self.resolvedList[index]['transition'] = 0
                self.resolvedList[index]['cut'] = 'C'

    def resolveSpeed(self):
        for index, item in enumerate(self.resolvedList):
            if item['speed'] != 1.0:
                duration = self.timecode.subTimecode(item['sourceout'],
                                                     item['sourcein'], self.frameRate)
                duration = self.timecode.framesToTimecode(
                    self.timecode.timecodeToFrames(duration, self.frameRate) * item['speed'],
                    self.frameRate)
                self.resolvedList[index]['sourceout'] = self.timecode.addTimecode(item['sourcein'],
                                                                                  duration, self.frameRate)
                self.resolvedList[index]['speed'] = 1.0

    def resolveTarget(self):
        startTC = self.resolvedList[0]['targetin']
        for index, item in enumerate(self.resolvedList):
            duration = self.timecode.subTimecode(item['sourceout'], item['sourcein'], self.frameRate)
            self.resolvedList[index]['targetin'] = startTC
            startTC = self.timecode.addTimecode(startTC, duration, self.frameRate)
            self.resolvedList[index]['targetout'] = startTC
            self.resolvedList[index]['duration'] = self.timecode.timecodeToFrames(duration, self.frameRate)

    def readEDL(self, edlPath):
        with open(edlPath, 'r') as edlfile:
            stringlist = edlfile.readlines()
        stringlist = map(str.strip, stringlist)
        # print(stringlist)

        count = 1
        for index, item in enumerate(stringlist):
            if self.eventRegex.match(item):
                tempdict = {'index': '', 'event': '', 'reel': '', 'media': '', 'cut': '', 'transition': 0,
                            'sourcein': '', 'sourceout': '', 'targetin': '', 'targetout': '', 'duration': '',
                            'effect': '',
                            'clipname': '', 'still': False, 'problem': '', 'comment': '', 'filter': '', 'speed': 1.0,
                            'longreel': '', 'shotcode': ''}
                eventvalues = self.eventRegex.match(item).groups()
                tempdict['index'] = count
                count += 1
                tempdict['event'] = eventvalues[0]
                tempdict['reel'] = eventvalues[1]
                tempdict['media'] = eventvalues[2]
                tempdict['cut'] = eventvalues[3]
                if len(eventvalues[4]) != 0:
                    tempdict['transition'] = int(eventvalues[4])
                tempdict['sourcein'] = eventvalues[5]
                tempdict['sourceout'] = eventvalues[6]
                tempdict['targetin'] = eventvalues[7]
                tempdict['targetout'] = eventvalues[8]
                self.edlList.append(tempdict)

            if self.effectRegex.match(item):
                if self.edlList[-1]['cut'] == 'D':
                    self.edlList[-1]['effect'] = self.effectRegex.match(item).groups()[-1]

            if self.fromClipNameRegex.match(item):
                if self.edlList[-1]['cut'] == 'D':
                    self.edlList[-2]['clipname'] = self.fromClipNameRegex.match(item).groups()[-1]
                else:
                    self.edlList[-1]['clipname'] = self.fromClipNameRegex.match(item).groups()[-1]

            if self.toClipNameRegex.match(item):
                if self.edlList[-1]['cut'] == 'D':
                    self.edlList[-1]['clipname'] = self.toClipNameRegex.match(item).groups()[-1]

            if self.stillRegex.match(item):
                self.edlList[-1]['still'] = True

            if self.problemRegex.match(item):
                self.edlList[-1]['problem'] = self.problemRegex.match(item).groups()[-1]

            if self.commentRegex.match(item):
                if self.edlList[-1]['cut'] == 'D':
                    self.edlList[-2]['comment'] = self.commentRegex.match(item).groups()[-1]
                else:
                    self.edlList[-1]['comment'] = self.commentRegex.match(item).groups()[-1]

            if self.filterRegex.match(item):
                if self.edlList[-1]['cut'] == 'D' and len(self.edlList[-2]['filter']) == 0:
                    self.edlList[-2]['filter'] = self.filterRegex.match(item).groups()[-1]
                else:
                    self.edlList[-1]['filter'] = self.filterRegex.match(item).groups()[-1]

            if self.speedRegex.match(item):
                speedvalues = self.speedRegex.match(item).groups()
                if self.edlList[-1]['cut'] == 'D':
                    if self.edlList[-2]['reel'] == speedvalues[0] and self.edlList[-2]['speed'] == 1.0:
                        self.edlList[-2]['speed'] = float(speedvalues[1]) / self.frameRate
                    else:
                        self.edlList[-1]['speed'] = float(speedvalues[1]) / self.frameRate
                else:
                    self.edlList[-1]['speed'] = float(speedvalues[1]) / self.frameRate

            if self.longReelRegex.match(item):
                longvalues = self.longReelRegex.match(item).groups()
                if self.edlList[-1]['cut'] == 'D':
                    if self.edlList[-2]['reel'] == longvalues[1] and len(self.edlList[-2]['longreel']) == 0:
                        self.edlList[-2]['longreel'] = longvalues[0]
                    else:
                        self.edlList[-1]['longreel'] = longvalues[0]
                else:
                    if self.edlList[-1]['reel'] == longvalues[1] and len(self.edlList[-1]['longreel']) == 0:
                        self.edlList[-1]['longreel'] = longvalues[0]

        self.resolvedList = copy.deepcopy(self.edlList)


if __name__ == '__main__':
    testclass = EDL_READER()
    testclass.setFrameRate(24)
    testclass.readEDL('/Users/mac/Documents/Projects/Python/EDL_Compare/ZAM_EDL/ANDY_TEST/20151108_RZYG_ToConform_V1.edl')
    testclass.resolveTransition()
    testclass.resolveSpeed()
    testclass.resolveTarget()
    print testclass
    # testclass.saveEDL('/Users/mac/Documents/Projects/Python/EDL_Compare/ZAM_EDL/test_video.edl')
