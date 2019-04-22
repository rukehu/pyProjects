# -*- coding: utf-8 -*-

__author__ = 'LI JUN'

from regLog import *
from regStruct import *
from string import Template
import re
import math
from assist import CAssist

class CRegister(object):
    """register"""
    def __init__(self, excelName, sheetName, csrName, regName, regType, regBaseAddr, regOffsetAddr, nRegs, nBits, count, table_struct_name, old_sheetName, nMacro, original_regName, reg_flag, reg_bar, idx_min, idx_max):
        self._excelName             = excelName             # 
        self._sheetName             = sheetName
        self._csrName               = csrName

        self._regName               = regName

        self._regBaseAddr           = regBaseAddr
        self._regOffsetAddr         = regOffsetAddr

        self._regBaseOffsetAddr     = []
        
        self._regType               = regType
        self._nRegs                 = nRegs
        self._regFieldList          = []                    # a list of CField object
        self._nBits                 = nBits
        self._tableCount            = count
        self._table_struct_name     = table_struct_name
        self._soc_type              = ""
        self._modeName              = sheetName
        self._old_sheetName         = old_sheetName
        self._old_regName           = regName
        self._original_regName      = original_regName
        self._nMacro                = nMacro

        self._reg_flag              = reg_flag
        self._reg_bar               = reg_bar

        self._tab_idx_min           = idx_min
        self._tab_idx_max           = idx_max

        
        #self._tabList               = []                     # a list of CTable object

        # self._tableDataValidWidth   = tableDataValidWidth
        # self._tableIndexRange       = tableIndexRange
        # self._tableSuggestCfg       = tableSuggestCfg
        # self._tableWidth            = tableWidth
        
        #print "\n%s  %s  %s  %s  %s %s  %s  %s\n" % (excelName, sheetName, csrName, regName, regType, regBaseAddr, regOffsetAddr, table_struct_name)

    @property
    def sheetName(self):
        return self._sheetName

    @sheetName.setter
    def sheetName(self, value):
        self._sheetName = value


    @property
    def csrName(self):
        return self._csrName

    @csrName.setter
    def csrName(self, value):
        self._csrName = value


    @property
    def regName(self):
        return self._regName

    @regName.setter
    def regName(self, value):
        self._regName = value


    @property
    def regBaseAddr(self):
        return self._regBaseAddr

    @regBaseAddr.setter
    def regBaseAddr(self, value):
        self._regBaseAddr = value


    @property
    def regOffsetAddr(self):
        return self._regOffsetAddr

    @regOffsetAddr.setter
    def regOffsetAddr(self, value):
        self._regOffsetAddr = value

    @property
    def nRegs(self):
        return self._nRegs

    @nRegs.setter
    def regType(self, value):
        self._nRegs = value


    @property
    def regType(self):
        return self._regType

    @regType.setter
    def regType(self, value):
        self._regType = value


    @property
    def regFieldList(self):
        return self._regFieldList

    def regFieldListAdd(self, value):
        self._regFieldList.append(value)

    def regFieldListInit(self):
        self._regFieldList = []

    @property
    def tabList(self):
        return self._tabList

    def tabListAdd(self, value):
        self._tabList.append(value)

    def tabListInit(self):
        self._tabList = []

    def get_register_num(self):
        pass
        # if self.regType != 'CAM' and self.regType != 'TAB':
        #     return 1
        # else:
        #     #print(self.regType,self._regFieldList[0].fieldRange)
        #     if self.regType == 'CAM':
        #         value = max(int(self._regFieldList[0].defaultVal), int(self._regFieldList[0].fieldRange))
        #     else:
        #         value = int(self._regFieldList[0].fieldRange)
        #
        #     num = value - 40
        #     if num <= 0:
        #         return 1
        #     else:
        #         if num % 64 == 0:
        #             return  (1 + num//64)
        #         else:
        #             return  (2 + num//64)


    def __str__(self):
        strTemp = 'CRegister object(regName: %s, regOffsetAddr: %s, regType: %s)\n' \
            %(self._regName, self._regOffsetAddr, self._regType)
        for field in self._regFieldList:
            strTemp += '        CField object(fieldName: %s, fieldRange: %s, fieldSuggestCfg: %s)\n' \
                %(field.fieldName, field.fieldRange, field.fieldSuggestCfg)

        for tab in self._tabList:
            strTemp += '        CTable object(tabName: %s, tabOffsetAddr: %s, tableDataValidWidth: %s, \
tableIndexRange: %s, \n\
                tableSuggestCfg: %s, tableWidth: %s)\n'\
                    %(tab._tabName, tab._tabOffsetAddr, tab._tableDataValidWidth, tab._tableIndexRange, \
                      tab._tableSuggestCfg, tab._tableWidth)
        return strTemp

    __repr__ = __str__

    def getRegisterReserveValue(self):
        if self._regFieldList[0].fieldName == 'reserved':
            return self._regFieldList[0].defaultVal
        else:
            return None

    @staticmethod
    def getFieldLen(fieldRange):
        if isinstance(fieldRange, int) or isinstance(fieldRange, float):
            return 1
        if isinstance(fieldRange, str):
            numList = fieldRange.split(":")
            if len(numList) == 2:
                return int(numList[0]) - int(numList[1]) + 1
            else:
                return 1

    @staticmethod
    def getFieldRangeToInt(fieldRange):
        if isinstance(fieldRange, int) or isinstance(fieldRange, float):
            return fieldRange
        if isinstance(fieldRange, str):
            numList = fieldRange.split(":")
            if len(numList) == 2:
                return (int(numList[0]), int(numList[1]))
            else:
                return fieldRange

    def GenerateCommand(self, baseAddr):
        strCommand = ""
        if self.regType not in ["CAM","TAB"]:
            """
            写寄存器命令模板：
            register write id 0 bar 10 base-addr 0xff offset-addr 0x10 len 64 data 0x1a2b3c4d5e6f7788
            """
            regSuggestCfg = ""
            for index, field in enumerate(self.regFieldList):
                regSuggestCfg += field.fieldSuggestCfg
                if index != len(self.regFieldList) - 1:
                    regSuggestCfg += ", "

            regSuggestCfg = ''.join([x for x in regSuggestCfg if x not in [" ","_"]])
            tokens = []
            CAssist.GetTokens(regSuggestCfg, tokens)
            regData = CAssist.tokensToData(tokens)
            if regData[-1] == "L":
                regData = regData[:-1]
            regCommand = "// " + self.regName + "\n"
            regCommand += "register write id %d bar %d base-addr %s offset-addr %s len 64 data %s\n"\
                            %(FPGA_ID, BAR_ID, baseAddr, self.regOffsetAddr, regData)
            logger.info(regCommand)
            strCommand += regCommand
        else:
            strCommand += "// " + self.regName + "\n"
            for tab in self.tabList:
                strCommand += tab.GenerateCommand(baseAddr)


        return strCommand




