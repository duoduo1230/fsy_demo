#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'AndyGuo'

from dayu_path import DayuPath
# from app._hiero.tools.zam import ZAM_TIMECODE as TC
# from app._hiero.tools.zam import EDL_READER as EDL

import ZAM_TIMECODE as TC
import EDL_READER as EDL
import os


class ZAM_EDL_Compare(object):
    def __init__(self, oldEDL, newEDL, framerate, resolveFX=True):
        super(ZAM_EDL_Compare, self).__init__()
        oldEDL = DayuPath(__file__).parent.child('template.edl')
        newEDL = DayuPath(__file__).parent.child('template.edl')
        self.oldEDLPath = oldEDL
        self.newEDLPath = newEDL
        self.conformClue = 'reel'
        self.timecode = TC.ZAM_TIMECODE()
        self.oldEDL = EDL.EDL_READER()
        self.framerate = framerate
        self.oldEDL.setFrameRate(framerate)
        self.newEDL = EDL.EDL_READER()
        self.newEDL.setFrameRate(framerate)
        self.oldEDL.readEDL(oldEDL)
        self.newEDL.readEDL(newEDL)
        if resolveFX:
            self.oldEDL.resolveTransition()
            self.oldEDL.resolveSpeed()
            self.oldEDL.resolveTarget()
            self.newEDL.resolveTransition()
            self.newEDL.resolveSpeed()
            self.newEDL.resolveTarget()

        # print(self.oldEDL, self.newEDL)
        self.newToOldMapping = {}
        self.oldToNewMapping = {}
        self.addList = {}
        self.deleteList = {}
        self.sameList = {}
        self.moveList = {}
        self.trimList = {}
        self.expandList = {}

    def checkAdd(self):
        for key in self.newToOldMapping:
            found = False
            if len(self.newToOldMapping[key]) == 0:
                self.addList[key] = []
            else:

                for item in self.newToOldMapping[key]:
                    oldevent = self.oldEDL.resolvedList[item - 1]
                    newevent = self.newEDL.resolvedList[key - 1]
                    if self.timecode.isOverlap(newevent['sourcein'], newevent['sourceout'],
                                               oldevent['sourcein'], oldevent['sourceout'], self.framerate):
                        found = True

            if not found:
                self.addList[key] = []

    def checkMove(self):
        for key in self.newToOldMapping:
            for item in self.newToOldMapping[key]:
                oldevent = self.oldEDL.resolvedList[item - 1]
                newevent = self.newEDL.resolvedList[key - 1]

                if self.timecode.isSame(newevent['sourcein'], newevent['sourceout'],
                                        oldevent['sourcein'], oldevent['sourceout'], self.framerate):
                    if self.timecode.isSame(newevent['targetin'], newevent['targetout'],
                                            oldevent['targetin'], oldevent['targetout'], self.framerate):
                        if self.sameList.has_key(key):
                            self.sameList[key].append(item)
                        else:
                            self.sameList[key] = []
                            self.sameList[key].append(item)

                    else:
                        if self.moveList.has_key(key):
                            self.moveList[key].append(item)
                        else:
                            self.moveList[key] = []
                            self.moveList[key].append(item)

                    self.newToOldMapping[key] = []

    def checkDelete(self):
        # print(self.oldToNewMapping)
        usedoldlist = set(self.oldToNewMapping.keys())
        totaloldlist = set(range(1, len(self.oldEDL.resolvedList) + 1))
        if self.ignorBLAX:
            deletedoldlist = [x for x in (usedoldlist ^ totaloldlist) if
                              self.oldEDL.resolvedList[x - 1]['reel'] not in ['BL', 'AX']]
        else:
            deletedoldlist = list(usedoldlist ^ totaloldlist)
        for index in deletedoldlist:
            self.deleteList[index] = []

        for key in self.oldToNewMapping:
            found = False
            for item in self.oldToNewMapping[key]:
                oldevent = self.oldEDL.resolvedList[key - 1]
                newevent = self.newEDL.resolvedList[item - 1]
                if self.timecode.isOverlap(newevent['sourcein'], newevent['sourceout'],
                                           oldevent['sourcein'], oldevent['sourceout'], self.framerate):
                    found = True
            if not found:
                self.deleteList[key] = []

    def checkChange(self):
        for key in self.newToOldMapping:
            for item in self.newToOldMapping[key]:
                oldevent = self.oldEDL.resolvedList[item - 1]
                newevent = self.newEDL.resolvedList[key - 1]

                if self.timecode.isInside(newevent['sourcein'], newevent['sourceout'],
                                          oldevent['sourcein'], oldevent['sourceout'], self.framerate):
                    if self.trimList.has_key(key):
                        self.trimList[key].append(item)
                    else:
                        self.trimList[key] = []
                        self.trimList[key].append(item)

                elif self.timecode.isOverlap(newevent['sourcein'], newevent['sourceout'],
                                             oldevent['sourcein'], oldevent['sourceout'],
                                             self.framerate) and not self.timecode.isSame(
                    newevent['sourcein'], newevent['sourceout'],
                    oldevent['sourcein'], oldevent['sourceout'], self.framerate):
                    if self.expandList.has_key(key):
                        self.expandList[key].append(item)
                    else:
                        self.expandList[key] = []
                        self.expandList[key].append(item)

    def getLinkedEvents(self, clickedEvent):
        if clickedEvent.has_key('old'):
            oldindex = clickedEvent['old']
            result = []
            for mylist in (self.addList, self.deleteList, self.sameList, self.moveList, self.trimList, self.expandList):
                for key in mylist:
                    if oldindex in mylist[key]:
                        result.append(key)
            return result

        if clickedEvent.has_key('new'):
            newindex = clickedEvent['new']
            result = []
            for mylist in (self.addList, self.deleteList, self.sameList, self.moveList, self.trimList, self.expandList):
                if newindex in mylist.keys():
                    result.extend(mylist[newindex])
            return result

    def getAllAddEvents(self):
        # result = '==== Add ====\n\n'
        result = []
        for key in sorted(self.addList.keys()):
            item = self.newEDL.resolvedList[key - 1]
            result.append('%s_%s' % (item['event'], item['sourcein']))
        return result

    def getAllDeletedEvents(self):
        result = []
        for key in sorted(self.deleteList.keys()):
            item = self.oldEDL.resolvedList[key - 1]
            result.append('%s_%s' % (item['event'], item['sourcein']))
        return result

    def getAllSameEvents(self):
        result = '==== Same ====\n\n'
        for key in sorted(self.sameList.keys()):
            item = self.newEDL.resolvedList[key - 1]
            result += str(item['event']).ljust(5)
            result += str(item[self.conformClue]).ljust(9)
            result += ' '
            result += str(item['media']).ljust(6)
            result += str(item['cut']).ljust(8)
            result += str(item['sourcein']).ljust(12)
            result += str(item['sourceout']).ljust(12)
            result += str(item['targetin']).ljust(12)
            result += str(item['targetout']).ljust(12)
            result += os.linesep
        return result

    def getAllMoveEvents(self):
        result = '==== Move ====\n\n'
        for key in sorted(self.moveList.keys()):
            item = self.newEDL.resolvedList[key - 1]
            result += str(item['event']).ljust(5)
            result += str(item[self.conformClue]).ljust(9)
            result += ' '
            result += str(item['media']).ljust(6)
            result += str(item['cut']).ljust(8)
            result += str(item['sourcein']).ljust(12)
            result += str(item['sourceout']).ljust(12)
            result += str(item['targetin']).ljust(12)
            result += str(item['targetout']).ljust(12)
            result += '\t <-- \t '
            result += str(self.oldEDL.resolvedList[self.moveList[key][0] - 1]['targetin']).ljust(12)
            result += str(self.oldEDL.resolvedList[self.moveList[key][0] - 1]['targetout']).ljust(12)
            result += str(self.moveList[key][0]).rjust(8)
            result += os.linesep
        return result

    def getAllTrimEvents(self):
        result = {}
        old_change = []
        for key in sorted(self.trimList.keys()):
            item = self.newEDL.resolvedList[key - 1]
            olditem = self.oldEDL.resolvedList[self.trimList[key][0] - 1]
            new_str = '%s_%s' % (item['event'], item['sourcein'])
            old_str = '%s_%s' % (olditem['event'], olditem['sourcein'])
            trim_value = item['duration'] - olditem['duration']
            result[new_str] = trim_value
            old_change.append(old_str)

        return old_change, result

    def getAllExpandEvents(self):
        result = {}
        old_change = []

        for key in sorted(self.expandList.keys()):
            item = self.newEDL.resolvedList[key - 1]
            olditem = self.oldEDL.resolvedList[self.expandList[key][0] - 1]
            new_str = '%s_%s' % (item['event'], item['sourcein'])
            old_str = '%s_%s' % (olditem['event'], olditem['sourcein'])

            trim_value = item['duration'] - olditem['duration']
            result[new_str] = trim_value
            old_change.append(old_str)

        return old_change, result

    def getDetails(self, clickedEvent):
        pass

    def compareEDLs(self, old_result, new_result, ignorBLAX=True, conformCLue='reel'):
        self.ignorBLAX = ignorBLAX
        self.conformClue = conformCLue

        self.oldEDL.resolvedList = old_result
        self.newEDL.resolvedList = new_result

        for indexnew, itemnew in enumerate(self.newEDL.resolvedList):
            if ignorBLAX and itemnew['reel'] in ['BL', 'AX'] and conformCLue == 'reel':
                continue
            self.newToOldMapping[indexnew + 1] = []
            for indexold, itemold in enumerate(self.oldEDL.resolvedList):
                if itemold[conformCLue] == itemnew[conformCLue]:
                    self.newToOldMapping[indexnew + 1].append(indexold + 1)

        for key in self.newToOldMapping:
            for item in self.newToOldMapping[key]:
                if self.oldToNewMapping.has_key(item):
                    self.oldToNewMapping[item].append(key)
                else:
                    self.oldToNewMapping[item] = []
                    self.oldToNewMapping[item].append(key)

        # do not change the process order!
        self.checkAdd()
        self.checkMove()
        self.checkDelete()
        self.checkChange()


if __name__ == '__main__':
    testclass = ZAM_EDL_Compare(r"E:\BaiduNetdiskDownload\20220830\GGKR_CUT0817_AAF_210817\v1.edl",
                                r"E:\BaiduNetdiskDownload\20220830\GGKR_CUT0817_AAF_210817\v2.edl",
                                24)
    testclass.compareEDLs(conformCLue='reel')
    print(testclass.getAllSameEvents())
    print(testclass.getAllAddEvents())
    print(testclass.getAllDeletedEvents())
    print(testclass.getAllTrimEvents())
    print(testclass.getAllExpandEvents())
