# -*- coding: utf-8 -*-

__author__ = 'LI JUN'


import getopt
from csr_parse import *
import copy

#from parse_main import *



import sys

table_pool_dict = {"L2_ENTRY_T":"HASH", "L3_ENTRY_IPV4_UNICAST_T":"HASH", "L3_ENTRY_IPV6_UNICAST_T":"HASH", "L3_ENTRY_IPV4_MULTICAST_T":"HASH", "L3_ENTRY_IPV6_MULTICAST_T":"HASH",
                   "L3_DEFIP_ALPM_IPV4_T":"DIRECT", "L3_DEFIP_ALPM_IPV4_1_T":"DIRECT", "L3_DEFIP_ALPM_IPV6_64_T":"DIRECT", "L3_DEFIP_ALPM_IPV6_64_1_T":"DIRECT", "L3_DEFIP_ALPM_IPV6_128_T":"DIRECT",
                   "L3_DEFIP_ALPM_IPV6_128_1_T":"DIRECT"}


tcam_data_list = [ "p0_st_my_station_data", "p1_st_my_station_data" , "p0_pt_l3_tunnel_data_only", "p1_pt_l3_tunnel_data_only", "p0_pt_l2_user_entry_data_only", "p1_pt_l2_user_entry_data_only", "p0_pt_udf_offset", "p1_pt_udf_offset", "st_l3_defip" ]      
tcam_key_list =  [ "my_station_tcam",       "my_station_tcam"       , "l3_tunnel_tcam",             "l3_tunnel_tcam",           "l2_user_entry_tcam",             "l2_user_entry_tcam",            "pa_tcam",         "pa_tcam",          "l3_lpm_tcam_0"]
tcam_dict = { "p0_st_my_station_data":"TCAM", "p1_st_my_station_data":"TCAM" , "p0_pt_l3_tunnel_data_only":"TCAM", "p1_pt_l3_tunnel_data_only":"TCAM", "p0_pt_l2_user_entry_data_only":"TCAM", "p1_pt_l2_user_entry_data_only":"TCAM", "p0_pt_udf_offset":"TCAM", "p1_pt_udf_offset":"TCAM", "st_l3_defip" : "TCAM"} 

hash_data_list = ["st_egr_vlan_xlate_data",  "st_vlan_xlate_data",   "st_mpls_entry_data", "st_trill_rfp_check_entry_data", "st_trill_forward_tree_data" ]
hash_key_list =  ["sst_egr_vlan_xlate",      "sst_vlan_xlate",       "sst_mpls_entry",     "sst_trill_rfp_check", "sst_trill_forward_tree" ]      
hash_dict = {"st_egr_vlan_xlate_data":"HASH",  "st_vlan_xlate_data":"HASH", "st_mpls_entry_data":"HASH", "st_trill_rfp_check_entry_data":"HASH", "st_trill_forward_tree_data":"HASH"}        



hash_tcam_data_list = hash_data_list + tcam_data_list
hash_tcam_key_list =  hash_key_list + tcam_key_list
hash_tcam_dict =dict(hash_dict.items() + tcam_dict.items())


key_type_field_info_dict = {"EGR_DVP_ATTRIBUTE_T":[46, 2],
                            "L3_DEFIP_T":[2, 2],                            
                            "L3_TUNNEL_DATA_ONLY_T":[0, 1], # need check, bug 
                            "EGR_L3_NEXT_HOP_T":[0, 3],
                            "ING_L3_NEXT_HOP_T":[0, 2],
                            "EGR_IP_TUNNEL_T":[0, 2],
                            "L3_TUNNEL_T":[1, 1],
                            "L3_TUNNEL_ONLY_T":[1, 1],
                            "L2_ENTRY_T":[1, 3],
                            "VLAN_MAC_T":[1, 4],
                            "POLICY":[0, 1], # need check, bug
                            "L2_USER_ENTRY_ONLY_T":[61, 1],
                            "L2_USER_ENTRY_DATA_ONLY_T":[61, 1],                            
                            "L3_DEFIP_ONLY_T":[2, 2],
                            "L3_DEFIP_DATA_ONLY_t":[2, 2],                            
                            "TRILL_FORWARD_TREE_T":[1, 1],
                            "TRILL_FORWARD_TREE_DATA_t":[1, 1],                            
                            "MPLS_ENTRY_T":[1, 3],
                            "MPLS_ENTRY_DATA_T":[1, 3],
                            "EGR_VLAN_XLATE_T":[1, 3],
                            "EGR_VLAN_XLATE_DATA_T":[1, 3],
                            "VLAN_XLATE_T":[1, 4],
                            "VLAN_XLATE_DATA_ONLY_T":[1, 4]
                            }


