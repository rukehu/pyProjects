# -*- coding: utf-8 -*-

__author__ = 'LI JUN'

import getopt
from csr_parse import *
from Gen_files import *
from Soc_gen_files import *
from Soc_gen_files_for_sdk import *
import sys
import copy


def usage():
    print("Usage:python Qos_cfg.py [configFileName]")


def find_reg_by_name(_list, name):
    for reg in _list:
        if reg._regName == name:
            return 1

    return 0


# Take the table struct name as the mode name, create the new mode and add it to the dict. Delete the table_pool mode
def reconstruct_table_for_table_pool(sameModeObjsDict):
    print "reconstruct_table_for_table_pool"

    mode = "table_pool"
    mem = copy.deepcopy(sameModeObjsDict[mode][2][1][0])
    regList = sameModeObjsDict[mode][2][1]
    for reg in range(sameModeObjsDict[mode][2][0]):
        for tableInfo in regList[reg]._regFieldList:  # there six tables' field stored in the field list

            mem._regName = tableInfo[0]
            mem._sheetName = mode
            mem._regType = tableInfo[1]
            mem._tableCount = tableInfo[2]
            mem._regFieldList = tableInfo[3]
            mem._table_struct_name = tableInfo[0]
            mem._modeName = tableInfo[0]

            # change the sheet name of registers in table pool
            regList__ = copy.deepcopy(sameModeObjsDict[mode][1][1])
            for reg__ in range(sameModeObjsDict[mode][1][0]):
                regList__[reg__]._sheetName = tableInfo[0]
                regList__[reg__]._modeName = tableInfo[0]
                regList__[reg__]._regName = (regList__[reg__]._sheetName + "_" + regList__[
                    reg__]._regName).lower()  # change the regName in table pool
                regList__[reg__]._old_sheetName = tableInfo[0]
            sameModeObjsDict[tableInfo[0]] = [tableInfo[0], [sameModeObjsDict[mode][1][0], copy.deepcopy(regList__)],
                                              [1, [copy.deepcopy(mem)]]]

    del sameModeObjsDict[mode]

    return sameModeObjsDict


