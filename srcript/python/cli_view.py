# -*- coding: utf-8 -*-
__author__ = 'GalaxyWind'

from cli_command import CCommand


class CView(object):
    """define a type for CLI"""
    __slots__ = ('_viewName', '_commandList')
    def __init__(self, viewName):
        self._viewName = viewName
        self._commandList = []      # a list of CCommand object

    @property
    def viewName(self):
        return self._viewName

    @viewName.setter
    def viewName(self, value):
        self._viewName = value

    @property
    def commandList(self):
        return self._commandList

    @commandList.setter
    def commandList(self, value):
        self._commandList = value

    def AddCommand(self, value):
        self._commandList.append(value)

    def __str__(self):
        return 'CCommand object(viewName: %s, commandList: %s)' \
                    %(self.viewName, str(self.commandList))

    __repr__ = __str__