class Generator():
    """Automaticly generate files, include header files and C files, also XML file."""


    def get_table_pool_table_type(self, mode):
        if mode in table_pool_dict:
            return table_pool_dict[mode]
        


    def get_table_type(self, mode):
        if mode in hash_tcam_dict:
            return hash_tcam_dict[mode]
        else:
            return "DIRECT"


    
    def GenerateSymbolFile(self, regList):
        print "Generate the allsymbol.h File."
        f = file('allsymbol.h', 'w')
        f.write("\n//THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!\n\n")

    
        for mode in objDict:            
            if objDict[mode][1][0] > 0:               
                str = "hash_entry_t reg_%s_hash_head[%d];\n" % (mode, (objDict[mode][1][0]/3+1)) # Hope each hash entry store 3 items, just hope

                    
                f.write(str)

            if objDict[mode][2][0] > 0:
                str += "hash_entry_t mem_%s_hash_head[%d];\n" % (mode, (objDict[mode][2][0]/3+1)) # Hope each hash entry store 3 items, just hope
                
            f.write(str)


        f.close()



        f.write("};\n")
        f.close()




    def insert_mem_to_hash_head(self, _file, mode, keyDict):
        #print "insert mems to %s \n" % _hash_head        
        
        for key in keyDict:
            if len(keyDict[key]) == 0:
                continue
            
            hash_head = "mem_%s_hash_head[%d]" % (mode, key)

            # define the hash_entry_t to store the reg

            for reg in range(len(keyDict[key])):
                item = "static hash_entry_t mem_%s_hash_head_%d_%d;\n" % (mode, key, reg)
                _file.write(item)

            #initialize hash list head
            str = """
%s.mem = NULL;
%s.reg = NULL;
%s.next = &mem_%s_hash_head_%d_%d;\n""" % (hash_head, hash_head, hash_head, mode, key, 0)
            _file.write(str)

            
            for reg in range(len(keyDict[key])):
                item = "mem_%s_hash_head_%d_%d" % (mode, key, reg)


                table_type = self.get_table_type(mode)
                if table_type in ["HASH", "TCAM"]:
                    prefix_ = "hash_tcam_"
                else :
                    prefix_ = ""


                    
                if reg == len(keyDict[key]) - 1:

                    # store the last one            
                    str = """
%s.mem = (void *)&%s%s_%sm;
%s.reg = NULL;
%s.next = NULL;\n""" % (item, prefix_, mode.upper(), keyDict[key][reg]._regName.upper(), item, item)
                    _file.write(str)
                    break
                
                # store the reg in the entry
                str = """
%s.mem = (void *)&%s%s_%sm;
%s.reg = NULL;
%s.next = &mem_%s_hash_head_%d_%d;\n""" % (item, prefix_, mode.upper(), keyDict[key][reg]._regName.upper(), item, item, mode, key, reg+1)
                _file.write(str)




    def insert_reg_to_hash_head(self, _file, mode, keyDict):
        #print "insert regs to %s \n" % _hash_head
        
        for key in keyDict:
            if len(keyDict[key]) == 0:
                continue
            
            hash_head = "reg_%s_hash_head[%d]" % (mode, key)

            
            # define the hash_entry_t to store the reg
            for reg in range(len(keyDict[key])):                
                item = "static hash_entry_t reg_%s_hash_head_%d_%d;\n" % (mode, key, reg)
                _file.write(item)

            #initialize hash list head
            str = """
%s.mem = NULL;
%s.reg = NULL;
%s.next = &reg_%s_hash_head_%d_%d;\n""" % (hash_head, hash_head, hash_head, mode, key, 0)
            _file.write(str)

            
            for reg in range(len(keyDict[key])):
                item = "reg_%s_hash_head_%d_%d" % (mode, key, reg)

                if reg == len(keyDict[key]) - 1:

                    # store the last one            
                    str = """
%s.mem = NULL;
%s.reg = &%s_%sr;
%s.next = NULL;\n""" % (item, item, mode.upper(), keyDict[key][reg]._regName.upper(), item)
                    _file.write(str)
                    break
                
                # store the reg in the entry
                str = """
%s.mem = NULL;
%s.reg = &%s_%sr;
%s.next = &reg_%s_hash_head_%d_%d;\n""" % (item, item, mode.upper(), keyDict[key][reg]._regName.upper(), item, mode, key, reg+1)
                _file.write(str)


            
       
    def hashfunc(self, reg_name, max_entry):
        str = reg_name.upper()
        str.replace("_", "")
        
            
        
        h = 0
        for ch in range(len(str)):


            c = ord(str[ch])
            h = (h << 3) ^ h ^ (h >> 7) ^c
            h = h %0x0fffffff
            
            #if str == "NGN_EN_CFG" :
            #    print str[ch]
            #    print ord(str[ch])
            #    print "h is %d" % h
            
        #if str == "NGN_EN_CFG" :
        #    print "key is %d  max is %d  h = %d \n" % ( h % max_entry, max_entry, h)
            
        return h % max_entry




    def GenerateAllModeHeaderCFile(self, objDict):
        print "Generate the allmode.h File."
        
        f = file('allmode.h', 'w')
        f.write("\n//THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!\n\n")
        f.write("void hash_head_init();\n")
        f.write("void mode_init();\n")
        f.close()



        print "Generate the allmode.c File."
        
        f = file('allmode.c', 'w')
        f.write("\n//THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!\n\n")
        f.write("#include <stdio.h>\n")
        f.write("#include \"common.h\"\n")
        f.write("#include \"allmode.h\"\n")
        f.write("#include \"cli_view.h\"\n")
        f.write("#include \"allfield.h\"\n")
        f.write("#include \"allreg.h\"\n")
        f.write("#include \"allmem.h\"\n")
        f.write("#include \"table_depth.h\"\n")
        

        f.write("\nextern void clean_mem(unsigned int base, unsigned int offset, int bits, int depth, char *name, char *sheetName, char *table_type);\n")
        
        f.write("\nmode_info_t mode_list[MAX_MODE];\n\n") # define the mode_list


        str = ""
        # define the hash head for registers and mems
        for mode in objDict:            
            if objDict[mode][1][0] > 0:               
                str = "static hash_entry_t reg_%s_hash_head[%d];\n" % (mode, (objDict[mode][1][0]/3+1)) # Hope each hash entry store 3 items, just hope
                
            if objDict[mode][2][0] > 0:
                str += "static hash_entry_t mem_%s_hash_head[%d];\n" % (mode, (objDict[mode][2][0]/3+1)) # Hope each hash entry store 3 items, just hope
                
            f.write(str)
            

        f.write("\n\nvoid hash_head_init()\n{\n")

        # initialize the hash head and insert the register to the hash head 
        regList = []                        
        for mode in objDict:            
            # for reg
            if objDict[mode][1][0] > 0:                
                regList = objDict[mode][1][1]
                keyDict = {} # store the regs which have the same key value
                for i in range(objDict[mode][1][0]/3+1):
                    keyDict[i] = [] # must be initialized                                
                for reg in regList:
                    key = self.hashfunc(reg._regName, (objDict[mode][1][0]/3+1))# calculate the hash key
                    keyDict[key].append(reg)
                    
                str = self.insert_reg_to_hash_head(f, mode, keyDict) # insert the reg into the hash entry
                
                    
            # for mems
            if objDict[mode][2][0] > 0:                
                regList = objDict[mode][2][1]
                keyDict = {} # store the mems which have the same key value
                for i in range(objDict[mode][2][0]/3+1):
                    keyDict[i] = [] # must be initialized
                for reg in regList:                    
                    nKeyType = len(reg._regFieldList)  # reg._regFieldList contain the list of [keyType, fieldList, tableWidth]
                    if nKeyType == 1:
                        key = self.hashfunc(reg._regName,(objDict[mode][2][0]/3+1))# calculate the hash key
                        keyDict[key].append(reg)
                    else :
                        for info in reg._regFieldList:                           
                            tmp_reg = CRegister("", "", "", reg._regName + "_" + info[0], "", "", "", "", "", 0, "0")  # tempory use the name of the register
                            key = self.hashfunc(reg._regName,(objDict[mode][2][0]/3+1))# calculate the hash key
                            keyDict[key].append(tmp_reg)

                    table_type = self.get_table_type(mode)
                    if table_type in ["HASH", "TCAM"]: # only added data table to the hash head. because we have mixed the data and the key table
                        break
                    
                str = self.insert_mem_to_hash_head(f, mode, keyDict) # insert the mem into the hash entry
                
        f.write("\n}\n\n")   



        # initialize the mode hash table
        f.write("void mode_init()\n{")

        for mode in objDict:
            if objDict[mode][1][0] > 0 and objDict[mode][2][0] > 0 :
                mode_id = "%s_MODE" % mode.upper()
                reg_hash_head = "&reg_%s_hash_head[0]" % mode
                mem_hash_head = "&mem_%s_hash_head[0]" % mode
                nKey_r = objDict[mode][1][0]/3+1
                nKey_m = objDict[mode][2][0]/3+1
                
            else:
                if objDict[mode][1][0] > 0 and objDict[mode][2][0] == 0 :
                    mode_id = "%s_MODE" % mode.upper()
                    reg_hash_head = "&reg_%s_hash_head[0]" % mode
                    mem_hash_head = "NULL"
                    nKey_r = objDict[mode][1][0]/3+1
                    nKey_m = 0

                else:
                    if objDict[mode][1][0] == 0 and objDict[mode][2][0] > 0 :
                        mode_id = "%s_MODE" % mode.upper()
                        reg_hash_head = "NULL"
                        mem_hash_head = "&mem_%s_hash_head[0]" % mode
                        nKey_r = 0
                        nKey_m = objDict[mode][2][0]/3+1
            
            str = """
    mode_list[%s_MODE].name = \"%s\";
    mode_list[%s_MODE].nKey_r = %d;
    mode_list[%s_MODE].nKey_m = %d;
    mode_list[%s_MODE].mode_id = %s;
    mode_list[%s_MODE].rHead = %s;
    mode_list[%s_MODE].mHead = %s;
"""% (mode.upper(), mode.lower(), mode.upper(), nKey_r, mode.upper(), nKey_m, mode.upper(), mode_id, mode.upper(), reg_hash_head, mode.upper(), mem_hash_head)
            
            f.write(str)
        
        f.write("\n}")




        # initialize all the table
        f.write("\n\nint all_table_init(int module_id, int argc, char *args[])\n{\n")

        for mode in objDict:            
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]
                for reg in range(len(regList)):                    
                    table_type = self.get_table_type(mode)                    
                    if table_type in ["HASH", "TCAM"]:
                        continue                

                    if mode in table_pool_dict: # if the table is in table pool, we only need clean one of them. here is L2_ENTRY_T
                        if mode != "L2_ENTRY_T" :
                            continue                        
                    
                    str = '''   clean_mem(%3d, %3d, %4d, %s, \"%s\", \"%s\", \"%s\");\n'''  % (regList[reg]._regBaseAddr, regList[reg]._regOffsetAddr, regList[reg]._nBits, regList[reg]._table_struct_name.upper(), regList[reg]._regName, regList[reg]._sheetName, regList[reg]._regType)
                    f.write(str)
                    #print str
                    
                            
        for mode in objDict:            
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]
                for reg in range(len(regList)):
                    table_type = self.get_table_type(mode)                    
                    if table_type in ["HASH", "TCAM"]:
                        str  = '''  clean_mem(%3d, %3d, %4d, %s, \"%s\", \"%s\", \"%s\");\n'''  % (regList[reg]._regBaseAddr, regList[reg]._regOffsetAddr, regList[reg]._nBits, regList[reg]._table_struct_name.upper(), regList[reg]._regName, regList[reg]._sheetName, regList[reg]._regType)
                        str += '''  clean_mem(%3d, %3d, %4d, %s, \"%s\", \"%s\", \"%s\");\n'''  % (regList[1]._regBaseAddr,   regList[1]._regOffsetAddr,   regList[1]._nBits,   regList[1]._table_struct_name.upper(),   regList[1]._regName, regList[1]._sheetName, regList[1]._regType)
                        f.write(str)
                        #print str
                        
                    if table_type in ["HASH", "TCAM"]:
                        break

        f.write("    return 0;\n}")
        f.close()



    def GenerateAllRegFile(self, objDict):
        print "Generate the allreg.h File."
        f = file('allreg.h', 'w')
        f.write("\n//THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!\n\n")

        regList = []
        # import extern variable field
        for mode in objDict:            
            if objDict[mode][1][0] > 0:
                regList = objDict[mode][1][1]
                for reg in range(len(regList)):
                    f.write("extern field_info_t %s_%sf[];\n" %(mode.lower(), (regList[reg]._regName).lower()))

                
        for mode in objDict:            
            if objDict[mode][1][0] > 0:
                regList = objDict[mode][1][1]
                #f.write("\nreg_info_t %s_reg_list[] = \n {" % mode.lower())
                for reg in regList:
                    str = "reg_info_t %s_%sr  = {\"%s\",\"%s\", %s, 0x%x, %d, %s_%sf};\n" % (mode.upper(), reg._regName.upper(), reg._regName, reg._regType, reg._regBaseAddr, reg._regOffsetAddr, len(reg._regFieldList), mode.lower(), (reg._regName).lower())
                    f.write(str)

                #f.write("};\n")
        f.close()

        

    def GenerateAllMemFile(self, objDict):
        print "Generate the allmem.h File."
        f = file('allmem.h', 'w')
        f.write("\n//THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!\n\n")

        f.write("\n#include \"table_depth.h\" \n\n")


        # below if is to store the info of key type for a table which have different keytypes
        for struct_name in key_type_field_info_dict:            
            f.write("extern field_info_t %s_keytype_f;\n" %((struct_name).lower()))  

        regList = []
        # import extern variable field
        for mode in objDict:            
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]                
                for reg in range(len(regList)):
                    
                    nKeyType = len(regList[reg]._regFieldList)
                    if nKeyType == 1:
                        f.write("extern field_info_t %s_%sf[];\n" %(mode.lower(), (regList[reg]._regName).lower()))
                    else :
                        for info in regList[reg]._regFieldList:
                            key = info[0]
                            f.write("extern field_info_t %s_%s_%sf[];\n" %(mode.lower(), (regList[reg]._regName).lower(), key))

                
        for mode in objDict:            
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]

                #if mode == "CB_CNT":
                #    for _reg in  regList :
                #        print "%s  %s  %s  %s " % (_reg._excelName, _reg._sheetName, _reg._regName, _reg._regFieldList)

                for reg in range(len(regList)):
                        
                    nKeyType = len(regList[reg]._regFieldList)
                    if nKeyType == 1:
                        
                        key = "255"
                        if regList[reg]._regFieldList[0][0] != "NULL":
                            key = copy.deepcopy(regList[reg]._regFieldList[0][0])
                        
                        str = "mem_info_t %s_%sm  = { \"%s\", \"%s\", %s, 0x%x, %d, %d, %s, %s_%sf, %s, NULL};\n" % (mode.upper(), regList[reg]._regName.upper(), regList[reg]._regName, regList[reg].regType, regList[reg]._regBaseAddr, regList[reg]._regOffsetAddr,   regList[reg]._regFieldList[0][2], len(regList[reg]._regFieldList[0][1]), key, mode.lower(), (regList[reg]._regName).lower(), regList[reg]._table_struct_name.upper())

                        f.write(str)
                    else :
                        for info in regList[reg]._regFieldList:
                            key = info[0]                            
                            str = "mem_info_t %s_%s_%sm  = { \"%s\", \"%s\", %s, 0x%x, %d, %d, %s,  %s_%s_%sf, %s, &%s_keytype_f};\n" % (mode.upper(), regList[reg]._regName.upper(), key, regList[reg]._regName, regList[reg].regType, regList[reg]._regBaseAddr, regList[reg]._regOffsetAddr, info[2], len(info[1]), key, mode.lower(), (regList[reg]._regName).lower(), key, regList[reg]._table_struct_name.upper(), (regList[reg]._table_struct_name).lower())
                            f.write(str)


                    
                            
        for mode in objDict:            
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]

                for reg in range(len(regList)):

                    table_type = self.get_table_type(mode)
                    if table_type in ["HASH", "TCAM"]:                                                

                        max_width_data = regList[0]._regFieldList[0][3]
                        max_width_key  = regList[1]._regFieldList[0][3]                            
                        
                        nKeyType = len(regList[reg]._regFieldList)
                        if nKeyType == 1:                            
                            str = "hash_tcam_mem_info_t  hash_tcam_%s_%sm = {%d, %d, &%s_%sm, &%s_%sm};\n" % (mode.upper(), regList[reg]._regName.upper(), max_width_data, max_width_key, mode.upper(), regList[reg]._regName.upper(), mode.upper(), regList[1]._regName.upper())

                            f.write(str)
                        else :
                            for info in regList[reg]._regFieldList:
                                key = info[0]                                
                                str = "hash_tcam_mem_info_t hash_tcam_%s_%s_%sm  = {%d, %d, &%s_%s_%sm,  &%s_%s_%sm};\n" % (mode.upper(), regList[reg]._regName.upper(), key, max_width_data, max_width_key, mode.upper(), regList[reg]._regName.upper(), key, mode.upper(), regList[1]._regName.upper(), key)
                                f.write(str)
                    if table_type in ["HASH", "TCAM"]:
                        break

                
        f.close()



    def GenerateAllFieldFile(self, objDict):
        print "Generate the allfield.h File."
        f = file('allfield.h', 'w')
        f.write("\n//THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!\n\n")

        regList = []
        
        for mode in objDict:            
            if objDict[mode][1][0] > 0:
                regList = objDict[mode][1][1]
                for reg in range(len(regList)):
                    f.write("field_info_t %s_%sf[] = \n{\n" %(mode.lower(), regList[reg]._regName.lower()))
        
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        str = "    {\"%s\", %d, %d, %dULL},\n" % (field._fieldName, field._fieldLen, field._fieldBp, field._default)
                        if fd + 1 == len(regList[reg]._regFieldList):
                            str = "    {\"%s\", %d, %d, %dULL}\n" % (field._fieldName, field._fieldLen, field._fieldBp, field._default)
                        f.write(str)
        
                    f.write("};\n\n")


        # below is to store the info of key type for a table which have different keytypes
        for struct_name in key_type_field_info_dict:            
            bp   = key_type_field_info_dict[struct_name][0]
            len_ = key_type_field_info_dict[struct_name][1]
            
            f.write("field_info_t %s_keytype_f = {\"key_type\", %d, %d, 0};\n" %(struct_name.lower(), len_, bp))            
                
        for mode in objDict:            
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]
                for reg in range(len(regList)): # regList only have one table. (but the table maybe divided to key or data table.)
                    
                    fieldInfoList = regList[reg]._regFieldList
                    nKeyType = len(fieldInfoList)
                    
                    if nKeyType > 1:
                        continue                  

                        fieldList = regList[reg]._regFieldList[0][1]
                        
                        f.write("field_info_t %s_%sf[] = \n{\n" %(mode.lower(), regList[reg]._regName.lower()))
                        
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            str = "    {\"%s\", %d, %d},\n" % (field._fieldName, field._fieldLen, field._fieldBp)
                            if fd + 1 == len(fieldList):
                                str = "    {\"%s\", %d, %d}\n" % (field._fieldName, field._fieldLen, field._fieldBp)
                            f.write(str)
                        f.write("};\n\n")

                        
                    else:                                                

                        fieldList = regList[reg]._regFieldList[0][1]
                    
                        f.write("field_info_t %s_%sf[] = \n{\n" %(mode.lower(), regList[reg]._regName.lower()))
                    
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            str = "    {\"%s\", %d, %d},\n" % (field._fieldName, field._fieldLen, field._fieldBp)
                            if fd + 1 == len(fieldList):
                                str = "    {\"%s\", %d, %d}\n" % (field._fieldName, field._fieldLen, field._fieldBp)
                            f.write(str)
                        f.write("};\n\n")


        # deal with the table with different key type
        for mode in objDict:            
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]
                for reg in range(len(regList)):
                    
                    fieldInfoList = regList[reg]._regFieldList
                    nKeyType = len(fieldInfoList)
                    
                    if nKeyType == 1:
                        continue                  

                        for info in fieldInfoList :
                            key = info[0]
                            fieldList = info[1]

                            f.write("field_info_t %s_%s_%sf[] = \n{\n" %(mode.lower(), regList[reg]._regName.lower(), key))
                    
                            for fd in range(len(fieldList)):
                                field = fieldList[fd]
                                str = "    {\"%s\", %d, %d},\n" % (field._fieldName, field._fieldLen, field._fieldBp)
                                if fd + 1 == len(fieldList):
                                    str = "    {\"%s\", %d, %d}\n" % (field._fieldName, field._fieldLen, field._fieldBp)
                                f.write(str)
                            f.write("};\n\n")


                    else:
                        for info in fieldInfoList :
                            key = info[0]
                            fieldList = info[1]                    
                    
                    
                            f.write("field_info_t %s_%s_%sf[] = \n{\n" %(mode.lower(), regList[reg]._regName.lower(), key))
                    
                            for fd in range(len(fieldList)):
                                field = fieldList[fd]
                                str = "    {\"%s\", %d, %d},\n" % (field._fieldName, field._fieldLen, field._fieldBp)
                                if fd + 1 == len(fieldList):
                                    str = "    {\"%s\", %d, %d}\n" % (field._fieldName, field._fieldLen, field._fieldBp)
                                f.write(str)
                            f.write("};\n\n")

    
        f.close()



    def GenerateCli_Mode_Mode_H(self, allObjDict, memObjDict):
        print "Generate the cli_mode.h File."
        f = file("cli_mode.h", 'w')
        f.write("\n//THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!\n\n")
        #f.write("extern struct cli_tree *ctree;\n")
        
        str = """\n
int cli_register_mode(int module_id, int argc, char *args[])
{
	ctree->mode = REGISTER_MODE;
	setPrompt("GalaxyWind(config/register)#");
	printf("func: cli_register_mode excuted!\\n");
	return 0;
}

int cli_register_exit(int module_id, int argc, char *args[])
{
	ctree->mode = CONFIG_MODE;
	setPrompt("GalaxyWind(config)#");
	printf("func: cli_register_exit excuted!\\n");
	return 0;
}

int cli_table_mode(int module_id, int argc, char *args[])
{
	ctree->mode = TABLE_MODE;
	setPrompt("GalaxyWind(config/table)#");
	printf("func: cli_table_mode excuted!\\n");
	return 0;
}

int cli_table_exit(int module_id, int argc, char *args[])
{
	ctree->mode = CONFIG_MODE;
	setPrompt("GalaxyWind(config)#");
	printf("func: cli_table_exit excuted!\\n");
	return 0;
}\n\n"""
        f.write(str)

        
        
        # add the function for different modes
        for mode in allObjDict:
            if mode in memObjDict:
                exit_mode = "TABLE_MODE"
                prefix = "table"
            else :
                exit_mode = "REGISTER_MODE"
                prefix = "register"
                
            str = """\n
int cli_%s_mode(int module_id, int argc, char *args[])
{
	ctree->mode = %s_MODE;
	setPrompt("GalaxyWind(config/%s)#");
	printf("func: cli_%s_mode excuted!\\n");
	return 0;
}

int cli_%s_exit(int module_id, int argc, char *args[])
{
	ctree->mode = %s;
	setPrompt("GalaxyWind(config/%s)#");
	printf("func: cli_%s_exit excuted!\\n");
	return 0;
}\n\n""" % (mode.lower(),mode.upper(),mode.lower(),mode.lower(), mode.lower(),exit_mode, prefix, mode.lower())
                
            f.write(str)

        f.close()            


    def order_by_mode_name_increase(self, sameModeObjsDict):

        old_mode_list = []
        new_mode_list = []
    
        for old_mode in sameModeObjsDict:        
            old_mode_list.append(old_mode)        
            new_mode_list.append("")
            #print "old mode :  %s " % old_mode

    
        for mode in old_mode_list:
            old_mode = mode

            i = 0
            for mode_ in old_mode_list:
                j = 0
                while (old_mode[j:j+1].lower() == mode_[j:j+1].lower()) and (old_mode[j:j+1].lower() != '') and (mode_[j:j+1].lower() != ''):
                    #print "%s > %s " % (old_mode[0:1].lower(),  mode_[0:1].lower())                
                    j = j+1
                if old_mode[j:j+1].lower() > mode_[j:j+1].lower():                
                    i = i+1                    
        
            while new_mode_list[i] != "":
                i= i+1
        
            new_mode_list[i] = old_mode

        return new_mode_list


    def GenerateRegisterXMLFile(self, allObjDict): # give the register obj
        print "Generate the register.xml File."
        

        # add the new mode for registers
        f = file("register.xml", 'w')
        str = """<?xml version="1.0" encoding="utf-8"?>
<!--
	Description:
                THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!
-->

<root>
	<view name="REGISTER_MODE">\n"""
        f.write(str)

        new_mode_list = self.order_by_mode_name_increase(allObjDict)
        for mode in new_mode_list:
            str = """
		<command type="normal">
			<cli>%s</cli>
			<help>
				<helpInfo>Access %s mode</helpInfo>
			</help>
			<funcName type="user">cli_%s_mode</funcName>
			<newMode>%s</newMode>
		</command>\n""" % (mode.lower(), mode.lower(), mode.lower(), mode.upper())
                
            f.write(str)

        # add the exit command            
        str = """
        <command type="normal">
            <cli>exit</cli>
            <help>
                <helpInfo>End current mode and down to previous mode</helpInfo>
            </help>
            <funcName type="user">cli_register_exit</funcName>
            <newMode></newMode>
        </command>\n	
    </view>
</root>\n"""
        f.write(str)

        f.close()
        
    def GenerateTableXMLFile(self, allObjDict): # give the table obj
        print "Generate the table.xml File."
        

        # add the new mode for tables
        f = file("table.xml", 'w')
        str = """<?xml version="1.0" encoding="utf-8"?>
<!--
	Description:
                THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!
-->

<root>
	<view name="TABLE_MODE">\n"""
        f.write(str)

        new_mode_list = self.order_by_mode_name_increase(allObjDict)
        for mode in new_mode_list:                
            str = """
		<command type="normal">
			<cli>%s</cli>
			<help>
				<helpInfo>Access %s mode</helpInfo>
			</help>
			<funcName type="user">cli_%s_mode</funcName>
			<newMode>%s</newMode>
		</command>\n""" % (mode.lower(), mode.lower(), mode.lower(), mode.upper())
                
            f.write(str)




        # add the set_table_pool_mode command            
        str = """
        <command type="normal">
            <cli>set_table_pool_mode ( 0 | 1 | 2 | 3 )</cli>
            <help>
                <helpInfo>set table pool mode</helpInfo>
                <helpInfo>Set the mode to mode 0</helpInfo>
                <helpInfo>Set the mode to mode 1</helpInfo>
                <helpInfo>Set the mode to mode 2</helpInfo>
                <helpInfo>Set the mode to mode 3</helpInfo>
            </help>
            <funcName type="user">cli_set_table_pool_mode</funcName>
            <newMode></newMode>
        </command>\n"""
        f.write(str)


        # add clean all tables command            
        str = """
        <command type="normal">
            <cli>clean_all_table</cli>
            <help>
                <helpInfo>clean all the table</helpInfo>                
            </help>
            <funcName type="user">all_table_init</funcName>
            <newMode></newMode>
        </command>\n"""
        f.write(str)

        

        # add the exit command            
        str = """
        <command type="normal">
            <cli>exit</cli>
            <help>
                <helpInfo>End current mode and down to previous mode</helpInfo>
            </help>
            <funcName type="user">cli_table_exit</funcName>
            <newMode></newMode>
        </command>\n	
    </view>
</root>\n"""
        f.write(str)
       
        f.close()


    def GenerateRegMemXMLFile_For_TCAM_st_l3_defip(self, allObjDict, mode):
        print "Generate the Register related XML File only for TCAM table st_l3_defip."
        if 1 == 1:

            # generate the commands for the current mode
            str = "%s.xml" % mode.lower()
            f = file(str, 'w')

            str = """<?xml version=\"1.0\" encoding=\"utf-8\"?>

<!--
        Description:
                THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!
-->


<root>"""

            f.write(str)

            
            str = """
    <view name="%s_MODE">\n""" %(mode.upper()) # Here the mode name should be upper.
            f.write(str)



            #add commands for registers
            if allObjDict[mode][1][0] > 0:
                regList = allObjDict[mode][1][1]
                
                for reg in range(allObjDict[mode][1][0]):                    
                    
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>setreg %s (WORD | {" % (regList[reg]._regName).lower()# register name should be lower
            
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            str += " %s WORD |" % (field._fieldName).lower()
                    str = str[:-1]
                    str += "})</cli>\n"
                    str += "            <help>\n"
                    str+= "                <helpInfo>Set a register value.</helpInfo>\n"
                    str+= "                <helpInfo>The register name.</helpInfo>\n"
                    str+= "                <helpInfo>The value set to the register</helpInfo>\n"
            
                    f.write(str)
            
                    #add more help info
                    str = ""
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                            str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop                            
                    f.write(str)

                    str = "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_%s_set_reg</funcName>\n" % (mode, regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)



                    #add read command for register
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>getreg %s </cli>\n" % (regList[reg]._regName).lower()
                    str+= "            <help>\n"
                    str+= "                <helpInfo>Get a register value.</helpInfo>\n"
                    str+= "                <helpInfo>The register name.</helpInfo>\n"            
                    str+= "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_%s_get_reg</funcName>\n" % (mode, regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)




            # add commands for tables  
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1] # for hash or tcam, there are two table, key and data.          

                reg=0
                fieldInfoList = regList[reg]._regFieldList                
                nKeyType = len(fieldInfoList)
                
                table_type = "TCAM"
                
                if table_type == "TCAM":                       
                    str = "        <command type=\"normal\">\n"
                    str+= "            <cli>init_tcam tcam WORD"
                    
                    str+="</cli>\n"                    
                    str+= "            <help>\n"
                    str+= "                <helpInfo>The init tcam.</helpInfo>\n"
                    str+= "                <helpInfo>tcam number.</helpInfo>\n"
                    str+= "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_tcam_init_%s</funcName>\n" % mode
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)

                    
                if nKeyType == 1:                    
                    print "error info: st_l3_defip key type not only one...."
                    return

              
                # add commands for tables which have different KeyTypes                                      
                for info in fieldInfoList :
                    key = info[0]
                    data_fieldList = info[1]

                    # find the key fileds
                    for keyTypeField in regList[1]._regFieldList:
                        if key == keyTypeField[0]:
                            key_fieldList = keyTypeField[1]
                                   

                    ad2_fields = [[],[]]
                    ad2_name = [[],[]]
                    
                    if key == "0":                        
                        ad2_fields[0] = allObjDict["L3_DEFIP_ALPM_IPV4_T"][2][1][0]._regFieldList
                        ad2_fields[1] = allObjDict["L3_DEFIP_ALPM_IPV4_1_T"][2][1][0]._regFieldList
                        ad2_name[0] = "L3_DEFIP_ALPM_IPV4_T"
                        ad2_name[1] = "L3_DEFIP_ALPM_IPV4_1_T"
                        
                    if key == "1":
                        ad2_fields[0] = allObjDict["L3_DEFIP_ALPM_IPV6_64_T"][2][1][0]._regFieldList
                        ad2_fields[1] = allObjDict["L3_DEFIP_ALPM_IPV6_64_1_T"][2][1][0]._regFieldList
                        ad2_name[0] = "L3_DEFIP_ALPM_IPV6_64_T"
                        ad2_name[1] = "L3_DEFIP_ALPM_IPV6_64_1_T"
                    if key == "3":
                        ad2_fields[0] = allObjDict["L3_DEFIP_ALPM_IPV6_128_T"][2][1][0]._regFieldList
                        ad2_fields[1] = allObjDict["L3_DEFIP_ALPM_IPV6_128_1_T"][2][1][0]._regFieldList
                        ad2_name[0] = "L3_DEFIP_ALPM_IPV6_128_T"
                        ad2_name[1] = "L3_DEFIP_ALPM_IPV6_128_1_T"
                       

                    index = "index WORD tcam WORD"

                    for i in range(2):
                        
                        ad2_field_list = ad2_fields[i][0][1]                        
                        ad2_table_name = ad2_name[i].lower()
                        
                        entry_view = "entry_view %d" % i

                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>setmem %s %s %s ({" % (key, index, (regList[1]._regName).lower())


                        # add key fields
                        for fd in range(len(key_fieldList)):
                            field = key_fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                str += " %s WORD |" % (field._fieldName).lower()
                        str = str[:-1]
                        
                        str += "}) "


                        str+= " %s %s ({" % ((regList[0]._regName).lower(), entry_view)

                        # add data fields
                        for fd in range(len(data_fieldList)):
                            field = data_fieldList[fd]
                            if field._fieldName.upper() != "RESERVED" and field._fieldName.upper() != "ENTRY_VIEW":
                                str += " %s WORD |" % (field._fieldName).lower()
                        str = str[:-1]
    
                        str += "}) "



                        # add ad2 fields
                        str+= " %s ({" % (ad2_table_name)
                        
                        for fd in range(len(ad2_field_list)):
                            field = ad2_field_list[fd]
                            if field._fieldName.upper() != "RESERVED":
                                str += " %s WORD |" % (field._fieldName).lower()
                        str = str[:-1]
    
                        str += "})</cli>\n"
                        f.write(str)


                        str = ""                        
                        str += "            <help>\n"
                        str+= "                <helpInfo>Set a table value.</helpInfo>\n"
                        str+= "                <helpInfo>The keyType of the table.</helpInfo>\n" 
                        str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                        str+= "                <helpInfo>The tcam type.</helpInfo>\n"                                               
                        str+= "                <helpInfo>The key table name.</helpInfo>\n"                                                               
                        f.write(str)
                
                        #add more help info
                        str = ""
                        for fd in range(len(key_fieldList)):
                            field = key_fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                                
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str)


                        str = "                <helpInfo>The data table name.</helpInfo>\n"                        
                        f.write(str)


                        str = ""
                        for fd in range(len(data_fieldList)):
                            field = data_fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str)



                        
                        str = "                <helpInfo>The ad2 table name.</helpInfo>\n"
                        f.write(str)

                        str = ""
                        for fd in range(len(ad2_field_list)):
                            field = ad2_field_list[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str)

                        str = "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_%s_set_mem_%s</funcName>\n" % (mode, regList[0]._regName, key, i)
                        str+= "            <newMode></newMode>\n        </command>\n\n"
                        f.write(str)




                        # add read command
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>getmem %s %s %s ({" % (key, index, (regList[1]._regName).lower())


                        # add key fields
                        for fd in range(len(key_fieldList)):
                            field = key_fieldList[fd]
                            if field._fieldName.upper() != "RESERVED" :
                                str += " %s WORD |" % (field._fieldName).lower()
                        str = str[:-1]
    
                        str += "})</cli>\n"
                        

                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Get a table value.</helpInfo>\n"
                        str+= "                <helpInfo>The keyType of the table.</helpInfo>\n"
                        str+= "                <helpInfo>The index you want to get.</helpInfo>\n"
                        str+= "                <helpInfo>The tcam type.</helpInfo>\n"                        
                        str+= "                <helpInfo>The key table name.</helpInfo>\n"
                        
                                                
                        for fd in range(len(key_fieldList)):
                            field = key_fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                                                
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_%s_get_mem_%s</funcName>\n" % (mode, regList[0]._regName, key, i)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)
                        


            # add the exit command
            
            str = """
        <command type="normal">
                <cli>exit</cli>
                <help>
                    <helpInfo>End current mode and down to previous mode</helpInfo>
                </help>
                <funcName type="user">cli_%s_exit</funcName>
                <newMode></newMode>
	</command>\n	
    </view>
</root>\n""" % mode.lower()
            f.write(str)
            f.close()





    def GenerateRegMemXMLFile_For_HASH_TCAM_divide_key_and_data(self, allObjDict, mode):
        print "Generate the Register related XML File For HAHS TCAM."
        if 1 == 1:


            # here only for "st_l3_defip", currently comment out
            if 1 == 0: #mode == "st_l3_defip":
                self.GenerateRegMemXMLFile_For_TCAM_st_l3_defip(allObjDict, mode)
                return
            
            # generate the commands for the current mode
            str = "%s.xml" % mode.lower()
            f = file(str, 'w')

            str = """<?xml version=\"1.0\" encoding=\"utf-8\"?>

<!--
        Description:
                THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!
-->


<root>"""

            f.write(str)

            
            str = """
    <view name="%s_MODE">\n""" %(mode.upper()) # Here the mode name should be upper.
            f.write(str)



            #add commands for registers
            if allObjDict[mode][1][0] > 0:
                regList = allObjDict[mode][1][1]
                
                for reg in range(allObjDict[mode][1][0]):                    
                    
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>setreg %s (WORD | {" % (regList[reg]._regName).lower()# register name should be lower
            
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            str += " %s WORD |" % (field._fieldName).lower()
                    str = str[:-1]
                    str += "})</cli>\n"
                    str += "            <help>\n"
                    str+= "                <helpInfo>Set a register value.</helpInfo>\n"
                    str+= "                <helpInfo>The register name.</helpInfo>\n"
                    str+= "                <helpInfo>The value set to the register</helpInfo>\n"
            
                    f.write(str)
            
                    #add more help info
                    str = ""
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                            str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop                            
                    f.write(str)

                    str = "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_%s_set_reg</funcName>\n" % (mode, regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)



                    #add read command for register
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>getreg %s </cli>\n" % (regList[reg]._regName).lower()
                    str+= "            <help>\n"
                    str+= "                <helpInfo>Get a register value.</helpInfo>\n"
                    str+= "                <helpInfo>The register name.</helpInfo>\n"            
                    str+= "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_%s_get_reg</funcName>\n" % (mode, regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)




            # add commands for tables only have one keyType            
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1] # for hash or tcam, there are two table, key and data.          

                reg=0
                fieldInfoList = regList[reg]._regFieldList                
                nKeyType = len(fieldInfoList)
                
                table_type = self.get_table_type(mode)
                
                if table_type == "TCAM":                       
                    str = "        <command type=\"normal\">\n"
                    
                    if mode == "st_l3_defip":
                        str+= "            <cli>init_tcam tcam WORD</cli>\n"                    
                        str+= "            <help>\n"
                        str+= "                <helpInfo>initialize tcam.</helpInfo>\n"
                        str+= "                <helpInfo>set tcam number.</helpInfo>\n"
                        str+= "                <helpInfo>The value of tcam number.</helpInfo>\n"
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_tcam_init_%s</funcName>\n" % mode
                        str+= "            <newMode></newMode>\n        </command>\n\n"
                        f.write(str)
                        
                    else:
                        str+= "            <cli>init_tcam</cli>\n"                    
                        str+= "            <help>\n"
                        str+= "                <helpInfo>initialize tcam.</helpInfo>\n"                        
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_tcam_init_%s</funcName>\n" % mode
                        str+= "            <newMode></newMode>\n        </command>\n\n"
                        f.write(str)
                    
                if nKeyType == 1:                    

                    if table_type == "HASH":
                        index = ""
                    else:                        
                        if table_type == "TCAM":
                            if mode == "st_l3_defip": # have three key type, so, won't come to here when mode is "st_l3_defip"
                                index = "index WORD tcam WORD"
                            else:
                                index = "index WORD"
                        else :
                            print "ERROR table type, error will happen. Please check..."


                            
                    # add key table
                    fieldList = regList[1]._regFieldList[0][1]# + regList[1]._regFieldList[0][1]
                                            
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>setmem "
                    str+= "%s %s (WORD | {" % (index, (regList[1]._regName).lower())

            
                    for fd in range(len(fieldList)):
                        field = fieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            str += " %s WORD |" % (field._fieldName).lower()
                    str = str[:-1] # delete the "|"

                    # deal with the table which have no field
                    if len(fieldList) > 0:
                        str += "}"
                    else :
                        str = str[:-2] # delete the "| "
                        
                        
                    str += ")"

                    # add data table
                    fieldList = regList[0]._regFieldList[0][1]

                    str+= " %s (WORD | {" % ((regList[0]._regName).lower())

            
                    for fd in range(len(fieldList)):
                        field = fieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            str += " %s WORD |" % (field._fieldName).lower()
                    str = str[:-1] # delete the "|"

                    # deal with the table which have no field
                    if len(fieldList) > 0:
                        str += "}"
                    else :
                        str = str[:-2] # delete the "| "
                        
                        
                    str += ")"


                    fieldList = regList[1]._regFieldList[0][1]
                    str+="</cli>\n"                    
                    str += "            <help>\n"
                    str+= "                <helpInfo>Set a table value.</helpInfo>\n"                    

                    if table_type == "HASH":
                        str += ""
                    else:                        
                        if table_type == "TCAM":
                            if mode == "st_l3_defip": # have three key type, so, won't come to here when mode is "st_l3_defip"                                
                                str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                                str+= "                <helpInfo>The index value.</helpInfo>\n"
                                str+= "                <helpInfo>set tcam number.</helpInfo>\n"
                                str+= "                <helpInfo>The value of tcam number.</helpInfo>\n"                                
                            else:
                                str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                                str+= "                <helpInfo>The index value.</helpInfo>\n"

                    
                    str+= "                <helpInfo>The key table name.</helpInfo>\n"
                    str+= "                <helpInfo>The value set to the table</helpInfo>\n"
                    f.write(str)
                    
                    #add more help info
                    str = ""
                    for fd in range(len(fieldList)):
                        field = fieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                            str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                            #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                    f.write(str)
                    


                    fieldList = regList[0]._regFieldList[0][1]
                    str = "                <helpInfo>The data table name.</helpInfo>\n"                    
                    str+= "                <helpInfo>The value set to the table</helpInfo>\n"
                    f.write(str)
                    
                    #add more help info
                    str = ""
                    for fd in range(len(fieldList)):
                        field = fieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                            str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                            #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                    f.write(str)
                    

                    str = "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_%s_set_mem</funcName>\n" % (mode, regList[0]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)



                    # add read command
                    fieldList = regList[1]._regFieldList[0][1]
                    
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>getmem %s %s (WORD | {" % (index, (regList[1]._regName).lower())


                    for fd in range(len(fieldList)):
                        field = fieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            str += " %s WORD |" % (field._fieldName).lower()
                    str = str[:-1] # delete the "|"

                    # deal with the table which have no field
                    if len(fieldList) > 0:
                        str += "}"
                    else :
                        str = str[:-2] # delete the "| "
                        
                        
                    str += ") </cli>\n"

                    
                    str+= "            <help>\n"
                    str+= "                <helpInfo>Get a table value.</helpInfo>\n"
                    
                    if table_type == "HASH":
                        str += ""
                    else:                        
                        if table_type == "TCAM":
                            if mode == "st_l3_defip": # have three key type, so, won't come to here when mode is "st_l3_defip"                                
                                str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                                str+= "                <helpInfo>The index value.</helpInfo>\n"
                                str+= "                <helpInfo>set tcam number.</helpInfo>\n"
                                str+= "                <helpInfo>The value of tcam number.</helpInfo>\n"                                
                            else:
                                str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                                str+= "                <helpInfo>The index value.</helpInfo>\n"

                    str+= "                <helpInfo>The key table name.</helpInfo>\n"                         
                    str+= "                <helpInfo>The value set to the table</helpInfo>\n"
                    f.write(str)
                
                    str = ""
                    for fd in range(len(fieldList)):
                        field = fieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                            str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop                            
                            #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                    f.write(str)
                    
                    str+= "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_%s_get_mem</funcName>\n" % (mode, regList[0]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n"
                    f.write(str)                                                        
                      




                # add commands for tables which have different KeyTypes             
                else:                    
                    for info in fieldInfoList :
                        key = info[0]
                        data_fieldList = info[1]

                        # find the key fileds
                        for keyTypeField in regList[1]._regFieldList:
                            if key == keyTypeField[0]:
                                key_fieldList = keyTypeField[1]
                                

                        table_type = self.get_table_type(mode)

                        if table_type == "HASH":
                            index = ""
                        else:                        
                            if table_type == "TCAM":
                                if mode == "st_l3_defip":
                                    index = "index WORD tcam WORD"
                                else:
                                    index = "index WORD"
                            else :
                                print "ERROR table type, error will happen. Please check..."

                                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>setmem "
                        str+= "%s %s %s (WORD | {" % (key, index, (regList[1]._regName).lower())


                        # add key fields
                        for fd in range(len(key_fieldList)):
                            field = key_fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                str += " %s WORD |" % (field._fieldName).lower()
                        str = str[:-1]
    
                        str += "})"


                        str+= "%s (WORD | {" % ((regList[0]._regName).lower())
                        # add data fields
                        for fd in range(len(data_fieldList)):
                            field = data_fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                str += " %s WORD |" % (field._fieldName).lower()
                        str = str[:-1]
    
                        str += "})</cli>\n"
                        f.write(str)


                        str = ""                        
                        str += "            <help>\n"
                        str+= "                <helpInfo>Set a table value.</helpInfo>\n"
                        str+= "                <helpInfo>The keyType of the table.</helpInfo>\n"
                        
                        if table_type == "HASH":
                            str += ""
                        else:                        
                            if table_type == "TCAM":
                                if mode == "st_l3_defip": 
                                    str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                                    str+= "                <helpInfo>The index value.</helpInfo>\n"
                                    str+= "                <helpInfo>set tcam number.</helpInfo>\n"
                                    str+= "                <helpInfo>The value of tcam number.</helpInfo>\n"                                
                                else:
                                    str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                                    str+= "                <helpInfo>The index value.</helpInfo>\n"

                        str+= "                <helpInfo>The key table name.</helpInfo>\n" 
                        str+= "                <helpInfo>The value set to the table</helpInfo>\n"                
                        f.write(str)
                
                        #add more help info
                        str = ""
                        for fd in range(len(key_fieldList)):
                            field = key_fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str)



                        str = "                <helpInfo>The data table name.</helpInfo>\n"                                               
                        str+= "                <helpInfo>The value set to the table</helpInfo>\n"
                        f.write(str)

                        str = ""
                        for fd in range(len(data_fieldList)):
                            field = data_fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str)

                        str = "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_%s_set_mem</funcName>\n" % (mode, regList[0]._regName, key)
                        str+= "            <newMode></newMode>\n        </command>\n\n"
                        f.write(str)



                        # add read command
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>getmem %s %s %s (WORD | {" % (key, index, (regList[1]._regName).lower())


                        # add key fields
                        for fd in range(len(key_fieldList)):
                            field = key_fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                str += " %s WORD |" % (field._fieldName).lower()
                        str = str[:-1]
    
                        str += "})</cli>\n"
                        


                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Get a table value.</helpInfo>\n"
                        str+= "                <helpInfo>The keyType of the table.</helpInfo>\n"
                         
                        if table_type == "HASH":
                            str += ""
                        else:                        
                            if table_type == "TCAM":
                                if mode == "st_l3_defip": 
                                    str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                                    str+= "                <helpInfo>The index value.</helpInfo>\n"
                                    str+= "                <helpInfo>set tcam number.</helpInfo>\n"
                                    str+= "                <helpInfo>The value of tcam number.</helpInfo>\n"                                
                                else:
                                    str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                                    str+= "                <helpInfo>The index value.</helpInfo>\n"


                        str+= "                <helpInfo>The key table name.</helpInfo>\n"                      
                        str+= "                <helpInfo>The value set to the table</helpInfo>\n"
                        
                        
                        for fd in range(len(key_fieldList)):
                            field = key_fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                                                
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_%s_get_mem</funcName>\n" % (mode, regList[0]._regName, key)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)


            # add test commands for test all registers
            if allObjDict[mode][1][0] > 0:                   
                str = "        <command type=\"normal\">\n"            
                str+= "            <cli>test_reg (default | WORD )</cli>\n"
                str+= "            <help>\n"
                str+= "                <helpInfo>Test all register.</helpInfo>\n"
                str+= "                <helpInfo>Get the default value of all registers.</helpInfo>\n"
                str+= "                <helpInfo>The value set to the register then compare.</helpInfo>\n"
                str+= "            </help>\n"
                str+= "            <funcName type=\"user\">cli_%s_test_reg</funcName>\n" % (mode)
                str+= "            <newMode></newMode>\n        </command>\n\n"                    
                f.write(str)


            # add test commands for test all registers by i2c
            if allObjDict[mode][1][0] > 0:                   
                str = "        <command type=\"normal\">\n"            
                str+= "            <cli>test_reg_i2c port &lt;1-65535&gt; ip A.B.C.D (default | WORD )</cli>\n"
                str+= "            <help>\n"
                str+= "                <helpInfo>Test all register.</helpInfo>\n"
                str+= "                <helpInfo>set port number</helpInfo>\n"
                str+= "                <helpInfo>port value &lt;1-65535&gt;</helpInfo>\n"
                str+= "                <helpInfo>Internet Protocol address.</helpInfo>\n"
                str+= "                <helpInfo>Internet Protocol address.</helpInfo>\n"				
                str+= "                <helpInfo>Get the default value of all registers.</helpInfo>\n"
                str+= "                <helpInfo>The value set to the register then compare.</helpInfo>\n"
                str+= "            </help>\n"
                str+= "            <funcName type=\"user\">cli_%s_i2c_test_reg</funcName>\n" % (mode)
                str+= "            <newMode></newMode>\n        </command>\n\n"                    
                f.write(str)
                

            # add test commands for test all index for table
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1]
                
                for reg in range(allObjDict[mode][2][0]):
                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>test_mem %s index WORD data WORD</cli>\n" % ((regList[reg]._regName).lower())
                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Test a table to see if the specified index can be write successfully .</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"                        
                        str+= "                <helpInfo>The index of the table.</helpInfo>\n"                        
                        str+= "                <helpInfo>The index value.</helpInfo>\n"
                        str+= "                <helpInfo>The data you want to set.</helpInfo>\n"
                        str+= "                <helpInfo>The data value.</helpInfo>\n"                        
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_test_mem</funcName>\n" % (mode, regList[reg]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)

             # add test commands for test all index for table by i2c
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1]
                
                for reg in range(allObjDict[mode][2][0]):
                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>test_mem_i2c %s port &lt;1-65535&gt; ip A.B.C.D index WORD data WORD</cli>\n" % ((regList[reg]._regName).lower())
                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Test a table to see if the specified index can be write successfully .</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"
                        str+= "                <helpInfo>set port number</helpInfo>\n"
                        str+= "                <helpInfo>port value &lt;1-65535&gt;</helpInfo>\n"
                        str+= "                <helpInfo>Internet Protocol address.</helpInfo>\n"
                        str+= "                <helpInfo>Internet Protocol address.</helpInfo>\n"
                        str+= "                <helpInfo>The index of the table.</helpInfo>\n"                        
                        str+= "                <helpInfo>The index value.</helpInfo>\n"
                        str+= "                <helpInfo>The data you want to set.</helpInfo>\n"
                        str+= "                <helpInfo>The data value.</helpInfo>\n"                        
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_i2c_test_mem</funcName>\n" % (mode, regList[reg]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)
                                 



            # add mem dump and clean commands for tables
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1]
                
                for reg in range(allObjDict[mode][2][0]):
                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>mem %s ((dump index WORD) | ( clean index WORD ( (data WORD) | ) ) )</cli>\n" % ((regList[reg]._regName).lower())                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Dump all valid data of the table, or clean the table.</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"
                        str+= "                <helpInfo>dump the table data</helpInfo>\n"
                        str+= "                <helpInfo>the index you want to dump or clean</helpInfo>\n"
                        str+= "                <helpInfo>the index value</helpInfo>\n"			
                        str+= "                <helpInfo>clean the table</helpInfo>\n"
                        str+= "                <helpInfo>the index you want to dump or clean</helpInfo>\n"
                        str+= "                <helpInfo>the index value</helpInfo>\n"
                        str+= "                <helpInfo>clean with the initial data</helpInfo>\n"
                        str+= "                <helpInfo>the initial data</helpInfo>\n"			
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_dump_or_clean_mem</funcName>\n" % (mode, regList[reg]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)
                        break # because this is hash or tcam         


            # add the exit command
            
            str = """
        <command type="normal">
                <cli>exit</cli>
                <help>
                    <helpInfo>End current mode and down to previous mode</helpInfo>
                </help>
                <funcName type="user">cli_%s_exit</funcName>
                <newMode></newMode>
	</command>\n	
    </view>
</root>\n""" % mode.lower()
            f.write(str)
            f.close()






    def GenerateRegMemXMLFile_For_TABLE_POOL(self, allObjDict, mode):
        print "Generate the Register related XML File For table which store in TABLE POOL."

        if 1 == 1:

            # generate the commands for the current mode
            str = "%s.xml" % mode.lower()
            f = file(str, 'w')

            str = """<?xml version=\"1.0\" encoding=\"utf-8\"?>

<!--
        Description:
                THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!
-->


<root>"""

            f.write(str)

            
            str = """
    <view name="%s_MODE">\n""" %(mode.upper()) # Here the mode name should be upper.
            f.write(str)



            #add commands for registers
            if allObjDict[mode][1][0] > 0:
                regList = allObjDict[mode][1][1]
                
                for reg in range(allObjDict[mode][1][0]):                    
                    
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>setreg %s (WORD | {" % (regList[reg]._regName).lower()# register name should be lower
            
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            str += " %s WORD |" % (field._fieldName).lower()
                    str = str[:-1]
                    str += "})</cli>\n"
                    str += "            <help>\n"
                    str+= "                <helpInfo>Set a register value.</helpInfo>\n"
                    str+= "                <helpInfo>The register name.</helpInfo>\n"
                    str+= "                <helpInfo>The value set to the register</helpInfo>\n"
            
                    f.write(str)
            
                    #add more help info
                    str = ""
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                            str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                                        
                    f.write(str)

                    str = "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_%s_set_reg</funcName>\n" % (mode, regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)



                    #add read command for register
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>getreg %s </cli>\n" % (regList[reg]._regName).lower()
                    str+= "            <help>\n"
                    str+= "                <helpInfo>Get a register value.</helpInfo>\n"
                    str+= "                <helpInfo>The register name.</helpInfo>\n"            
                    str+= "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_%s_get_reg</funcName>\n" % (mode, regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)




            # add commands for tables only have one keyType            
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1] # for table pool, there are only one key type.          
                
                reg=0
                fieldInfoList = regList[reg]._regFieldList                
                nKeyType = len(fieldInfoList)                
                if nKeyType == 1:

                    # below dictionary only for l2 entry and l3 entry hash table. This is special handle. Hard code. Any better solution ?
                    filedList_dict_ = { "L2_ENTRY_T":["MAC_ADDR", "VLAN_ID", "KEY_TYPE", "VALID"],
                              "L3_ENTRY_IPV4_UNICAST_T":["IPV4UC__VRF_ID", "IPV4UC__IP_ADDR", "KEY_TYPE", "VALID"],
                              "L3_ENTRY_IPV6_UNICAST_T":["IPV6UC__VRF_ID", "IPV6UC__IP_ADDR_LWR_64", "KEY_TYPE_0", "IPV6UC__IP_ADDR_UPR_64", "VALID"],
                              "L3_ENTRY_IPV4_MULTICAST_T":["VRF_ID", "SOURCE_IP_ADDR", "GROUP_IP_ADDR", "KEY_TYPE_0", "L3IIF_VLANID", "VALID"],
                              "L3_ENTRY_IPV6_MULTICAST_T":["VRF_ID", "GROUP_IP_ADDR_LWR_64", "KEY_TYPE_0", "GROUP_IP_ADDR_UPR_56", "SOURCE_IP_ADDR_LWR_64", "L3IIF_VLANID", "SOURCE_IP_ADDR_UPR_64", "VALID"]}


                    table_type = self.get_table_pool_table_type(mode)
                    if table_type == "HASH":
                        
                        keyFiledList  = []
                        dataFiledList = []

                        fieldList = regList[0]._regFieldList[0][1]
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() in filedList_dict_[mode]:
                                keyFiledList.append(field)
                            else:
                                dataFiledList.append(field)


                            
                        # add key table
                        fieldList = keyFiledList
                                            
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>setmem "
                        str+= "%s_KEY ({" % ((regList[0]._regName).lower())

            
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                str += " %s WORD |" % (field._fieldName).lower()
                        str = str[:-1] # delete the "|"

                        # deal with the table which have no field
                        if len(fieldList) > 0:
                            str += "}"
                        else :
                            str = str[:-2] # delete the "| "
                        
                        
                        str += ")"

                        # add data table
                        fieldList = dataFiledList

                        str+= " %s_DATA ({" % ((regList[0]._regName).lower())

            
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                str += " %s WORD |" % (field._fieldName).lower()
                        str = str[:-1] # delete the "|"

                        # deal with the table which have no field
                        if len(fieldList) > 0:
                            str += "}"
                        else :
                            str = str[:-2] # delete the "| "
                        
                        
                        str += ")"


                        fieldList = keyFiledList
                        str+="</cli>\n"                    
                        str += "            <help>\n"
                        str+= "                <helpInfo>Set a table value.</helpInfo>\n"                    
                        str+= "                <helpInfo>Set the key.</helpInfo>\n"
                                                
            
                        f.write(str)
                    
                        #add more help info
                        str = ""
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str)
                    


                        fieldList = dataFiledList
                        str = "                <helpInfo>Set the data.</helpInfo>\n"                    
                        
                        f.write(str)
                    
                        #add more help info
                        str = ""
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str)
                    

                        str = "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_set_mem</funcName>\n" % (mode, regList[0]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n\n"
                        f.write(str)




                        # add read command
                        fieldList = keyFiledList
                    
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>getmem %s_KEY ({" % ((regList[0]._regName).lower())


                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                str += " %s WORD |" % (field._fieldName).lower()
                        str = str[:-1] # delete the "|"

                        # deal with the table which have no field
                        if len(fieldList) > 0:
                            str += "}"
                        else :
                            str = str[:-2] # delete the "| "
                        
                        
                        str += ") </cli>\n"

                    
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Get a table value.</helpInfo>\n"
                        str+= "                <helpInfo>Set the key.</helpInfo>\n"
                        
                        f.write(str)
                
                        str = ""
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str)
                    
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_get_mem</funcName>\n" % (mode, regList[0]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)                                                        
            



                    if table_type == "DIRECT":                        
                        fieldList = regList[0]._regFieldList[0][1]
                                            
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>setmem "
                        str+= "%s index WORD (WORD | {" % ((regList[0]._regName).lower())

            
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                str += " %s WORD |" % (field._fieldName).lower()
                        str = str[:-1] # delete the "|"
    
                        # deal with the table which have no field
                        if len(fieldList) > 0:
                            str += "}"
                        else :
                            str = str[:-2] # delete the "| "
                        
                        
                        str += ")"

                    
                        fieldList = regList[0]._regFieldList[0][1]
                        str+="</cli>\n"                    
                        str += "            <help>\n"
                        str+= "                <helpInfo>Set a table value.</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"
                        str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                        str+= "                <helpInfo>The index vlaue you want to set.</helpInfo>\n"                           
                        str+= "                <helpInfo>The value set to the table</helpInfo>\n"
            
                        f.write(str)
                    
                        #add more help info
                        str = ""
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str)


                        str = "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_set_mem</funcName>\n" % (mode, regList[0]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n\n"
                        f.write(str)



                        # add read command   
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>getmem %s index WORD </cli>\n" % (regList[0]._regName).lower()
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Get a table value.</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"
                        str+= "                <helpInfo>The index you want to get.</helpInfo>\n"
                        str+= "                <helpInfo>The index value.</helpInfo>\n"
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_get_mem</funcName>\n" % (mode, regList[0]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str) 

            # add test commands for test all registers
            if allObjDict[mode][1][0] > 0:                   
                str = "        <command type=\"normal\">\n"            
                str+= "            <cli>test_reg (default | WORD )</cli>\n"
                str+= "            <help>\n"
                str+= "                <helpInfo>Test all register.</helpInfo>\n"
                str+= "                <helpInfo>Get the default value of all registers.</helpInfo>\n"
                str+= "                <helpInfo>The value set to the register then compare.</helpInfo>\n"
                str+= "            </help>\n"
                str+= "            <funcName type=\"user\">cli_%s_test_reg</funcName>\n" % (mode)
                str+= "            <newMode></newMode>\n        </command>\n\n"                    
                f.write(str)


            # add test commands for test all registers by i2c
            if allObjDict[mode][1][0] > 0:                   
                str = "        <command type=\"normal\">\n"            
                str+= "            <cli>test_reg_i2c port &lt;1-65535&gt; ip A.B.C.D (default | WORD )</cli>\n"
                str+= "            <help>\n"
                str+= "                <helpInfo>Test all register.</helpInfo>\n"
                str+= "                <helpInfo>set port number</helpInfo>\n"
                str+= "                <helpInfo>port value &lt;1-65535&gt;</helpInfo>\n"
                str+= "                <helpInfo>Internet Protocol address.</helpInfo>\n"
                str+= "                <helpInfo>Internet Protocol address.</helpInfo>\n"				
                str+= "                <helpInfo>Get the default value of all registers.</helpInfo>\n"
                str+= "                <helpInfo>The value set to the register then compare.</helpInfo>\n"
                str+= "            </help>\n"
                str+= "            <funcName type=\"user\">cli_%s_i2c_test_reg</funcName>\n" % (mode)
                str+= "            <newMode></newMode>\n        </command>\n\n"                    
                f.write(str)
                

            # add test commands for test all index for table
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1]
                
                for reg in range(allObjDict[mode][2][0]):
                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>test_mem %s index WORD data WORD</cli>\n" % ((regList[reg]._regName).lower())
                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Test a table to see if the specified index can be write successfully .</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"                        
                        str+= "                <helpInfo>The index of the table.</helpInfo>\n"                        
                        str+= "                <helpInfo>The index value.</helpInfo>\n"
                        str+= "                <helpInfo>The data you want to set.</helpInfo>\n"
                        str+= "                <helpInfo>The data value.</helpInfo>\n"                        
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_test_mem</funcName>\n" % (mode, regList[reg]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)

             # add test commands for test all index for table by i2c
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1]
                
                for reg in range(allObjDict[mode][2][0]):
                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>test_mem_i2c %s port &lt;1-65535&gt; ip A.B.C.D index WORD data WORD</cli>\n" % ((regList[reg]._regName).lower())
                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Test a table to see if the specified index can be write successfully .</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"
                        str+= "                <helpInfo>set port number</helpInfo>\n"
                        str+= "                <helpInfo>port value &lt;1-65535&gt;</helpInfo>\n"
                        str+= "                <helpInfo>Internet Protocol address.</helpInfo>\n"
                        str+= "                <helpInfo>Internet Protocol address.</helpInfo>\n"
                        str+= "                <helpInfo>The index of the table.</helpInfo>\n"                        
                        str+= "                <helpInfo>The index value.</helpInfo>\n"
                        str+= "                <helpInfo>The data you want to set.</helpInfo>\n"
                        str+= "                <helpInfo>The data value.</helpInfo>\n"                        
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_i2c_test_mem</funcName>\n" % (mode, regList[reg]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)
                                 


            # add mem dump and clean commands for tables
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1]
                
                for reg in range(allObjDict[mode][2][0]):
                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>mem %s ((dump index WORD) | ( clean index WORD ( (data WORD) | ) ) )</cli>\n" % ((regList[reg]._regName).lower())                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Dump all valid data of the table, or clean the table.</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"
                        str+= "                <helpInfo>dump the table data</helpInfo>\n"
                        str+= "                <helpInfo>the index you want to dump or clean</helpInfo>\n"
                        str+= "                <helpInfo>the index value</helpInfo>\n"
                        str+= "                <helpInfo>clean the table</helpInfo>\n"
                        str+= "                <helpInfo>the index you want to dump or clean</helpInfo>\n"
                        str+= "                <helpInfo>the index value</helpInfo>\n"
                        str+= "                <helpInfo>clean with the initial data</helpInfo>\n"
                        str+= "                <helpInfo>the initial data</helpInfo>\n"
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_dump_or_clean_mem</funcName>\n" % (mode, regList[reg]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)
                                 


            # add the exit command
            
            str = """
        <command type="normal">
                <cli>exit</cli>
                <help>
                    <helpInfo>End current mode and down to previous mode</helpInfo>
                </help>
                <funcName type="user">cli_%s_exit</funcName>
                <newMode></newMode>
	</command>\n	
    </view>
</root>\n""" % mode.lower()
            f.write(str)
            f.close()


              

    def GenerateRegMemXMLFile(self, allObjDict):
        print "Generate the Register related XML File."

        for mode in allObjDict:            
            if mode.upper() in table_pool_dict:
                self.GenerateRegMemXMLFile_For_TABLE_POOL(allObjDict, mode)
                continue
            
            table_type = self.get_table_type(mode)
            if table_type in ["HASH", "TCAM"]: # if the table is hash or tcam.                
                #self.GenerateRegMemXMLFile_For_HASH_TCAM(allObjDict, mode)
                self.GenerateRegMemXMLFile_For_HASH_TCAM_divide_key_and_data(allObjDict, mode)
                
                continue
            

            # generate the commands for the current mode
            str = "%s.xml" % mode.lower()
            f = file(str, 'w')

            str = """<?xml version=\"1.0\" encoding=\"utf-8\"?>

<!--
        Description:
                THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!
-->


<root>"""

            f.write(str)

            
            str = """
    <view name="%s_MODE">\n""" %(mode.upper()) # Here the mode name should be upper.
            f.write(str)



            #add commands for registers
            if allObjDict[mode][1][0] > 0:
                regList = allObjDict[mode][1][1]
                
                for reg in range(allObjDict[mode][1][0]):
                            
                # The formate of set Command
                #<command type="normal">
                #   <cli>setreg reg_name (WORD | { fd1 WORD | fd2 WORD | fd3 WORD .... })</cli>
                #   <help>
                #	<helpInfo>Set a register value.</helpInfo>				
                #	<helpInfo>The register name</helpInfo>
                #	<helpInfo>The value set to the register</helpInfo>
                #       ... ...
                #   </help>
                #   <funcName type="user">cli_reg_name_set</funcName>
                #   <newMode></newMode>
                #</command>

                    
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>setreg %s (WORD | {" % (regList[reg]._regName).lower()# register name should be lower
            
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        if field._fieldName.upper() != "RESERVED":                            
                            str += " %s WORD |" % (field._fieldName).lower()
                    str = str[:-1]
                    str += "})</cli>\n"
                    str += "            <help>\n"
                    str+= "                <helpInfo>Set a register value.</helpInfo>\n"
                    str+= "                <helpInfo>The register name.</helpInfo>\n"
                    str+= "                <helpInfo>The value set to the register</helpInfo>\n"
            
                    f.write(str)
            
                    #add more help info
                    str = ""
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                            str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                    f.write(str)

                    str = "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_%s_set_reg</funcName>\n" % (mode, regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)


                    # The formate of get Command
                    #<command type="normal">
                    #   <cli>getreg reg_name</cli>
                    #   <help>
                    #	<helpInfo>Set a register value.</helpInfo>				
                    #	<helpInfo>The register name</helpInfo>
                    #   </help>
                    #   <funcName type="user">cli_reg_name_get</funcName>
                    #   <newMode></newMode>
                    #</command>

                    #add read command for register
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>getreg %s </cli>\n" % (regList[reg]._regName).lower()
                    str+= "            <help>\n"
                    str+= "                <helpInfo>Get a register value.</helpInfo>\n"
                    str+= "                <helpInfo>The register name.</helpInfo>\n"            
                    str+= "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_%s_get_reg</funcName>\n" % (mode, regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)



            # add commands for tables only have one keyType            
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1]
                
                for reg in range(allObjDict[mode][2][0]):

                    fieldInfoList = regList[reg]._regFieldList
                    nKeyType = len(fieldInfoList)
                    if nKeyType > 1:
                        continue
                    
                    #print "%s %s %s" % (regList[reg]._excelName, regList[reg]._sheetName, regList[reg]._regName)
                    
                    fieldList = regList[reg]._regFieldList[0][1]
                        
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>setmem  %s (pio | dma) index WORD (WORD | {" % (regList[reg]._regName).lower()

            
                    for fd in range(len(fieldList)):
                        field = fieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            str += " %s WORD |" % (field._fieldName).lower()
                    str = str[:-1] # delete the "|"

                    # deal with the table which have no field
                    if len(fieldList) > 0:
                        str += "}"
                    else :
                        str = str[:-2] # delete the "| "
                        
                        
                    str += ")</cli>\n"                    
                    str += "            <help>\n"
                    str+= "                <helpInfo>Set a table value.</helpInfo>\n"                    
                    str+= "                <helpInfo>The table name.</helpInfo>\n"
                    str+= "                <helpInfo>Set the table by PIO.</helpInfo>\n"
                    str+= "                <helpInfo>Set the table by DMA.</helpInfo>\n"                    
                    str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                    str+= "                <helpInfo>The index vlaue you want to set.</helpInfo>\n"
                    str+= "                <helpInfo>The value set to the table</helpInfo>\n"
            
                    f.write(str)
            
                    #add more help info
                    str = ""
                    for fd in range(len(fieldList)):
                        field = fieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                            str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop                            
                            #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                    f.write(str)

                    str = "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_%s_set_mem</funcName>\n" % (mode, regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)


                    # add read command
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>getmem %s (pio | dma) index WORD </cli>\n" % (regList[reg]._regName).lower()
                    str+= "            <help>\n"
                    str+= "                <helpInfo>Get a table value.</helpInfo>\n"
                    str+= "                <helpInfo>The table name.</helpInfo>\n"
                    str+= "                <helpInfo>Set the table by PIO.</helpInfo>\n"
                    str+= "                <helpInfo>Set the table by DMA.</helpInfo>\n" 
                    str+= "                <helpInfo>The index you want to get.</helpInfo>\n"
                    str+= "                <helpInfo>The index value.</helpInfo>\n"
                    str+= "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_%s_get_mem</funcName>\n" % (mode, regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n"
                    f.write(str)                                                        
                        

            # add commands for tables which have different KeyTypes
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1]
                
                for reg in range(allObjDict[mode][2][0]):

                    fieldInfoList = regList[reg]._regFieldList
                    nKeyType = len(fieldInfoList)

                    if nKeyType  == 1:
                        continue                    
                    
                    for info in fieldInfoList :
                        key = info[0]
                        fieldList = info[1]
                        
                                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>setmem %s (pio | dma) %s index WORD (WORD | {" % ((regList[reg]._regName).lower(), key)


            
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                str += " %s WORD |" % (field._fieldName).lower()
                        str = str[:-1]
    
                        str += "})</cli>\n"
                        
                        str += "            <help>\n"
                        str+= "                <helpInfo>Set a table value.</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"
                        str+= "                <helpInfo>Set the table by PIO.</helpInfo>\n"
                        str+= "                <helpInfo>Set the table by DMA.</helpInfo>\n" 
                        str+= "                <helpInfo>The keyType of the table.</helpInfo>\n"
                        str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                        str+= "                <helpInfo>The index vlaue you want to set.</helpInfo>\n"
                        str+= "                <helpInfo>The value set to the table</helpInfo>\n"
                
                        f.write(str)
                
                        #add more help info
                        str = ""
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str)

                        str = "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_%s_set_mem</funcName>\n" % (mode, regList[reg]._regName, key)
                        str+= "            <newMode></newMode>\n        </command>\n\n"
                        f.write(str)





                        # add read command
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>getmem %s (pio | dma) %s index WORD </cli>\n" % ((regList[reg]._regName).lower(), key)
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Get a table value.</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"
                        str+= "                <helpInfo>Set the table by PIO.</helpInfo>\n"
                        str+= "                <helpInfo>Set the table by DMA.</helpInfo>\n" 
                        str+= "                <helpInfo>The keyType of the table.</helpInfo>\n"
                        str+= "                <helpInfo>The index you want to get.</helpInfo>\n"                        
                        str+= "                <helpInfo>The index value.</helpInfo>\n"
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_%s_get_mem</funcName>\n" % (mode, regList[reg]._regName, key)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)



            # add test commands for test all registers
            if allObjDict[mode][1][0] > 0:                   
                str = "        <command type=\"normal\">\n"            
                str+= "            <cli>test_reg (default | WORD )</cli>\n"
                str+= "            <help>\n"
                str+= "                <helpInfo>Test all register.</helpInfo>\n"
                str+= "                <helpInfo>Get the default value of all registers.</helpInfo>\n"
                str+= "                <helpInfo>The value set to the register then compare.</helpInfo>\n"
                str+= "            </help>\n"
                str+= "            <funcName type=\"user\">cli_%s_test_reg</funcName>\n" % (mode)
                str+= "            <newMode></newMode>\n        </command>\n\n"                    
                f.write(str)


            # add test commands for test all registers by i2c
            if allObjDict[mode][1][0] > 0:                   
                str = "        <command type=\"normal\">\n"            
                str+= "            <cli>test_reg_i2c port &lt;1-65535&gt; ip A.B.C.D (default | WORD )</cli>\n"
                str+= "            <help>\n"
                str+= "                <helpInfo>Test all register.</helpInfo>\n"
                str+= "                <helpInfo>set port number</helpInfo>\n"
                str+= "                <helpInfo>port value &lt;1-65535&gt;</helpInfo>\n"
                str+= "                <helpInfo>Internet Protocol address.</helpInfo>\n"
                str+= "                <helpInfo>Internet Protocol address.</helpInfo>\n"				
                str+= "                <helpInfo>Get the default value of all registers.</helpInfo>\n"
                str+= "                <helpInfo>The value set to the register then compare.</helpInfo>\n"
                str+= "            </help>\n"
                str+= "            <funcName type=\"user\">cli_%s_i2c_test_reg</funcName>\n" % (mode)
                str+= "            <newMode></newMode>\n        </command>\n\n"                    
                f.write(str)
                

            # add test commands for test all index for table
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1]
                
                for reg in range(allObjDict[mode][2][0]):
                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>test_mem %s index WORD data WORD</cli>\n" % ((regList[reg]._regName).lower())
                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Test a table to see if the specified index can be write successfully .</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"                        
                        str+= "                <helpInfo>The index of the table.</helpInfo>\n"                        
                        str+= "                <helpInfo>The index value.</helpInfo>\n"
                        str+= "                <helpInfo>The data you want to set.</helpInfo>\n"
                        str+= "                <helpInfo>The data value.</helpInfo>\n"                        
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_test_mem</funcName>\n" % (mode, regList[reg]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)

            # add test commands for test all index for table by i2c
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1]
                
                for reg in range(allObjDict[mode][2][0]):
                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>test_mem_i2c %s port &lt;1-65535&gt; ip A.B.C.D index WORD data WORD</cli>\n" % ((regList[reg]._regName).lower())
                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Test a table to see if the specified index can be write successfully .</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"
                        str+= "                <helpInfo>set port number</helpInfo>\n"
                        str+= "                <helpInfo>port value &lt;1-65535&gt;</helpInfo>\n"
                        str+= "                <helpInfo>Internet Protocol address.</helpInfo>\n"
                        str+= "                <helpInfo>Internet Protocol address.</helpInfo>\n"
                        str+= "                <helpInfo>The index of the table.</helpInfo>\n"                        
                        str+= "                <helpInfo>The index value.</helpInfo>\n"
                        str+= "                <helpInfo>The data you want to set.</helpInfo>\n"
                        str+= "                <helpInfo>The data value.</helpInfo>\n"                        
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_i2c_test_mem</funcName>\n" % (mode, regList[reg]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)
                                 

                                

            # add mem dump and clean commands for tables
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1]
                
                for reg in range(allObjDict[mode][2][0]):
                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>mem %s ((dump index WORD) | ( clean index WORD ( (data WORD) | ) ) )</cli>\n" % ((regList[reg]._regName).lower())                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Dump all valid data of the table, or clean the table.</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"
                        str+= "                <helpInfo>dump the table data</helpInfo>\n"
                        str+= "                <helpInfo>the index you want to dump or clean</helpInfo>\n"
                        str+= "                <helpInfo>the index value</helpInfo>\n"
                        str+= "                <helpInfo>clean the table</helpInfo>\n"
                        str+= "                <helpInfo>the index you want to dump or clean</helpInfo>\n"
                        str+= "                <helpInfo>the index value</helpInfo>\n"
                        str+= "                <helpInfo>clean with the initial data</helpInfo>\n"
                        str+= "                <helpInfo>the initial data</helpInfo>\n"			
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_dump_or_clean_mem</funcName>\n" % (mode, regList[reg]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)



            
            # add clean commands for all registers and tables in cb_cfg and cb_cnt mode
            if mode.lower() in ["cb_cfg", "cb_cnt"]:                                   
                str = "        <command type=\"normal\">\n"            
                str+= "            <cli>clean (reg | mem | all)</cli>\n"
                str+= "            <help>\n"
                str+= "                <helpInfo>Clean all register or table or all of them in cb_cfg and cb_cnt mode.</helpInfo>\n"
                str+= "                <helpInfo>Clean all registers.</helpInfo>\n"
                str+= "                <helpInfo>Clean all tables.</helpInfo>\n"
                str+= "                <helpInfo>Clean all registers and tables.</helpInfo>\n"
                str+= "            </help>\n"
                str+= "            <funcName type=\"user\">cli_clean_all_%s_reg_table</funcName>\n" % mode
                str+= "            <newMode></newMode>\n        </command>\n\n"
                f.write(str)
                

            if mode.lower() == "bfd": # special handing for bfd mode. added a command for read the state table of bfd.
#                str = """
#        <command type="normal">
#                <cli>bfd_status_table (read | (write data WORD)) index WORD</cli>
#                <help>
#                    <helpInfo>Read or Write bfd status table</helpInfo>
#                    <helpInfo>Read bfd status table</helpInfo>
#                    <helpInfo>Write bfd status table</helpInfo>
#                    <helpInfo>Date : write  to bfd status table</helpInfo>
#                    <helpInfo>Date value</helpInfo>
#                    <helpInfo>index of the table</helpInfo>
#                    <helpInfo>index value</helpInfo>                    
#                </help>
#                <funcName type="user">cli_bfd_status</funcName>
#                <newMode></newMode>
#	</command>\n"""
#                f.write(str)




                if 1 == 1:                                    
                    fieldList = []                
                    fieldList.append(CField("valid", 1,  48))
                    fieldList.append(CField("even_parity1", 1,  47))
                    fieldList.append(CField("even_parity0", 1,  46))
                    fieldList.append(CField("multi_counter", 6,  40))
                    fieldList.append(CField("tx_timer_id", 3,  37))
                    fieldList.append(CField("rx_timer_id", 3,  34))
                    fieldList.append(CField("your_discriminator", 32,  2))
                    fieldList.append(CField("stat", 2, 0))
                        
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>setmem bfd_status_table index WORD (WORD | {"

            
                    for fd in range(len(fieldList)):
                        field = fieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            str += " %s WORD |" % (field._fieldName).lower()
                    str = str[:-1] # delete the "|"

                    # deal with the table which have no field
                    if len(fieldList) > 0:
                        str += "}"
                    else :
                        str = str[:-2] # delete the "| "
                        
                        
                    str += ")</cli>\n"                    
                    str += "            <help>\n"
                    str+= "                <helpInfo>Set a table value.</helpInfo>\n"                    
                    str+= "                <helpInfo>The table name.</helpInfo>\n"
                    str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                    str+= "                <helpInfo>The index vlaue you want to set.</helpInfo>\n"
                    str+= "                <helpInfo>The value set to the table</helpInfo>\n"
            
                    f.write(str)
            
                    #add more help info
                    str = ""
                    for fd in range(len(fieldList)):
                        field = fieldList[fd]
                        if field._fieldName.upper() != "RESERVED":
                            scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                            str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop                            
                            #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                    f.write(str)

                    str = "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_bfd_status_set_mem</funcName>\n"
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)


                    # add read command
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>getmem bfd_status_table index WORD </cli>\n"
                    str+= "            <help>\n"
                    str+= "                <helpInfo>Get a table value.</helpInfo>\n"
                    str+= "                <helpInfo>The table name.</helpInfo>\n"
                    str+= "                <helpInfo>The index you want to get.</helpInfo>\n"                    
                    str+= "                <helpInfo>The index value.</helpInfo>\n"
                    str+= "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_bfd_status_get_mem</funcName>\n"
                    str+= "            <newMode></newMode>\n        </command>\n"
                    f.write(str)


            # add the exit command
            
            str = """
        <command type="normal">
                <cli>exit</cli>
                <help>
                    <helpInfo>End current mode and down to previous mode</helpInfo>
                </help>
                <funcName type="user">cli_%s_exit</funcName>
                <newMode></newMode>
	</command>\n	
    </view>
</root>\n""" % mode.lower()
            f.write(str)
            f.close()





    def GenerateRegMemInterfaces(self, allObjDict):
        print "Generate the C Source Code File."
        

        f = file("reg_mem_interface.c", "w")
        f.write("\n/* THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!*/\n\n")

        f.write("#include \"table_depth.h\"\n")
        f.write("extern int reg_set(int module_id, int argc, char *args[], char *name);\n")
        f.write("extern int reg_get(int module_id, int argc, char *args[], char *name);\n")
        f.write("extern int mem_set(int module_id, int argc, char *args[], char *name, unsigned char keyType, char *type);\n")
        f.write("extern int mem_get(int module_id, int argc, char *args[], char *name, unsigned char keyType, char *type);\n\n")
        f.write("extern int mem_test(int module_id, int argc, char *args[], char *name, char *type);\n\n")
        f.write("extern int mem_i2c_test(int module_id, int argc, char *args[], char *name, char *type);\n\n")
        f.write("extern int mem_dump_or_clean(int module_id, int argc, char *args[], char *name, char *type, int depth);\n\n")
        f.write("extern int reg_test(int module_id, int argc, char *args[]);\n\n")
        f.write("extern int reg_i2c_test(int module_id, int argc, char *args[]);\n\n")
        f.write("extern int cli_clean_all_cb_reg_table(int module_id, int argc, char *args[]);\n\n")

        
        for mode in allObjDict:
            if allObjDict[mode][1][0] > 0:
                regList = allObjDict[mode][1][1]

                for reg in range(len(regList)):
                    #add set function for register
                    str = "int cli_%s_%s_set_reg(int module_id, int argc, char *args[])\n" % (mode, regList[reg]._regName)
                    str += "{\n    return reg_set(module_id, argc, args, \"%s\");\n}\n\n" % regList[reg]._regName

                    #add get function for register
                    str += "int cli_%s_%s_get_reg(int module_id, int argc, char *args[])\n" % (mode, regList[reg]._regName)
                    str += "{\n    return reg_get(module_id, argc, args, \"%s\");\n}\n\n" % regList[reg]._regName
                    f.write(str)


            table_type = self.get_table_type(mode)
            if mode in table_pool_dict:
                table_type = "TABLEPOOL"
                

            
            # START : deal with the "st_l3_defip", this is an exception, currently comment out
            if 1 == 0: #mode == "st_l3_defip":           
                memList = allObjDict[mode][2][1]

                for mem in range(len(memList)):
                    fieldInfoList = memList[mem]._regFieldList
                    
                    nKeyType = len(fieldInfoList)
                    
                    for info in fieldInfoList:                        
                        key = info[0]
                        
                        for i in range(2):                        
                            #add set function for table
                            str = "int cli_%s_%s_%s_set_mem_%s(int module_id, int argc, char *args[])\n" % (mode, memList[mem]._regName, key, i)
                            str += "{\n    return mem_set(module_id, argc, args, \"%s\", %d, \"%s\");\n}\n\n" % (memList[mem]._regName, int(key), table_type)
    
                            #add get function for table
                            str += "int cli_%s_%s_%s_get_mem_%s(int module_id, int argc, char *args[])\n" % (mode, memList[mem]._regName, key, i)
                            str += "{\n    return mem_get(module_id, argc, args, \"%s\", %d, \"%s\");\n}\n\n" % (memList[mem]._regName, int(key), table_type)
                            f.write(str)

                    break # only for data table                    
                continue

            # END : deal with the "st_l3_defip", this is an exception
            
                        
            if allObjDict[mode][2][0] > 0:
                memList = allObjDict[mode][2][1]

                for mem in range(len(memList)):

                    fieldInfoList = memList[mem]._regFieldList                    
                    nKeyType = len(fieldInfoList)
                    if nKeyType  > 1:
                        continue

                    key = "255"
                    if fieldInfoList[0][0] != "NULL":
                        key = fieldInfoList[0][0]                       

                    #add set function for table
                    str = "int cli_%s_%s_set_mem(int module_id, int argc, char *args[])\n" % (mode, memList[mem]._regName)
                    str += "{\n    return mem_set(module_id, argc, args, \"%s\", %s, \"%s\");\n}\n\n" % (memList[mem]._regName, int(key), table_type)
    
                    #add get function for table
                    str += "int cli_%s_%s_get_mem(int module_id, int argc, char *args[])\n" % (mode, memList[mem]._regName)
                    str += "{\n    return mem_get(module_id, argc, args, \"%s\", %s, \"%s\");\n}\n\n" % (memList[mem]._regName, int(key), table_type)
                    f.write(str)

                    table_type = self.get_table_type(mode)
                    if table_type in ["HASH", "TCAM"]: # only for data table when table is tcam or hash
                        break
                    

            # deal with tables which have different KeyTypes
            if allObjDict[mode][2][0] > 0:
                memList = allObjDict[mode][2][1]

                for mem in range(len(memList)):
                    fieldInfoList = memList[mem]._regFieldList
                    
                    nKeyType = len(fieldInfoList)
                    if nKeyType  == 1:
                        continue
                    
                    for info in fieldInfoList:                        
                        key = info[0]
                    
                        #print "sheet %s \n" % mode
                        #add set function for table
                        str = "int cli_%s_%s_%s_set_mem(int module_id, int argc, char *args[])\n" % (mode, memList[mem]._regName, key)
                        str += "{\n    return mem_set(module_id, argc, args, \"%s\", %d, \"%s\");\n}\n\n" % (memList[mem]._regName, int(key), table_type)
    
                        #add get function for table
                        str += "int cli_%s_%s_%s_get_mem(int module_id, int argc, char *args[])\n" % (mode, memList[mem]._regName, key)
                        str += "{\n    return mem_get(module_id, argc, args, \"%s\", %d, \"%s\");\n}\n\n" % (memList[mem]._regName, int(key), table_type)
                        f.write(str)

                    table_type = self.get_table_type(mode)
                    if table_type in ["HASH", "TCAM"]: # only for data table when table is tcam or hash
                        break


            # add test commands for test all registers
            if allObjDict[mode][1][0] > 0:                
                str = "int cli_%s_test_reg(int module_id, int argc, char *args[])\n" % (mode)
                str += "{\n    return reg_test(module_id, argc, args);\n}\n\n"

                str += "int cli_%s_i2c_test_reg(int module_id, int argc, char *args[])\n" % (mode)
                str += "{\n    return reg_i2c_test(module_id, argc, args);\n}\n\n"
                f.write(str)


            # add test commands for test all index for table also dump and clean commands
            if allObjDict[mode][2][0] > 0:
                table_type = self.get_table_type(mode)
                if mode in table_pool_dict:
                    table_type = "TABLEPOOL"

                memList = allObjDict[mode][2][1]
                for mem in range(len(memList)):
                        str = "int cli_%s_%s_test_mem(int module_id, int argc, char *args[])\n" % (mode, memList[mem]._regName)
                        str += "{\n    return mem_test(module_id, argc, args, \"%s\", \"%s\");\n}\n\n" % (memList[mem]._regName, table_type)
                        str += "int cli_%s_%s_i2c_test_mem(int module_id, int argc, char *args[])\n" % (mode, memList[mem]._regName)
                        str += "{\n    return mem_i2c_test(module_id, argc, args, \"%s\", \"%s\");\n}\n\n" % (memList[mem]._regName, table_type)
                        str += "int cli_%s_%s_dump_or_clean_mem(int module_id, int argc, char *args[])\n" % (mode, memList[mem]._regName)
                        str += "{\n    return mem_dump_or_clean(module_id, argc, args, \"%s\", \"%s\", %s);\n}\n\n" % (memList[mem]._regName, table_type, memList[mem]._table_struct_name)
                        f.write(str)


            # add clean commands for all registers and tables in cb_cfg and cb_cnt mode
            if mode.lower() in ["cb_cfg", "cb_cnt"]:
                str = "int cli_clean_all_%s_reg_table(int module_id, int argc, char *args[])\n" % (mode)
                str += "{\n    return cli_clean_all_cb_reg_table(module_id, argc, args);\n}\n\n"
                f.write(str)


        f.close()



