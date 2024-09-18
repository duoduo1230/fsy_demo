#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from ui_center.qt import *


class DYCascadingEnumerationComboBox(QComboBox):
    kSeparator = '/'

    def __init__(self, parent=None):
        super(DYCascadingEnumerationComboBox, self).__init__(parent)
        self.root_menu = QMenu()
        self.root_menu.triggered.connect(self.slot_on_action_triggered)
        self._actions = []

    def setup_menu(self, values):
        self.root_menu.clear()
        self.sub_menu_map = dict()
        self._actions = []
        self.clear()
        if not values:
            return
        for value in values:
            components = value.split(DYCascadingEnumerationComboBox.kSeparator)
            action_name = components[-1]
            action_menu = self.get_action_menu(components[:-1])
            action = action_menu.addAction(action_name)
            action.setCheckable(True)
            self.addItem(action_name)
            self._actions.append(action)

    def get_action_menu(self, components):
        if not components:  # list is empty, return the root
            return self.root_menu
        else:
            # If this menu already exists, return it, otherwise to a recursive call
            # to get the parent, and create it
            key = DYCascadingEnumerationComboBox.kSeparator.join(components)
            if key in self.sub_menu_map:
                return self.sub_menu_map[key]
            else:
                parent_menu = self.get_action_menu(components[:-1])
                menu = parent_menu.addMenu(components[-1])
                self.sub_menu_map[key] = menu
                return menu

    def showPopup(self):
        """ Override default showPopup() and show our menu instead """
        QComboBox.hidePopup(self)
        self.root_menu.popup(self.mapToGlobal(QPoint(0, self.height())))

    def setCurrentIndex(self, index):
        """ Set the current index and set the checked state of the menu entries. """
        QComboBox.setCurrentIndex(self, index)
        text = self.itemText(index)
        for action in self._actions:
            action.setChecked(action.text() == text)

    def slot_on_action_triggered(self, action):
        """ Callback from a menu action being triggered, set the index. """
        index = self._actions.index(action)
        self.setCurrentIndex(index)