def reconstruct_hash_tcam_table(sameModeObjsDict):
    reg_list = []
    mem_list = []
    already_mixed_key = []
    count = 0
    for mode in sameModeObjsDict:
        if mode in hash_tcam_key_list:
            continue

        for ii in range(len(hash_tcam_data_list)):  # mixed the data and key table.
            if mode == hash_tcam_data_list[ii]:
                print "mixed %s " % mode
                key_mode_name = hash_tcam_key_list[ii]
                sameModeObjsDict[mode][1][0] += copy.deepcopy(sameModeObjsDict[key_mode_name][1][0])
                sameModeObjsDict[mode][1][1] += copy.deepcopy(sameModeObjsDict[key_mode_name][1][1])
                sameModeObjsDict[mode][2][0] += copy.deepcopy(sameModeObjsDict[key_mode_name][2][0])
                sameModeObjsDict[mode][2][1] += copy.deepcopy(
                    sameModeObjsDict[key_mode_name][2][1])  # must added the data before the key.

                """
                if mode == "st_l3_defip": # only for table pool ad2                    
                    mode__ = "table_pool"
                    mem = copy.deepcopy(sameModeObjsDict[mode__][2][1][0])
                    regList = sameModeObjsDict[mode__][2][1]
                    for reg in range(sameModeObjsDict[mode__][2][0]):            
                        for tableInfo in regList[reg]._regFieldList: # there six tables' field stored in the field list
                            mem._regName = tableInfo[0]
                            mem._sheetName = mode
                            mem._regType = tableInfo[1]
                            mem._tableCount = tableInfo[2]
                            mem._regFieldList = tableInfo[3]
                            mem._table_struct_name = tableInfo[0]
                            #mem._modeName = tableInfo[0] # here may have bug, current not consider the ad2. not familiar with ad2.
                                                        
                            sameModeObjsDict[mode][2][0] += 1 # for TABLE POOL AD2              
                            sameModeObjsDict[mode][2][1] += [(copy.deepcopy(mem))] # for TABLE POOL AD2, added at the end.
                """

                # expand the register name in sheet l3_lpm_tcam_[1:15]. make it accordance with l3_lpm_tcam_0.
                if mode == "l3_defip":
                    for count in range(16):
                        if count == 0:
                            continue

                        mode_name_ = "l3_lpm_tcam_%d" % count
                        regList = sameModeObjsDict[mode_name_][1][1]
                        for reg in range(sameModeObjsDict[mode_name_][1][0]):
                            regList[reg]._regName = mode_name_ + "_" + regList[reg]._regName
                            regList[reg]._old_regName = regList[reg]._regName
                            regList[reg]._old_sheetName = mode_name_
                            # print " %s --- %s" % (mode_name_, regList[reg]._regName)

                # change the reg name.
                regList = sameModeObjsDict[mode][1][1]
                for reg in range(sameModeObjsDict[mode][1][0]):
                    if regList[reg]._sheetName in hash_tcam_data_list:
                        # regList[reg]._regName = regList[reg]._regName + "_DATA"
                        regList[reg]._regName = mode + "_" + regList[reg]._regName
                        regList[reg]._old_regName = regList[reg]._regName
                        regList[reg]._old_sheetName = mode  # _old_sheetName equal mode originally
                        # print "data--> %s" % regList[reg]._regName
                    if regList[reg]._sheetName in hash_tcam_key_list:
                        # regList[reg]._regName = regList[reg]._regName + "_KEY"
                        regList[reg]._regName = key_mode_name + "_" + regList[reg]._regName
                        regList[reg]._old_regName = regList[reg]._regName
                        regList[reg]._old_sheetName = mode  # change the sheetName from key_mode_name to data_mode_name
                        # print " key--> %s" % regList[reg]._regName

                regList = sameModeObjsDict[mode][2][1]
                for reg in range(sameModeObjsDict[mode][2][0]):
                    if regList[reg]._sheetName in hash_tcam_data_list:
                        # regList[reg]._regName = regList[reg]._regName + "_DATA"
                        regList[reg]._regName = mode
                        regList[reg]._sheetName = mode
                    if regList[reg]._sheetName in hash_tcam_key_list:
                        # regList[reg]._regName = regList[reg]._regName + "_KEY"
                        regList[reg]._regName = key_mode_name
                        regList[reg]._sheetName = mode  # change the sheetName from key_mode_name to data_mode_name

                    if reg > 1:  # only for table pool ad2
                        break

                break

    mode_list = sameModeObjsDict.keys()
    for mode_ in mode_list:
        if mode_ in hash_tcam_key_list:  # delete the key table, as it already be added to data table.
            # print "delete  %s " % mode_
            del sameModeObjsDict[mode_]

    return sameModeObjsDict


def delete_same_name_register_in_the_same_mode(sameModeObjsDict, type_):
    reg_list = []
    mem_list = []
    new_total_count = 0
    count = 0
    for mode in sameModeObjsDict:
        # if mode.upper() == "CB_CNT":
        #    print "Past: %s reg = %d mem = %d " %(mode, sameModeObjsDict[mode][1][0],sameModeObjsDict[mode][2][0])
        # for reg
        for reg in sameModeObjsDict[mode][1][1]:
            if find_reg_by_name(reg_list, reg._regName) == 1:
                continue
            reg._soc_type = "_" + type_
            reg_list.append(reg)
            count += 1

        sameModeObjsDict[mode][1][1] = reg_list
        sameModeObjsDict[mode][1][0] = count
        new_total_count += count
        reg_list = []
        count = 0

        # for mem
        for reg in sameModeObjsDict[mode][2][1]:
            if find_reg_by_name(mem_list, reg._regName) == 1:
                continue
            reg._soc_type = "_" + type_
            mem_list.append(reg)
            count += 1

        sameModeObjsDict[mode][2][1] = mem_list
        sameModeObjsDict[mode][2][0] = count
        new_total_count += count
        mem_list = []
        count = 0
        # if mode.upper() == "CB_CNT":
        #    print "Now : %s reg = %d mem = %d \n" %(mode, sameModeObjsDict[mode][1][0], sameModeObjsDict[mode][2][0])

    print "new count %d \n" % new_total_count

    return sameModeObjsDict


