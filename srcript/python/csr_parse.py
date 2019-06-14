#-*- coding: utf-8 -*-

__author__ = 'LI JUN'


import os
import sys
import re
import xlrd
from collections import OrderedDict
import getopt
from regLog import *
from Register import CRegister
from RegField import CField
import time
import copy
#from table import CTable
#from regStruct import *
from assist import CAssist
#import copy

macroDict          = {} # store the macro name and the corresponding base address
tableFieldDict     = {} # store the table name and the corresponding fields infomation

ES480_Register_Sumup_reg_dict = {}

table_list_in_register_folder = ["policy"] # This list is used for table name which in register folder. The detail table struct dependence on this name.


class CCsrConfig(object):
    """description of class"""
    def __init__(self, excelName):
        self._registerDict      = OrderedDict()
        self._cfgParamDict      = OrderedDict()

        self._excelName         = excelName
        self._excelfd           = None
        self._for_sdk           = 0        

        #self._fieldNameSet      = set()
        #self._OffsetAddrSet     = set()

    def OpenExcel(self):
        #logger.info(self._excelName)
        if self._excelName == "":
            self._excelName = None
        else:
            self._excelfd = xlrd.open_workbook(self._excelName)
            for sheetName in self._excelfd.sheet_names():
                #logger.info("sheet name %s " % sheetName)
                pass

            #logger.info(CAssist.get_cur_info())

    def enable_for_sdk(self):
        self._for_sdk = 1

    def disable_for_sdk(self):
        self._for_sdk = 0
        

    def get_excel_name(self):
        str = self._excelName
        p = str.find("/")
        while(p>0):
            str = str[p+1:]
            p = str.find("/")
        return str

        
    def get_reg_name(self, str):
        name = str.replace('[n]', '')

        return name



    def initialize_the_table_fields(self):
       
        for sheetName in self._excelfd.sheet_names():
            
            #1过滤掉无用的sheet
            if sheetName in [u"版本记录", u"版本说明"]:
                continue
            
            table = self._excelfd.sheet_by_name(sheetName)
            #print sheetName
            tableName = sheetName.replace(" ", "")
            tableName = tableName.upper()
            
            tableCount = str(table.cell(1, 0).value)
            if tableCount.find("K") != -1 or tableCount.find("k") != -1:
                tableCount = int(tableCount[:-1])*1024
            else:
                tableCount = int(float(tableCount))


            #tableWidth = str(table.cell(1, 1).value)
            #print "%s --> is %s " % (sheetName, tableWidth)            
            #tableWidth = int(float(tableWidth))


            # find the column number of field description
            if table.cell(2, 5).value.lower() == "description":
                field_description = 5 
            else:
                if table.cell(2, 6).value.lower() == "description":
                    field_description = 6 
                else:
                    print "ERROR!!!!!! Can not found the column of field descritpion."
            
            tableType = table.cell(1, 2).value
            tableType = tableType.replace(" ", "")
            
            max_width = 0
                       
            row_start = 3 # default, from the 3                        
                        
            row = row_start
            keyTypeList = []
            while row < table.nrows:
                
                if 1 == 1: #table.cell(row, 0).value != "" :  # keyType can be null
                    keyType = table.cell(row, 0).value                                        
                    keyType = keyType.replace(" ", "")

                    pos_ = keyType.find("(")
                    if pos_ != -1:
                        keyType_name = keyType[:pos_]                        
                    else:
                        pos_ = keyType.find(u"（") # some chinese character
                        if pos_ != -1:
                            keyType_name = keyType[:pos_]
                        else:
                            keyType_name = keyType

                    keyType_name = keyType_name.upper()
                    #print "%-35s----  %-30s  ---- %s " % (sheetName, keyType, keyType_name)
                    
                    
                    if keyType.find("0x") != -1:
                        keyType = keyType[keyType.find("0x")+2:keyType.find(")")]
                        keyType = str(int(keyType,16))                        
                    else :
                        keyType = "NULL"

                    
                    fieldList = []
                    
                    (field_name, field_len, field_bp) = self.get_field_info(table.cell(row, 1).value, table.cell(row, 2).value)


                    ######################### consider at length > 64 bits ######################
                    if field_len > 64:

                        field_bp_tmp = field_bp
                        field_bp_len = field_len
                        
                        #print "######## %s ---- %d   %d " % (field_name, field_bp, field_len)
                                    
                        fieldObj = CField(field_name + "_0", 64, field_bp, desc = table.cell(row, field_description).value) # create the field obj
                        fieldList.append(fieldObj)
                        number = 1                                            
                        #print "%s  bp = %d len = %d " % (fieldObj._fieldName, fieldObj._fieldBp, fieldObj._fieldLen)
                                            
                        while( 1 ):
                            suffix = "_%s" % number
                                        
                            field_len -= 64
                                        
                            if field_len > 64:
                                field_bp = field_bp + 64
                                fieldObj = CField(field_name + suffix, 64, field_bp, desc = table.cell(row, field_description).value) # create the field obj
                                fieldList.append(fieldObj)
                                number += 1
                                            
                                #print "%s  bp = %d len = %d " % (fieldObj._fieldName, fieldObj._fieldBp, fieldObj._fieldLen)
                            else :
                                field_bp = field_bp + 64
                                fieldObj = CField(field_name + suffix, field_len%65, field_bp, desc = table.cell(row, field_description).value) # create the field obj
                                fieldList.append(fieldObj)
                                number += 1 
                                #print "%s  bp = %d len = %d " % (fieldObj._fieldName, fieldObj._fieldBp, fieldObj._fieldLen)
                                break

                        field_bp = field_bp_tmp
                        field_len = field_bp_len
                                    
                    else:
                        fieldObj = CField(field_name, field_len, field_bp, desc = table.cell(row, field_description).value) # create the field obj
                        fieldList.append(fieldObj)


                    tableWidth = field_bp + field_len  # the first field show the length of the table
                    
                    i = row + 1
                    if i != table.nrows :
                        while(table.cell(i, 0).value == ""):                        
                            if table.cell(i, 1).value != "":
                                (field_name, field_len, field_bp) = self.get_field_info(table.cell(i, 1).value, table.cell(i, 2).value)

                                ######################### consider at length > 64 bits ######################
                                
                                
                                if field_len > 64:

                                    field_bp_tmp = field_bp
                                    field_bp_len = field_len

                                    #print "######## %s ---- %d   %d " % (field_name, field_bp, field_len)
                                    
                                    fieldObj = CField(field_name + "_0", 64, field_bp, desc = table.cell(i, field_description).value) # create the field obj
                                    fieldList.append(fieldObj)
                                    number = 1                                            
                                    #print "%s  bp = %d len = %d " % (fieldObj._fieldName, fieldObj._fieldBp, fieldObj._fieldLen)
                                            
                                    while( 1 ):
                                        suffix = "_%s" % number
                                        
                                        field_len -= 64
                                        
                                        if field_len > 64:
                                            field_bp = field_bp + 64
                                            fieldObj = CField(field_name + suffix, 64, field_bp, desc = table.cell(i, field_description).value) # create the field obj
                                            fieldList.append(fieldObj)
                                            number += 1
                                            
                                            #print "%s  bp = %d len = %d " % (fieldObj._fieldName, fieldObj._fieldBp, fieldObj._fieldLen)
                                        else :
                                            field_bp = field_bp + 64
                                            fieldObj = CField(field_name + suffix, field_len%65, field_bp, desc = table.cell(i, field_description).value) # create the field obj
                                            fieldList.append(fieldObj)
                                            number += 1 
                                            #print "%s  bp = %d len = %d " % (fieldObj._fieldName, fieldObj._fieldBp, fieldObj._fieldLen)
                                            break                                        

                                    field_bp = field_bp_tmp
                                    field_len = field_bp_len
                                    
                                else:
                                    fieldObj = CField(field_name, field_len, field_bp, desc = table.cell(i, field_description).value) # create the field obj
                                    fieldList.append(fieldObj)
                                    
                            # else : 
                            # Here we can get the secondary  field information. currently, no need to implement.  

                            i += 1
                            if i == table.nrows :
                                break


                    # deal with some field  not ended with 0.
                    key_width = field_bp
                    tableWidth -= key_width
                    for fd in fieldList:
                        fd._fieldBp = fd._fieldBp - key_width

                    # get the max width of different key type
                    if tableWidth > max_width:
                        max_width = tableWidth

                    have_valid_bit = 0
                    for fd_ in fieldList:
                        fd_._fieldName = fd_._fieldName.replace("__", "_")

                        #if fd_._fieldName.lower().find("valid") != -1:
                        #    have_valid_bit = 1
                        #    print "%-8s %-30s %-8s %-20s bp=%4d, len=%4d" % (tableType, sheetName, keyType, fd_._fieldName, fd_._fieldBp, fd_._fieldLen)
                        
                    #if have_valid_bit == 0:
                    #    print "%-8s %-30s #########################################################" % (tableType, sheetName)
                    
                    keyTypeList.append([keyType, fieldList, tableWidth, max_width, keyType_name])
                    
                    row = i
                
                else :
                    row +=1

            for list_ in keyTypeList:
                list_[3] = max_width

            if tableName in tableFieldDict:
                print "Error %s already have." % tableName
            
            tableFieldDict[tableName] = [tableName, tableType, tableCount, keyTypeList, self._excelName]
            logger.debug("table_name = %s"%(tableName))






    def parse_table_fields(self):

        hash_list = []
        direct_list = []
        tcam_list = []
        other_list = []
        
        for info in tableFieldDict :
            tableInfo = tableFieldDict[info]
            if tableInfo[1].upper() == "HASH":                
                hash_list.append(tableInfo)
            else :
                if tableInfo[1].upper() == "DIRECT":                    
                    direct_list.append(tableInfo)
                else:
                    if tableInfo[1].upper() == "TCAM":                    
                        tcam_list.append(tableInfo)
                    else:
                        other_list.append(tableInfo)
            
        

        f = file("./tmp/allTableFieldInfo", 'w')        
        
        for _list in [hash_list, direct_list, tcam_list, other_list]:            
            for _ll in  _list :            
                f.write("%s  %s Count = %d  file: %s \n" % (_ll[1], _ll[0], _ll[2], _ll[4]))
                for fdList in _ll[3] :
                    f.write("    keyType = %s  width = %d\n" % (fdList[0], fdList[2]))
                f.write("\n")
            f.write("\n\n")
            
        f.close()                
        return


        
        for key in tableFieldDict :
            _ll = tableFieldDict[key]            
            print "%s  type = %s   Count = %d\n" % (_ll[0], _ll[1], _ll[2])            
            for fdList in _ll[3] :
                print "    keyType = %s  width = %d\n" % (fdList[0], fdList[2])
                for fd in fdList[1]:
                    #print "        name = %-20s  %d  %d\n" % (fd._fieldName, fd._fieldLen, fd._fieldBp)
                    pass


        
    def get_fields_by_tableNmae(self, tableName):
        
        if tableFieldDict.has_key(tableName) == True:
            #print "Found the fields for %s  TABLE  %s" % (tableFieldDict[tableName][1], tableName)            

            #if tableName == "VLAN_XLATE_DATA_ONLY_T":                
            #    for fdList in tableFieldDict[tableName][3]:
            #        for fd in fdList[1]:
            #            print " name = %-20s  bp = %d  len = %d\n" % (fd._fieldName, fd._fieldBp, fd._fieldLen)
                        
            return tableFieldDict[tableName]
        else :
            ###### Only for table pool start #######
            tableNameList = []
            pos = 0
            pos = tableName.find(",")
            while ( pos != -1):
                if tableFieldDict.has_key(tableName[0:pos]) == True:                
                    tableNameList.append(tableFieldDict[tableName[0:pos]])
                else :
                    print "Can not found the fields for %s" % tableName[0:pos]
                
                tableName = tableName[pos+1:]
                pos = tableName.find(",")

            if tableFieldDict.has_key(tableName[0:]) == True:                
                tableNameList.append(tableFieldDict[tableName[0:]])
                #logger.debug("TableName_ok = %s" % (tableName[0:]))
            else :
                #logger.debug("TableName_ERROR = %s" % (tableName[0:]))
                print "Can not found the fields for %s" % tableName[0:]
            
            if len(tableNameList) > 0:
                return ["", "TABLEPOOL", 0, tableNameList, ""]
        
            ###### Only for table pool end #######
            
            else:                
                return []
                

    


    def get_baseAddr_by_csrMacro(self, csrMacro):
        #print csrMacro
        #print '#####'
        if 'CB_COUNTER_ADDR_PREFIX'==csrMacro:
            print '########################'
            print '***********************'
            print '########################'
            print '***********************'
        if len(macroDict) > 0:
            if macroDict.has_key(csrMacro) == True:
                #print "Found the base address for %s" % csrMacro
                return macroDict[csrMacro]
            else:
                if ( csrMacro.find("0x") != -1):
                    pos = csrMacro.find("0x")
                    csrMacro1 = csrMacro[pos:]
                    #print '1q'
                    #print csrMacro1
                else:
                    if ( csrMacro.find("h") != -1):
                        pos = csrMacro.find("h")
                        csrMacro1 = "0x" + csrMacro[pos+1:]
                        print '2'
                        print csrMacro1
                    logger.debug(csrMacro)
                        
                #print "Can not found the base address for %s, transfer to %d" % (csrMacro, int(csrMacro_, 16))

                return int(csrMacro1, 16)
                
        # try to get the base addr through the macro
        #fd = xlrd.open_workbook(u"ES90_CSR节点地址分配_v1.6.xlsx")
        fd = xlrd.open_workbook("../reg_tab/ES90_CSR_node_addr_alloc_v1.6.xlsx")

        print "ES90_CSR_node_addr_alloc_v1.6.xlsx"
        f = file("./tmp/allMacro", 'w')
        
        for sheetName in fd.sheet_names():
            print sheetName
            #1过滤掉无用的sheet
            if sheetName in [u"版本记录", u"地址分配说明"]:
                continue
            
            table = fd.sheet_by_name(sheetName)
            row_start = 0
            
            #1过滤掉前面的标题部分
            for row in range(table.nrows):
                row_start = row + 1
                print "######################### %s "  % table.cell(row, 5).value
                
                if table.cell(row, 5).value.strip() == u"基地址": 
                    break
                
            
            
            row = row_start
            while row < table.nrows:
                if table.cell(row, 4).value == "" :
                    break
                macro = table.cell(row, 4).value
                base = table.cell(row, 5).value
                macro = macro.replace(" ", "")
                base = base.replace(" ", "")
                base = int(base[3:], 16)
                macroDict[macro] = base
                row += 1
                f.write("%10s  %-20s = %d \n" % (sheetName, macro, macroDict[macro]))
            
        f.close()

        if len(macroDict) > 0 : # for the first one macro
            if macroDict.has_key(csrMacro) == True:                
                #print macroDict[csrMacro]
                return macroDict[csrMacro]
        
        return "NULL"
    

    def get_reg_base_macro(self, str):
        nMacro = 1
        macroList = []

        str = str.replace("\n", "")
        str = str.replace(" ", "")
        str = str.replace(u"，", ",")

        
        while str.find(",") >= 0:
            p = str.find(",")
            nMacro += 1
            macroList.append(str[:p])
            str = str[p+1:]
        if str != "":    
            macroList.append(str)

        return macroList


    
    def get_reg_offset(self, str):

        pattorn = '(0[xX][0-9a-fA-F]+)\+[nN]([0-9]*)\*(0[xX][0-9a-fA-F]+)'
        ret = re.match(pattorn, str)

        if ret is None:
            # print "offset %d  %d  %d" % (int(str, 16), 1, 0)
            return (int(str, 16), 1, 0)
        else:
            # print "offset %s  %s  %s" % (ret.group(1),ret.group(2),ret.group(3))
            gro_2 = ret.group(2)
            # print 'gro_2 = ', gro_2
            if len(gro_2) == 0:
                gro_2 = '1'
            return (int(ret.group(1), 16), int(gro_2), int(ret.group(3), 16))


    def get_field_info(self, name, scop):
        scop = str(scop)
        scop = scop.replace("[", "")
        scop = scop.replace("]", "")
        s = scop.find(":")
        if s != -1:
            bp = int(scop[s+1:])
            length = int(scop[:s])-bp+1
        else :
            bp=0
            if scop != "":
                bp = int(float(scop))                
            length=1

        field_name = name.replace('[n]', '')        
        field_name = field_name.replace('[', '')
        field_name = field_name.replace(']', '')
        field_name = field_name.replace(':', '_')
        field_name = field_name.replace(' ', '_')
        field_name = field_name.replace('(', '_')
        field_name = field_name.replace(')', '_')

        if field_name[len(field_name)-1] == "_":            
            field_name = field_name[:-1]

        #print "%-20s  bp = %5d   len = %5d " % (field_name, bp, length)
        return (field_name, length, bp)


    def get_reg_field_info(self, name, scop, default):
        scop = str(scop)
        s = scop.find(":")
        if s != -1:
            bp = int(scop[s+1:])
            length = int(scop[:s])-bp+1
        else :
            bp=0
            if scop != "":
                bp = int(float(scop))                
            length=1

        field_name = name.replace('[n]', '')        
        field_name = field_name.replace('[', '')
        field_name = field_name.replace(']', '')
        field_name = field_name.replace(':', '_')
        field_name = field_name.replace(' ', '_')
        field_name = field_name.replace('(', '_')
        field_name = field_name.replace(')', '_')
        field_name = field_name.replace('__', '_')

        if field_name[len(field_name)-1] == "_":            
            field_name = field_name[:-1]


        old_ = default
        default = default.replace("_", "")
        default = default.replace(" ", "")
        if default.find("h") != -1:
            value = int(default[default.find("h")+1:], 16)
        else:
            if default.find("d") != -1:
                value = int(default[default.find("d")+1:], 10)
            else:
                if default.find("b") != -1:
                    value = int(default[default.find("b")+1:], 2)
                else:
                    if default == "":
                        value = 0
                    else:
                        value = int(default, 10)                        
                                        
        #print "%s --- %d " % (old_, value)
        
        
        #print "%s  bp = %d   len = %d " % (field_name, bp, length)
        return (field_name, length, bp, value)



    def checkMacro(self):         
        row_start = 0
        #logger.info(sys._getframe().f_code.co_name)

        objList = []       
        row = None

        f= file("./tmp/macro_not_define", "a")
        for sheetName in self._excelfd.sheet_names():
            print sheetName
            csrCfgSheet = self._excelfd.sheet_by_name(sheetName)
            #print csrCfgSheet.nrows
            if None != csrCfgSheet:
                #logger.info("csrCfgSheet: %s rows=%d"%(sheetName, csrCfgSheet.nrows))
                if csrCfgSheet.nrows == 0:
                    continue
                
                table = csrCfgSheet
                
            #1过滤掉无用的sheet
            if sheetName in [u"CSR寄存器填写规则及模板"]:
                continue
            if sheetName in [u"版本记录"]:
                continue

            for row in range(csrCfgSheet.nrows):
                #print row
                if table.cell(row, 0).value.strip() == u"基地址":
                    self.baseAddr = table.cell(row, 1).value
                    #print self.baseAddr
                    break                    
                if table.cell(row, 0).value.strip() == u"CSR节点号":
                    self.baseAddr = table.cell(row, 1).value
                    #print self.baseAddr
                    break
            if row+1 == csrCfgSheet.nrows : # if there is no macro info in the sheet
                continue
            
            macroList = self.get_reg_base_macro(self.baseAddr)
            #print macroList
            for csrMacro in macroList:
                base_addr = self.get_baseAddr_by_csrMacro(csrMacro)
                if base_addr == "NULL":                    
                    print "%s  %s Macro %s \n" % (self.get_excel_name(), sheetName, csrMacro)
                    f.write("%-30s  %-30s  %-30s \n" % (self.get_excel_name(), sheetName, csrMacro))
            
        f.close()   



    # judge if the reg need to expand
    def if_the_reg_need_expand(self, reg_name, mode_name, reg_type):
        #reg_name suffix with "_SET" or "_MASK" need expand
        reg_name  = reg_name.upper()
        mode_name = mode_name.upper()
        reg_type  = reg_type.upper()

        if mode_name == "TABLE_POOL": # registers in table pool, do not expand
            return 0
        
        if reg_name[-4:] == "_SET" or  reg_name[-5:] == "_MASK":        
            #print "########## reg_name ######## %s --- %s --- %s" % (mode_name, reg_name, reg_type)
            return 1

        if mode_name in ["MAC_COUNTER", "MAC_CLOCK", "MAC", "HSS"]:
            #print "########## mode_name ####### %s --- %s --- %s" % (mode_name, reg_name, reg_type)
            return 1

        if reg_type in ["RO", "IPSC", "IPSC2", "BPSC", "BPSC2", "INTWC", "ELOGF", "ELOGL"]:
            #print "########## reg_type ####### %s --- %s --- %s" % (mode_name, reg_name, reg_type)
            return 1
                
        return 0                                


    def get_field_list_in_ES480_Register_Sumup(self, reg_name__):

        if ES480_Register_Sumup_reg_dict.has_key(reg_name__) == True:
            #print "Found the fields for %s " % (reg_name__)                        
            return ES480_Register_Sumup_reg_dict[reg_name__]
        
        else :
            if len(ES480_Register_Sumup_reg_dict) != 0: # if already initialized
                return []
            
            #print "Initialize the ES480_Register_Sumup_reg_dict...."            
            _excelfd = xlrd.open_workbook("../reg_tab/ES90_Register_Sumup.xls")

            for sheetName in _excelfd.sheet_names():
                if sheetName == "multiplex":
                    table = _excelfd.sheet_by_name(sheetName)
                    
                    row = 1
                    while row < table.nrows :                                            
                        if table.cell(row, 0).value != "": # the first line of a register                        
                            fieldList = []

                            reg_type = table.cell(row, 6).value
                            nBits = 64
                            
                            reg_name = self.get_reg_name(table.cell(row, 0).value)
                            if reg_name[len(reg_name)-1] == "_":
                                #print "%s --- %s" % (reg_name, reg_name[:-1])
                                reg_name = reg_name[:-1]

                                                    
                            n_regs = table.cell(row, 2).value
                            #print "reg %s   n_regs = %d " % (reg_name, n_regs)
                            

                            (field_name, field_len, field_bp) = self.get_field_info(table.cell(row, 3).value, table.cell(row, 4).value)                        
                            fieldObj = CField(field_name, field_len, field_bp, 0, desc = table.cell(row, 5).value) # create the field obj
                            fieldList.append(fieldObj)
                            #print "             %-30s bp = %-5d len = %-5d" % (field_name, field_bp, field_len)

                            # get follow fields
                            i = row + 1
                            if i != table.nrows:
                                
                                while(table.cell(i, 0).value == ""):
                                    (field_name, field_len, field_bp) = self.get_field_info(table.cell(i, 3).value, table.cell(i, 4).value)                                
                                    fieldObj = CField(field_name, field_len, field_bp, 0, desc = table.cell(row, 5).value)
                                    fieldList.append(fieldObj)
                                    #print "             %-30s bp = %-5d len = %-5d" % (field_name, field_bp, field_len)
                                    i = i + 1
                                    if i == table.nrows:
                                        break
                        row = i
                        
                        if n_regs > 1:
                            
                            for n in range(int(n_regs)):                                                                
                                #print "reg_name %s_%d" % (reg_name.lower(), n)
                                new_reg_name = "%s_%d" % (reg_name.lower(), n)
                                ES480_Register_Sumup_reg_dict[new_reg_name] = fieldList
                        else:
                            #print "reg_name %s" % reg_name
                            ES480_Register_Sumup_reg_dict[reg_name.lower()] = fieldList
                        

            if ES480_Register_Sumup_reg_dict.has_key(reg_name__) == True:
                #print "Found the fields for %s " % (reg_name__)                        
                return ES480_Register_Sumup_reg_dict[reg_name__]
            else:
                return []

            

    def ReadCSRCfg(self):         
        row_start = 0
        #logger.info(sys._getframe().f_code.co_name)

        objList = []       
        row = None
        
        for sheetName in self._excelfd.sheet_names():
            csrCfgSheet = self._excelfd.sheet_by_name(sheetName)
            if None != csrCfgSheet:
                #logger.info("csrCfgSheet: %s rows=%d"%(sheetName, csrCfgSheet.nrows))
                if csrCfgSheet.nrows == 0:  # no content
                    continue
                table = csrCfgSheet
            #1过滤掉无用的sheet
            if sheetName in [u"CSR寄存器填写规则及模板",u"目录",u"版本记录"]:
                continue
                
            field_of_table = ""
            print csrCfgSheet
            
            #1过滤掉前面的标题部分
            for row in range(csrCfgSheet.nrows):                
                if table.cell(row, 0).value.strip() == u"基地址":
                    self.baseAddr = table.cell(row, 1).value
                    field_of_table = table.cell(row, 5).value
                    field_of_table = field_of_table.replace("\n", "")
                    field_of_table = field_of_table.replace(" ", "")
                    #print "######## %s " % field_of_table
                    
                if table.cell(row, 0).value.strip() == u"CSR节点号":
                    self.baseAddr = table.cell(row, 1).value
                    field_of_table = table.cell(row, 5).value
                    field_of_table = field_of_table.replace("\n", "")
                    field_of_table = field_of_table.replace(" ", "")
                    #print "######## %s " % field_of_table
                    
                if table.cell(row, 0).value.strip() == u"寄存器名字":
                    row_start = row + 1
                    break

            if row+1 == csrCfgSheet.nrows : # if there is no macro info in the sheet
                continue

            macroList = self.get_reg_base_macro(self.baseAddr)

            # only used to print the information about macros, can be deleted after the finished the project.
            #if len(macroList)>1:
            #    print "\n%s  --->   %s" % (self._excelName, sheetName)
            #    for iii in range(len(macroList)):
            #        print "     %s" % macroList[iii]


            # print the sheet name in table_csr_excel.
            #if self._excelName.find("table_csr_excel") != -1:
            #    print "%s  :  %-30s  : %s " % (self._excelName, sheetName, field_of_table)

            
            #正文部分开始遍历
            try:
                #print "len %d start %d \n" % (table.nrows, row_start)
                row = row_start
                while row < table.nrows :
                #for row in list(range(table.nrows))[row_start:]:

                    if table.cell(row, 0).value != "": # the first line of a register
                        
                        fieldList = []

                        reg_type = table.cell(row, 6).value
                        nBits = 64
                        
                        reg_name = self.get_reg_name(table.cell(row, 0).value)

                        if reg_name[len(reg_name)-1] == "_":
                            #print "%s --- %s" % (reg_name, reg_name[:-1])
                            reg_name = reg_name[:-1]

                        if reg_name.lower() == "eco_reg": # 
                            #print "%s --- %s --- %s" % (self.get_excel_name(), sheetName, reg_name)
                            row += 1
                            continue

                        # get the reg flag
                        if sheetName == "HSS" or sheetName == "CIU":
                            reg_flag = table.cell(row, 8).value
                            reg_flag = reg_flag.replace(" ", "")
                            if reg_flag == "":
                                reg_flag = "0"
                        else:
                            if self._excelName.find("counter") != -1:
                                reg_flag = "SOC_REG_FLAG_COUNTER"
                            else:
                                reg_flag = "0"

                        reg_bar = 4
                        if reg_flag == "SOC_REG_FLAG_VP_CODE":
                            reg_bar = 0

                        # reg_base = self.get_reg_base(self.baseAddr)
                        (reg_offset_start, n_regs, reg_offset_offset) = self.get_reg_offset(table.cell(row, 1).value)

                        (field_name, field_len, field_bp, default) = self.get_reg_field_info(table.cell(row, 3).value, table.cell(row, 4).value, table.cell(row, 5).value)

                        fieldObj = CField(field_name, field_len, field_bp, default, table.cell(row, 7).value) # create the field obj
                        fieldList.append(fieldObj)

                        table_index_count = 100 # assumed depth is 100, if not be specified
                        table_struct_name = sheetName
                        if reg_type in ["TAB","CAM"]: # if this is a table, do special operation to get the fields
                            # get the fields of the table
                            
                            fieldList = []                            
                            if field_of_table != "" or field_name in table_list_in_register_folder:   # if this is a table with detail fields info, especial deal with the tables in register folder.
                                if (field_name in table_list_in_register_folder) and (field_of_table == ""): # especial deal with the tables in register folder.
                                    nBits = field_bp # use the len in the sheet, bp is the length
                                    field_info = self.get_fields_by_tableNmae(field_name.upper())
                                    table_struct_name = field_name.upper()
                                else:
                                    field_info = self.get_fields_by_tableNmae(field_of_table.upper()) # here field name is the table name, capital
                                    table_struct_name = field_of_table.upper()

                                                                                                
                                if len(field_info) == 0 :                                    
                                    print "Have not found the field info for table %s, The detial fields for the table will lost." % field_of_table                                    
                                    # Still use the default info, not from excel in folder 'Tabls'.
                                    field_len = field_bp # some error in the excel file, we do this to avoid the error
                                    field_bp = 0            # some error in the excel file, we do this to avoid the error
                                    nBits = field_len   # some error in the excel file, we do this to avoid the error

                                    fieldObj = CField(field_name, field_len, field_bp, table.cell(row, 7).value) 
                                    fieldList = [fieldObj]                                
                                    fieldList = [["NULL", fieldList, nBits, nBits]] # keytype should be NULL

                                    

                                else:
                                    #if self._excelName.find("table_csr_excel") != -1:
                                    #    print "For %s --> Mode: %s\n" % (self._excelName, sheetName)

                                    table_index_count = field_info[2]
                                    reg_type = field_info[1] # set type to HASH or DIRECT or TCAM, only for TABLE
                                    if reg_type == "":
                                        reg_type = "UNKNOWEN"
                                        print "Table type for %s not filled...." % field_of_table.upper()
                                    fieldList = field_info[3]  # here, the list maybe have several kinds of fields with different keyTypes and width

                            else: # this is a table, but no detial fields info
                                #print "table in register folder....."
                                #if self._excelName.find("table_csr_excel") != -1:
                                #    print "Not fill the table index for:  %s-->%s " % (self._excelName, sheetName)
                                
                                field_len = field_bp # some error in the excel file, we do this to avoid the error
                                field_bp = 0            # some error in the excel file, we do this to avoid the error
                                nBits = field_len   # some error in the excel file, we do this to avoid the error

                                fieldObj = CField(field_name, field_len, field_bp, table.cell(row, 7).value) 
                                fieldList = [fieldObj]                                
                                fieldList = [["NULL", fieldList, nBits, nBits]] # keytype should be NULL

                                table_struct_name = reg_name.upper()  # assume the table struct name is the table name

                            
                            reg_name = table_struct_name # set the table name with the table struct name                            
                            if nBits <= 40:
                                shift = 1
                            else :
                                shift = 1 + (nBits - 41 + 64) / 64 
                            i = row + shift

                            if field_of_table != "":   # there is no more info
                                i = table.nrows

                            if sheetName in ["table_pool"] :
                                i = row + 14 # table pool have 864 bits

                        else: # it's a register, get follow fields
                            i = row + 1
                            if i != table.nrows:
                                while(table.cell(i, 0).value.rstrip() == ''):
                                    (field_name, field_len, field_bp, default) = self.get_reg_field_info(table.cell(i, 3).value, table.cell(i, 4).value, table.cell(i, 5).value)
                                    fieldObj = CField(field_name, field_len, field_bp, default, table.cell(i, 7).value)
                                    fieldList.append(fieldObj)

                                    i = i + 1
                                    if i == table.nrows:
                                        break
                        row = i

                        sheetName = sheetName.replace(".", "")
                        sheetName = sheetName.replace(" ", "")
                        mode_name = sheetName

                        if reg_type == "R0":
                            print "ERRRRRRRRRRROOOOOOOOORRRRRRRRR : %s --- %s --- %s type is R0" % (self.get_excel_name(), sheetName, reg_name) 

                        expand = self.if_the_reg_need_expand(reg_name, mode_name, reg_type)  # judge if the reg need to expand


                        if n_regs > 1:
                            for n in range(n_regs): # create the register obj                            
                                reg_offset = reg_offset_start + n*reg_offset_offset
                                reg_name_tmp = reg_name + '_%s' % (n)

                                #######################################################
                                # Deal with the register in ES90_Register_Sumup.xlsx #
                                
                                fieldList_for_reg_in_ES480_Register_Sumup = self.get_field_list_in_ES480_Register_Sumup(reg_name_tmp.lower())                        
                                if len(fieldList_for_reg_in_ES480_Register_Sumup) > 0 :
                                    #print "reg -----%s----- fieldList found ..................\n" % reg_name_tmp
                                    fieldList = fieldList_for_reg_in_ES480_Register_Sumup
                                    
                                #######################################################

                                i = 0
                                
                                if expand == 1 and len(macroList) > 1: 
                                    for csrMacro in macroList:                                        
                                        if len(macroList) > 1: 
                                            mode_name = ("%s_%s") % (sheetName, i)
                                            i += 1
                                        base_addr = [] # only one base address
                                        base_addr.append(self.get_baseAddr_by_csrMacro(csrMacro))
                                        
                                        regObj = CRegister(self.get_excel_name(), mode_name, csrMacro, mode_name + "_" + reg_name_tmp, reg_type, base_addr, reg_offset, n_regs, nBits, table_index_count, table_struct_name, sheetName, len(macroList), reg_name, reg_flag, reg_bar, 0, table_index_count-1)
                                        regObj._regFieldList = fieldList
                                        objList.append(regObj)

                                else:
                                    base_addr = [] # have more than one address, how many macro then how many base address
                                    for csrMacro in macroList:                                    
                                        base_addr.append(self.get_baseAddr_by_csrMacro(csrMacro))
                                        
                                    regObj = CRegister(self.get_excel_name(), mode_name, csrMacro, reg_name_tmp, reg_type, base_addr, reg_offset, n_regs, nBits, table_index_count, table_struct_name, sheetName, len(macroList), reg_name, reg_flag, reg_bar, 0, table_index_count-1)
                                    regObj._regFieldList = fieldList
                                    objList.append(regObj)
                                    
                        else :
                                reg_offset = reg_offset_start                                
                                i = 0

                                #######################################################
                                # Deal with the register in ES90_Register_Sumup.xlsx #
                                
                                fieldList_for_reg_in_ES480_Register_Sumup = self.get_field_list_in_ES480_Register_Sumup(reg_name.lower())                        
                                if len(fieldList_for_reg_in_ES480_Register_Sumup) > 0 :
                                    #print "reg -----%s----- fieldList found ..................\n" % reg_name
                                    fieldList = fieldList_for_reg_in_ES480_Register_Sumup
                                    
                                #######################################################
                            
                                if expand == 1 and len(macroList) > 1:
                                    for csrMacro in macroList:
                                        if len(macroList) > 1:
                                            mode_name = ("%s_%s") % (sheetName, i)
                                            i += 1
                                        base_addr = []
                                        base_addr.append(self.get_baseAddr_by_csrMacro(csrMacro))
                                        
                                        regObj = CRegister(self.get_excel_name(), mode_name, csrMacro, mode_name + "_" +  reg_name, reg_type, base_addr, reg_offset, n_regs, nBits, table_index_count, table_struct_name, sheetName, len(macroList), reg_name, reg_flag, reg_bar, 0, table_index_count-1)
                                        regObj._regFieldList = fieldList
                                        objList.append(regObj)

                                else:
                                    base_addr = []
                                    for csrMacro in macroList:                                    
                                        base_addr.append(self.get_baseAddr_by_csrMacro(csrMacro))
                                        
                                    regObj = CRegister(self.get_excel_name(), mode_name, csrMacro, reg_name, reg_type, base_addr, reg_offset, n_regs, nBits, table_index_count, table_struct_name, sheetName, len(macroList), reg_name, reg_flag, reg_bar, 0, table_index_count-1)
                                    regObj._regFieldList = fieldList
                                    objList.append(regObj)
                    else:
                        row +=1
                                                
            except Exception as e:
                time.sleep(0.2)
                logger.error("%s"%e)
                logger.error("error: %s table.nrows = %d, rownum = %d\n"%(sheetName, table.nrows, row))
                time.sleep(0.1)

        return objList



    def parse_physical_table_excel_file(self):         

        print "parse_physical_table_excel_file..."

        row_start = 0
        #logger.info(sys._getframe().f_code.co_name)
                
        have_tab_struct_objList = []
        no_tab_struct_objList   = []
        row = None
        
        for sheetName in self._excelfd.sheet_names():
            csrCfgSheet = self._excelfd.sheet_by_name(sheetName)
            if None != csrCfgSheet:
                #logger.info("csrCfgSheet: %s rows=%d"%(sheetName, csrCfgSheet.nrows))
                if csrCfgSheet.nrows == 0:  # no content
                    continue
                table = csrCfgSheet

            
            #正文部分开始遍历
            try:
                #print "len %d start %d \n" % (table.nrows, row_start)
                row = 1
                while row < table.nrows :                
                                        
                    reg_name = table.cell(row, 0).value
                    reg_name = reg_name.replace(" ", "")
                    reg_type = table.cell(row, 1).value                    
                    nBits = table.cell(row, 2).value

                    idx_min = table.cell(row, 3).value
                    idx_max = table.cell(row, 4).value                    
                    table_index_count = idx_max - idx_min + 1

                    baseAddr = self.get_baseAddr_by_csrMacro(table.cell(row, 5).value)
                    reg_offset = int(table.cell(row, 6).value, 16)
                    
                    table_struct_name = table.cell(row, 8).value
                    table_struct_name = table_struct_name.replace(" ", "")

                    fieldList = []
                    
                    # get the detial fields
                    if table_struct_name != "":
                        field_info = self.get_fields_by_tableNmae(table_struct_name.upper()) # here field name is the table name, capital
                        reg_type = field_info[1] # set type to HASH or DIRECT or TCAM, only for TABLE
                        if reg_type == "":
                            reg_type = "UNKNOWEN"
                            print "Table type for %s not filled...." % table_struct_name.upper()
                        fieldList = field_info[3]
                                        
                    mode_name = sheetName

                    reg_flag = table.cell(row, 7).value
                    reg_flag = reg_flag.replace(" ", "")
                    if reg_flag == "":
                        reg_flag = "0"

                    reg_bar = 4
                    #print "name=%s type=%s nBits=%d index=%d baseaddr=%d offset=%d struct_name=%s mode_name=%s" % (reg_name, reg_type, nBits, table_index_count, baseAddr, reg_offset, table_struct_name, mode_name)


                    if table_struct_name == "":
                        table_struct_name = reg_name
                    
                        regObj = CRegister(self.get_excel_name(), mode_name, "", reg_name, reg_type, [baseAddr], reg_offset, 1, nBits, table_index_count, table_struct_name, sheetName, 1, reg_name, reg_flag, reg_bar, idx_min, idx_max)
                        regObj._regFieldList = fieldList
                        no_tab_struct_objList.append(regObj)
                    else:
                        regObj = CRegister(self.get_excel_name(), mode_name, "", reg_name, reg_type, [baseAddr], reg_offset, 1, nBits, table_index_count, table_struct_name, sheetName, 1, reg_name, reg_flag, reg_bar, idx_min, idx_max)
                        regObj._regFieldList = fieldList
                        have_tab_struct_objList.append(regObj)

                    
                    row +=1
                                                
            except Exception as e:                
                logger.error("%s"%e)
                logger.error("error: %s table.nrows = %d, rownum = %d\n"%(sheetName, table.nrows, row))
            #finally:

                #print 'finally'
                #logger.info(u"This sheet %s has %d register. There are %s"\
                #            %(sheetName, len(regInfoList), str(regInfoList)))

        return [have_tab_struct_objList, no_tab_struct_objList]


    def GenerateCommand(self):
        strCommand = ""
        for regName, register in self._registerDict.items():
            if register != None:
                strCommand += register.GenerateCommand(self.baseAddr)
                strCommand += "\n"
        saveFileNamePath = ((self._excelName.lower()).split("."))[0]
        saveFileNamePath += ".command"
        with open(saveFileNamePath,"w") as file:
            file.write(strCommand)





    def _attr_str(self):
        code_str = ''

        for register in self._registerDict.values():
            reg_name = register.regName
            #判断寄存器类型，如果是TAB或者CAM则需要只需要取出_M的，并取出寄存器的名字
            if register.regType in ['TAB', 'CAM']:
                if register.regName[-1:] != 'M':
                    continue
                else:
                    reg_name = reg_name[:-2]

            if register.regType != 'TAB' and register.regType !='CAM' :
                reserve_value = register.getRegisterReserveValue()
                if reserve_value is None:
                    chl = '{%s};' % (reg_name)
                else:
                    chl = '{%s,%s};' % (reserve_value, reg_name)
            else:
                chl = reg_name + ';'
            #print('register num:', register.get_register_num())

            regNum = register.get_register_num()
            if regNum == 1:
                code_str += '			    12\'h%s:reg_rd_data <= %s\n' % (register.regOffsetAddr[2:], chl)
            else:
                ss = ''
                for i in range(regNum):
                    off = int(register.regOffsetAddr, 16) + i
                    off_str = hex(off)[2:].zfill(3)
                    ss += '12\'h%s,' % off_str.upper()
                ss = ss[:-1]   #去掉末尾的逗号
                code_str += '			    %s:reg_rd_data <= %s\n' % (ss, chl)
        code_str += '			    default:reg_rd_data <= 64\'h00;'
        return code_str
    

    def getAddrOffsetFormat(self, regAddrOffset):
        pattorn = '(0[xX][0-9a-fA-F]+)\+[nN]([0-9]+)\*(0[xX][0-9a-fA-F]+)'
        ret = re.match(pattorn, regAddrOffset)
        if ret is None:
            return None
        else:
            return (int(ret.group(1), 16), int(ret.group(2)), int(ret.group(3), 16))


        

    def _addRegRepeat(self, register_dict, register_tem, unit, space):
        register_temp = None
        n = 0
        reg_name_tem = ''
        for i in range(unit):
            for index in range(len(register_tem)):
                register = copy.copy(register_tem[index])
                register.regOffsetAddr = hex(int(register.regOffsetAddr, 16) + i*space)
                reg_name_tem = register.regName
                if register.regType in ['TAB', 'CAM'] and register.regName[-2:] == '_M':
                    #register.regName = register.regName[:-2] + '_%d'%i + '_M'
                    register.regName = register.regName.replace('[n]', str(i))
                else:
                    #register.regName += '_%d'%i
                    register.regName = register.regName.replace('[n]', str(i))

                #判断需要添加位置是否在末尾
                if reg_name_tem[-3:] == '[n]':
                    if i>=0 and i<=9:
                        end_len = -1
                    elif i>=10 and i<=99:
                        end_len = -2
                    else:
                        end_len = -3
                    if n == 2 or n == 1:
                        if register.regName[-4+end_len:end_len] == '_SET':
                            register_temp.regIntSet = register
                            register.regINTRW  = register_temp
                        if register.regName[-5+end_len:end_len] == '_MASK':
                            register_temp.regIntMask = register
                            register.regINTRW  = register_temp
                        n -= 1
                else:
                    if n == 2 or n == 1:
                        if register.regName[-4:] == '_SET':
                            register_temp.regIntSet = register
                            register.regINTRW  = register_temp
                        if register.regName[-5:] == '_MASK':
                            register_temp.regIntMask = register
                            register.regINTRW  = register_temp
                        n -= 1



                if register.regType == 'INTWC':
                    n = 2
                    register_temp = register


                register.regFieldListInit()
                for field in (register_tem[index].regFieldList):
                    field = copy.copy(field)
                    if field.fieldName != 'reserved':
                        #field.fieldName += '_%d' % i
                        field.fieldName = field.fieldName.replace('[n]', str(i))
                    register.regFieldListAdd(field)
                self._registerDict[register.regName] = register




    def checkFieldName(self, fieldName, row, column):
        ret = True
        row = row + 1
        column = column +1
        if not fieldName:
            # 如果字段名字为空，记录日志，并标志格式error
            logger.error(u"CSR配置表: fieldName: NULL(row = %d, column = %d)"\
                         %(row, column))
            ret = False
        else:
            str_name = fieldName.replace('[n]', '')
            m = re.match(matchRuleStr, str_name)
            #m = re.match(matchRuleStr,fieldName)
            if m == None:
                # 字段名字只能为数字、字母、下划线，但不能以数字开头
                logger.error(u"CSR配置表: fieldName format: %s(row = %d, column = %d)"\
                             %(fieldName, row, column))
                ret = False
            elif fieldName != "reserved":
                if fieldName in self._fieldNameSet:
                    # 如果字段名字有重复，记录日志，并标志格式error
                    logger.error(u"CSR配置表: fieldName repetition: %s(row = %d, column = %d)"\
                                 %(fieldName, row, column))
                    ret = False
            else:
                pass

        if ret == False:
            self._formatError = True
        else:
            self._fieldNameSet.add(fieldName)



    def checkfieldOrTabIndexRangeAndDefaultVal(self, regFieldList):
        curFieldStart = 0
        lastFieldEnd = -1
        count = 0
        curLen = 0


        for field in reversed(regFieldList):
            m = re.match("(\d+)(:(\d+))?", str(field.fieldOrTabIndexRange))
            if None == m:
                return False
            else:
                if None == m.group(3):
                    curFieldEnd     = int(m.group(1))
                    curFieldStart   = int(m.group(1))
                else:
                    curFieldEnd     = int(m.group(1))
                    curFieldStart   = int(m.group(3))

                if curFieldStart != (lastFieldEnd + 1):
                    return False

                curLen = curFieldEnd - curFieldStart + 1
                count += curLen

                lastFieldEnd = curFieldEnd


            m = re.match("(\d+)'([hbd])([0-9a-fA-F]+)", field.defaultVal)
            if None == m:
                n = re.match("`[A-Za-z]+$", field.defaultVal)
                if n == None:
                    return False
                else:
                    return 'WARNING'
            else:
                len = int(m.group(1))
                if len != curLen:
                    return False

                if m.group(2) == 'h' and int(m.group(3), 16) > int('F' * len, 16):
                    return  False
                if m.group(2) == 'b' and int(m.group(3), 2) > int('1'*len, 2):
                    return False
                if m.group(2) == 'd' and int(m.group(3)) > int('9'*len, 10):
                    return False

        if (lastFieldEnd != 63) and (count != 64):
            return False

        return True


    def checkRegName(self, regName, row, column):
        row = row + 1
        column = column +1
        if regName == "":
            # 如果寄存器名字为空，记录日志，并标志格式error
            logger.error(u"CSR配置表: regName: NULL(row = %d, column = %d)"\
                         %(row, column))
            self._formatError = True
        else:
            reg_str = regName.replace('[n]', '')
            m = re.match(matchRuleStr, reg_str)
           # m = re.match(matchRuleStr, regName)
            if m == None:
                # 寄存器名字只能为数字、字母、下划线，但不能以数字开头
                logger.error(u"CSR配置表: regName format: %s(row = %d, column = %d)"\
                             %(regName, row, column))
                self._formatError = True
            else:
                if regName in self._registerDict:
                    # 如果有寄存器名字重复，记录日志，并标志格式error
                    logger.error(u"CSR配置表: regName repetition: %s(row = %d, column = %d)"\
                                 %(regName, row, column))
                    self._formatError = True

                    

    def checkCsrPoint(self, csrPoint, row, column):
        row = row + 1
        column = column +1
        if csrPoint == "":
            # 如果节点号为空，记录日志，并标志格式error
            logger.error(u"CSR配置表: CSR point: NULL(row = %d, column = %d)"\
                         %(row, column))
            self._formatError = True
        else:
            m = re.match("[0-9]+\'h([0-9a-fA-F]+)", csrPoint)
            if m == None:
                # 节点号格式不对
                logger.error(u"CSR配置表: CSR point format: %s(row = %d, column = %d)"\
                             %(csrPoint, row, column))
                self._formatError = True


    def checkBaseAddr(self, baseAddr, row, column):
        row = row + 1
        column = column +1
        if baseAddr == "":
            # 如果寄存器偏移量为空，记录日志，并标志格式error
            logger.error(u"CSR配置表: baseAddr: NULL(row = %d, column = %d)"\
                         %(row, column))
            self._formatError = True
        else:
            m = re.match("0[xX]([0-9a-fA-F]+)", baseAddr)
            if m == None:
                # 基地址格式不对
                logger.error(u"CSR配置表: baseAddr format: %s(row = %d, column = %d)"\
                             %(baseAddr, row, column))
                self._formatError = True
            else:
                self._baseAddrLen = len(m.group(1))
                if self._baseAddrLen != 2:
                    # 基地址格式不对
                    logger.error(u"CSR配置表: baseAddr format: %s(row = %d, column = %d)"\
                                 %(baseAddr, row, column))
                    self._formatError = True


    def checkRegOffset(self, regOffsetAddr, row, column):
        row = row + 1
        column = column +1
        if regOffsetAddr == "":
            # 如果寄存器偏移量为空，记录日志，并标志格式error
            logger.error(u"CSR配置表: regOffsetAddr: NULL(row = %d, column = %d)"\
                         %(row, column))
            self._formatError = True
        else:
            RuleStr = "0[xX]([0-9a-fA-F]+)"     #tchen改
            m = re.match(RuleStr, regOffsetAddr)
            if m == None:
                # 寄存器偏移量不符合填写格式规范
                logger.error(u"CSR配置表: regOffsetAddr format: %s(row = %d, column = %d)"\
                             %(regOffsetAddr, row, column))
                self._formatError = True
            else:
                if regOffsetAddr in self._OffsetAddrSet:
                    # 如果有寄存器偏移量地址重复，记录日志，并标志格式error
                    logger.error(u"CSR配置表: regOffsetAddr repetition: %s(row = %d, column = %d)"\
                                 %(regOffsetAddr, row, column))
                    self._formatError = True
                else:
                    self._OffsetAddrSet.add(regOffsetAddr)


    # 检查regName之后的两个连续寄存器是否为"%s_SET"%regName,"%s_MASK"%regName
    def checkINT(self, regNameCellList, rowNum, regName):
        setName = self._table.cell(regNameCellList[rowNum + 1][0], regNameCellList[rowNum + 1][2]).value
        maskName = self._table.cell(regNameCellList[rowNum + 2][0], regNameCellList[rowNum + 2][2]).value
        if setName != "%s_SET"%regName:
            logger.error(u"CSR配置表:   no %s_SET for %s(row = %d, column = 1)"\
                 %(regName, regName, rowNum + 1))
            self._formatError = True

        if maskName != "%s_MASK"%regName:
            logger.error(u"CSR配置表:   no %s_MASK for %s(row = %d, column = 1)"\
                 %(regName, regName, rowNum + 1))
            self._formatError = True


    def checkRegType(self, regType, row, column):
        row = row + 1
        column = column +1
        if regType == "":
            # 如果寄存器类型为空，记录日志，并标志格式error
            logger.error(u"CSR配置表: regType: NULL(row = %d, column = %d)"%\
                         (row, column))
            self._formatError = True
        else:
            if regType not in ["RW", "RO", "IPSC", "IPSC2", "BPSC", "BPSC2",
                               "RW1C", "ELOGF", "ELOGL", "TAB", "CAM", "INTWC"]:
                # 寄存器名字只能为数字、字母、下划线，但不能以数字开头
                logger.error(u"CSR配置表: regType format: %s(row = %d, column = %d)"\
                             %(regType, row, column))
                self._formatError = True

    #检查最低位不能是reserved
    def checkFieldNameReserved(self, regFieldList):
        for field in reversed(regFieldList):
            if field.fieldName == 'reserved':
                return False
            else:
                return True

    #检查INT MASK SET的reserved对应位相同
    def checkIMSReserved(self, registerInt, registerMask, registerSet):
        int_field_list = registerInt.regFieldList
        mask_field_list = registerMask.regFieldList
        set_field_list = registerSet.regFieldList

        int_range_list = []
        mask_range_list = []
        set_range_list = []

        for field in int_field_list:
            if field.fieldName != 'reserved':
                int_range_list.append(CAssist.getFieldLen(field.fieldOrTabIndexRange))
        for field in mask_field_list:
            if field.fieldName != 'reserved':
                mask_range_list.append(CAssist.getFieldLen(field.fieldOrTabIndexRange))
        for field in set_field_list:
            if field.fieldName != 'reserved':
                set_range_list.append(CRegister.getFieldLen(field.fieldOrTabIndexRange))

        if len(int_range_list) == len(mask_range_list) and len(int_range_list) == len(set_range_list):
            list_len  = len(int_range_list)
            for index in range(list_len):
                if int_range_list[index] not in mask_range_list:
                    return False
                if int_range_list[index] not in set_range_list:
                    return False
                if mask_range_list[index] not in int_range_list:
                    return False
                if mask_range_list[index] not in set_range_list:
                    return False
                if set_range_list[index] not in mask_range_list:
                    return False
                if set_range_list[index] not in int_range_list:
                    return False
            return True
        else:
            return False



    def checkTabCamReg(self,regName, regFieldName, regFieldRange, regFieldDefault, row, colum):
        if regName[-2:] == '_M':
            if not regFieldName:
                #字段名称为空
                logger.error(u"CSR配置表: regFieldName: NULL(row = %d, column = %d)"\
                                         %(row+1, colum + FIELD_NAME_OR_TABLE_WIDTH + 1))
                self._formatError = True


            if not regFieldRange:
                #字段范围为空
                logger.error(u"CSR配置表: regFieldRange: NULL(row = %d, column = %d)"\
                                         %(row+1, colum + FIELD_OR_INDEX_RANGE + 1))
                self._formatError = True

            if  (regFieldDefault == '' or regFieldDefault is None):
                #字段默认值未填写
                logger.error(u"CSR配置表: regDefaultVal: NULL(row = %d, column = %d)"\
                                         %(row+1, colum + SUGGEST_CFG + 1))
                self._formatError = True
            return

        else:
            ret = re.search('_S([0-9]+)$', regName)
            if ret is None:
                #名称错误
                print(regName)
                logger.error(u"CSR配置表: regName is wrong(row = %d, column = %d)"\
                                             %(row+1, colum + REG_NAME + 1))
                self._formatError = True
            else:

                if regFieldName:
                    #非_M的字段名称未合并
                    logger.error(u"CSR配置表: regFieldName not merge(row = %d, column = %d)"\
                                                 %(row+1, colum + FIELD_NAME_OR_TABLE_WIDTH + 1))
                    self._formatError = True
                    pass

                if regFieldRange:
                    #非_M的字段范围未合并
                    logger.error(u"CSR配置表: regFieldRange not merge(row = %d, column = %d)"\
                                                 %(row+1, colum + FIELD_OR_INDEX_RANGE + 1))
                    self._formatError = True


                if (regFieldDefault != '' and regFieldDefault is not None):
                    #非_M字段默认值未合并
                    logger.error(u"CSR配置表: field DefaultVal not merge(row = %d, column = %d)"\
                                                 %(row+1, colum + SUGGEST_CFG + 1))
                    self._formatError = True

            return



