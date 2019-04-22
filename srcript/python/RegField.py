# -*- coding: utf-8 -*-

__author__ = 'LI JUN'

class CField(object):
    """define a type for Field in register"""
    def __init__(self, name, len, bp, default = 0, desc = "The Field Name."):
        self._fieldName     = name
        self._fieldLen      = len
        self._fieldBp       = bp
        self._default       = default

        if desc.replace(" ", "") == "":
            self._desc  = "The Field Name."            
        else:
            desc = desc.replace("&", " ")
            desc = desc.replace("<", " ")
            desc = desc.replace(">", " ")
            desc = desc.replace("\n", " ")
            desc = desc.replace("\"", " ")
            self._desc = u"%s" % desc
        
        #self._fieldSuggestCfg   = defaultVal

    @property
    def fieldName(self):
        return self._fieldName

    @fieldName.setter
    def fieldName(self, value):
        self._fieldName = value

    @property
    def fieldLen(self):
        return self._fieldLen

    @fieldLen.setter
    def fieldRange(self, value):
        self._fieldLen = value

    @property
    def fieldBp(self):
        return self._fieldBp

    @fieldBp.setter
    def fieldBp(self, value):
        self._fieldBp = value

    def __str__(self):
        return 'CField object(fieldName: %s, fieldLen: %s, defaultVal: %s)' \
                    %(self._fieldName, self._fieldLen, self._fieldBp)

    __repr__ = __str__