def find_same_reg_by_address(_list, name, base, offset):
    for reg in _list:
        # if reg._regName == name:
        if reg._regName == name and reg._regBaseAddr == base and reg._regOffsetAddr == offset:
            reg._soc_type = ""
            return 1

    return 0


def delete_same_register(sameModeObjsDict):
    reg_list = []
    mem_list = []
    new_total_count = 0
    count = 0
    for mode in sameModeObjsDict:
        # for reg
        for reg in sameModeObjsDict[mode][1][1]:
            if find_same_reg_by_address(reg_list, reg._regName, reg._regBaseAddr, reg._regOffsetAddr) == 1:
                continue

            reg_list.append(reg)
            count += 1

        sameModeObjsDict[mode][1][1] = reg_list
        sameModeObjsDict[mode][1][0] = count
        new_total_count += count
        reg_list = []
        count = 0

        # for mem
        for reg in sameModeObjsDict[mode][2][1]:
            if find_same_reg_by_address(mem_list, reg._regName, reg._regBaseAddr, reg._regOffsetAddr) == 1:
                continue

            mem_list.append(reg)
            count += 1

        sameModeObjsDict[mode][2][1] = mem_list
        sameModeObjsDict[mode][2][0] = count
        new_total_count += count
        mem_list = []
        count = 0

    # print "new count %d \n" % new_total_count

    return sameModeObjsDict


def whose_field_len_more_than_64(sameModeObjs):
    f = file("./tmp/fields_more_than_64", 'w')
    for mode in sameModeObjs:
        # if mode == "table_pool":
        #    continue

        for _reg in sameModeObjs[mode][1][1]:
            # print "\n%s  %s reg %-10s %-20s %-10s  %-5s\n" % (_reg._excelName, mode, _reg._csrName, _reg._regName, _reg._regBaseAddr, _reg._regOffsetAddr)
            # f.write("\n%s  %s reg %-10s %-20s %-10s  %-5s\n" % (_reg._excelName, mode, _reg._csrName, _reg._regName, _reg._regBaseAddr, _reg._regOffsetAddr))
            for fd in _reg._regFieldList:
                # f.write("    %-20s len = %-5s bp = %-5s \n" % (fd._fieldName, fd._fieldLen, fd._fieldBp))
                pass
        for _tab in sameModeObjs[mode][2][1]:
            # f.write("\n%s ------ %s \n" % (_tab._excelName, mode))
            for key_type_list in _tab._regFieldList:
                # print "key_type_list %s " % key_type_list
                # f.write("    keyType %-10s  width %d \n" % (key_type_list[0], key_type_list[2]))
                for fd in key_type_list[1]:
                    if fd._fieldLen > 64:
                        f.write("%-30s %-30s %-30s %-6s\n" % (_tab._excelName, mode, fd._fieldName, fd._fieldLen))
                    # f.write("      %-20s len = %-5s bp = %-5s \n" % (fd._fieldName, fd._fieldLen, fd._fieldBp))

    f.close()


def print_all_int_register(allObjList):
    print "print_all_int_register......"
    f = file("./tmp/int_registers", 'w')

    for mode in allObjList:
        for _reg in allObjList[mode][1][1]:
            reg_name = _reg._original_regName.upper()

            len_ = len(_reg._original_regName)

            if _reg._regType.upper() == "INTWC":  # or reg_name[len_-4:] == "_SET" or reg_name[len_-5:] == "_MASK" :
                f.write("\n%-20s %-40s %-10s %-10s\n" % (
                    mode, _reg._original_regName, _reg._regBaseAddr, _reg._regOffsetAddr))

                for fd in _reg._regFieldList:
                    if fd._fieldName.lower() == "reserved":
                        continue
                    f.write("    %-30s bp = %d len = %d \n" % (fd._fieldName, fd._fieldBp, fd._fieldLen))

    f.close()
    print "Finished print_all_int_register......"


