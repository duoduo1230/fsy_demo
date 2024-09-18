#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/23/2019 11:23 AM

__author__ = 'pengyuxuan'

import hiero.core
import hiero.ui

from ui_center.qt import *


class CustomSpreadsheetColumns(QObject):
    currentView = hiero.ui.activeView()

    # This is the list of Columns available
    gCustomColumnList = [
        {'name': 'Colourspace', 'cellType': 'readonly'},
        {'name': 'Resolution', 'cellType': 'readonly'},
        {'name': 'Framerate', 'cellType': 'readonly'},
        {'name': 'Compression Name', 'cellType': 'readonly'},
    ]

    def numColumns(self):
        """
          Return the number of custom columns in the spreadsheet view
        """
        return len(self.gCustomColumnList)

    def columnName(self, column):
        """
          Return the name of a custom column
        """
        return self.gCustomColumnList[column]['name']

    def getTagsString(self, item):
        """
          Convenience method for returning all the Notes in a Tag as a string
        """
        tagNames = []
        tags = item.tags()
        for tag in tags:
            tagNames += [tag.name()]
        tagNameString = ','.join(tagNames)
        return tagNameString

    def getNotes(self, item):
        """
          Convenience method for returning all the Notes in a Tag as a string
        """
        notes = ''
        tags = item.tags()
        for tag in tags:
            note = tag.note()
            if len(note) > 0:
                notes += tag.note() + ', '
        return notes[:-2]

    def _getSourceMediaMetadata(self, item, key):
        try:
            clip = item.source()
            source_md = clip.mediaSource().metadata()
            if source_md.hasKey(key):
                return source_md.value(key)
        except Exception as e:
            import traceback
            traceback.print_exc()
        return '--'

    def getData(self, row, column, item):
        """
          Return the data in a cell
        """
        currentColumn = self.gCustomColumnList[column]
        if currentColumn['name'] == 'Colourspace':
            try:
                colTransform = item.sourceMediaColourTransform()
            except:
                colTransform = '--'
            return colTransform
        if currentColumn['name'] == 'Resolution':
            return self._getSourceMediaMetadata(item, 'foundry.source.resolution')
        if currentColumn['name'] == 'Framerate':
            return self._getSourceMediaMetadata(item, 'foundry.source.framerate')
        if currentColumn['name'] == 'Compression Name':
            return self._getSourceMediaMetadata(item, 'media.exr.compressionName')
        return ""

    def getBackground(self, row, column, item):
        """
          Return the background colour for a cell
        """
        if not item.source().mediaSource().isMediaPresent():
            return QColor(80, 20, 20)
        return None

    def getForeground(self, row, column, item):
        """
          Return the foreground colour for a cell
        """
        return None

    def getFont(self, row, column, item):
        """
          Return the font for a cell
        """
        return None

    def setData(self, row, column, item, data):
        """
          Set the data in a cell - unused in this example
        """

        return None

    def getIcon(self, row, column, item):
        """
          Return the icon for a cell
        """
        currentColumn = self.gCustomColumnList[column]
        if currentColumn['name'] == 'Colourspace':
            return QIcon("icons:LUT.png")

        return None

    def paintCell(self, row, column, item, painter, option):
        """
          Paint a custom cell. Return True if the cell was painted, or False to continue
          with the default cell painting.
        """
        return False

    def createEditor(self, row, column, item, view):
        """
          Create an editing widget for a custom cell
        """
        self.currentView = view
        currentColumn = self.gCustomColumnList[column]
        if currentColumn['cellType'] == 'readonly':
            cle = QLabel()
            cle.setEnabled(False)
            cle.setVisible(False)
            return cle

    def setModelData(self, row, column, item, editor):
        return False

    def dropMimeData(self, row, column, item, data, items):
        """
          Handle a drag and drop operation - adds a Dragged Tag to the shot
        """
        for thing in items:
            if isinstance(thing, hiero.core.Tag):
                item.addTag(thing)
        return None
