# -*- coding: utf-8 -*-
__author__ = 'GalaxyWind'


class CCommand(object):
    """define a type for CLI"""
    __slots__ = ('_cmdStr', '_helpInfoList', '_funcId', '_funcName', '_newMode', '_cliType')
    def __init__(self, cmdStr, helpInfoList, funcId, funcName, newMode, cliType):
        self._cmdStr        = cmdStr
        self._helpInfoList  = helpInfoList     # a list of CCommand string
        self._funcId        = funcId
        self._funcName      = funcName
        self._newMode       = newMode
        self._cliType       = cliType
        #print "\n CCommand is %s \n" % self
    @property
    def cliType(self):
        return self._cliType

    @cliType.setter
    def cliType(self, value):
        self._cliType = value

    @property
    def cmdStr(self):
        return self._cmdStr

    @cmdStr.setter
    def cmdStr(self, value):
        self._cmdStr = value

    @property
    def helpInfoList(self):
        return self._helpInfoList

    @helpInfoList.setter
    def helpInfoList(self, value):
        self._helpInfoList = value

    @property
    def funcId(self):
        return self._funcId

    @funcId.setter
    def funcId(self, value):
        self._funcId = value

    @property
    def funcName(self):
        return self._funcName

    @funcName.setter
    def funcName(self, value):
        self._funcName = value

    @property
    def newMode(self):
        return self._newMode

    @newMode.setter
    def newMode(self, value):
        self._newMode = value

    def AddHelpInfo(self, value):
        self._helpInfoList.append(value)

    def __str__(self):
        return 'CCommand object(cmdStr: %s, funcName: %s, newMode: %s, helpInfoList: %s)' \
                    %(self.cmdStr, self.funcName, self.newMode, str(self.helpInfoList))

    __repr__ = __str__