def parse_all_reg(allObjList):
    # below code is tring to get the regs who have the same mode
    f = file("./tmp/allMode", 'w')
    checked = []
    sameModeObjs = {}

    for obj in allObjList:

        mode = obj._old_sheetName  # use old_sheetName, not sheet name which is expanded
        #print "mode = %s" % mode
        found = 0
        for ch_name in checked:
            if mode == ch_name:  # check if the mode have already be iterated
                found = 1
                break

        if found == 1:
            continue

        checked.append(mode)

        reg_count = 0
        tab_count = 0
        sameModeRegList = []
        sameModeTabList = []

        for obj2 in allObjList:
            if (obj2._old_sheetName == mode):  # use old_sheetName, not sheet name which is expanded
                if obj2.regType in ["TAB", "CAM", "TCAM", "HASH", "DIRECT", "UNKNOWEN", "TABLEPOOL"]:
                    tab_count += 1
                    obj2._regName = obj2._regName.replace("__", "_")
                    sameModeTabList.append(obj2)
                else:
                    reg_count += 1
                    obj2._regName = obj2._regName.replace("__", "_")
                    sameModeRegList.append(obj2)

        sameModeObjs[mode] = [mode, [reg_count, sameModeRegList], [tab_count, sameModeTabList]]

        # print "Mode: %-25s reg = %d    table = %d \n" % (mode, sameModeObjs[mode][1][0],sameModeObjs[mode][2][0])
        f.write("Mode: %-25s reg = %d    table = %d \n" % (mode, sameModeObjs[mode][1][0], sameModeObjs[mode][2][0]))

    total = 0
    # print all regs/tables in each mode
    for mode in sameModeObjs:
        if mode == "table_pool":
            continue
        print mode
        total += (sameModeObjs[mode][1][0] + sameModeObjs[mode][2][0])
        for _reg in sameModeObjs[mode][1][1]:
            # print "\n%s  %s reg %-10s %-20s %-10s  %-5s\n" % (_reg._excelName, mode, _reg._csrName, _reg._regName, _reg._regBaseAddr, _reg._regOffsetAddr)
            f.write("\n%s  %s reg %-10s %-20s %-10s  %-5s\n" % (
                _reg._excelName, mode, _reg._csrName, _reg._regName, _reg._regBaseAddr, _reg._regOffsetAddr))
            for fd in _reg._regFieldList:
                f.write("    %-20s len = %-5s bp = %-5s \n" % (fd._fieldName, fd._fieldLen, fd._fieldBp))

        for _tab in sameModeObjs[mode][2][1]:
            f.write("\n%s  %s table %-10s %-20s %-10s  %-5s\n" % (
                _tab._excelName, mode, _tab._csrName, _tab._regName, _tab._regBaseAddr, _tab._regOffsetAddr))
            for key_type_list in _tab._regFieldList:
                # print "key_type_list %s " % key_type_list
                f.write("    keyType %-10s  width %d \n" % (key_type_list[0], key_type_list[2]))
                for fd in key_type_list[1]:
                    f.write("      %-20s len = %-5s bp = %-5s \n" % (fd._fieldName, fd._fieldLen, fd._fieldBp))

    print total

    f.close()

    return sameModeObjs


