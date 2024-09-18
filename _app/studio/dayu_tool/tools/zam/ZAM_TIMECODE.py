#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'AndyGuo'

import re
import math


class ZAM_TIMECODE(object):
    def __init__(self):
        super(ZAM_TIMECODE, self).__init__()
        self.SMPTE_Regex_NDF = re.compile(r'^(?:(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d):)?([0-5]?\d)$')
        self.SMPTE_Regex_DF = re.compile(r'^(?:(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d);)?([0-5]?\d)$')
        self.SRT_Regex = re.compile(r'^(?:(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d),)?(\d\d\d)$')
        self.DLP_Regex = re.compile(r'^(?:(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d):)?([0-2][0-4]\d)$')

    def isSame(self, checkin, checkout, limitin, limitout, framerate, type='SMPTE_NDF'):
        if checkin == limitin and checkout == limitout:
            return True
        else:
            return False

    def isInside(self, checkin, checkout, limitin, limitout, framerate, type='SMPTE_NDF'):
        if (checkin >= limitin and checkout < limitout) or (checkin > limitin and checkout <= limitout):
            return True
        else:
            return False

    def isOverlap(self, checkin, checkout, limitin, limitout, framerate, type='SMPTE_NDF'):
        if (checkout  <=  limitout and checkout >= limitin) or (checkin >= limitin and checkin <= limitout):
            return True
        else:
            return False

    def overlapDuration(self, checkin, checkout, limitin, limitout, framerate, type='SMPTE_NDF'):
        if self.isOverlap(checkin, checkout,limitin, limitout, framerate):
            if checkin >= limitin and checkout < limitout:
                return self.duration(checkin, checkout)
            if checkin >= limitin and checkout >= limitout:
                return self.duration(checkin, limitout)
            if checkin <limitin and checkout >= limitout:
                return self.duration(limitin, limitout)
            if checkin < limitin and checkout < limitout:
                return self.duration(limitin, checkout)


    def findMissing(self, checkin, checkout, limitin, limitout, framerate, type='SMPTE_NDF'):
        result = {'left': [], 'right': []}
        if self.isInside(checkin, checkout, limitin, limitout,framerate):
            return result
        else:
            if checkin < limitin:
                result['left'] = [checkin, min(checkout, limitin)]
            if checkout > limitout:
                result['right'] = [max(checkin, limitout), checkout]
            return result


    def addTimecode(self, tc1, tc2, framerate, type='SMPTE_NDF'):
        frame1 = self.timecodeToFrames(tc1, framerate)
        frame2 = self.timecodeToFrames(tc2, framerate)
        return self.framesToTimecode(frame1 + frame2, framerate, type=type)

    def subTimecode(self, tc1, tc2, framerate, type='SMPTE_NDF'):
        frame1 = self.timecodeToFrames(tc1, framerate)
        frame2 = self.timecodeToFrames(tc2, framerate)
        myframes = frame1 - frame2
        # if myframes < 0:
        #     myframes += 3600 * framerate * 24
        return self.framesToTimecode(myframes, framerate, type=type)

    def duration(self, inTimecode, outTimecode, framerate, type='SMPTE_NDF'):
        frame1 = self.timecodeToFrames(inTimecode, framerate)
        frame2 = self.timecodeToFrames(outTimecode, framerate)
        myframes = frame2 - frame1 + 1
        # if myframes < 0:
        #     myframes += 3600 * framerate
        return self.framesToTimecode(myframes, framerate, type=type)

    def framesToTimecode(self, framecount, framerate, type='SMPTE_NDF'):
        if type == 'SMPTE_NDF':
            hh = framecount // (framerate * 3600) % 24
            mm = (framecount // (framerate * 60)) % 60
            ss = (framecount // framerate) % 60
            ff = framecount % framerate
            return '{0:02d}:{1:02d}:{2:02d}:{3:02d}'.format(int(hh), int(mm), int(ss), int(ff))
        if type == 'SMPTE_DF':
            mm = (framecount // (framerate * 60)) % 60
            myframes = framecount + mm * 2 - (mm // 10) * 2
            hh = myframes // (framerate * 3600) % 24
            mm = (myframes // (framerate * 60)) % 60
            ss = (myframes // framerate) % 60
            ff = myframes % framerate
            # ff = ff + mm*2 - (mm // 10)*2
            return '{0:02d}:{1:02d}:{2:02d};{3:02d}'.format(int(hh), int(mm), int(ss), int(ff))
        if type == 'SRT':
            hh = framecount // (framerate * 3600) % 24
            mm = (framecount // (framerate * 60)) % 60
            ss = (framecount // framerate) % 60
            ff = int((framecount % framerate) / float(framerate) * 1000)
            return '{0:02d}:{1:02d}:{2:02d},{3:03d}'.format(int(hh), int(mm), int(ss), int(ff))
        if type == 'DLP':
            hh = framecount // (framerate * 3600) % 24
            mm = (framecount // (framerate * 60)) % 60
            ss = (framecount // framerate) % 60
            ff = int((framecount % framerate) / float(framerate) * 250)
            return '{0:02d}:{1:02d}:{2:02d}:{3:03d}'.format(int(hh), int(mm), int(ss), int(ff))

    def timecodeToFrames(self, tc, framerate):
        framecount = 0
        if self.SMPTE_Regex_NDF.match(tc):
            mytc = [x for x in self.SMPTE_Regex_NDF.match(tc).groups()]
            for index, item in enumerate(mytc):
                if item == None:
                    mytc[index] = 0
                else:
                    mytc[index] = int(item)
            framecount = mytc[0] * 3600 * framerate \
                         + mytc[1] * 60 * framerate \
                         + mytc[2] * framerate \
                         + mytc[3]
            return math.ceil(framecount)

        if self.SMPTE_Regex_DF.match(tc):
            mytc = [x for x in self.SMPTE_Regex_DF.match(tc).groups()]
            for index, item in enumerate(mytc):
                if item == None:
                    mytc[index] = 0
                else:
                    mytc[index] = int(item)
            framecount = mytc[0] * 3600 * framerate \
                         + mytc[1] * 60 * framerate \
                         + mytc[2] * framerate \
                         + mytc[3]
            framecount = framecount - mytc[1] * 2 + mytc[1] // 10 * 2
            return math.ceil(framecount)

        if self.SRT_Regex.match(tc):
            mytc = [x for x in self.SRT_Regex.match(tc).groups()]
            for index, item in enumerate(mytc):
                if item == None:
                    mytc[index] = 0
                else:
                    mytc[index] = int(item)
            framecount = mytc[0] * 3600 * framerate \
                         + mytc[1] * 60 * framerate \
                         + mytc[2] * framerate \
                         + int(mytc[3] / 1000.0 * framerate)
            return math.ceil(framecount)

        if self.DLP_Regex.match(tc):
            mytc = [x for x in self.DLP_Regex.match(tc).groups()]
            for index, item in enumerate(mytc):
                if item == None:
                    mytc[index] = 0
                else:
                    mytc[index] = int(item)
            framecount = mytc[0] * 3600 * framerate \
                         + mytc[1] * 60 * framerate \
                         + mytc[2] * framerate \
                         + int(mytc[3] / 250.0 * framerate)
            return math.ceil(framecount)


if __name__ == '__main__':
    testclass = ZAM_TIMECODE()
    print(testclass.framesToTimecode(1439, 24, type='DLP'))
    print(testclass.timecodeToFrames('00:02:01;25', 30))
    print(testclass.duration('23:59:45:00', '00:00:01:00', 24))
    print(testclass.subTimecode('00:00:01:00', '00:00:00:12', 24))
