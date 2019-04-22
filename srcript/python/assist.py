# -*- coding: utf-8 -*-

__author__ = 'LI JUN'

from regLog import *
import re
import math
import sys

class CAssist(object):
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
    def GetTokens(str2, tokens):
        leftBraceCount = 0
        rightBraceCount = 0
        strLen = len(str2)
        str2 = ''.join([x for x in str2 if x != " "])
        for index, val in enumerate(str2):
            if "{" == val:
                ++leftBraceCount
            elif "}" == val:
                ++rightBraceCount
            else:
                pass

        if leftBraceCount != rightBraceCount:
            logger.error(CAssist.get_cur_info() + "{ } format error")
            return -1

        while str2[0] == '{':
            strLen = len(str2)
            if str2[0] == '{':
                leftBraceCount = 0
                rightBraceCount = 0
                index = 0
                for index, val in enumerate(str2):
                    if '{' == val:
                        leftBraceCount = leftBraceCount + 1
                    elif '}' == val:
                        rightBraceCount = rightBraceCount + 1
                    else:
                        pass

                    if leftBraceCount == rightBraceCount:
                        break

                if index == strLen-1:
                    str2 = str2[1:-1]
                else:
                    break


        startIndex = 0
        endIndex = 0
        braceFlag = 0
        strLen = len(str2)
        index = 0
        leftBraceCount = 0
        rightBraceCount = 0
        getTokenEn = 1
        repeatNum = 0
        while index < strLen:
            val = str2[index]
            if ',' == val and 1 == getTokenEn:
                endIndex = index
                tokens.append(str2[startIndex:endIndex])
                startIndex = index + 1
            if '{' == val:
                leftBraceCount = leftBraceCount + 1
                if index == 0:
                    startIndex = index
                    getTokenEn = 0

                if 1 == getTokenEn:
                    startIndex = index
                    if str2[index-1] != ',':
                        i = str2[:index].rfind(',')
                        repeatNum = int(str2[i+1:index])
                        logger.info("repeatNum = %d"%repeatNum)
                getTokenEn = 0
            if '}' == val:
                rightBraceCount = rightBraceCount + 1
                if rightBraceCount == leftBraceCount:
                    logger.info("rightBraceCount:%d   leftBraceCount:%d"%(rightBraceCount, leftBraceCount))
                    endIndex = index + 1
                    logger.info(str2[startIndex:endIndex])
                    if 0 == repeatNum:
                         CAssist.GetTokens(str2[startIndex:endIndex], tokens)
                    elif repeatNum > 0:
                        while repeatNum != 0:
                            CAssist.GetTokens(str2[startIndex:endIndex], tokens)
                            repeatNum = repeatNum - 1
                    else:
                        pass
                    braceFlag = 0
                    startIndex = index + 2
                    getTokenEn = 1
                    index = index + 1
                else:
                    pass

            index = index + 1

        if str2[startIndex:] != "":
            tokens.append(str2[startIndex:])

    @staticmethod
    def get_cur_info():
        strInfo = ""
        strInfo += "FILE_NAME:%s   "%sys._getframe().f_code.co_filename
        strInfo += "FUNC_NAME:%s   "%sys._getframe().f_code.co_name
        strInfo += "LINE_NUN :%s   "%sys._getframe().f_lineno

        return strInfo

    @staticmethod
    def tokensToData(tokens):
        strTemp = ""
        for strToken in tokens:
            m = re.match("(\d+)'(d|b|h)([0-9a-fA-F]+)", strToken)
            if None == m:
                logger.error(CAssist.get_cur_info())
            else:
                if 'd' == m.group(2) and None != re.match("\d+", m.group(3)):
                    strTemp = strTemp + (str(bin(int(m.group(3),10)))[2:]).zfill(int(m.group(1)))
                elif 'b' == m.group(2) and None != re.match("[01]+", m.group(3)):
                    strTemp = strTemp + (str(bin(int(m.group(3), 2)))[2:]).zfill(int(m.group(1)))
                elif 'h' == m.group(2) and None != re.match("[0-9a-fA-F]+", m.group(3)):
                    strTemp = strTemp + (str(bin(int(m.group(3),16)))[2:]).zfill(int(m.group(1)))
                else:
                    logger.error(CAssist.get_cur_info())

        return hex(int(strTemp,2))