def get_obj_list(dir_name):
    objList = []

    list = os.listdir(dir_name)

    for item in list:
        item = dir_name + item
        # print "item %s" % item
        if os.path.isfile(item) and (item[-5:] == '.xlsx' or item[-5:] == '.xlsm'):
            if item.find("$") != -1 or item.find("csr_example") != -1:

                continue

            csrConfig = CCsrConfig(item)
            print 'list name:', item
            csrConfig.OpenExcel()
            # csrConfig.enable_for_sdk()  # this is to open the switch,  then the different MACRO will not be enlarged to different mode.
            tmp = csrConfig.ReadCSRCfg()
            #print "tmp%d" % len(tmp)
            csrConfig.checkMacro()  # added to check the macro
            objList += tmp
            # print "File %s has %d regs\n " % (item, len(tmp))

        elif os.path.isdir(item):
            item = item + '/'
            new_obj_list = []
            new_obj_list = get_obj_list(item)

            for each in new_obj_list:
                objList.append(each)

    return objList


def initialize_table_fields(dir_name):
    list = os.listdir(dir_name)
    for item in list:
        item = dir_name + item
        if os.path.isfile(item) and (item[-5:] == '.xlsx' or item[-5:] == '.xlsm'):
            if item.find("$") != -1:
                # print item
                continue

            print item
            csrConfig = CCsrConfig(item)
            csrConfig.OpenExcel()
            tmp = csrConfig.initialize_the_table_fields()

        elif os.path.isdir(item):
            item = item + '/'
            get_obj_list(item)


def parse_the_reg_type(sameModeObjsDict):
    reg_list = []
    reg_type_dict = {}

    f = file("./tmp/allregType", 'w')
    for mode in sameModeObjsDict:
        # for reg
        for reg in sameModeObjsDict[mode][1][1]:
            # f.write("%-30s :  %-30s  %-10s\n" % (reg._excelName, reg._sheetName, reg._regType))
            type_ = reg._regType
            if type_ in reg_type_dict:
                reg_type_dict[type_].append(reg)
            else:
                reg_type_dict[type_] = []
                reg_type_dict[type_].append(reg)

    for type_ in reg_type_dict:
        # print "type is %s " % type_
        for reg in reg_type_dict[type_]:
            f.write("%-30s :  %-30s  %-30s  %-10s\n" % (reg._excelName, reg._sheetName, reg._regName, reg._regType))

    f.close()


def add_the_two_dict(dict1, dict2):
    dict_ = dict1

    for mode in dict2:
        if mode in dict_:
            dict_[mode][1][0] = dict_[mode][1][0] + dict2[mode][1][0]
            dict_[mode][1][1] = dict_[mode][1][1] + dict2[mode][1][1]
            dict_[mode][2][0] = dict_[mode][2][0] + dict2[mode][2][0]
            dict_[mode][2][1] = dict_[mode][2][1] + dict2[mode][2][1]
        else:
            dict_[mode] = dict2[mode]

    return dict_


def for_soc_sdk(soc):
    f = file("./tmp/macro_not_define", "w")
    f.close()

    csrConfig = CCsrConfig("NULL")  # only use to show the field info
    csrConfig.parse_table_fields()  # only use to show the field info

    Gen = Soc_for_sdk_Generator()

    ######## for physical_table.xlsx file #########
    csrConfig = CCsrConfig("../reg_tab/physical_table.xlsx")
    csrConfig.OpenExcel()

    have_tab_struct_objList = []
    no_tab_struct_objList = []
    [have_tab_struct_objList, no_tab_struct_objList] = csrConfig.parse_physical_table_excel_file()
    Gen.set_physical_table_obj(no_tab_struct_objList)
    ######## for physical_table.xlsx file end #########

    ##################### register operation ###############
    allRegObjList = []
    regSameModeObjsDict = {}

    print "Parse register folder...................."

    allRegObjList = get_obj_list("../reg_tab/csr_excel/counter/")
    allRegObjList += get_obj_list("../reg_tab/csr_excel/register/asic/")

    print "Reg Obj in total %d\n" % len(allRegObjList)

    regSameModeObjsDict = parse_all_reg(
        allRegObjList)  # the dictionary have the mode as the key, the registers and tables under the mode as the content
    regSameModeObjsDict = delete_same_name_register_in_the_same_mode(regSameModeObjsDict,
                                                                     soc)  # We need delete the register which have the same name in one mode.

    Gen.GenerateRegisterXMLFile(regSameModeObjsDict, soc)  # register.xml

    print_all_int_register(regSameModeObjsDict)  # no useful

    ##################### table operation ###############
    allMemObjList = []
    memSameModeObjsDict = {}
    print "Parse table folder...................."
    allMemObjList = get_obj_list("../reg_tab/csr_excel/table_csr_excel/")
    print "Mem Obj in total %d\n" % len(allMemObjList)

    memSameModeObjsDict = parse_all_reg(allMemObjList)

    memSameModeObjsDict = delete_same_name_register_in_the_same_mode(memSameModeObjsDict, soc)

    memSameModeObjsDict = reconstruct_hash_tcam_table(
        memSameModeObjsDict)  # delete the key table, and add it to data table.
    #memSameModeObjsDict = reconstruct_table_for_table_pool(memSameModeObjsDict)  # for table pool.

    # mixed the tables from the physical_table.xlsx
    memSameModeObjsDict["physical_table"] = ["physical_table", [0, []],
                                             [len(have_tab_struct_objList), have_tab_struct_objList]]

    Gen.GenerateTableXMLFile(memSameModeObjsDict, soc)  # table.xml

    ################### common operation ###################
    totalSameModeObjsDict = {}
    totalSameModeObjsDict = dict(regSameModeObjsDict.items() + memSameModeObjsDict.items())

    Gen.show_the_same_name_register_in_different_mode(totalSameModeObjsDict,
                                                      soc)  #######  used to get the same name register in different mode.
    Gen.show_the_same_name_table_in_different_mode(totalSameModeObjsDict,
                                                   soc)  #######  used to get the same name table in different mode.

    # Gen.GenerateSocXMLFile(totalSameModeObjsDict, soc) # currently, we do not considerate the multi-soc

    ################# below is new structure for SDK ########################################

    Gen.get_all_filed_in_regs_and_tables(totalSameModeObjsDict,
                                         soc)  # get all filed name, unique, discard the same name field.

    (new_reg_list, new_tab_list,
     unique_name_objs_in_mode) = Gen.reconstruct_the_reg_table_and_create_unique_name_for_same_mode(
        totalSameModeObjsDict, soc)

    Gen.GenerateRegMemXMLFile(totalSameModeObjsDict)     # commands' define
    Gen.GenerateRegMemInterfaces(totalSameModeObjsDict)  # reg_mem_interface.c

    Gen.GenerateCli_Mode_Mode_H(totalSameModeObjsDict, memSameModeObjsDict, soc)  # cli_mode.h

    Gen.GenerateAllRegTableStruct(totalSameModeObjsDict, soc)  ###### generate the table struct define file
    Gen.GenerateAllAPI(totalSameModeObjsDict, soc)             ###### generate the APIs

    Gen.GenerateAllRegAndTableSymbol(totalSameModeObjsDict, soc)  # allsymbol.h

    Gen.GenerateAllRegFile(new_reg_list, soc)  # allreg.h
    Gen.GenerateAllMemFile(new_tab_list, soc)  # allmem.h
    Gen.GenerateAllFieldFile(new_reg_list, new_tab_list, soc)  # allfield.h

    print '####################################################'


def init_table_fields():
    print "Begining initialize_table_fields ****************\n"
    initialize_table_fields('../reg_tab/Tables/')
    print "Finished initialize_table_fields ****************\n"


def start():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"]);

        # check all param
        for opt, arg in opts:
            print (opt)
            print (arg)
            if opt in ("-h", "--help"):
                usage()
                # sys.exit(1)
            else:
                print("%s  ==> %s" % (opt, arg))

    except getopt.GetoptError:
        print("getopt error!")
        usage()
        sys.exit(1)

    Gen = Generator()

    init_table_fields()
    #print "2"
    for_soc_sdk("sf9564")

    print '####################################################'
