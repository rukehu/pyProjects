# -*- coding: utf-8 -*-

__author__ = 'LI JUN'

import os
import sys
import getopt
from csr_parse import *
import copy
import time

#from parse_main import *


multi_addr_reg_list = [
"VLAN_CTRL",
"ING_OUTER_TPID_0",
"ING_OUTER_TPID_1",
"ING_OUTER_TPID_2",
"ING_OUTER_TPID_3",
"UDF_ENABLE",
"EGR_OUTER_TPID_0",
"EGR_OUTER_TPID_1",
"EGR_OUTER_TPID_2",
"EGR_OUTER_TPID_3",
"EGR_CONFIG",
"EGR_TRILL_HEADER_ATTRIBUTES",
"ING_IPMC_SIZE",
"EGR_VLAN_CONTROL_0",
"EGR_VLAN_CONTROL_1",
"EGR_VLAN_CONTROL_2",
"EGR_VLAN_CONTROL_3",
"EGR_VLAN_CONTROL_4",
"EGR_VLAN_CONTROL_5",
"EGR_VLAN_CONTROL_6",
"EGR_VLAN_CONTROL_7",
"EGR_VLAN_CONTROL_8",
"EGR_VLAN_CONTROL_9",
"EGR_VLAN_CONTROL_10",
"EGR_VLAN_CONTROL_11",
"EGR_VLAN_CONTROL_12",
"EGR_VLAN_CONTROL_13",
"EGR_VLAN_CONTROL_14",
"EGR_VLAN_CONTROL_15",
"EGR_VLAN_CONTROL_16",
"EGR_VLAN_CONTROL_17",
"EGR_VLAN_CONTROL_18",
"EGR_VLAN_CONTROL_19",
"EGR_VLAN_CONTROL_20",
"EGR_VLAN_CONTROL_21",
"EGR_VLAN_CONTROL_22",
"EGR_VLAN_CONTROL_23",
"EGR_VLAN_CONTROL_24",
"EGR_VLAN_CONTROL_25",
"EGR_VLAN_CONTROL_26",
"EGR_VLAN_CONTROL_27",
"EGR_VLAN_CONTROL_28",
"EGR_VLAN_CONTROL_29",
"EGR_VLAN_CONTROL_30",
"EGR_VLAN_CONTROL_31",
"EGR_VLAN_CONTROL_32",
"EGR_VLAN_CONTROL_33",
"EGR_VLAN_CONTROL_34",
"EGR_VLAN_CONTROL_35",
"EGR_VLAN_CONTROL_36",
"EGR_VLAN_CONTROL_37",
"EGR_VLAN_CONTROL_38",
"EGR_VLAN_CONTROL_39",
"EGR_VLAN_CONTROL_40",
"EGR_VLAN_CONTROL_41",
"EGR_VLAN_CONTROL_42",
"EGR_VLAN_CONTROL_43",
"EGR_VLAN_CONTROL_44",
"EGR_VLAN_CONTROL_45",
"EGR_VLAN_CONTROL_46",
"EGR_VLAN_CONTROL_47",
"EGR_VLAN_CONTROL_48",
"EGR_VLAN_CONTROL_49",
"EGR_VLAN_CONTROL_50",
"EGR_VLAN_CONTROL_51",
"EGR_VLAN_CONTROL_52",
"EGR_VLAN_CONTROL_53",
"EGR_VLAN_CONTROL_54",
"EGR_VLAN_CONTROL_55",
"EGR_VLAN_CONTROL_56",
"EGR_VLAN_CONTROL_57",
"EGR_VLAN_CONTROL_58",
"EGR_VLAN_CONTROL_59",
"EGR_VLAN_CONTROL_60",
"EGR_VLAN_CONTROL_61",
"EGR_VLAN_CONTROL_62",
"EGR_VLAN_CONTROL_63",
"ING_MISC_CONFIG",
"ING_CONFIG_64",
"TOCPU_CONTROL_1",
"TOCPU_CONTROL_2",
"PD_PROBE_CONTROL",
"CHIP_GLOBAL_MODULE",
"PORT_BRIDGE_BITMAP"
]


multi_addr_tab_list = ["NONUCAST_TRUNK_BLOCK_MASK_T",
                       "VISLICE_TCAM_TABLE_M",
                       "POLICY",
                       "ESLICE_TCAM_TABLE_M",
                       "ING_L3_NEXT_HOP_T",
                       "TRUNK_BITMAP_T" ]


# below dictionary only for l2 entry and l3 entry hash table. This is special handle. Hard code. Any better solution ?
hash_key_filedList_dict_ = { "L2_ENTRY_T":["MAC_ADDR", "VLAN_ID_VFI", "KEY_TYPE", "VALID"],
                    "L3_ENTRY_IPV4_UNICAST_T":["VRF_ID", "IP_ADDR", "KEY_TYPE", "VALID"],                             
                    "L3_ENTRY_IPV6_UNICAST_T":["VRF_ID", "IP_ADDR_LWR_64", "KEY_TYPE_0", "IP_ADDR_UPR_64", "VALID_0"],                             
                    "L3_ENTRY_IPV4_MULTICAST_T":["VRF_ID", "SOURCE_IP_ADDR", "GROUP_IP_ADDR", "KEY_TYPE_0", "L3IIF_VLANID", "VALID_0"],                             
                    "L3_ENTRY_IPV6_MULTICAST_T":["VRF_ID", "GROUP_IP_ADDR_LWR_64", "KEY_TYPE_0", "GROUP_IP_ADDR_UPR_56", "SOURCE_IP_ADDR_LWR_64", "L3IIF_VLANID", "SOURCE_IP_ADDR_UPR_64", "VALID_0"]}



# below is record the table type through the table struct name, only for table stored in table pool. 
table_pool_dict = {"L2_ENTRY_T":"HASH", "L3_ENTRY_IPV4_UNICAST_T":"HASH", "L3_ENTRY_IPV6_UNICAST_T":"HASH", "L3_ENTRY_IPV4_MULTICAST_T":"HASH", "L3_ENTRY_IPV6_MULTICAST_T":"HASH",
                   "L3_DEFIP_ALPM_IPV4_T":"DIRECT", "L3_DEFIP_ALPM_IPV4_1_T":"DIRECT", "L3_DEFIP_ALPM_IPV6_64_T":"DIRECT", "L3_DEFIP_ALPM_IPV6_64_1_T":"DIRECT", "L3_DEFIP_ALPM_IPV6_128_T":"DIRECT",
                   "L3_DEFIP_ALPM_IPV6_128_1_T":"DIRECT"}


# below is record the hash and tcam tables. include the "data" sheet name and "key" sheet name. and the type of the table
# tcam_data_list = [ "my_station_data", "l3_tunnel_data_only", "l2_user_entry_data_only", "udf_offset"]
# tcam_key_list =  [ "my_station_tcam", "l3_tunnel_tcam",      "l2_user_entry_tcam",      "udf_tcam"]
# tcam_dict = {"my_station_data":"TCAM", "l3_tunnel_data_only":"TCAM", "l2_user_entry_data_only":"TCAM", "udf_offset":"TCAM", "l3_defip" : "TCAM"}
#
# hash_data_list = ["egr_vlan_xlate_data",  "vlan_xlate_data",   "mpls_entry_data", "trill_rfp_check_entry_data", "trill_forward_tree_data" ]
# hash_key_list =  ["egr_vlan_xlate",       "vlan_xlate",        "mpls_entry",      "trill_rfp_check",            "trill_forward_tree" ]
# hash_dict = {"egr_vlan_xlate_data":"HASH",  "vlan_xlate_data":"HASH", "mpls_entry_data":"HASH", "trill_rfp_check_entry_data":"HASH", "trill_forward_tree_data":"HASH"}
#

tcam_data_list = [ "VLAN_SUBNET_TCAM_DATA_ONLY_t", "l3_tunnel_data_only", "l2_user_entry_data_only", "udf_offset"]
tcam_key_list =  [ "MY_STATION_TCAM_DATA_ONLY_T", "l3_tunnel_tcam",      "l2_user_entry_tcam",      "udf_tcam"]
tcam_dict = {"p0_st_my_station_data":"TCAM", "l3_tunnel_data_only":"TCAM", "l2_user_entry_data_only":"TCAM", "udf_offset":"TCAM", "l3_defip" : "TCAM"}

hash_data_list = ["egr_vlan_xlate_data",  "vlan_xlate_data",   "mpls_entry_data", "trill_rfp_check_entry_data", "trill_forward_tree_data" ]
hash_key_list =  ["egr_vlan_xlate",       "vlan_xlate",        "mpls_entry",      "trill_rfp_check",            "trill_forward_tree" ]
hash_dict = {"egr_vlan_xlate_data":"HASH",  "vlan_xlate_data":"HASH", "mpls_entry_data":"HASH", "trill_rfp_check_entry_data":"HASH", "trill_forward_tree_data":"HASH"}




hash_tcam_data_list = hash_data_list + tcam_data_list
hash_tcam_key_list =  hash_key_list + tcam_key_list
hash_tcam_dict =dict(hash_dict.items() + tcam_dict.items())


key_type_field_info_dict = {"EGR_DVP_ATTRIBUTE_T":[46, 2],
                            "L3_DEFIP_T":[2, 2],                            
                            "EGR_L3_NEXT_HOP_T":[0, 3],
                            "ING_L3_NEXT_HOP_T":[0, 2],
                            "EGR_IP_TUNNEL_T":[0, 2],
                            "EGR_IP_TUNNEL_IPV4_T":[0, 2],
                            "EGR_IP_TUNNEL_IPV6_T":[0, 2],
                            "EGR_IP_TUNNEL_MPLS_T":[0, 2],
                            "l3_tunnel_tcam_t":[1, 1],
                            "L2_ENTRY_T":[1, 3],
                            "VLAN_MAC_T":[1, 4],
                            "POLICY":[0, 1], # need check                                                       
                            "L3_DEFIP_ONLY_T":[2, 2],                            
                            "TRILL_FORWARD_TREE_T":[1, 1],                            
                            "MPLS_ENTRY_T":[1, 3],                            
                            "EGR_VLAN_XLATE_T":[1, 3],                            
                            "VLAN_XLATE_T":[1, 4],                            
                            "VICAP_POLICY_T":[162, 2]
                            }

# hash table, data table have no key type field
no_key_type_field_info_dict = { "TRILL_FORWARD_TREE_DATA_ONLY_T":[1, 1],
                                "MPLS_ENTRY_DATA_ONLY_T":[1, 3],
                                "EGR_VLAN_XLATE_DATA_ONLY_T":[1, 3],
                                "VLAN_XLATE_DATA_ONLY_T":[1, 4]
                                }


class Soc_for_sdk_Generator():
    """Automaticly generate files, include header files and C files, also XML file."""
    def __init__(self):
        self.sameNameRegList = []
        self.sameNameTabList = []
        self.allFieldNameList= []
        
        self.max_reg_id    = 0
        self.max_table_id  = 0
        self.max_field_id  = 0
        
        self.reg_list  = []
        self.tab_list  = []

        self.reg_type_list = []
        self.tab_type_list = []

        self.physical_table_list = []


    def set_physical_table_obj(self, objList):
        self.physical_table_list = objList
        
        
    def get_table_pool_table_type(self, mode):
        if mode in table_pool_dict:
            return table_pool_dict[mode]


    def get_table_type(self, mode):
        if mode in hash_tcam_dict:
            return hash_tcam_dict[mode]
        else:
            return "DIRECT"



    def GenerateCli_Mode_Mode_H(self, allObjDict, memObjDict, soc):
        print "Generate the cli_mode.h File."

        if soc != "": # if soc not been given, we can't give the prefix for the field name
            soc = soc + "_"
            
        f = file("./tmp/cli_mode.h", 'w')
        f.write("\n//THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!\n\n")
        #f.write("extern struct cli_tree *ctree;\n")
        
        str = """\n
int32_t cli_register_mode(int32_t module_id, int32_t argc, char_t *args[])
{
	ctree->mode = REGISTER_MODE;
	setPrompt("GalaxyWind(config/register)#");
	debug(LOG, "func: cli_register_mode executed!\\n");
	return 0;
}

int32_t cli_register_exit(int32_t module_id, int32_t argc, char_t *args[])
{
	ctree->mode = CONFIG_MODE;
	setPrompt("GalaxyWind(config)#");
	debug(LOG, "func: cli_register_exit executed!\\n");
	return 0;
}

int32_t cli_table_mode(int32_t module_id, int32_t argc, char_t *args[])
{
	ctree->mode = TABLE_MODE;
	setPrompt("GalaxyWind(config/table)#");
	debug(LOG, "func: cli_table_mode executed!\\n");
	return 0;
}

int32_t cli_table_exit(int32_t module_id, int32_t argc, char_t *args[])
{
	ctree->mode = CONFIG_MODE;
	setPrompt("GalaxyWind(config)#");
	debug(LOG, "func: cli_table_exit executed!\\n");
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
int32_t cli_%s_mode(int32_t module_id, int32_t argc, char_t *args[])
{
	ctree->mode = %s_MODE;
	setPrompt("GalaxyWind(config/%s)#");
	debug(LOG, "func: cli_%s_mode executed!\\n");
	return 0;
}

int32_t cli_%s_exit(int32_t module_id, int32_t argc, char_t *args[])
{
	ctree->mode = %s;
	setPrompt("GalaxyWind(config/%s)#");
	debug(LOG, "func: cli_%s_exit executed!\\n");
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


    def GenerateRegisterXMLFile(self, allObjDict, soc): # give the register obj
        print "Generate the register.xml File."
        

        # add the new mode for registers
        f = file("./tmp/register.xml", 'w')
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
        
    def GenerateTableXMLFile(self, allObjDict, soc): # give the table obj
        print "Generate the table.xml File."
        

        # add the new mode for tables
        f = file("./tmp/table.xml", 'w')
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




        # add the update_table_pool_mode command            
        str = """
        <command type="normal">
            <cli>update_table_pool_mode</cli>
            <help>
                <helpInfo>update table pool mode</helpInfo>                
            </help>
            <funcName type="user">cli_update_table_pool_mode</funcName>
            <newMode></newMode>
        </command>\n"""
        f.write(str)


        # add the update_ipmc_size_mode command            
        str = """
        <command type="normal">
            <cli>update_ipmc_size_mode</cli>
            <help>
                <helpInfo>update ipmc size mode</helpInfo>                
            </help>
            <funcName type="user">cli_update_ipmc_size_mode</funcName>
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
            <funcName type="user">cli_clean_all_table</funcName>
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
            str = "./tmp/%s.xml" % mode.lower()
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


            self.GenerateMultiAddrRegMemXMLFile(f, allObjDict, mode)
            
            #add commands for registers
            regList = self.reg_list
            for reg in range(len(regList)):
                if regList[reg]._old_sheetName == mode:
                    if regList[reg]._regName.upper() in multi_addr_reg_list:
                        continue
                    
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>setreg %s (WORD | {" % (regList[reg]._old_regName).lower()# register name should be lower
            
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
                            str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop                            
                    f.write(str.encode("utf-8"))

                    str = "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_set_reg</funcName>\n" % (regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)



                    #add read command for register
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>getreg %s </cli>\n" % (regList[reg]._old_regName).lower()
                    str+= "            <help>\n"
                    str+= "                <helpInfo>Get a register value.</helpInfo>\n"
                    str+= "                <helpInfo>The register name.</helpInfo>\n"            
                    str+= "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_get_reg</funcName>\n" % (regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
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

            return




            # add commands for tables  
            if allObjDict[mode][2][0] > 0:
                print "Never come to here....."
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
                    print "ERROR info: st_l3_defip key type not only one...."
                    

              
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
                                str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                                
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str.encode("utf-8"))


                        str = "                <helpInfo>The data table name.</helpInfo>\n"                        
                        f.write(str)


                        str = ""
                        for fd in range(len(data_fieldList)):
                            field = data_fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str.encode("utf-8"))



                        
                        str = "                <helpInfo>The ad2 table name.</helpInfo>\n"
                        f.write(str)

                        str = ""
                        for fd in range(len(ad2_field_list)):
                            field = ad2_field_list[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str.encode("utf-8"))

                        str = "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_set_mem_%s</funcName>\n" % (regList[0]._regName, key, i)
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
                                str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                                                
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_get_mem_%s</funcName>\n" % (regList[0]._regName, key, i)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str.encode("utf-8"))
                        


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
            #if mode == "st_l3_defip":                
            #    self.GenerateRegMemXMLFile_For_TCAM_st_l3_defip(allObjDict, mode)                
            #    return
            
            # generate the commands for the current mode
            str = "./tmp/%s.xml" % mode.lower()
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


            self.GenerateMultiAddrRegMemXMLFile(f, allObjDict, mode)
            
            #add commands for registers
            regList = self.reg_list
            for reg in range(len(regList)):
                if regList[reg]._old_sheetName == mode: # so, we need change the _old_sheetName and _old_regName when "reconstruct_hash_tcam_table" function
                    if regList[reg]._regName.upper() in multi_addr_reg_list:
                        continue
                    
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>setreg %s (WORD | {" % (regList[reg]._old_regName).lower()# register name should be lower
            
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
                            str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop                            
                    f.write(str.encode("utf-8"))

                    str = "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_set_reg</funcName>\n" % (regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)



                    #add read command for register
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>getreg %s </cli>\n" % (regList[reg]._old_regName).lower()
                    str+= "            <help>\n"
                    str+= "                <helpInfo>Get a register value.</helpInfo>\n"
                    str+= "                <helpInfo>The register name.</helpInfo>\n"            
                    str+= "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_get_reg</funcName>\n" % (regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)




            # add commands for tables only have one keyType            
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1] # for hash or tcam, there are two table, key and data.          

                reg=0
                fieldInfoList = regList[reg]._regFieldList                
                nKeyType = len(fieldInfoList)
                
                table_type = self.get_table_type(mode)
                
                #if table_type == "TCAM":                    
                #    str = "        <command type=\"normal\">\n"
                #    str+= "            <cli>init_tcam</cli>\n"                    
                #    str+= "            <help>\n"
                #    str+= "                <helpInfo>initialize tcam.</helpInfo>\n"                        
                #    str+= "            </help>\n"
                #    str+= "            <funcName type=\"user\">cli_tcam_init_%s</funcName>\n" % mode
                #    str+= "            <newMode></newMode>\n        </command>\n\n"
                #    f.write(str)
                    
                if nKeyType == 1:                    

                    if table_type == "HASH":
                        index = ""
                    else:                        
                        if table_type == "TCAM":
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
                            str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                            #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                    f.write(str.encode("utf-8"))
                    


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
                            str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                            #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                    f.write(str.encode("utf-8"))
                    

                    str = "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_set_mem</funcName>\n" % (regList[0]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)



                    # add read command
                    fieldList = regList[1]._regFieldList[0][1]

                    if table_type == "HASH":
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
                        str+= "                <helpInfo>The key table name.</helpInfo>\n"                         
                        str+= "                <helpInfo>The value set to the table</helpInfo>\n"
                        f.write(str)
                    
                        str = ""
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop                            
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"

                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_get_mem</funcName>\n" % (regList[0]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str.encode("utf-8"))

                    if table_type == "TCAM":
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>getmem %s</cli>\n" % index                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Get a table value.</helpInfo>\n"                        
                        str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                        str+= "                <helpInfo>The index value.</helpInfo>\n"                        
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_get_mem</funcName>\n" % (regList[0]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)




                # add commands for tables which have different KeyTypes             
                else:                    
                    for info in fieldInfoList :
                        key = info[0]
                        data_fieldList = info[1]
                        key_type_desc = info[4]
                        
                        # find the key fileds
                        for keyTypeField in regList[1]._regFieldList:
                            if key == keyTypeField[0]:
                                key_fieldList = keyTypeField[1]
                                

                        table_type = self.get_table_type(mode)

                        if table_type == "HASH":
                            index = ""
                        else:                        
                            if table_type == "TCAM":
                                index = "index WORD"
                            else :
                                print "ERROR table type, error will happen. Please check..."

                                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>setmem "
                        str+= "%s %s %s (WORD | {" % (key, index, (regList[1]._regName).lower())

                        # print str
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
                        str+= "                <helpInfo>%s.</helpInfo>\n" % key_type_desc
                        
                        if table_type == "HASH":
                            str += ""
                        else:                        
                            if table_type == "TCAM":
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
                                str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str.encode("utf-8"))



                        str = "                <helpInfo>The data table name.</helpInfo>\n"                                               
                        str+= "                <helpInfo>The value set to the table</helpInfo>\n"
                        f.write(str)

                        str = ""
                        for fd in range(len(data_fieldList)):
                            field = data_fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str.encode("utf-8"))

                        str = "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_set_mem</funcName>\n" % (regList[0]._regName, key)
                        str+= "            <newMode></newMode>\n        </command>\n\n"
                        f.write(str)


                        if table_type == "HASH":
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
                            str+= "                <helpInfo>%s.</helpInfo>\n" % key_type_desc
                            str+= "                <helpInfo>The key table name.</helpInfo>\n"                      
                            str+= "                <helpInfo>The value set to the table</helpInfo>\n"
                            
                            
                            for fd in range(len(key_fieldList)):
                                field = key_fieldList[fd]
                                if field._fieldName.upper() != "RESERVED":
                                    scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                    str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                                    str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                                                    
                            str+= "            </help>\n"
                            str+= "            <funcName type=\"user\">cli_%s_%s_get_mem</funcName>\n" % (regList[0]._regName, key)
                            str+= "            <newMode></newMode>\n        </command>\n"
                            f.write(str.encode("utf-8"))

                        if table_type == "TCAM":
                            str = "        <command type=\"normal\">\n"            
                            str+= "            <cli>getmem %s</cli>\n" % index                        
                            str+= "            <help>\n"
                            str+= "                <helpInfo>Get a table value.</helpInfo>\n"                        
                            str+= "                <helpInfo>The index you want to set.</helpInfo>\n"
                            str+= "                <helpInfo>The index value.</helpInfo>\n"                        
                            str+= "            </help>\n"
                            str+= "            <funcName type=\"user\">cli_%s_get_mem</funcName>\n" % (regList[0]._regName)
                            str+= "            <newMode></newMode>\n        </command>\n"
                            f.write(str)



            # add mem dump and clean commands for tables
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1]
                
                for reg in range(allObjDict[mode][2][0]):
                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>mem %s (dump | clean)</cli>\n" % ((regList[reg]._regName).lower())                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Dump all valid data of the table, or clean the table.</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"
                        str+= "                <helpInfo>dump the table data</helpInfo>\n"
                        str+= "                <helpInfo>clean the table</helpInfo>\n"
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_dump_or_clean_mem</funcName>\n" % (regList[reg]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)
                        break # because this is hash or tcam         


            # add search commands for tcam tables, current, tcam only have one keyType.
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1] # for hash or tcam, there are two table, key and data.          

                reg=0
                fieldInfoList = regList[reg]._regFieldList                
                nKeyType = len(fieldInfoList)
                
                table_type = self.get_table_type(mode)

                if nKeyType == 1:                    

                    if table_type == "TCAM":                                                    
                        # add key table
                        fieldList = regList[1]._regFieldList[0][1]# + regList[1]._regFieldList[0][1]
                                                
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>search "
                        str+= "%s ({" % ((regList[1]._regName).lower())
                
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.lower().find("_mask") != -1:
                                continue
                            if field._fieldName.lower().find("invalid") != -1:
                                continue                            
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
                        str+= "                <helpInfo>Search tcam table.</helpInfo>\n" 
                        str+= "                <helpInfo>The key table name.</helpInfo>\n"                        
                        f.write(str)
                        
                        #add more help info
                        str = ""
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.lower().find("_mask") != -1:
                                continue
                            if field._fieldName.lower().find("invalid") != -1:
                                continue                             
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                
                        f.write(str.encode("utf-8"))
                  
                        str = "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_search_mem</funcName>\n" % (regList[0]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n\n"
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






    def GenerateRegMemXMLFile_For_TABLE_POOL(self, allObjDict, mode):
        print "Generate the Register related XML File For table which store in TABLE POOL."

        if 1 == 1:

            # generate the commands for the current mode
            str = "./tmp/%s.xml" % mode.lower()
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

            self.GenerateMultiAddrRegMemXMLFile(f, allObjDict, mode)

            #add commands for registers
            regList = self.reg_list
            for reg in range(len(regList)):
                if regList[reg]._old_sheetName == mode:
                    if regList[reg]._regName.upper() in multi_addr_reg_list:
                        continue
                    
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>setreg %s (WORD | {" % (regList[reg]._old_regName).lower()# register name should be lower
            
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
                            str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                                        
                    f.write(str.encode("utf-8"))

                    str = "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_set_reg</funcName>\n" % (regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)



                    #add read command for register
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>getreg %s </cli>\n" % (regList[reg]._old_regName).lower()
                    str+= "            <help>\n"
                    str+= "                <helpInfo>Get a register value.</helpInfo>\n"
                    str+= "                <helpInfo>The register name.</helpInfo>\n"            
                    str+= "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_get_reg</funcName>\n" % (regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)




            # add commands for tables only have one keyType            
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1] # for table pool, there are only one key type.          
                
                reg=0
                fieldInfoList = regList[reg]._regFieldList                
                nKeyType = len(fieldInfoList)                
                if nKeyType == 1:

                    table_type = self.get_table_pool_table_type(mode)
                    if table_type == "HASH":
                        
                        keyFiledList  = []
                        dataFiledList = []

                        fieldList = regList[0]._regFieldList[0][1]
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() in hash_key_filedList_dict_[mode]:
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
                                str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str.encode("utf-8"))
                    


                        fieldList = dataFiledList
                        str = "                <helpInfo>Set the data.</helpInfo>\n"                    
                        
                        f.write(str)
                    
                        #add more help info
                        str = ""
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                scop = "&lt;0x0-0x%x&gt;" % ((1<<field._fieldLen)-1)
                                str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str.encode("utf-8"))
                    

                        str = "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_set_mem</funcName>\n" % (regList[0]._regName)
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
                                str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str.encode("utf-8"))
                    
                        str = "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_get_mem</funcName>\n" % (regList[0]._regName)
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
                                str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str.encode("utf-8"))


                        str = "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_set_mem</funcName>\n" % (regList[0]._regName)
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
                        str+= "            <funcName type=\"user\">cli_%s_get_mem</funcName>\n" % (regList[0]._regName)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str) 



            # add mem dump and clean commands for tables
            if allObjDict[mode][2][0] > 0:
                regList = allObjDict[mode][2][1]
                
                for reg in range(allObjDict[mode][2][0]):
                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>mem %s (dump | clean)</cli>\n" % ((regList[reg]._regName).lower())                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Dump all valid data of the table, or clean the table.</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"
                        str+= "                <helpInfo>dump the table data</helpInfo>\n"
                        str+= "                <helpInfo>clean the table</helpInfo>\n"
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_dump_or_clean_mem</funcName>\n" % (regList[reg]._regName)
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


              
    def GenerateMultiAddrRegMemXMLFile(self, f, allObjDict, mode):        
                
        for item in self.sameNameRegList:
            regList = item[2]
            for reg in range(len(regList)):
                if (regList[reg]._old_sheetName == mode) and (regList[reg]._regName.upper() in multi_addr_reg_list):                    

                    #add commands for registers                             
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>setreg %s (WORD | {" % (regList[reg]._old_regName).lower()# register name should be lower
            
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
                            str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc                            
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                    f.write(str.encode("utf-8"))

                    str = "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_%s_set_reg</funcName>\n" % (mode, regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)


                    #add read command for register
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>getreg %s </cli>\n" % (regList[reg]._old_regName).lower()
                    str+= "            <help>\n"
                    str+= "                <helpInfo>Get a register value.</helpInfo>\n"
                    str+= "                <helpInfo>The register name.</helpInfo>\n"            
                    str+= "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_%s_get_reg</funcName>\n" % (mode, regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)
        

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
            str = "./tmp/%s.xml" % mode.lower()
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

            
            self.GenerateMultiAddrRegMemXMLFile(f, allObjDict, mode)
            
            #add commands for registers
            regList = self.reg_list
            for reg in range(len(regList)):
                if regList[reg]._old_sheetName == mode:
                    
                    if regList[reg]._regName.upper() in multi_addr_reg_list:
                        continue
                            
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
                    str+= "            <cli>setreg %s (WORD | {" % (regList[reg]._old_regName).lower()# register name should be lower
            
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
                            str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop
                    f.write(str.encode("utf-8"))

                    str = "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_set_reg</funcName>\n" % (regList[reg]._regName)
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
                    str+= "            <cli>getreg %s </cli>\n" % (regList[reg]._old_regName).lower()
                    str+= "            <help>\n"
                    str+= "                <helpInfo>Get a register value.</helpInfo>\n"
                    str+= "                <helpInfo>The register name.</helpInfo>\n"            
                    str+= "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_get_reg</funcName>\n" % (regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)


            # below dict for tables, which have belong to two mode.
            multi_mode_table_dict = {"storm0_cnt_t"         :"storm1_cnt_t",            "nonucast_trunk_block_mask"  :"hirar_trunktable",
                                     "fp_ing_l3_next_hop":"ing_l3_next_hop",      "efc_offset0_t"                 :"efc_offset1_t",
                                     "p0_ifc_offset_t"      :"p1_ifc_offset_t",         "trunk_bitmap"               :"hirar_strunktable",
                                     
                                     "storm1_cnt_t"         :"storm0_cnt_t",            "hirar_trunktable"              :"nonucast_trunk_block_mask",
                                     "ing_l3_next_hop"   :"fp_ing_l3_next_hop",   "efc_offset1_t"                 :"efc_offset0_t",
                                     "p1_ifc_offset_t"      :"p0_ifc_offset_t",         "hirar_strunktable"             :"trunk_bitmap"}
            


            # add commands for tables only have one keyType
            regList = self.tab_list
            for reg in range(len(regList)):

                is_multi_mode_table = 0
                #if mode in multi_mode_table_dict:                    
                #    if regList[reg]._old_sheetName.lower() == multi_mode_table_dict[mode]:
                #        is_multi_mode_table = 1                        

                if regList[reg]._old_sheetName == mode or is_multi_mode_table:
            
                    fieldInfoList = regList[reg]._regFieldList
                    nKeyType = len(fieldInfoList)
                    if nKeyType > 1:
                        continue
                    
                    #print "%s %s %s" % (regList[reg]._excelName, regList[reg]._sheetName, regList[reg]._regName)
                    
                    fieldList = regList[reg]._regFieldList[0][1]
                        
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>setmem  %s index WORD (WORD | {" % (regList[reg]._regName).lower()

            
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
                            str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop                            
                            #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                    f.write(str.encode("utf-8"))

                    str = "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_set_mem</funcName>\n" % (regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n\n"
                    f.write(str)


                    # add read command
                    str = "        <command type=\"normal\">\n"            
                    str+= "            <cli>getmem %s index WORD </cli>\n" % (regList[reg]._regName).lower()
                    str+= "            <help>\n"
                    str+= "                <helpInfo>Get a table value.</helpInfo>\n"
                    str+= "                <helpInfo>The table name.</helpInfo>\n"
                    str+= "                <helpInfo>The index you want to get.</helpInfo>\n"
                    str+= "                <helpInfo>The index value.</helpInfo>\n"
                    str+= "            </help>\n"
                    str+= "            <funcName type=\"user\">cli_%s_get_mem</funcName>\n" % (regList[reg]._regName)
                    str+= "            <newMode></newMode>\n        </command>\n"
                    f.write(str)                                                        
                        

            # add commands for tables which have different KeyTypes
            regList = self.tab_list
            for reg in range(len(regList)):
                
                is_multi_mode_table = 0
                #if mode in multi_mode_table_dict:                    
                #    if regList[reg]._old_sheetName.lower() == multi_mode_table_dict[mode]:
                #        is_multi_mode_table = 1
                                                
                if regList[reg]._old_sheetName == mode or is_multi_mode_table:
            
                    fieldInfoList = regList[reg]._regFieldList
                    nKeyType = len(fieldInfoList)

                    if nKeyType  == 1:
                        continue                    
                    
                    for info in fieldInfoList :
                        key = info[0]
                        fieldList = info[1]
                        key_type_desc = info[4]                        
                                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>setmem %s %s index WORD (WORD | {" % ((regList[reg]._regName).lower(), key)


            
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.upper() != "RESERVED":
                                str += " %s WORD |" % (field._fieldName).lower()
                        str = str[:-1]
    
                        str += "})</cli>\n"
                        
                        str += "            <help>\n"
                        str+= "                <helpInfo>Set a table value.</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"                        
                        str+= "                <helpInfo>%s.</helpInfo>\n" % key_type_desc
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
                                str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                                str+= "                <helpInfo>value %s</helpInfo>\n" % scop                                
                                #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                                #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                        f.write(str.encode("utf-8"))

                        str = "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_set_mem</funcName>\n" % (regList[reg]._regName, key)
                        str+= "            <newMode></newMode>\n        </command>\n\n"
                        f.write(str)





                        # add read command
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>getmem %s %s index WORD </cli>\n" % ((regList[reg]._regName).lower(), key)
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Get a table value.</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"                        
                        str+= "                <helpInfo>%s.</helpInfo>\n" % key_type_desc
                        str+= "                <helpInfo>The index you want to get.</helpInfo>\n"                        
                        str+= "                <helpInfo>The index value.</helpInfo>\n"
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_%s_get_mem</funcName>\n" % (regList[reg]._regName, key)
                        str+= "            <newMode></newMode>\n        </command>\n"
                        f.write(str)


                                

            # add mem dump and clean commands for tables
            regList = self.tab_list
            for reg in range(len(regList)):

                is_multi_mode_table = 0
                #if mode in multi_mode_table_dict:                    
                #    if regList[reg]._old_sheetName.lower() == multi_mode_table_dict[mode]:
                #        is_multi_mode_table = 1                        

                if regList[reg]._old_sheetName == mode or is_multi_mode_table:
                        
                        str = "        <command type=\"normal\">\n"            
                        str+= "            <cli>mem %s (dump | clean) { (index WORD) |}</cli>\n" % ((regList[reg]._regName).lower())                        
                        str+= "            <help>\n"
                        str+= "                <helpInfo>Dump all valid data of the table, or clean the table.</helpInfo>\n"
                        str+= "                <helpInfo>The table name.</helpInfo>\n"
                        str+= "                <helpInfo>dump the table data</helpInfo>\n"
                        str+= "                <helpInfo>clean the table</helpInfo>\n"                        
                        str+= "                <helpInfo>Specify the index scope of the table.</helpInfo>\n"
                        str+= "                <helpInfo>index like 0:50.</helpInfo>\n"                        
                        str+= "            </help>\n"
                        str+= "            <funcName type=\"user\">cli_%s_dump_or_clean_mem</funcName>\n" % (regList[reg]._regName)
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
                            str+= """                <helpInfo>%s</helpInfo>\n""" % field._desc
                            str+= "                <helpInfo>value %s</helpInfo>\n" % scop                            
                            #str+= "                <helpInfo>The Field name.</helpInfo>\n"
                            #str+= "                <helpInfo>The value set to the field</helpInfo>\n"
                    f.write(str.encode("utf-8"))

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



            
    def GenerateMultiAddrRegMemInterfaces(self, f, allObjDict, mode):
        
        for item in self.sameNameRegList:
            regList = item[2]
            for reg in range(len(regList)):
                if (regList[reg]._old_sheetName == mode) and (regList[reg]._regName.upper() in multi_addr_reg_list):                    

                    #add set function for register
                    str = "int32_t cli_%s_%s_set_reg(int32_t module_id, int32_t argc, char_t *args[])\n" % (mode, regList[reg]._regName)
                    str += "{\n    return cli_reg_set(module_id, argc, args, \"%s\", %sr);\n}\n\n" % (regList[reg]._regName, regList[reg]._regName.upper())

                    #add get function for register
                    str += "int32_t cli_%s_%s_get_reg(int32_t module_id, int32_t argc, char_t *args[])\n" % (mode, regList[reg]._regName)
                    str += "{\n    return cli_reg_get(module_id, argc, args, \"%s\", %sr);\n}\n\n" % (regList[reg]._regName, regList[reg]._regName.upper())
                    f.write(str)

                    

    def GenerateRegMemInterfaces(self, allObjDict):
        print "Generate the C Source Code File."
        
        f = file("./tmp/reg_mem_interface.c", "w")        
        
        f.write("\n/* THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!*/\n\n")

        f.write("#include \"soc/soc_ctrl.h\"\n")
        f.write("#include \"sal/sal_core.h\"\n")
        
        f.write("extern int32_t cli_reg_set(int32_t module_id, int32_t argc, char_t *args[], char_t *name, int32_t id);\n")
        f.write("extern int32_t cli_reg_get(int32_t module_id, int32_t argc, char_t *args[], char_t *name, int32_t id);\n")
        f.write("extern int32_t cli_mem_set(int32_t module_id, int32_t argc, char_t *args[], char_t *name, uint8_t keyType, char_t *type, int32_t id, int32_t id_key);\n")
        f.write("extern int32_t cli_mem_get(int32_t module_id, int32_t argc, char_t *args[], char_t *name, uint8_t keyType, char_t *type, int32_t id, int32_t id_key);\n\n")
        f.write("extern int32_t cli_mem_dump_or_clean(int32_t module_id, int32_t argc, char_t *args[], char_t *name, char_t *type, int32_t data_id, int32_t key_id);\n\n")
        f.write("extern int32_t cli_clean_all_cb_reg_table(int32_t module_id, int32_t argc, char_t *args[]);\n\n")
        f.write("extern int32_t cli_tcam_search(int32_t module_id, int32_t argc, char_t *args[], char_t *name, uint8_t keyType, char_t *type, int32_t data_id, int32_t key_id);\n\n")
        
        for mode in allObjDict:
            
            if mode in table_pool_dict:
                continue

            self.GenerateMultiAddrRegMemInterfaces(f, allObjDict, mode) # add the multi-addr register in the mode
            
            regList = self.reg_list
            for reg in range(len(regList)):
                if regList[reg]._old_sheetName == mode:
                    if regList[reg]._regName.upper() in multi_addr_reg_list:
                        continue

                    reg_name = regList[reg]._regName                        
                        
                    #add set function for register
                    str = "int32_t cli_%s_set_reg(int32_t module_id, int32_t argc, char_t *args[])\n" % (reg_name)
                    str += "{\n    return cli_reg_set(module_id, argc, args, \"%s\", %sr);\n}\n\n" % (reg_name, reg_name.upper())

                    #add get function for register
                    str += "int32_t cli_%s_get_reg(int32_t module_id, int32_t argc, char_t *args[])\n" % (reg_name)
                    str += "{\n    return cli_reg_get(module_id, argc, args, \"%s\", %sr);\n}\n\n" % (reg_name, reg_name.upper())
                    f.write(str)


        # below is only for table pool registers
        for mode in allObjDict:
            if mode not in table_pool_dict:
                continue
            
            self.GenerateMultiAddrRegMemInterfaces(f, allObjDict, mode) # add the multi-addr register in the mode
            
            regList = self.reg_list
            for reg in range(len(regList)):
                if regList[reg]._old_sheetName == mode:
                    if regList[reg]._regName.upper() in multi_addr_reg_list:
                        continue

                    reg_name =  regList[reg]._regName                
                        
                    #add set function for register
                    str = "int32_t cli_%s_set_reg(int32_t module_id, int32_t argc, char_t *args[])\n" % (regList[reg]._regName)
                    str += "{\n    return cli_reg_set(module_id, argc, args, \"%s\", %sr);\n}\n\n" % (regList[reg]._regName, "TABLEPOOL_" + regList[reg]._old_regName.upper())

                    #add get function for register
                    str += "int32_t cli_%s_get_reg(int32_t module_id, int32_t argc, char_t *args[])\n" % (regList[reg]._regName)
                    str += "{\n    return cli_reg_get(module_id, argc, args, \"%s\", %sr);\n}\n\n" % (regList[reg]._regName, "TABLEPOOL_" + regList[reg]._old_regName.upper())
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
                            str = "int32_t cli_%s_%s_set_mem_%s(int32_t module_id, int32_t argc, char_t *args[])\n" % (memList[mem]._regName, key, i)
                            str += "{\n    return cli_mem_set(module_id, argc, args, \"%s\", %d, \"%s\");\n}\n\n" % (memList[mem]._regName, int(key), table_type)
    
                            #add get function for table
                            str += "int32_t cli_%s_%s_get_mem_%s(int32_t module_id, int32_t argc, char_t *args[])\n" % (memList[mem]._regName, key, i)
                            str += "{\n    return cli_mem_get(module_id, argc, args, \"%s\", %d, \"%s\");\n}\n\n" % (memList[mem]._regName, int(key), table_type)
                            f.write(str)

                    break # only for data table                    
                continue

            # END : deal with the "st_l3_defip", this is an exception
            
        iterated_list = []
        for mode in allObjDict:
                
            if allObjDict[mode][2][0] > 0:
                memList = allObjDict[mode][2][1]

                for mem in range(len(memList)):

                    if memList[mem]._regName.upper() in iterated_list:  
                        continue                    
                    iterated_list.append(memList[mem]._regName.upper())
                    

                    fieldInfoList = memList[mem]._regFieldList                    
                    nKeyType = len(fieldInfoList)
                    if nKeyType  > 1:
                        continue

                    key = "0"
                    if fieldInfoList[0][0] != "NULL":
                        key = fieldInfoList[0][0]                       


                    key_table_struct = '0'
                    table_type = self.get_table_type(mode)
                    if table_type in ["HASH", "TCAM"]:
                        key_table_struct = memList[1]._table_struct_name.upper() + "m"

                    if mode in table_pool_dict:
                        table_type = "TABLEPOOL"

                    #add set function for table
                    str = "int32_t cli_%s_set_mem(int32_t module_id, int32_t argc, char_t *args[])\n" % (memList[mem]._regName)
                    str += "{\n    return cli_mem_set(module_id, argc, args, \"%s\", %s, \"%s\", %sm, %s);\n}\n\n" % (memList[mem]._regName, int(key), table_type, memList[mem]._table_struct_name.upper(), key_table_struct)
    
                    #add get function for table
                    str += "int32_t cli_%s_get_mem(int32_t module_id, int32_t argc, char_t *args[])\n" % (memList[mem]._regName)
                    str += "{\n    return cli_mem_get(module_id, argc, args, \"%s\", %s, \"%s\", %sm, %s);\n}\n\n" % (memList[mem]._regName, int(key), table_type, memList[mem]._table_struct_name.upper(), key_table_struct)
                    f.write(str)

                    table_type = self.get_table_type(mode)
                    if table_type in ["HASH", "TCAM"]: # only for data table when table is tcam or hash
                        break

                    
        iterated_list = []
        for mode in allObjDict:
                
            # deal with tables which have different KeyTypes
            if allObjDict[mode][2][0] > 0:
                memList = allObjDict[mode][2][1]

                for mem in range(len(memList)):

                    if memList[mem]._regName.upper() in iterated_list:  
                        continue                    
                    iterated_list.append(memList[mem]._regName.upper())
                    
                    
                    fieldInfoList = memList[mem]._regFieldList
                    
                    nKeyType = len(fieldInfoList)
                    if nKeyType  == 1:
                        continue

                    key_table_struct = '0'
                    table_type = self.get_table_type(mode)
                    if table_type in ["HASH", "TCAM"]:
                        key_table_struct = memList[1]._table_struct_name.upper() + "m"
                        
                    if mode in table_pool_dict:
                        table_type = "TABLEPOOL"
                    
                    for info in fieldInfoList:                        
                        key = info[0]
                        
                        print "sheet %s key= %s\n" % (mode, key)
                        #add set function for table
                        str = "int32_t cli_%s_%s_set_mem(int32_t module_id, int32_t argc, char_t *args[])\n" % (memList[mem]._regName, key)
                        str += "{\n    return cli_mem_set(module_id, argc, args, \"%s\", %d, \"%s\", %sm, %s);\n}\n\n" % (memList[mem]._regName, int(key), table_type, memList[mem]._table_struct_name.upper(), key_table_struct)
    
                        #add get function for table
                        str += "int32_t cli_%s_%s_get_mem(int32_t module_id, int32_t argc, char_t *args[])\n" % (memList[mem]._regName, key)
                        str += "{\n    return cli_mem_get(module_id, argc, args, \"%s\", %d, \"%s\", %sm, %s);\n}\n\n" % (memList[mem]._regName, int(key), table_type, memList[mem]._table_struct_name.upper(), key_table_struct)
                        f.write(str)

                    table_type = self.get_table_type(mode)
                    if table_type in ["HASH", "TCAM"]: # only for data table when table is tcam or hash
                        break

        iterated_list = []
        for mode in allObjDict:
            
            # add dump and clean commands
            if allObjDict[mode][2][0] > 0:

                memList = allObjDict[mode][2][1]
                for mem in range(len(memList)):

                    if memList[mem]._regName.upper() in iterated_list:  
                        continue                    
                    iterated_list.append(memList[mem]._regName.upper())


                    key_table_struct = '0'
                    table_type = self.get_table_type(mode)
                    if table_type in ["HASH", "TCAM"]:
                        key_table_struct = memList[1]._table_struct_name.upper() + "m"


                    if mode in table_pool_dict:
                        table_type = "TABLEPOOL"                        
                                        
                    str = "int32_t cli_%s_dump_or_clean_mem(int32_t module_id, int32_t argc, char_t *args[])\n" % (memList[mem]._regName)
                    str += "{\n    return cli_mem_dump_or_clean(module_id, argc, args, \"%s\", \"%s\", %sm, %s);\n}\n\n" % (memList[mem]._regName, table_type, memList[mem]._table_struct_name, key_table_struct)
                    f.write(str)

                    # for tcam search
                    if table_type == "TCAM":
                        str = "int32_t cli_%s_search_mem(int32_t module_id, int32_t argc, char_t *args[])\n" % (memList[mem]._regName)
                        str += "{\n    return cli_tcam_search(module_id, argc, args, \"%s\", 0, \"%s\", %sm, %s);\n}\n\n" % (memList[mem]._regName, table_type, memList[mem]._table_struct_name, key_table_struct)
                        f.write(str)

                    table_type = self.get_table_type(mode)
                    if table_type in ["HASH", "TCAM"]: # only for data table when table is tcam or hash
                        break
                    
            # add clean commands for all registers and tables in cb_cfg and cb_cnt mode
            if mode.lower() in ["cb_cfg", "cb_cnt"]:
                str = "int32_t cli_clean_all_%s_reg_table(int32_t module_id, int32_t argc, char_t *args[])\n" % (mode)
                str += "{\n    return cli_clean_all_cb_reg_table(module_id, argc, args);\n}\n\n"
                f.write(str)


        f.close()




##########################################################################################################################################################################################################

    def GenerateSocXMLFile(self, allObjDict, soc): # such as es1000.xml and es2000.xml

        print "GenerateSocXMLFile"
        
        f = file("./tmp/%s.xml" % soc, 'w')
        str = """<?xml version="1.0" encoding="utf-8"?>
<!--
	Description:
                THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANUALLY!!!
-->

<root>
	<view name="%s_MODE">\n""" % soc.upper()
        f.write(str)

	str = """	
		<command type="normal">
			<cli>table</cli>
			<help>
				<helpInfo>Access table</helpInfo>
				<helpInfo>Table Mode</helpInfo>
			</help>
			<funcName type="user">cli_%s_table_mode</funcName>
			<newMode>%s_TABLE</newMode>
		</command>
		
		<command type="normal">
			<cli>register</cli>
			<help>
				<helpInfo>Access register</helpInfo>
				<helpInfo>Register Mode</helpInfo>
			</help>
			<funcName type="user">cli_%s_register_mode</funcName>
			<newMode>%s_REGISTER</newMode>
		</command>

		<!--exit -->
		<command type="normal">
			<cli>exit</cli>
			<help>
				<helpInfo>End current mode and down to previous mode</helpInfo>
			</help>
			<funcName type="user">cli_%s_exit</funcName>
			<newMode></newMode>
		</command>
		
	</view>
</root>""" % (soc, soc.upper(), soc, soc.upper(), soc)

        f.write(str)
       
        f.close()



#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################


    def if_the_table_need_expand_name(self, name):
        
        (sameNameRegModeList, same_name_reg_list) = self.is_in_sameNameTabList(name)

        if sameNameRegModeList != []: 
            if name.upper() in multi_addr_tab_list: # no expand, multi-addr                            
                return 0
            else: # expand                        
                return 1
            
        else: # single addr, no expand
            return 0





    def get_field_varible_type(self, field):
        num = ""
        varible_type = "uint8_t"
        
        if field._fieldLen <= 8 :
            varible_type = "uint8_t "
            string = "8"
        if field._fieldLen > 8 :
            varible_type = "uint16_t "
            string = "16"
        if field._fieldLen > 16 :
            varible_type = "uint32_t "
            string = "32"
        if field._fieldLen > 32 :
            varible_type = "uint64_t "
            string = "64"

        return (varible_type, num, string)  # ignore all field length more than  64 bits


    
        if field._fieldLen > 64 :
            #print "%s  %d " % (field._fieldName, field._fieldLen )
            varible_type = "uint64_t "
            num          = "[2]"
            string = "64"
        if field._fieldLen > 128 :
            varible_type = "uint64_t "
            num          = "[3]"
            string = "64"
        if field._fieldLen > 192 :
            varible_type = "uint64_t "
            num          = "[4]"
            string = "64"
        if field._fieldLen > 256 :
            varible_type = "uint64_t "
            num          = "[5]"
            string = "64"
        if field._fieldLen > 320 :
            varible_type = "// too long ##############################// "
            print "len = %d  --->  %s " % (field._fieldLen, varible_type)
            varible_type = "char_t * "
            string = "64"

        return (varible_type, num, string)


    def if_the_reg_of_the_mode_already_in_the_list(self, name, mode, reg_list):
        for item in reg_list:
            # reg original name and the old (original) sheet name should be same
            if name == item[0] and mode == item[1]:
                return 1
        return 0                





                       



    def GenerateRegStruct(self, f, objDict, soc):
        
        f.write("\n//THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANUALLY!!!\n\n")

        multi_macro_reg_list = []
        regList = self.reg_list
        for reg in range(len(regList)):
            if regList[reg]._modeName in table_pool_dict:
                continue

            if regList[reg]._nMacro > 1 and self.is_in_table_excel(regList[reg]._excelName) == 0:
                
                if self.if_the_reg_of_the_mode_already_in_the_list(regList[reg]._original_regName, regList[reg]._old_sheetName, multi_macro_reg_list) == 1:
                    continue                
                multi_macro_reg_list.append([regList[reg]._original_regName, regList[reg]._old_sheetName])
                
                reg_name = regList[reg]._original_regName.lower()

            else: 
                reg_name = regList[reg]._regName.lower()

            # ignore the reg which have only one field
            if len(regList[reg]._regFieldList) == 1 and (regList[reg]._regName.upper() not in multi_addr_reg_list):
                continue

            # ignore the reg which _old_sheetName is MAC_COUNTER
            if regList[reg]._old_sheetName == "MAC_COUNTER":                
                continue
            
            fieldList = regList[reg]._regFieldList
            f.write("typedef struct soc_groot_%s_s \n{\n" %(reg_name))
                    
            for fd in range(len(fieldList)):
                field = fieldList[fd]
                if field.fieldName.upper() == "RESERVED":
                    continue
                                                
                (varible_type, num, type_) = self.get_field_varible_type(field)                            
                            
                f.write("    %-10s %s%s; /* %dbit */\n" % (varible_type, field._fieldName.lower(), num, field._fieldLen))

            f.write("}soc_groot_%s_t;\n\n" % reg_name)



        table_pool_reg_list = []
        for reg in range(len(regList)):
            if regList[reg]._modeName not in table_pool_dict:
                continue

            if regList[reg]._modeName in table_pool_dict:

                if regList[reg]._original_regName.upper() in table_pool_reg_list:
                    continue
                table_pool_reg_list.append(regList[reg]._original_regName.upper())

                #reg_name = "TABLEPOOL_" + regList[reg]._old_regName.upper()
                reg_struct_name = "TABLEPOOL_" + regList[reg]._original_regName.upper()

            # ignore the reg which have only one field
            if len(regList[reg]._regFieldList) == 1:
                continue
            
            fieldList = regList[reg]._regFieldList
            f.write("typedef struct soc_groot_%s_s \n{\n" %(reg_struct_name.lower()))
                    
            for fd in range(len(fieldList)):
                field = fieldList[fd]
                if field.fieldName.upper() == "RESERVED":
                    continue
                                                
                (varible_type, num, type_) = self.get_field_varible_type(field)                            
                            
                f.write("    %-10s %s%s; /* %dbit */\n" % (varible_type, field._fieldName.lower(), num, field._fieldLen))

            f.write("}soc_groot_%s_t;\n\n" % reg_struct_name.lower())



        multi_macro_reg_list = []
        regList = self.reg_list
        for reg in range(len(regList)):

            if regList[reg]._modeName in table_pool_dict:
                continue

            if regList[reg]._nMacro > 1 and self.is_in_table_excel(regList[reg]._excelName) == 0:               
                reg_name = regList[reg]._original_regName.lower()
                
            else :
                reg_name = regList[reg]._regName.lower()

            # ignore the reg which have only one field
            if len(regList[reg]._regFieldList) == 1:
                continue

            # ignore the reg which _old_sheetName is MAC_COUNTER
            if regList[reg]._old_sheetName == "MAC_COUNTER":                
                continue
            
            str  = "sf_status_t soc_groot_set_%s_reg(uint32_t chip_id, soc_groot_%s_t *reg);\n" % (regList[reg]._regName.lower(), reg_name)
            str += "sf_status_t soc_groot_get_%s_reg(uint32_t chip_id, soc_groot_%s_t *reg);\n" % (regList[reg]._regName.lower(), reg_name)
            f.write(str)


        table_pool_reg_list = []
        for reg in range(len(regList)):

            if regList[reg]._modeName not in table_pool_dict:
                continue

            if regList[reg]._modeName in table_pool_dict:

                if regList[reg]._old_regName.upper() in table_pool_reg_list:
                    continue
                table_pool_reg_list.append(regList[reg]._old_regName.upper())
                
                reg_name = "TABLEPOOL_" + regList[reg]._old_regName.upper()
                reg_struct_name = "TABLEPOOL_" + regList[reg]._original_regName.upper()
                                
            # ignore the reg which have only one field
            if len(regList[reg]._regFieldList) == 1:
                continue
            
            str  = "sf_status_t soc_groot_set_%s_reg(uint32_t chip_id, soc_groot_%s_t *reg);\n" % (reg_name.lower(), reg_struct_name.lower())
            str += "sf_status_t soc_groot_get_%s_reg(uint32_t chip_id, soc_groot_%s_t *reg);\n" % (reg_name.lower(), reg_struct_name.lower())
            f.write(str)

                   

    def GenerateDirectTabStruct(self, f, objDict, soc):

        f.write("\n//THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANUALLY!!!\n\n")
        
        # special added
        f.write("#define L3_DEFIP_IPV4_32_T     0\n")
        f.write("#define L3_DEFIP_IPV6_64_T     1\n")
        f.write("#define L3_DEFIP_IPV6_128_T    3\n\n")
       
        regList = []

        table_struct = []
        
        for mode in objDict:                                       
            
            # hash or tcam
            table_type = self.get_table_type(mode)
            if table_type in ["HASH", "TCAM"]:
                print "########### hash_tcam %s" % mode
                continue

            # if table pool
            if mode in table_pool_dict:
                #print "////////////////////////////////////////////////table pool %s" % mode
                continue

            # common direct table
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]
                
                for reg in range(len(regList)):

                    if regList[reg]._table_struct_name.lower() in table_struct:
                        continue            
                    table_struct.append(regList[reg]._table_struct_name.lower())
                
                                        
                    fieldInfoList = regList[reg]._regFieldList
                    nKeyType = len(fieldInfoList)

                    f.write("/* MODE \"%s\" */\n" % mode.upper())

                    if nKeyType > 1: # have more than one key type
                        for info in fieldInfoList :
                            key = info[0]
                            fieldList = info[1]
                            key_name = info[4] # we need key name
                                                                 
                            f.write("typedef struct soc_groot_%s_s \n{\n" %(key_name.lower()))
                    
                            for fd in range(len(fieldList)):
                                field = fieldList[fd]
                                if field.fieldName.upper() == "RESERVED":
                                    continue

                                (varible_type, num, type_) = self.get_field_varible_type(field)                                
                                f.write("    %-10s %s%s; /* %dbit */\n" % (varible_type, field._fieldName.lower(), num, field._fieldLen))

                            f.write("}soc_groot_%s_t;\n\n" % (key_name.lower()))
                            

                        # below code: define the table struct include above struct.

                        f.write("typedef struct soc_groot_%s_s \n{\n" %(regList[reg]._table_struct_name.lower().lower()))
                        # add the entry_type
                        f.write("    %-10s %s%s; /* %dbit */\n" % ("uint8_t", "entry_type", "", 8))
                        f.write("    %-10s soc_groot_%s_union\n" % ("union", regList[reg]._table_struct_name.lower()))
                        f.write("    {\n")
                        
                        for info in fieldInfoList :
                            key = info[0]
                            key_name = info[4] # we need key name                            
                            f.write("        soc_groot_%s_t %s_entry;\n" % (key_name.lower(), key_name.lower()))

                        f.write("    }ent;\n")

                        f.write("}soc_groot_%s_t;\n\n" % (regList[reg]._table_struct_name.lower()))

                        # define the macro for the table for different key type.
                        for info in fieldInfoList :
                            key = info[0]                            
                            key_name = info[4] # we need key name                            
                            f.write("#define SOC_%s_T %s\n" % (key_name.upper(), key))

                        f.write("\n\n")

                        
                    else: # only have one key type
                        fieldList = regList[reg]._regFieldList[0][1]                                        
                        f.write("typedef struct soc_groot_%s_s \n{\n" %(regList[reg]._table_struct_name.lower()))
                    
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field.fieldName.upper() == "RESERVED":
                                continue

                            (varible_type, num, type_) = self.get_field_varible_type(field)                                
                            f.write("    %-10s %s%s; /* %dbit */\n" % (varible_type, field._fieldName.lower(), num, field._fieldLen))

                        f.write("}soc_groot_%s_t;\n\n" % regList[reg]._table_struct_name.lower())


        table_struct = []
        for mode in objDict:                                       
            
            # hash or tcam
            table_type = self.get_table_type(mode)
            if table_type in ["HASH", "TCAM"]:
                #print "########### hash_tcam %s" % mode
                continue

            # if table pool
            if mode in table_pool_dict:
                #print "////////////////////////////////////////////////table pool %s" % mode
                continue

            # common direct table
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]                
                
                for reg in range(len(regList)):

                    if regList[reg]._table_struct_name.lower() in table_struct:
                        continue            
                    table_struct.append(regList[reg]._table_struct_name.lower())

                    f.write("/* MODE \"%s\" */\n" % mode.upper())
                    # functions declaration
                    str  = "sf_status_t soc_groot_set_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry);\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())                        
                    str += "sf_status_t soc_groot_get_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry);\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())
                    str += "sf_status_t soc_groot_mem_array_set_%s(uint32_t chip_id, uint32_t index_min, uint32_t index_max, soc_groot_%s_t *entry);\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())
                    str += "sf_status_t soc_groot_mem_array_get_%s(uint32_t chip_id, uint32_t index_min, uint32_t index_max, soc_groot_%s_t *entry);\n\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())
                    f.write(str)



    # define the struct for each table
    def GenerateHashTcamTabStruct(self, f, objDict, soc):
        
        f.write("\n//THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANUALLY!!!\n\n")

        regList = []
        table_struct = []
        #print "......GenerateHashTcamTabStruct......\n"
        for mode in objDict:                        
            #print "enter table_type\n"
            # hash or tcam
            
            table_type = self.get_table_type(mode)
            #print "GenerateHashTcamTabStruct   table_type: ", table_type
            if table_type in ["HASH", "TCAM"]: # only for data table when table is tcam or hash           
    
                if objDict[mode][2][0] > 0:
                    regList = objDict[mode][2][1]

                    if regList[0]._table_struct_name.lower() in table_struct:
                        continue
                    table_struct.append(regList[0]._table_struct_name.lower()) 

                    
                    fieldInfoList = regList[0]._regFieldList                
                    nKeyType = len(fieldInfoList)

                    dataFieldList = []
                    keyFieldList  = []
                       
                    f.write("/* MODE \"%s\" */\n" % mode.upper())

                    if nKeyType > 1: # have more than one key type
                        
                        for info in fieldInfoList :
                            key = info[0]
                            dataFieldList = info[1]
                            key_name = info[4]
                            
                            # find the key fileds
                            for keyTypeField in regList[1]._regFieldList:
                                if key == keyTypeField[0]:
                                    keyFieldList = keyTypeField[1]
                            
                            fieldList = keyFieldList + dataFieldList                                      
                            f.write("typedef struct soc_groot_%s_s \n{\n" %(key_name.lower()))
                            f.write("    /* key table */\n")
                    
                            for fd in range(len(fieldList)):
                                if fd == len(keyFieldList):
                                    f.write("\n    /* data table */\n")
                                
                                field = fieldList[fd]
                                if field.fieldName.upper() == "RESERVED":
                                    continue

                                (varible_type, num, type_) = self.get_field_varible_type(field)                                    
                                f.write("    %-10s %s%s; /* %dbit */\n" % (varible_type, field._fieldName.lower(), num, field._fieldLen))

                            f.write("}soc_groot_%s_t;\n\n" % (key_name.lower()))
                            

                        # below code: define the table struct include above struct.

                        f.write("typedef struct soc_groot_%s_s \n{\n" %(regList[1]._table_struct_name.lower()))
                        # add the entry_type
                        f.write("    %-10s %s%s; /* %dbit */\n" % ("uint8_t", "entry_type", "", 8))
                        f.write("    %-10s soc_groot_%s_union\n" % ("union", regList[1]._table_struct_name.lower()))
                        f.write("    {\n")
                        
                        for info in fieldInfoList :
                            key = info[0]
                            key_name = info[4]
                            
                            f.write("        soc_groot_%s_t %s_entry;\n" % (key_name.lower(), key_name.lower()))

                        f.write("    }ent;\n")

                        f.write("}soc_groot_%s_t;\n\n" % (regList[1]._table_struct_name.lower()))

                        # define the macro for the table for different key type.
                        for info in fieldInfoList :
                            key = info[0]
                            key_name = info[4]
                            f.write("#define SOC_%s_T %s\n" % (key_name.upper(), key))

                        f.write("\n\n")

                        
                    else: # only have one key type

                        # set key table and data table
                        dataFieldList = regList[0]._regFieldList[0][1]
                        keyFieldList  = regList[1]._regFieldList[0][1]  

                        fieldList = keyFieldList + dataFieldList                 
                        f.write("typedef struct soc_groot_%s_s \n{\n" %(regList[1]._table_struct_name.lower()))
                        f.write("    /* key table */\n")
                        
                        for fd in range(len(fieldList)):
                            if fd == len(keyFieldList):
                                f.write("\n    /* data table */\n")
                                
                            field = fieldList[fd]
                            if field.fieldName.upper() == "RESERVED":
                                continue

                            (varible_type, num, type_) = self.get_field_varible_type(field)                                
                            f.write("    %-10s %s%s; /* %dbit */\n" % (varible_type, field._fieldName.lower(), num, field._fieldLen))

                        f.write("}soc_groot_%s_t;\n\n" % regList[1]._table_struct_name.lower())

                    
        table_struct = []
        for mode in objDict:            

            # hash or tcam
            table_type = self.get_table_type(mode)
            if table_type in ["HASH", "TCAM"]: # only for data table when table is tcam or hash                           

                if objDict[mode][2][0] > 0:
                    regList = objDict[mode][2][1]

                    if regList[0]._table_struct_name.lower() in table_struct:
                        continue
                    table_struct.append(regList[0]._table_struct_name.lower()) 

                    f.write("/* MODE \"%s\" */\n" % mode.upper())
                    if table_type == "HASH":
                        str  = "sf_status_t soc_groot_set_%s(uint32_t chip_id, soc_groot_%s_t *entry);\n" % (regList[1]._table_struct_name.lower(), regList[1]._table_struct_name.lower())                        
                        str += "sf_status_t soc_groot_get_%s(uint32_t chip_id, soc_groot_%s_t *entry);\n\n" % (regList[1]._table_struct_name.lower(), regList[1]._table_struct_name.lower())
                    else :
                        str  = "sf_status_t soc_groot_set_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry);\n" % (regList[1]._table_struct_name.lower(), regList[1]._table_struct_name.lower())                        
                        str += "sf_status_t soc_groot_get_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry);\n\n" % (regList[1]._table_struct_name.lower(), regList[1]._table_struct_name.lower())
                    f.write(str)


            

    def GenerateTablePoolStruct(self, f, objDict, soc):
        
        f.write("\n//THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANUALLY!!!\n\n")

        regList = []
        table_struct = []
        
        for mode in objDict:
            
            # if table pool
            if mode in table_pool_dict:                
                if objDict[mode][2][0] > 0:
                    regList = objDict[mode][2][1]
                    
                    if regList[0]._table_struct_name.lower() in table_struct:
                        continue
                    table_struct.append(regList[0]._table_struct_name.lower()) 
                    
                    fieldInfoList = regList[0]._regFieldList                
                    nKeyType = len(fieldInfoList)

                    if nKeyType == 1:      # tables in table pool only have one key

                        f.write("/* MODE \"%s\" */\n" % mode.upper())
                        
                        table_type = self.get_table_pool_table_type(mode)                        
                        if table_type == "HASH": # if hash                            
                        
                            keyFieldList  = []
                            dataFieldList = []

                            fieldList = regList[0]._regFieldList[0][1]                            
                            for fd in range(len(fieldList)):
                                field = fieldList[fd]
                                if field._fieldName.upper() in hash_key_filedList_dict_[mode]:
                                    keyFieldList.append(field)
                                else:
                                    dataFieldList.append(field)

                        
                            fieldList = keyFieldList + dataFieldList                 
                            f.write("typedef struct soc_groot_%s_s \n{\n" %(regList[0]._table_struct_name.lower()))
                            f.write("    /* key table */\n")
                            
                            for fd in range(len(fieldList)):
                                if fd == len(keyFieldList):
                                    f.write("\n    /* data table */\n")
                                    
                                field = fieldList[fd]
                                if field.fieldName.upper() == "RESERVED":
                                    continue

                                (varible_type, num, type_) = self.get_field_varible_type(field)                                    
                                f.write("    %-10s %s%s; /* %dbit */\n" % (varible_type, field._fieldName.lower(), num, field._fieldLen))

                            f.write("}soc_groot_%s_t;\n\n" % regList[0]._table_struct_name.lower())

                            
                        else: # if direct table in table pool
                            fieldList = regList[0]._regFieldList[0][1]                                                                 
                            f.write("typedef struct soc_groot_%s_s \n{\n" %(regList[0]._table_struct_name.lower()))
                        
                            for fd in range(len(fieldList)):
                                field = fieldList[fd]
                                if field.fieldName.upper() == "RESERVED":
                                    continue

                                (varible_type, num, type_) = self.get_field_varible_type(field)                                
                                f.write("    %-10s %s%s; /* %dbit */\n" % (varible_type, field._fieldName.lower(), num, field._fieldLen))

                            f.write("}soc_groot_%s_t;\n\n" % regList[0]._table_struct_name.lower())


        str="""
#define L2_ENTRY_T_L2                       0
#define L2_ENTRY_T_VFI                      1

#define L3_ENTRY_IPV4_UNICAST_T             0
#define L3_ENTRY_IPV4_MULTICAST_T           1
#define L3_ENTRY_IPV6_UNICAST_T             2
#define L3_ENTRY_IPV6_MULTICAST_T           3

"""
        f.write(str)

                            
        table_struct = []
        for mode in objDict:
            
            # if table pool
            if mode in table_pool_dict:
                if objDict[mode][2][0] > 0:
                    regList = objDict[mode][2][1]

                    if regList[0]._table_struct_name.lower() in table_struct:
                        continue
                    table_struct.append(regList[0]._table_struct_name.lower()) 

                    fieldInfoList = regList[0]._regFieldList                
                    nKeyType = len(fieldInfoList)                    

                    if nKeyType == 1:      # tables in table pool only have one key

                        f.write("/* MODE \"%s\" */\n" % mode.upper())

                        table_type = self.get_table_pool_table_type(mode)                        
                        if table_type == "HASH": # if hash                            
                        
                            str  = "sf_status_t soc_groot_set_%s(uint32_t chip_id, soc_groot_%s_t *entry);\n" % (regList[0]._table_struct_name.lower(), regList[0]._table_struct_name.lower())                    
                            str += "sf_status_t soc_groot_get_%s(uint32_t chip_id, soc_groot_%s_t *entry);\n\n" % (regList[0]._table_struct_name.lower(), regList[0]._table_struct_name.lower())
                            f.write(str)               
                            
                        else: # if direct table in table pool
                            
                            str  = "sf_status_t soc_groot_set_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry);\n" % (regList[0]._table_struct_name.lower(), regList[0]._table_struct_name.lower())
                            str += "sf_status_t soc_groot_get_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry);\n" % (regList[0]._table_struct_name.lower(), regList[0]._table_struct_name.lower())
                            str += "sf_status_t soc_groot_mem_array_set_%s(uint32_t chip_id, uint32_t index_min, uint32_t index_max, soc_groot_%s_t *entry);\n" % (regList[0]._table_struct_name.lower(), regList[0]._table_struct_name.lower())
                            str += "sf_status_t soc_groot_mem_array_get_%s(uint32_t chip_id, uint32_t index_min, uint32_t index_max, soc_groot_%s_t *entry);\n\n" % (regList[0]._table_struct_name.lower(), regList[0]._table_struct_name.lower())
                            f.write(str)               



    def GenerateAllRegTableStruct(self, objDict, soc):
        print "Generate the all table struct and all reg struct header File."

        if soc != "": # if soc not been given, we can't give the prefix for the field name
            soc = soc + "_"

        time_ = ("%s-%s-%s %d:%d:%d" % (time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday, time.gmtime().tm_hour ,time.gmtime().tm_min ,time.gmtime().tm_sec))
                
        str = """
/** @file 
  * @note Shenzhen Forward Industry Co.Ltd - Copyright (c) 2017.
  * @brief    
  * 
  * @author   lijun
  * @date     %s
  * @version  1.0
  * 
  * @note     THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANUALLY!!! 
  * $LastChangedDate$
  * $LastChangedRevision$
  * $LastChangedBy$
  */
  
"""  % ("")

        f_reg        = file("./tmp/soc_groot_reg.h", 'w')
        f_direct     = file("./tmp/soc_groot_direct.h", 'w')
        f_hash_tcam  = file("./tmp/soc_groot_hash_tcam.h", 'w')
        f_table_pool = file("./tmp/soc_groot_table_pool.h", 'w')

        f_reg.write(str)
        f_reg.write("\n#ifdef SF_GROOT_SUPPORT\n")
        f_reg.write("#ifndef __SOC_GROOT_REG_H__\n")
        f_reg.write("#define __SOC_GROOT_REG_H__\n\n")
        self.GenerateRegStruct         (f_reg,        objDict,  soc)
        f_reg.write("#endif\n")
        f_reg.write("""\n#endif /* SF_GROOT_SUPPORT */\n""")
        
        f_direct.write(str)
        f_direct.write("\n#ifdef SF_GROOT_SUPPORT\n")
        f_direct.write("#ifndef __SOC_GROOT_DIRECT_H__\n")
        f_direct.write("#define __SOC_GROOT_DIRECT_H__\n\n")    
        self.GenerateDirectTabStruct   (f_direct,     objDict,  soc)
        f_direct.write("#endif\n")
        f_direct.write("""\n#endif /* SF_GROOT_SUPPORT */\n""")

        f_hash_tcam.write(str)
        f_hash_tcam.write("\n#ifdef SF_GROOT_SUPPORT\n")
        f_hash_tcam.write("#ifndef __SOC_GROOT_HASH_TCAM_H__\n")
        f_hash_tcam.write("#define __SOC_GROOT_HASH_TCAM_H__\n\n")    
        self.GenerateHashTcamTabStruct (f_hash_tcam,  objDict,  soc)
        f_hash_tcam.write("#endif\n")
        f_hash_tcam.write("""\n#endif /* SF_GROOT_SUPPORT */\n""")

        #f_table_pool.write(str)
        #f_table_pool.write("\n#ifdef SF_GROOT_SUPPORT\n")
        #f_table_pool.write("#ifndef __SOC_GROOT_TABLE_POOL_H__\n")
        #f_table_pool.write("#define __SOC_GROOT_TABLE_POOL_H__\n\n")    
        #self.GenerateTablePoolStruct   (f_table_pool, objDict,  soc)
        #f_table_pool.write("#endif\n")
        #f_table_pool.write("""\n#endif /* SF_GROOT_SUPPORT */\n""")

        
        f_reg.close()
        f_direct.close()
        f_hash_tcam.close()
        f_table_pool.close()



    def GenerateRegApi(self, f, objDict, soc):

        time_ = ("%s-%s-%s %d:%d:%d" % (time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday, time.gmtime().tm_hour ,time.gmtime().tm_min ,time.gmtime().tm_sec))
                
        str = """
/** @file 
  * @note Shenzhen Forward Industry Co.Ltd - Copyright (c) 2017.
  * @brief    
  * 
  * @author   lijun
  * @date     %s
  * @version  1.0
  * 
  * @note     THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANUALLY!!! 
  * $LastChangedDate$
  * $LastChangedRevision$
  * $LastChangedBy$
  */
"""  % ("")

        f.write(str)
        
        f.write("\n#include \"./soc/soc_ctrl.h\"\n")
        f.write("\n#include \"./soc/service/reg_tab/groot/soc_groot_reg.h\"\n")
        f.write("\n#include \"./soc/service/reg_tab/groot/soc_groot_allsymbol.h\"\n")
        

        multi_macro_reg_list = []
        regList = self.reg_list
        
        # for regs       
        if 1 == 1:            
            if 1 == 1:                
                for reg in range(len(regList)):
                    
                    # ignore the reg which have only one field
                    if len(regList[reg]._regFieldList) == 1:
                        continue 

                    # ignore the reg which _old_sheetName is MAC_COUNTER
                    if regList[reg]._old_sheetName == "MAC_COUNTER":                
                        continue
            
                    if regList[reg]._modeName in table_pool_dict:
                        continue
                    
                    if regList[reg]._nMacro > 1 and self.is_in_table_excel(regList[reg]._excelName) == 0:               
                        reg_name = regList[reg]._original_regName.lower()
                
                    else :
                        reg_name = regList[reg]._regName.lower()

                    
                    # set function
                    str = "sf_status_t soc_groot_set_%s_reg(uint32_t chip_id, soc_groot_%s_t *reg)\n{\n" % (regList[reg]._regName.lower(), reg_name)
                    str += "    sf_status_t ret = SF_E_NONE;\n"
                    str += "    uint8_t reg_data[8];\n\n"
                    str += "    SF_IF_NULL_RETURN(reg);\n"
                    str += "    sal_memset(reg_data, 0, 8);\n\n"
                        
                    
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        if field.fieldName.upper() == "RESERVED":
                            continue
                        
                        (varible_type, num, type_) = self.get_field_varible_type(field)
                        str += "    SF_E_IF_ERROR_RETURN(soc_set_field%s_to_reg_data(chip_id, reg_data, %sr, reg->%-25s, %sf));\n" % (type_, regList[reg]._regName.upper(), field._fieldName.lower(), field._fieldName.upper())
                    
                    str += "\n    SF_E_IF_ERROR_RETURN(soc_set_reg(chip_id, %sr, reg_data));\n" % (regList[reg]._regName.upper())
                    str += "\n    return ret;\n"
                    str += "}\n\n"

                    # get function                    
                    str += "sf_status_t soc_groot_get_%s_reg(uint32_t chip_id, soc_groot_%s_t *reg)\n{\n" % (regList[reg]._regName.lower(), reg_name)
                    str += "    sf_status_t ret = SF_E_NONE;\n"
                    str += "    uint8_t reg_data[8];\n\n"

                    str += "    SF_IF_NULL_RETURN(reg);\n"
                    str += "    sal_memset(reg_data, 0, 8);\n\n"
                    
                    str += "    SF_E_IF_ERROR_RETURN(soc_get_reg(chip_id, %sr, reg_data));\n\n" % (regList[reg]._regName.upper())                    
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        if field.fieldName.upper() == "RESERVED":
                            continue
                        
                        (varible_type, num, type_) = self.get_field_varible_type(field)
                        str += "    soc_get_field%s_from_reg_data(chip_id, reg_data, %sr, &reg->%-25s, %sf);\n" % (type_, regList[reg]._regName.upper(), field._fieldName.lower(), field._fieldName.upper())

                    str += "\n    return ret;\n"
                    str += "}\n\n"

                    f.write(str)


                table_pool_reg_list = []
                # only for tablepool
                for reg in range(len(regList)):

                    # ignore the reg which have only one field
                    if len(regList[reg]._regFieldList) == 1:
                        continue
                    
                    if regList[reg]._modeName not in table_pool_dict:
                        continue

                    # regs in table pool only need one api
                    if regList[reg]._modeName in table_pool_dict:                

                        if regList[reg]._old_regName.upper() in table_pool_reg_list:
                            continue
                        table_pool_reg_list.append(regList[reg]._old_regName.upper())

                        reg_name = "TABLEPOOL_" + regList[reg]._old_regName.upper()
                        reg_struct_name = "TABLEPOOL_" + regList[reg]._original_regName.upper()
                    

                    # set function
                    str = "sf_status_t soc_groot_set_%s_reg(uint32_t chip_id, soc_groot_%s_t *reg)\n{\n" % (reg_name.lower(), reg_struct_name.lower())
                    str += "    sf_status_t ret = SF_E_NONE;\n"
                    str += "    uint8_t reg_data[8];\n\n"

                    str += "    SF_IF_NULL_RETURN(reg);\n"
                    str += "    sal_memset(reg_data, 0, 8);\n\n"
                    
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        if field.fieldName.upper() == "RESERVED":
                            continue
                        
                        (varible_type, num, type_) = self.get_field_varible_type(field)
                        str += "    SF_E_IF_ERROR_RETURN(soc_set_field%s_to_reg_data(chip_id, reg_data, %sr, reg->%-25s, %sf));\n" % (type_, reg_name.upper(), field._fieldName.lower(), field._fieldName.upper())
                    
                    str += "\n    SF_E_IF_ERROR_RETURN(soc_set_reg(chip_id, %sr, reg_data));\n" % (reg_name.upper())
                    str += "\n    return ret;\n"
                    str += "}\n\n"

                    # get function                    
                    str += "sf_status_t soc_groot_get_%s_reg(uint32_t chip_id, soc_groot_%s_t *reg)\n{\n" % (reg_name.lower(), reg_struct_name.lower())
                    str += "    sf_status_t ret = SF_E_NONE;\n"
                    str += "    uint8_t reg_data[8];\n\n"

                    str += "    SF_IF_NULL_RETURN(reg);\n"
                    str += "    sal_memset(reg_data, 0, 8);\n\n"
                    
                    str += "    SF_E_IF_ERROR_RETURN(soc_get_reg(chip_id, %sr, reg_data));\n\n" % (reg_name.upper())
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        if field.fieldName.upper() == "RESERVED":
                            continue
                        
                        (varible_type, num, type_) = self.get_field_varible_type(field)
                        str += "    soc_get_field%s_from_reg_data(chip_id, reg_data, %sr, &reg->%-25s, %sf);\n" % (type_, reg_name.upper(), field._fieldName.lower(), field._fieldName.upper())

                    str += "\n    return ret;\n"
                    str += "}\n\n"

                    f.write(str)
               


    def get_the_function_string(self, reg, field, func_type, key_name):

        (varible_type, num, type_) = self.get_field_varible_type(field)

        if key_name != "NULL":        
            if func_type == "set":            
                str = "    SF_E_IF_ERROR_RETURN(soc_set_field%s_to_tab_data(chip_id, entry_data, entry->entry_type, %sm, entry->ent.%s_entry.%s, %sf));\n" % (type_, reg._table_struct_name.upper(), key_name, field._fieldName.lower(), field._fieldName.upper())

            else :
                if func_type == "get":
                    str = "    soc_get_field%s_from_tab_data(chip_id, entry_data, entry->entry_type, %sm, &entry->ent.%s_entry.%s, %sf);\n" % (type_, reg._table_struct_name.upper(), key_name, field._fieldName.lower(), field._fieldName.upper())

        else :
            if func_type == "set":            
                str = "    SF_E_IF_ERROR_RETURN(soc_set_field%s_to_tab_data(chip_id, entry_data, 0, %sm, entry->%-25s, %sf));\n" % (type_, reg._table_struct_name.upper(), field._fieldName.lower(), field._fieldName.upper())

            else :
                if func_type == "get":
                    str = "    soc_get_field%s_from_tab_data(chip_id, entry_data, 0, %sm, &entry->%-25s, %sf);\n" % (type_, reg._table_struct_name.upper(), field._fieldName.lower(), field._fieldName.upper())
            
        
        return str


   

    def GenerateDirectTabApi(self, f, objDict, soc):
        
        time_ = ("%s-%s-%s %d:%d:%d" % (time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday, time.gmtime().tm_hour ,time.gmtime().tm_min ,time.gmtime().tm_sec))
                
        str = """
/** @file 
  * @note Shenzhen Forward Industry Co.Ltd - Copyright (c) 2017.
  * @brief    
  * 
  * @author   lijun
  * @date     %s
  * @version  1.0
  * 
  * @note     THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANUALLY!!! 
  * $LastChangedDate$
  * $LastChangedRevision$
  * $LastChangedBy$
  */
"""  % ("")

        f.write(str)      

        f.write("\n#include \"./soc/soc_ctrl.h\"\n")
        f.write("\n#include \"./soc/service/reg_tab/groot/soc_groot_direct.h\"\n")
        f.write("\n#include \"./soc/service/reg_tab/groot/soc_groot_allsymbol.h\"\n")
    
        regList = []
        table_struct = []
        
        for mode in objDict:                                       
            
            # hash or tcam
            table_type = self.get_table_type(mode)
            if table_type in ["HASH", "TCAM"]:
                continue

            # if table pool
            if mode in table_pool_dict:
                continue

            # common direct table
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]

                for reg in range(len(regList)):

                    if regList[reg]._table_struct_name.lower() in table_struct:
                        continue            
                    table_struct.append(regList[reg]._table_struct_name.lower())

                    
                    fieldInfoList = regList[reg]._regFieldList
                    nKeyType = len(fieldInfoList)

                    if nKeyType > 1: # have more than one key type

                        # soc_xxx_TO_data function
                        str  = "sf_status_t soc_groot_%s_TO_data(uint32_t chip_id, soc_groot_%s_t *entry, uint8_t *entry_data)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())

                        str += "    SF_IF_NULL_RETURN(entry);\n"
                        str += "    SF_IF_NULL_RETURN(entry_data);\n\n"

                        str += "    switch (entry->entry_type)\n"
                        str +="    {\n"

                        for info in fieldInfoList :
                            key = info[0]                            
                            key_name = info[4]
                            
                            fieldList = info[1]                            

                            str += "    case SOC_%s_T:\n" % (key_name.upper())
                            for fd in range(len(fieldList)):
                                field = fieldList[fd]
                                if field.fieldName.upper() == "RESERVED":
                                    continue

                                #(varible_type, num, type_) = self.get_field_varible_type(field)                          
                                #str += "    soc_set_field%s_to_tab_data(chip_id, entry_data, entry->entry_type, %sm, entry->ent.key_%s_entry.%s, %sf);\n" % (type_, regList[reg]._table_struct_name.upper(), key_name, field._fieldName.lower(), field._fieldName.upper())

                                str += self.get_the_function_string(regList[reg], field, "set", key_name.lower())
                                
                            str += "        break;\n"
                        str += "    default:\n"
                        str += "        break;\n"
                        str += "    }\n"
                        
                        str += "\n    return SF_E_NONE;\n"
                        str += "}\n\n"


                        # soc_data_TO_xxx function

                        str += "sf_status_t soc_groot_data_TO_%s(uint32_t chip_id, soc_groot_%s_t *entry, uint8_t *entry_data)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())
                        str += "    soc_get_entry_type(chip_id, entry_data, &entry->entry_type, %sm);\n" % (regList[reg]._table_struct_name.upper())

                        str += "    SF_IF_NULL_RETURN(entry);\n"
                        str += "    SF_IF_NULL_RETURN(entry_data);\n\n"
                        
                        str += "    switch (entry->entry_type)\n"
                        str +="    {\n"

                        for info in fieldInfoList :
                            key = info[0]
                            key_name = info[4]
                            fieldList = info[1]                            

                            str += "    case SOC_%s_T:\n" % (key_name.upper())
                            for fd in range(len(fieldList)):
                                field = fieldList[fd]
                                if field.fieldName.upper() == "RESERVED":
                                    continue
                                
                                #(varible_type, num, type_) = self.get_field_varible_type(field)
                                #str += "    soc_get_field%s_from_tab_data(chip_id, entry_data, entry->entry_type, %sm, entry->ent.key_%s_entry.%s, %sf);\n" % (type_, regList[reg]._table_struct_name.upper(), key, field._fieldName.lower(), field._fieldName.upper())

                                str += self.get_the_function_string(regList[reg], field, "get", key_name.lower())
                                
                            str += "        break;\n"
                        str += "    default:\n"
                        str += "        break;\n"
                        str += "    }\n"
                        
                        str += "\n    return SF_E_NONE;\n"
                        str += "}\n\n"


                        # soc_set_xxx function
                        str += "sf_status_t soc_groot_set_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())
                        str += "    sf_status_t ret = SF_E_NONE;\n"
                        str += "    uint8_t *entry_data = NULL;\n"
                        
                        str += "    uint16_t tab_bytes = soc_get_tab_length_by_bytes(chip_id, %sm);\n\n" % (regList[reg]._table_struct_name.upper())
                        str += "    SF_IF_NULL_RETURN(entry);\n"
                        str += "    entry_data = sal_malloc(tab_bytes, SOC_SERV_REG_TAB_NAME);\n"
                        str += "    SF_GOTO_LABEL_IF_NULL(entry_data, ret, result);\n"
                        str += "    sal_memset(entry_data, 0, tab_bytes);\n\n"
                                                
                        str += "    SF_ERROR_GOTO(soc_groot_%s_TO_data(chip_id, entry, entry_data), ret, result);\n" % (regList[reg]._table_struct_name.lower())

                        str += "\n    ret = soc_set_direct_tab(chip_id, index, %sm, entry_data);\n" % (regList[reg]._table_struct_name.upper())

                        str += "\nresult:\n"
                        str += "    sal_free(entry_data);\n"
                        str += "    return ret;\n"
                        str += "}\n\n"

                        # soc_mem_array_set_xxx function
                        str += "sf_status_t soc_groot_mem_array_set_%s(uint32_t chip_id, uint32_t index_min, uint32_t index_max, soc_groot_%s_t *entry)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())

                        str += "    sf_status_t ret = SF_E_NONE;\n"
                        str += "    uint8_t *array_data = NULL;\n"
                        str += "    uint16_t index = 0;\n"
                        str += "    uint16_t single_entry_length = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[reg]._table_struct_name.upper())

                        str += "    SF_IF_NULL_RETURN(entry);\n"
                        str += "    array_data = sal_malloc(single_entry_length*(index_max - index_min + 1), SOC_SERV_REG_TAB_NAME);\n\n"
                        str += "    SF_GOTO_LABEL_IF_NULL(array_data, ret, result);\n"
                        str += "    sal_memset(array_data, 0, single_entry_length*(index_max - index_min + 1));\n"
                                                
                        str += "    for (index = 0; index < (index_max - index_min + 1); ++index)\n"
                        str +="    {\n"
                        str += "        SF_ERROR_GOTO(soc_groot_%s_TO_data(chip_id, &entry[index], array_data + single_entry_length * index), ret, result);\n" % (regList[reg]._table_struct_name.lower())
                        str +="    }\n\n"

                        
                        str += "    ret = soc_mem_array_write_range(chip_id, %sm, index_min, index_max, array_data);\n" % (regList[reg]._table_struct_name.upper())

                        str += "\nresult:\n"
                        str += "    sal_free(array_data);\n"
                        str += "    return ret;\n"
                        str += "}\n\n"
                        
                        f.write(str)


                        # soc_get_xxx function
                        str = "sf_status_t soc_groot_get_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())

                        str += "    sf_status_t ret = SF_E_NONE;\n"
                        str += "    uint8_t *entry_data = NULL;\n"
                        str += "    uint16_t tab_bytes = soc_get_tab_length_by_bytes(chip_id, %sm);\n\n" % (regList[reg]._table_struct_name.upper())

                        str += "    SF_IF_NULL_RETURN(entry);\n"
                        str += "    entry_data = sal_malloc(tab_bytes, SOC_SERV_REG_TAB_NAME);\n"
                        str += "    SF_GOTO_LABEL_IF_NULL(entry_data, ret, result);\n"
                        str += "    sal_memset(entry_data, 0, tab_bytes);\n\n"
                        
                        str += "    SF_ERROR_GOTO(soc_get_direct_tab(chip_id, index, %sm, entry_data), ret, result);\n\n" % (regList[reg]._table_struct_name.upper())
                         
                        
                        str += "    soc_groot_data_TO_%s(chip_id, entry, entry_data);\n" % (regList[reg]._table_struct_name.lower())

                        str += "\nresult:\n"
                        str += "    sal_free(entry_data);\n"
                        str += "    return ret;\n"
                        str += "}\n\n"


                        # soc_mem_array_get_xxx function
                        str += "sf_status_t soc_groot_mem_array_get_%s(uint32_t chip_id, uint32_t index_min, uint32_t index_max, soc_groot_%s_t *entry)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())

                        str += "    sf_status_t ret = SF_E_NONE;\n"
                        str += "    uint8_t *array_data = NULL;\n"
                        str += "    uint16_t index = 0;\n"
                        str += "    uint16_t single_entry_length = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[reg]._table_struct_name.upper())

                        str += "    SF_IF_NULL_RETURN(entry);\n"
                        str += "    array_data = sal_malloc(single_entry_length*(index_max - index_min + 1), SOC_SERV_REG_TAB_NAME);\n\n"
                        str += "    SF_GOTO_LABEL_IF_NULL(array_data, ret, result);\n"
                        str += "    sal_memset(array_data, 0, single_entry_length*(index_max - index_min + 1));\n"

                        str += "    SF_ERROR_GOTO(soc_mem_array_read_range(chip_id, %sm, index_min, index_max, array_data), ret, result);\n" % (regList[reg]._table_struct_name.upper())

                        
                        str += "    for (index = 0; index < (index_max - index_min + 1); ++index)\n"
                        str +="    {\n"
                        str += "        soc_groot_data_TO_%s(chip_id, &entry[index], array_data + single_entry_length * index);\n" % (regList[reg]._table_struct_name.lower())
                        str +="    }\n\n"


                        
                        str += "\nresult:\n"
                        str += "    sal_free(array_data);\n"
                        str += "    return ret;\n"
                        str += "}\n\n"
                        
                        f.write(str)

                                                
                        
                    else: # only have one key type
                        fieldList = regList[reg]._regFieldList[0][1]

                        
                        # soc_xxx_TO_data function
                        str  = "sf_status_t soc_groot_%s_TO_data(uint32_t chip_id, soc_groot_%s_t *entry, uint8_t *entry_data)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())

                        str += "    SF_IF_NULL_RETURN(entry);\n"
                        str += "    SF_IF_NULL_RETURN(entry_data);\n\n"
                                               
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field.fieldName.upper() == "RESERVED":
                                continue
                            
                            #(varible_type, num, type_) = self.get_field_varible_type(field)
                            #str += "    soc_set_field%s_to_tab_data(chip_id, entry_data, 0, %sm, entry->%-25s, %sf);\n" % (type_, regList[reg]._table_struct_name.upper(), field._fieldName.lower(), field._fieldName.upper())

                            str += self.get_the_function_string(regList[reg], field, "set", "NULL")
                            
                        str += "\n    return SF_E_NONE;\n"
                        str += "}\n\n"

                        
                        # soc_data_TO_xxx function
                        str += "sf_status_t soc_groot_data_TO_%s(uint32_t chip_id, soc_groot_%s_t *entry, uint8_t *entry_data)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())

                        str += "    SF_IF_NULL_RETURN(entry);\n"
                        str += "    SF_IF_NULL_RETURN(entry_data);\n\n"                        

                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field.fieldName.upper() == "RESERVED":
                                continue
                            
                            #(varible_type, num, type_) = self.get_field_varible_type(field)
                            #str += "    soc_get_field%s_from_tab_data(chip_id, entry_data, 0, %sm, &entry->%-25s, %sf);\n" % (type_, regList[reg]._table_struct_name.upper(), field._fieldName.lower(), field._fieldName.upper())

                            str += self.get_the_function_string(regList[reg], field, "get", "NULL")
                            
                        str += "\n    return SF_E_NONE;\n"
                        str += "}\n\n"


                        # soc_set_xxx function
                        str += "sf_status_t soc_groot_set_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())
                        str += "    sf_status_t ret = SF_E_NONE;\n"
                        str += "    uint8_t *entry_data = NULL;\n"
                        
                        str += "    uint16_t tab_bytes = soc_get_tab_length_by_bytes(chip_id, %sm);\n\n" % (regList[reg]._table_struct_name.upper())
                        str += "    SF_IF_NULL_RETURN(entry);\n"
                        str += "    entry_data = sal_malloc(tab_bytes, SOC_SERV_REG_TAB_NAME);\n"
                        str += "    SF_GOTO_LABEL_IF_NULL(entry_data, ret, result);\n"
                        str += "    sal_memset(entry_data, 0, tab_bytes);\n\n"
                                                
                        str += "    SF_ERROR_GOTO(soc_groot_%s_TO_data(chip_id, entry, entry_data), ret, result);\n" % (regList[reg]._table_struct_name.lower())

                        str += "\n    ret = soc_set_direct_tab(chip_id, index, %sm, entry_data);\n" % (regList[reg]._table_struct_name.upper())

                        str += "\nresult:\n"
                        str += "    sal_free(entry_data);\n"
                        str += "    return ret;\n"
                        str += "}\n\n"

                        # soc_mem_array_set_xxx function
                        str += "sf_status_t soc_groot_mem_array_set_%s(uint32_t chip_id, uint32_t index_min, uint32_t index_max, soc_groot_%s_t *entry)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())

                        str += "    sf_status_t ret = SF_E_NONE;\n"
                        str += "    uint8_t *array_data = NULL;\n"
                        str += "    uint16_t index = 0;\n"
                        str += "    uint16_t single_entry_length = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[reg]._table_struct_name.upper())

                        str += "    SF_IF_NULL_RETURN(entry);\n"
                        str += "    array_data = sal_malloc(single_entry_length*(index_max - index_min + 1), SOC_SERV_REG_TAB_NAME);\n\n"
                        str += "    SF_GOTO_LABEL_IF_NULL(array_data, ret, result);\n"
                        str += "    sal_memset(array_data, 0, single_entry_length*(index_max - index_min + 1));\n"
                                                
                        str += "    for (index = 0; index < (index_max - index_min + 1); ++index)\n"
                        str +="    {\n"
                        str += "        SF_ERROR_GOTO(soc_groot_%s_TO_data(chip_id, &entry[index], array_data + single_entry_length * index), ret, result);\n" % (regList[reg]._table_struct_name.lower())
                        str +="    }\n\n"

                        
                        str += "    ret = soc_mem_array_write_range(chip_id, %sm, index_min, index_max, array_data);\n" % (regList[reg]._table_struct_name.upper())

                        str += "\nresult:\n"
                        str += "    sal_free(array_data);\n"
                        str += "    return ret;\n"
                        str += "}\n\n"
                        
                        f.write(str)


                        # soc_get_xxx function
                        str = "sf_status_t soc_groot_get_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())

                        str += "    sf_status_t ret = SF_E_NONE;\n"
                        str += "    uint8_t *entry_data = NULL;\n"
                        str += "    uint16_t tab_bytes = soc_get_tab_length_by_bytes(chip_id, %sm);\n\n" % (regList[reg]._table_struct_name.upper())

                        str += "    SF_IF_NULL_RETURN(entry);\n"
                        str += "    entry_data = sal_malloc(tab_bytes, SOC_SERV_REG_TAB_NAME);\n"
                        str += "    SF_GOTO_LABEL_IF_NULL(entry_data, ret, result);\n"
                        str += "    sal_memset(entry_data, 0, tab_bytes);\n\n"
                        
                        str += "    SF_ERROR_GOTO(soc_get_direct_tab(chip_id, index, %sm, entry_data), ret, result);\n\n" % (regList[reg]._table_struct_name.upper())
                         
                        
                        str += "    soc_groot_data_TO_%s(chip_id, entry, entry_data);\n" % (regList[reg]._table_struct_name.lower())

                        str += "\nresult:\n"
                        str += "    sal_free(entry_data);\n"
                        str += "    return ret;\n"
                        str += "}\n\n"


                        # soc_mem_array_get_xxx function
                        str += "sf_status_t soc_groot_mem_array_get_%s(uint32_t chip_id, uint32_t index_min, uint32_t index_max, soc_groot_%s_t *entry)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())

                        str += "    sf_status_t ret = SF_E_NONE;\n"
                        str += "    uint8_t *array_data = NULL;\n"
                        str += "    uint16_t index = 0;\n"
                        str += "    uint16_t single_entry_length = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[reg]._table_struct_name.upper())

                        str += "    SF_IF_NULL_RETURN(entry);\n"
                        str += "    array_data = sal_malloc(single_entry_length*(index_max - index_min + 1), SOC_SERV_REG_TAB_NAME);\n\n"
                        str += "    SF_GOTO_LABEL_IF_NULL(array_data, ret, result);\n"
                        str += "    sal_memset(array_data, 0, single_entry_length*(index_max - index_min + 1));\n"

                        str += "    SF_ERROR_GOTO(soc_mem_array_read_range(chip_id, %sm, index_min, index_max, array_data), ret, result);\n" % (regList[reg]._table_struct_name.upper())

                        
                        str += "    for (index = 0; index < (index_max - index_min + 1); ++index)\n"
                        str +="    {\n"
                        str += "        soc_groot_data_TO_%s(chip_id, &entry[index], array_data + single_entry_length * index);\n" % (regList[reg]._table_struct_name.lower())
                        str +="    }\n\n"


                        
                        str += "\nresult:\n"
                        str += "    sal_free(array_data);\n"
                        str += "    return ret;\n"
                        str += "}\n\n"
                        
                        f.write(str)




    def GenerateHashTcamTabApi(self, f, objDict, soc):
        
        time_ = ("%s-%s-%s %d:%d:%d" % (time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday, time.gmtime().tm_hour ,time.gmtime().tm_min ,time.gmtime().tm_sec))
                
        str = """
/** @file 
  * @note Shenzhen Forward Industry Co.Ltd - Copyright (c) 2017.
  * @brief    
  * 
  * @author   lijun
  * @date     %s
  * @version  1.0
  * 
  * @note     THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANUALLY!!! 
  * $LastChangedDate$
  * $LastChangedRevision$
  * $LastChangedBy$
  */
"""  % ("")

        f.write(str)

        f.write("\n#include \"./soc/soc_ctrl.h\"\n")
        f.write("\n#include \"./soc/service/reg_tab/groot/soc_groot_hash_tcam.h\"\n")
        f.write("\n#include \"./soc/service/reg_tab/groot/soc_groot_allsymbol.h\"\n")
        
        table_struct = []

        print hash_tcam_dict
        for mode in objDict:

            # if hash or tcam
            logger.debug(mode)
            table_type = self.get_table_type(mode)
            logger.debug( "table_type = %s" %table_type)
            if table_type in ["HASH", "TCAM"]: # only for data table when table is tcam or hash                
                if objDict[mode][2][0] > 0:
                    regList = objDict[mode][2][1]

                    if regList[0]._table_struct_name.lower() in table_struct:
                        continue            
                    table_struct.append(regList[0]._table_struct_name.lower())                    
                    
                    fieldInfoList = regList[0]._regFieldList                
                    nKeyType = len(fieldInfoList)

                    #dataFieldList = []
                    #keyFieldList  = []
                
                    if nKeyType == 1:
                        for reg in range(2):
                            fieldList = regList[reg]._regFieldList[0][1] # reg = 0 is data table, reg = 1 is key table
                            if reg == 0 :
                                data_or_key = "data"
                            else:
                                data_or_key = "key"                              
                            
                            # soc_xxx_TO_data function
                            str  = "sf_status_t soc_groot_%s_TO_%s(uint32_t chip_id, soc_groot_%s_t *entry, uint8_t *entry_data)\n{\n" % (regList[1]._table_struct_name.lower(), data_or_key, regList[1]._table_struct_name.lower())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                            str += "    SF_IF_NULL_RETURN(entry_data);\n\n"
                        
                            for fd in range(len(fieldList)):
                                field = fieldList[fd]
                                if field.fieldName.upper() == "RESERVED":
                                    continue

                                str += self.get_the_function_string(regList[reg], field, "set", "NULL")
                                
                            str += "\n    return SF_E_NONE;\n"
                            str += "}\n\n"


                            # soc_data_TO_xxx function
                            str += "sf_status_t soc_groot_%s_TO_%s(uint32_t chip_id, soc_groot_%s_t *entry, uint8_t *entry_data)\n{\n" % (data_or_key, regList[1]._table_struct_name.lower(), regList[1]._table_struct_name.lower())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                            str += "    SF_IF_NULL_RETURN(entry_data);\n\n"
                                                    
                            for fd in range(len(fieldList)):
                                field = fieldList[fd]
                                if field.fieldName.upper() == "RESERVED":
                                    continue
                                
                                str += self.get_the_function_string(regList[reg], field, "get", "NULL")
                                
                            str += "\n    return SF_E_NONE;\n"
                            str += "}\n\n"

                            f.write(str)
                                

                        if table_type == "HASH":
                            # set function
                            str  = "sf_status_t soc_groot_set_%s(uint32_t chip_id, soc_groot_%s_t *entry)\n{\n" % (regList[1]._table_struct_name.lower(), regList[1]._table_struct_name.lower())

                            str += "    sf_status_t ret = SF_E_NONE;\n"
                            str += "    uint8_t *entry_key          = NULL;\n"
                            str += "    uint8_t *entry_data         = NULL;\n"

                            str += "    uint16_t entry_key_bytes    = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[1]._table_struct_name.upper())
                            str += "    uint16_t entry_data_bytes   = soc_get_tab_length_by_bytes(chip_id, %sm);\n\n" % (regList[0]._table_struct_name.upper())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                                
                            str += "    entry_key = sal_malloc(entry_key_bytes, SOC_SERV_REG_TAB_NAME);\n"                            
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_key, ret, result);\n"
                            str += "    sal_memset(entry_key, 0, entry_key_bytes);\n"

                            str += "    entry_data = sal_malloc(entry_data_bytes, SOC_SERV_REG_TAB_NAME);\n"
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_data, ret, result);\n"
                            str += "    sal_memset(entry_data, 0, entry_data_bytes);\n"
                            

                            
                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_key(chip_id, entry, entry_key), ret, result);\n" % (regList[1]._table_struct_name.lower())
                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_data(chip_id, entry, entry_data), ret, result);\n" % (regList[1]._table_struct_name.lower())
                            str += "\n    ret = soc_set_hash_tab(chip_id, %sm, 0, entry_key, entry_data);\n" % (regList[1]._table_struct_name.upper())

                            str += "\nresult:\n"
                            str += "\n    sal_free(entry_key);\n"
                            str += "    sal_free(entry_data);\n"
                            str += "    return ret;\n"
                            str += "}\n\n"

                            
                            # get function
                            str += "sf_status_t soc_groot_get_%s(uint32_t chip_id, soc_groot_%s_t *entry)\n{\n" % (regList[1]._table_struct_name.lower(), regList[1]._table_struct_name.lower())
                            str += "    sf_status_t ret = SF_E_NONE;\n"

                            str += "    uint8_t *entry_key          = NULL;\n"
                            str += "    uint8_t *entry_data         = NULL;\n"

                            str += "    uint16_t entry_key_bytes    = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[1]._table_struct_name.upper())
                            str += "    uint16_t entry_data_bytes   = soc_get_tab_length_by_bytes(chip_id, %sm);\n\n" % (regList[0]._table_struct_name.upper())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                                
                            str += "    entry_key = sal_malloc(entry_key_bytes, SOC_SERV_REG_TAB_NAME);\n"                            
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_key, ret, result);\n"
                            str += "    sal_memset(entry_key, 0, entry_key_bytes);\n"

                            str += "    entry_data = sal_malloc(entry_data_bytes, SOC_SERV_REG_TAB_NAME);\n"
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_data, ret, result);\n"
                            str += "    sal_memset(entry_data, 0, entry_data_bytes);\n"

                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_key(chip_id, entry, entry_key), ret, result);\n\n" % (regList[1]._table_struct_name.lower())                            
                            str += "    ret = soc_get_hash_tab(chip_id, %sm, 0, entry_key, entry_data);\n\n" % (regList[1]._table_struct_name.upper())
                            str += "    soc_groot_data_TO_%s(chip_id, entry, entry_data);\n\n" % (regList[1]._table_struct_name.lower())
                                
                            str += "\nresult:\n"
                            str += "\n    sal_free(entry_key);\n"
                            str += "    sal_free(entry_data);\n"
                            str += "    return ret;\n"
                            str += "}\n\n"


                        if table_type == "TCAM":
                            # set function
                            str  = "sf_status_t soc_groot_set_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry)\n{\n" % (regList[1]._table_struct_name.lower(), regList[1]._table_struct_name.lower())
                            str += "    sf_status_t ret = SF_E_NONE;\n"

                            str += "    uint8_t *entry_key          = NULL;\n"
                            str += "    uint8_t *entry_data         = NULL;\n"

                            str += "    uint16_t entry_key_bytes    = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[1]._table_struct_name.upper())
                            str += "    uint16_t entry_data_bytes   = soc_get_tab_length_by_bytes(chip_id, %sm);\n\n" % (regList[0]._table_struct_name.upper())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                                
                            str += "    entry_key = sal_malloc(entry_key_bytes, SOC_SERV_REG_TAB_NAME);\n"                            
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_key, ret, result);\n"
                            str += "    sal_memset(entry_key, 0, entry_key_bytes);\n"

                            str += "    entry_data = sal_malloc(entry_data_bytes, SOC_SERV_REG_TAB_NAME);\n"
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_data, ret, result);\n"
                            str += "    sal_memset(entry_data, 0, entry_data_bytes);\n"

                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_key(chip_id, entry, entry_key), ret, result);\n" % (regList[1]._table_struct_name.lower())
                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_data(chip_id, entry, entry_data), ret, result);\n" % (regList[1]._table_struct_name.lower())
                            
                            str += "\n    ret = soc_set_tcam_tab(chip_id, index, %sm, entry_key, entry_data);\n" % (regList[1]._table_struct_name.upper())
                            
                            str += "\nresult:\n"
                            str += "\n    sal_free(entry_key);\n"
                            str += "    sal_free(entry_data);\n"
                            str += "    return ret;\n"
                            str += "}\n\n"
                            
                            # get function
                            str += "sf_status_t soc_groot_get_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry)\n{\n" % (regList[1]._table_struct_name.lower(), regList[1]._table_struct_name.lower())
                            str += "    sf_status_t ret = SF_E_NONE;\n"

                            str += "    uint8_t *entry_key          = NULL;\n"
                            str += "    uint8_t *entry_data         = NULL;\n"

                            str += "    uint16_t entry_key_bytes    = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[1]._table_struct_name.upper())
                            str += "    uint16_t entry_data_bytes   = soc_get_tab_length_by_bytes(chip_id, %sm);\n\n" % (regList[0]._table_struct_name.upper())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                                
                            str += "    entry_key = sal_malloc(entry_key_bytes, SOC_SERV_REG_TAB_NAME);\n"                            
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_key, ret, result);\n"
                            str += "    sal_memset(entry_key, 0, entry_key_bytes);\n"

                            str += "    entry_data = sal_malloc(entry_data_bytes, SOC_SERV_REG_TAB_NAME);\n"
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_data, ret, result);\n"
                            str += "    sal_memset(entry_data, 0, entry_data_bytes);\n"

                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_key(chip_id, entry, entry_key), ret, result);\n" % (regList[1]._table_struct_name.lower())
                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_data(chip_id, entry, entry_data), ret, result);\n" % (regList[1]._table_struct_name.lower())

                            str += "    ret = soc_get_tcam_tab(chip_id, index, %sm, entry_key, entry_data);\n\n" % (regList[1]._table_struct_name.upper())

                            str += "    soc_groot_key_TO_%s(chip_id, entry, entry_key);\n\n" % (regList[1]._table_struct_name.lower())
                            str += "    soc_groot_data_TO_%s(chip_id, entry, entry_data);\n\n" % (regList[1]._table_struct_name.lower())
                                
                            str += "\nresult:\n"
                            str += "\n    sal_free(entry_key);\n"
                            str += "    sal_free(entry_data);\n"
                            str += "    return ret;\n"
                            str += "}\n\n"
                        

                        f.write(str)

                        
                    else:
                        for reg in range(2):                            
                            if reg == 0 :
                                data_or_key = "data"
                            else:
                                data_or_key = "key"                              
                            
                            # soc_xxx_TO_data function

                            str  = "sf_status_t soc_groot_%s_TO_%s(uint32_t chip_id, soc_groot_%s_t *entry, uint8_t *entry_data)\n{\n" % (regList[1]._table_struct_name.lower(), data_or_key, regList[1]._table_struct_name.lower())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                            str += "    SF_IF_NULL_RETURN(entry_data);\n\n"
                            
                            str += "    switch (entry->entry_type)\n"
                            str +="    {\n"
                            
                            fieldInfoList = regList[reg]._regFieldList
                            for info in fieldInfoList :
                                key = info[0]
                                key_name = info[4]
                                fieldList = info[1]                            

                                str += "    case SOC_%s_T:\n" % (key_name.upper())
                                for fd in range(len(fieldList)):
                                    field = fieldList[fd]
                                    if field.fieldName.upper() == "RESERVED":
                                        continue
                                    
                                    str += self.get_the_function_string(regList[reg], field, "set", key_name.lower())
                                    
                                str += "        break;\n"
                            str += "    default:\n"
                            str += "        break;\n"
                            str += "    }\n"
                            
                            str += "\n    return SF_E_NONE;\n"
                            str += "}\n\n"


                            # soc_data_TO_xxx function

                            str += "sf_status_t soc_groot_%s_TO_%s(uint32_t chip_id, soc_groot_%s_t *entry, uint8_t *entry_data)\n{\n" % (data_or_key, regList[1]._table_struct_name.lower(), regList[1]._table_struct_name.lower())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                            str += "    SF_IF_NULL_RETURN(entry_data);\n\n"

                            #str += "    soc_get_entry_type(chip_id, entry_data, &entry->entry_type, %sm);\n" % (regList[reg]._table_struct_name.upper())
                            str += "    switch (entry->entry_type)\n"
                            str +="    {\n"

                            fieldInfoList = regList[reg]._regFieldList
                            for info in fieldInfoList :
                                key = info[0]
                                key_name = info[4]
                                fieldList = info[1]                            

                                str += "    case SOC_%s_T:\n" % (key_name.upper())
                                for fd in range(len(fieldList)):
                                    field = fieldList[fd]
                                    if field.fieldName.upper() == "RESERVED":
                                        continue

                                    str += self.get_the_function_string(regList[reg], field, "get", key_name.lower())
                                    
                                str += "        break;\n"
                            str += "    default:\n"
                            str += "        break;\n"
                            str += "    }\n"
                            
                            str += "\n    return SF_E_NONE;\n"
                            str += "}\n\n"

                            f.write(str)


                        if table_type == "HASH":
                            # set function
                            str  = "sf_status_t soc_groot_set_%s(uint32_t chip_id, soc_groot_%s_t *entry)\n{\n" % (regList[1]._table_struct_name.lower(), regList[1]._table_struct_name.lower())

                            str += "    sf_status_t ret = SF_E_NONE;\n"
                            str += "    uint8_t *entry_key          = NULL;\n"
                            str += "    uint8_t *entry_data         = NULL;\n"

                            str += "    uint16_t entry_key_bytes    = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[1]._table_struct_name.upper())
                            str += "    uint16_t entry_data_bytes   = soc_get_tab_length_by_bytes(chip_id, %sm);\n\n" % (regList[0]._table_struct_name.upper())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                                
                            str += "    entry_key = sal_malloc(entry_key_bytes, SOC_SERV_REG_TAB_NAME);\n"                            
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_key, ret, result);\n"
                            str += "    sal_memset(entry_key, 0, entry_key_bytes);\n"

                            str += "    entry_data = sal_malloc(entry_data_bytes, SOC_SERV_REG_TAB_NAME);\n"
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_data, ret, result);\n"
                            str += "    sal_memset(entry_data, 0, entry_data_bytes);\n"
                            

                            
                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_key(chip_id, entry, entry_key), ret, result);\n" % (regList[1]._table_struct_name.lower())
                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_data(chip_id, entry, entry_data), ret, result);\n" % (regList[1]._table_struct_name.lower())
                            str += "\n    ret = soc_set_hash_tab(chip_id, %sm, entry->entry_type, entry_key, entry_data);\n" % (regList[1]._table_struct_name.upper())

                            str += "\nresult:\n"
                            str += "\n    sal_free(entry_key);\n"
                            str += "    sal_free(entry_data);\n"
                            str += "    return ret;\n"
                            str += "}\n\n"

                            
                            # get function
                            str += "sf_status_t soc_groot_get_%s(uint32_t chip_id, soc_groot_%s_t *entry)\n{\n" % (regList[1]._table_struct_name.lower(), regList[1]._table_struct_name.lower())
                            str += "    sf_status_t ret = SF_E_NONE;\n"

                            str += "    uint8_t *entry_key          = NULL;\n"
                            str += "    uint8_t *entry_data         = NULL;\n"

                            str += "    uint16_t entry_key_bytes    = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[1]._table_struct_name.upper())
                            str += "    uint16_t entry_data_bytes   = soc_get_tab_length_by_bytes(chip_id, %sm);\n\n" % (regList[0]._table_struct_name.upper())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                                
                            str += "    entry_key = sal_malloc(entry_key_bytes, SOC_SERV_REG_TAB_NAME);\n"                            
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_key, ret, result);\n"
                            str += "    sal_memset(entry_key, 0, entry_key_bytes);\n"

                            str += "    entry_data = sal_malloc(entry_data_bytes, SOC_SERV_REG_TAB_NAME);\n"
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_data, ret, result);\n"
                            str += "    sal_memset(entry_data, 0, entry_data_bytes);\n"

                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_key(chip_id, entry, entry_key), ret, result);\n\n" % (regList[1]._table_struct_name.lower())                            
                            str += "    ret = soc_get_hash_tab(chip_id, %sm, entry->entry_type, entry_key, entry_data);\n\n" % (regList[1]._table_struct_name.upper())
                            str += "    soc_groot_data_TO_%s(chip_id, entry, entry_data);\n\n" % (regList[1]._table_struct_name.lower())
                                
                            str += "\nresult:\n"
                            str += "\n    sal_free(entry_key);\n"
                            str += "    sal_free(entry_data);\n"
                            str += "    return ret;\n"
                            str += "}\n\n"


                        if table_type == "TCAM":
                            # set function
                            str  = "sf_status_t soc_groot_set_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry)\n{\n" % (regList[1]._table_struct_name.lower(), regList[1]._table_struct_name.lower())
                            str += "    sf_status_t ret = SF_E_NONE;\n"

                            str += "    uint8_t *entry_key          = NULL;\n"
                            str += "    uint8_t *entry_data         = NULL;\n"

                            str += "    uint16_t entry_key_bytes    = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[1]._table_struct_name.upper())
                            str += "    uint16_t entry_data_bytes   = soc_get_tab_length_by_bytes(chip_id, %sm);\n\n" % (regList[0]._table_struct_name.upper())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                                
                            str += "    entry_key = sal_malloc(entry_key_bytes, SOC_SERV_REG_TAB_NAME);\n"                            
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_key, ret, result);\n"
                            str += "    sal_memset(entry_key, 0, entry_key_bytes);\n"

                            str += "    entry_data = sal_malloc(entry_data_bytes, SOC_SERV_REG_TAB_NAME);\n"
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_data, ret, result);\n"
                            str += "    sal_memset(entry_data, 0, entry_data_bytes);\n"

                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_key(chip_id, entry, entry_key), ret, result);\n" % (regList[1]._table_struct_name.lower())
                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_data(chip_id, entry, entry_data), ret, result);\n" % (regList[1]._table_struct_name.lower())
                            
                            str += "\n    ret = soc_set_tcam_tab(chip_id, index, %sm, entry_key, entry_data);\n" % (regList[1]._table_struct_name.upper())
                            
                            str += "\nresult:\n"
                            str += "\n    sal_free(entry_key);\n"
                            str += "    sal_free(entry_data);\n"
                            str += "    return ret;\n"
                            str += "}\n\n"
                            
                            # get function
                            str += "sf_status_t soc_groot_get_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry)\n{\n" % (regList[1]._table_struct_name.lower(), regList[1]._table_struct_name.lower())
                            str += "    sf_status_t ret = SF_E_NONE;\n"

                            str += "    uint8_t *entry_key          = NULL;\n"
                            str += "    uint8_t *entry_data         = NULL;\n"

                            str += "    uint16_t entry_key_bytes    = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[1]._table_struct_name.upper())
                            str += "    uint16_t entry_data_bytes   = soc_get_tab_length_by_bytes(chip_id, %sm);\n\n" % (regList[0]._table_struct_name.upper())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                                
                            str += "    entry_key = sal_malloc(entry_key_bytes, SOC_SERV_REG_TAB_NAME);\n"                            
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_key, ret, result);\n"
                            str += "    sal_memset(entry_key, 0, entry_key_bytes);\n"

                            str += "    entry_data = sal_malloc(entry_data_bytes, SOC_SERV_REG_TAB_NAME);\n"
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_data, ret, result);\n"
                            str += "    sal_memset(entry_data, 0, entry_data_bytes);\n"

                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_key(chip_id, entry, entry_key), ret, result);\n" % (regList[1]._table_struct_name.lower())
                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_data(chip_id, entry, entry_data), ret, result);\n" % (regList[1]._table_struct_name.lower())

                            str += "    ret = soc_get_tcam_tab(chip_id, index, %sm, entry_key, entry_data);\n\n" % (regList[1]._table_struct_name.upper())

                            str += "    soc_groot_key_TO_%s(chip_id, entry, entry_key);\n\n" % (regList[1]._table_struct_name.lower())
                            str += "    soc_groot_data_TO_%s(chip_id, entry, entry_data);\n\n" % (regList[1]._table_struct_name.lower())
                                
                            str += "\nresult:\n"
                            str += "\n    sal_free(entry_key);\n"
                            str += "    sal_free(entry_data);\n"
                            str += "    return ret;\n"
                            str += "}\n\n"
                        

                        f.write(str)

                    

    def GenerateTablePoolApi(self, f, objDict, soc):
        
        time_ = ("%s-%s-%s %d:%d:%d" % (time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday, time.gmtime().tm_hour ,time.gmtime().tm_min ,time.gmtime().tm_sec))
                
        str = """
/** @file 
  * @note Shenzhen Forward Industry Co.Ltd - Copyright (c) 2017.
  * @brief    
  * 
  * @author   lijun
  * @date     %s
  * @version  1.0
  * 
  * @note     THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANUALLY!!! 
  * $LastChangedDate$
  * $LastChangedRevision$
  * $LastChangedBy$
  */
"""  % ("")

        f.write(str)

        f.write("\n#include \"./soc/soc_ctrl.h\"\n")
        f.write("\n#include \"./soc/service/reg_tab/groot/soc_groot_table_pool.h\"\n")
        f.write("\n#include \"./soc/service/reg_tab/groot/soc_groot_allsymbol.h\"\n")

        table_struct = []

        for mode in objDict:

            # if table pool
            if mode in table_pool_dict:
                if objDict[mode][2][0] > 0:
                    regList = objDict[mode][2][1]

                    if regList[0]._table_struct_name.lower() in table_struct:
                        continue            
                    table_struct.append(regList[0]._table_struct_name.lower())
                    
                    fieldInfoList = regList[0]._regFieldList                
                    nKeyType = len(fieldInfoList)

                    if nKeyType == 1:      # tables in table pool only have one key

                        table_type = self.get_table_pool_table_type(mode)                        
                        if table_type == "HASH": # if hash                            
                        
                            keyFieldList  = []
                            dataFieldList = []

                            fieldList = regList[0]._regFieldList[0][1]                            
                            for fd in range(len(fieldList)):
                                field = fieldList[fd]
                                if field._fieldName.upper() in hash_key_filedList_dict_[mode]:
                                    keyFieldList.append(field)
                                else:
                                    dataFieldList.append(field)
                        
                            data_and_key_field_list = [dataFieldList, keyFieldList]

                            i = 0
                            for fieldList in data_and_key_field_list:
                                
                                if i == 0 :
                                    data_or_key = "data"
                                    i += 1
                                else:
                                    data_or_key = "key"                                 
                                
                                # soc_xxx_TO_data function
                                str  = "sf_status_t soc_groot_%s_TO_%s(uint32_t chip_id, soc_groot_%s_t *entry, uint8_t *entry_data)\n{\n" % (regList[0]._table_struct_name.lower(), data_or_key, regList[0]._table_struct_name.lower())

                                str += "    SF_IF_NULL_RETURN(entry);\n"
                                str += "    SF_IF_NULL_RETURN(entry_data);\n\n"
                               
                                for fd in range(len(fieldList)):
                                    field = fieldList[fd]
                                    if field.fieldName.upper() == "RESERVED":
                                        continue                                    
                                    
                                    str += self.get_the_function_string(regList[0], field, "set", "NULL")
                                    
                                str += "\n    return SF_E_NONE;\n"
                                str += "}\n\n"


                                # soc_data_TO_xxx function
                                str += "sf_status_t soc_groot_%s_TO_%s(uint32_t chip_id, soc_groot_%s_t *entry, uint8_t *entry_data)\n{\n" % (data_or_key, regList[0]._table_struct_name.lower(), regList[0]._table_struct_name.lower())

                                str += "    SF_IF_NULL_RETURN(entry);\n"
                                str += "    SF_IF_NULL_RETURN(entry_data);\n\n"
                                
                                for fd in range(len(fieldList)):
                                    field = fieldList[fd]
                                    if field.fieldName.upper() == "RESERVED":
                                        continue
                                    
                                    str += self.get_the_function_string(regList[0], field, "get", "NULL")
                                    
                                str += "\n    return SF_E_NONE;\n"
                                str += "}\n\n"

                                f.write(str)


                            # set function
                            str  = "sf_status_t soc_groot_set_%s(uint32_t chip_id, soc_groot_%s_t *entry)\n{\n" % (regList[0]._table_struct_name.lower(), regList[0]._table_struct_name.lower())


                            str += "    sf_status_t ret = SF_E_NONE;\n"
                            str += "    uint8_t *entry_key          = NULL;\n"
                            
                            str += "    uint16_t entry_key_bytes    = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[0]._table_struct_name.upper())
                            
                            str += "    SF_IF_NULL_RETURN(entry);\n"
                                
                            str += "    entry_key = sal_malloc(entry_key_bytes, SOC_SERV_REG_TAB_NAME);\n"                            
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_key, ret, result);\n"
                            str += "    sal_memset(entry_key, 0, entry_key_bytes);\n"
                            

                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_key(chip_id, entry, entry_key), ret, result);\n" % (regList[0]._table_struct_name.lower())
                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_data(chip_id, entry, entry_key), ret, result);\n" % (regList[0]._table_struct_name.lower())

                            str += "\n    ret = soc_set_hash_tab(chip_id, %sm, 0, entry_key, NULL);\n" % (regList[0]._table_struct_name.upper())

                            str += "\nresult:\n"
                            str += "\n    sal_free(entry_key);\n"                            
                            str += "    return ret;\n"
                            str += "}\n\n"

                            
                            # get function
                            str += "sf_status_t soc_groot_get_%s(uint32_t chip_id, soc_groot_%s_t *entry)\n{\n" % (regList[0]._table_struct_name.lower(), regList[0]._table_struct_name.lower())

                            str += "    sf_status_t ret = SF_E_NONE;\n"
                            str += "    uint8_t *entry_key          = NULL;\n"
                            
                            str += "    uint16_t entry_key_bytes    = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[0]._table_struct_name.upper())
                            
                            str += "    SF_IF_NULL_RETURN(entry);\n"
                                
                            str += "    entry_key = sal_malloc(entry_key_bytes, SOC_SERV_REG_TAB_NAME);\n"                            
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_key, ret, result);\n"
                            str += "    sal_memset(entry_key, 0, entry_key_bytes);\n"

                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_key(chip_id, entry, entry_key), ret, result);\n\n" % (regList[0]._table_struct_name.lower())                            
                            str += "    ret = soc_get_hash_tab(chip_id, %sm, 0, entry_key, NULL);\n\n" % (regList[0]._table_struct_name.upper())
                            str += "    soc_groot_data_TO_%s(chip_id, entry, entry_key);\n\n" % (regList[0]._table_struct_name.lower())
                                
                            str += "\nresult:\n"
                            str += "\n    sal_free(entry_key);\n"                            
                            str += "    return ret;\n"
                            str += "}\n\n"

                            f.write(str)
                            

                        else: # if direct table in table pool
                                            
                            reg = 0
                            fieldList = regList[reg]._regFieldList[0][1]
                            
                            # soc_xxx_TO_data function
                            str  = "sf_status_t soc_groot_%s_TO_data(uint32_t chip_id, soc_groot_%s_t *entry, uint8_t *entry_data)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                            str += "    SF_IF_NULL_RETURN(entry_data);\n\n"
                                
                            for fd in range(len(fieldList)):
                                field = fieldList[fd]
                                if field.fieldName.upper() == "RESERVED":
                                    continue

                                str += self.get_the_function_string(regList[reg], field, "set", "NULL")
                                
                            str += "\n    return SF_E_NONE;\n"
                            str += "}\n\n"


                            # soc_data_TO_xxx function
                            str += "sf_status_t soc_groot_data_TO_%s(uint32_t chip_id, soc_groot_%s_t *entry, uint8_t *entry_data)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                            str += "    SF_IF_NULL_RETURN(entry_data);\n\n"
                            
                            for fd in range(len(fieldList)):
                                field = fieldList[fd]
                                if field.fieldName.upper() == "RESERVED":
                                    continue

                                str += self.get_the_function_string(regList[reg], field, "get", "NULL")
                                
                            str += "\n    return SF_E_NONE;\n"
                            str += "}\n\n"


                            # soc_set_xxx function
                            str += "sf_status_t soc_groot_set_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())
                            str += "    sf_status_t ret = SF_E_NONE;\n"
                            str += "    uint8_t *entry_data = NULL;\n"
                            
                            str += "    uint16_t tab_bytes = soc_get_tab_length_by_bytes(chip_id, %sm);\n\n" % (regList[reg]._table_struct_name.upper())
                            str += "    SF_IF_NULL_RETURN(entry);\n"
                            str += "    entry_data = sal_malloc(tab_bytes, SOC_SERV_REG_TAB_NAME);\n"
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_data, ret, result);\n"
                            str += "    sal_memset(entry_data, 0, tab_bytes);\n\n"
                                                    
                            str += "    SF_ERROR_GOTO(soc_groot_%s_TO_data(chip_id, entry, entry_data), ret, result);\n" % (regList[reg]._table_struct_name.lower())

                            str += "\n    ret = soc_set_direct_tab(chip_id, index, %sm, entry_data);\n" % (regList[reg]._table_struct_name.upper())

                            str += "\nresult:\n"
                            str += "    sal_free(entry_data);\n"
                            str += "    return ret;\n"
                            str += "}\n\n"

                            # soc_mem_array_set_xxx function
                            str += "sf_status_t soc_groot_mem_array_set_%s(uint32_t chip_id, uint32_t index_min, uint32_t index_max, soc_groot_%s_t *entry)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())

                            str += "    sf_status_t ret = SF_E_NONE;\n"
                            str += "    uint8_t *array_data = NULL;\n"
                            str += "    uint16_t index = 0;\n"
                            str += "    uint16_t single_entry_length = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[reg]._table_struct_name.upper())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                            str += "    array_data = sal_malloc(single_entry_length*(index_max - index_min + 1), SOC_SERV_REG_TAB_NAME);\n\n"
                            str += "    SF_GOTO_LABEL_IF_NULL(array_data, ret, result);\n"
                            str += "    sal_memset(array_data, 0, single_entry_length*(index_max - index_min + 1));\n"
                                                    
                            str += "    for (index = 0; index < (index_max - index_min + 1); ++index)\n"
                            str +="    {\n"
                            str += "        SF_ERROR_GOTO(soc_groot_%s_TO_data(chip_id, &entry[index], array_data + single_entry_length * index), ret, result);\n" % (regList[reg]._table_struct_name.lower())
                            str +="    }\n\n"
                           
                            str += "    ret = soc_mem_array_write_range(chip_id, %sm, index_min, index_max, array_data);\n" % (regList[reg]._table_struct_name.upper())

                            str += "\nresult:\n"
                            str += "    sal_free(array_data);\n"
                            str += "    return ret;\n"
                            str += "}\n\n"
                            
                            f.write(str)


                            # soc_get_xxx function
                            str = "sf_status_t soc_groot_get_%s(uint32_t chip_id, uint32_t index, soc_groot_%s_t *entry)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())

                            str += "    sf_status_t ret = SF_E_NONE;\n"
                            str += "    uint8_t *entry_data = NULL;\n"
                            str += "    uint16_t tab_bytes = soc_get_tab_length_by_bytes(chip_id, %sm);\n\n" % (regList[reg]._table_struct_name.upper())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                            str += "    entry_data = sal_malloc(tab_bytes, SOC_SERV_REG_TAB_NAME);\n"
                            str += "    SF_GOTO_LABEL_IF_NULL(entry_data, ret, result);\n"
                            str += "    sal_memset(entry_data, 0, tab_bytes);\n\n"
                            
                            str += "    SF_ERROR_GOTO(soc_get_direct_tab(chip_id, index, %sm, entry_data), ret, result);\n\n" % (regList[reg]._table_struct_name.upper())
                            
                            str += "    soc_groot_data_TO_%s(chip_id, entry, entry_data);\n" % (regList[reg]._table_struct_name.lower())

                            str += "\nresult:\n"
                            str += "    sal_free(entry_data);\n"
                            str += "    return ret;\n"
                            str += "}\n\n"

                            # soc_mem_array_get_xxx function
                            str += "sf_status_t soc_groot_mem_array_get_%s(uint32_t chip_id, uint32_t index_min, uint32_t index_max, soc_groot_%s_t *entry)\n{\n" % (regList[reg]._table_struct_name.lower(), regList[reg]._table_struct_name.lower())

                            str += "    sf_status_t ret = SF_E_NONE;\n"
                            str += "    uint8_t *array_data = NULL;\n"
                            str += "    uint16_t index = 0;\n"
                            str += "    uint16_t single_entry_length = soc_get_tab_length_by_bytes(chip_id, %sm);\n" % (regList[reg]._table_struct_name.upper())

                            str += "    SF_IF_NULL_RETURN(entry);\n"
                            str += "    array_data = sal_malloc(single_entry_length*(index_max - index_min + 1), SOC_SERV_REG_TAB_NAME);\n\n"
                            str += "    SF_GOTO_LABEL_IF_NULL(array_data, ret, result);\n"
                            str += "    sal_memset(array_data, 0, single_entry_length*(index_max - index_min + 1));\n"

                            str += "    SF_ERROR_GOTO(soc_mem_array_read_range(chip_id, %sm, index_min, index_max, array_data), ret, result);\n" % (regList[reg]._table_struct_name.upper())
                            
                            str += "    for (index = 0; index < (index_max - index_min + 1); ++index)\n"
                            str +="    {\n"
                            str += "        soc_groot_data_TO_%s(chip_id, &entry[index], array_data + single_entry_length * index);\n" % (regList[reg]._table_struct_name.lower())
                            str +="    }\n\n"

                            str += "\nresult:\n"
                            str += "    sal_free(array_data);\n"
                            str += "    return ret;\n"
                            str += "}\n\n"
                            
                            f.write(str)


    def GenerateAllAPI(self, objDict, soc):
        print "Generate the Api  File."

        if soc != "": # if soc not been given, we can't give the prefix for the field name
            soc = soc + "_"
    
        f_reg        = file("./tmp/soc_groot_reg.c", 'w')
        f_direct     = file("./tmp/soc_groot_direct.c", 'w')
        f_hash_tcam  = file("./tmp/soc_groot_hash_tcam.c", 'w')
        f_table_pool = file("./tmp/soc_groot_table_pool.c", 'w')


        self.GenerateRegApi         (f_reg,         objDict, soc)
        self.GenerateDirectTabApi   (f_direct,      objDict, soc)
        self.GenerateHashTcamTabApi (f_hash_tcam,   objDict, soc)
        self.GenerateTablePoolApi   (f_table_pool,  objDict, soc)

        f_reg.close()
        f_direct.close()
        f_hash_tcam.close()
        f_table_pool.close()



        
    def is_in_sameNameTabList(self, table_struct_name):
        
        for item in self.sameNameTabList:
            if table_struct_name.upper() == item[1].upper():
                return (item[0], item[2])
        return [[], []]


    def is_in_sameNameRegList(self, reg_name):
        
        for item in self.sameNameRegList:
            if reg_name.upper() == item[1].upper():
                return (item[0], item[2])
        return [[], []]






    def GenerateAllRegAndTableSymbol(self, objDict, soc):        
        print "Generate the allsymbol.h File."

        if soc != "": # if soc not been given, we can't give the prefix for the field name
            soc = soc + "_"
                    
        f = file("./tmp/soc_groot_allsymbol.h", 'w')


        time_ = ("%s-%s-%s %d:%d:%d" % (time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday, time.gmtime().tm_hour ,time.gmtime().tm_min ,time.gmtime().tm_sec))
                
        str = """
/** @file 
  * @note Shenzhen Forward Industry Co.Ltd - Copyright (c) 2017.
  * @brief    
  * 
  * @author   lijun
  * @date     %s
  * @version  1.0
  * 
  * @note     THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANUALLY!!! 
  * $LastChangedDate$
  * $LastChangedRevision$
  * $LastChangedBy$
  */
"""  % ("")

        f.write(str)
        
        f.write("\n#ifdef SF_GROOT_SUPPORT\n")

        f.write("#ifndef __SOC_GROOT_ALLSYMBOL_H__\n")
        f.write("#define __SOC_GROOT_ALLSYMBOL_H__\n\n")

        f.write("\n\n\n //################ table id  ################################### \n\n\n")

        i = 0
        iterated_list = []
        for mode in objDict:            
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]                
                for reg in range(len(regList)):

                    if regList[reg]._table_struct_name.upper() in iterated_list:
                        continue

                    iterated_list.append(regList[reg]._table_struct_name.upper())
                    
                    # assume no table need expand with the prefix "sheetname"
                    f.write("#define %sm %d\n" % (regList[reg]._table_struct_name.upper(), i))                    
                    i +=1

        for tab in self.physical_table_list:
            f.write("#define %sm %d\n" % (tab._table_struct_name.upper(), i))                    
            i +=1

        f.write("#define SF9564_MAX_TABLE_ID %d\n" % (i))
        
        self.max_table_id  = i


                
        f.write("\n\n\n //################## register id ################################# \n\n\n")
        i = 0


        regList = self.reg_list

        table_pool_reg_list = []
        
        for reg in range(len(regList)):

            # regs in table pool only need one object
            if regList[reg]._modeName in table_pool_dict:                

                if regList[reg]._old_regName.upper() in table_pool_reg_list:
                    continue
                table_pool_reg_list.append(regList[reg]._old_regName.upper())

                id_ = "TABLEPOOL_" + regList[reg]._old_regName.upper()                

            else :
                id_ = regList[reg]._regName.upper()
                
            
            f.write("#define %sr %d\n" % (id_, i))                                
            i +=1


        f.write("#define SF9564_MAX_REG_ID %d\n" % (i))
        
        self.max_reg_id    = i



        f.write("\n\n\n //################## field id ################################# \n\n\n")
        i = 0
        for fd_name in self.allFieldNameList:
            f.write("#define %sf %d\n" % (fd_name.upper(), i))
            i +=1
            
        f.write("#define MAX_FIELD_ID %d\n" % (i))

        self.max_field_id  = i

        f.write("#endif\n")
        
        f.write("""\n#endif /* SF_GROOT_SUPPORT */\n""")
        
        f.close()


       
       
    def reconstruct_the_reg_table_and_create_unique_name_for_same_mode(self, objDict, soc):
        
        print "reconstruct_the_reg_table_and_create_unique_name_for_same_mode.. \n"

        objDict__ = copy.deepcopy(objDict)
        
        new_reg_list = []
        iterated_list = []        
        for mode in objDict:            
            if objDict[mode][1][0] > 0:
                regList = objDict[mode][1][1]                
                for reg in range(len(regList)):
                    
                    if regList[reg]._regName.upper() in iterated_list:  
                        continue                    

                    iterated_list.append(regList[reg]._regName.upper())
                    
                    (sameNameRegModeList, same_name_reg_list) = self.is_in_sameNameRegList(regList[reg]._regName.upper())

                    
                    if sameNameRegModeList != []:
                        
                        if regList[reg]._regName.upper() in multi_addr_reg_list: # no expand, multi-addr                            
                            baseAddr_list = []
                            BaseOffsetAddr = []
                            for reg_i in same_name_reg_list:
                                baseAddr_list += reg_i._regBaseAddr # merge the base address to one list, then the register will be only show in one mode.

                                # expand the base-offset address pair. Because some registers have different base and offset.
                                for base in reg_i._regBaseAddr:
                                    BaseOffsetAddr.append([base, reg_i._regOffsetAddr])
                                
                            temp_reg = copy.deepcopy(regList[reg])
                            temp_reg._regBaseAddr = baseAddr_list
                            temp_reg._regBaseOffsetAddr = BaseOffsetAddr
                            new_reg_list.append(temp_reg)

                            """
                            # only one mode can have the register. set the register only can through the one mode.
                            for mode__ in sameNameRegModeList:     
                                if mode__ == mode:
                                    continue
                                
                                if objDict__[mode__][1][0] > 0:                                    
                                    for reg__ in range(len(objDict__[mode__][1][1])):
                                        if objDict__[mode__][1][1][reg__]._regName == regList[reg]._regName:                                            
                                            objDict__[mode__][1][1].pop(reg__)
                                            objDict__[mode__][1][0] -= 1
                                            break
                            """
                            
                        else: # expand                            
                            for reg_i in same_name_reg_list:
                                temp_reg = copy.deepcopy(reg_i)
                                temp_reg._regName = temp_reg._old_sheetName + "_" + temp_reg._regName                                
                                new_reg_list.append(temp_reg)

                            # expand it name in different mode
                            for mode__ in sameNameRegModeList:
                                if objDict__[mode__][1][0] > 0:                                    
                                    for reg__ in objDict__[mode__][1][1]:
                                        if reg__._regName == regList[reg]._regName:
                                            reg__._regName = reg__._old_sheetName + "_" + reg__._regName
                                            
                                                                
                    else: # single addr
                        temp_reg = copy.deepcopy(regList[reg])                        
                        new_reg_list.append(temp_reg)



        new_tab_list = []
        iterated_list = []
        for mode in objDict:            
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]                
                for reg in range(len(regList)):

                    if regList[reg]._table_struct_name.upper() in iterated_list:
                        continue

                    iterated_list.append(regList[reg]._table_struct_name.upper())
                    
                    (sameNameTabModeList, same_name_tab_list) = self.is_in_sameNameTabList(regList[reg]._table_struct_name.upper())                    


                    if sameNameTabModeList != []:
                        # we assume all table is multi-addr, no expand
                        if 1 == 1 : # regList[reg]._regName.upper() in multi_addr_tab_list: # no expand, multi-addr                            
                            baseAddr_list = []
                            BaseOffsetAddr = []                            
                            for reg_i in same_name_tab_list:
                                baseAddr_list += reg_i._regBaseAddr # merge the base address to one list
                                
                                # expand the base-offset address pair. Because some table have different base and offset.                                
                                for base in reg_i._regBaseAddr:
                                    BaseOffsetAddr.append([base, reg_i._regOffsetAddr])
                                
                            temp_reg = copy.deepcopy(regList[reg])
                            temp_reg._regBaseAddr = baseAddr_list
                            temp_reg._regBaseOffsetAddr = BaseOffsetAddr
                            new_tab_list.append(temp_reg)
                            
                                                        
                            """
                            # only one mode can have the register. set the register only can through the one mode.
                            for mode__ in sameNameTabModeList:                                
                                if mode__ == mode:
                                    continue
                                
                                if objDict__[mode__][2][0] > 0:
                                    for reg__ in range(len(objDict__[mode__][2][1])):
                                        if objDict__[mode__][2][1][reg__]._regName == regList[reg]._regName:
                                            objDict__[mode__][2][1].pop(reg__)
                                            objDict__[mode__][2][0] -= 1
                                            break
                            """

                            
                        else: # if expand, for hash_tcam, we can not know the relationship between key and data table. so , we can't expand
                            print "expand the table %s " % regList[reg]._regName.upper()
                            for reg_i in same_name_tab_list:
                                temp_reg = copy.deepcopy(reg_i)
                                temp_reg._regName = temp_reg._old_sheetName + "_" + temp_reg._regName                                
                                new_tab_list.append(temp_reg)

                            # expand it name in different mode
                            for mode__ in sameNameTabModeList:
                                if objDict__[mode__][2][0] > 0:                                    
                                    for reg__ in objDict__[mode__][2][1]:
                                        if reg__._regName == regList[reg]._regName:
                                            reg__._regName = reg__._old_sheetName + "_" + reg__._regName


                    else: # single addr
                        BaseOffsetAddr = []
                        # expand the base-offset address pair. Because some table have different base and offset.                                
                        for base in regList[reg]._regBaseAddr:
                            BaseOffsetAddr.append([base, regList[reg]._regOffsetAddr])
                            
                        temp_reg = copy.deepcopy(regList[reg])
                        temp_reg._regName = temp_reg._table_struct_name
                        temp_reg._regBaseOffsetAddr = BaseOffsetAddr
                        new_tab_list.append(temp_reg)
                        

        self.reg_list = new_reg_list
        self.tab_list = new_tab_list

        return (new_reg_list, new_tab_list, objDict__)


       
    def reconstruct_the_reg_table(self, objDict, soc):
        
        print "reconstruct the reg and table... \n"
        
        new_reg_list = []
        iterated_list = []        
        for mode in objDict:            
            if objDict[mode][1][0] > 0:
                regList = objDict[mode][1][1]                
                for reg in range(len(regList)):
                    
                    if regList[reg]._regName.upper() in iterated_list:                        
                        continue                    

                    iterated_list.append(regList[reg]._regName.upper())
                    
                    (sameNameRegModeList, same_name_reg_list) = self.is_in_sameNameRegList(regList[reg]._regName.upper())

                    
                    if sameNameRegModeList != []:
                        
                        if regList[reg]._regName.upper() in multi_addr_reg_list: # no expand, multi-addr                            
                            baseAddr_list = []
                            for reg_i in same_name_reg_list:
                                baseAddr_list += reg_i._regBaseAddr # merge the base address to one list

                            temp_reg = copy.deepcopy(regList[reg])
                            temp_reg._regBaseAddr = baseAddr_list 
                            new_reg_list.append(temp_reg)
                                
                        else: # expand                            
                            for reg_i in same_name_reg_list:
                                temp_reg = copy.deepcopy(reg_i)
                                temp_reg._regName = temp_reg._old_sheetName + "_" + temp_reg._regName                                
                                new_reg_list.append(temp_reg)                                
                                
                    else: # single addr
                        temp_reg = copy.deepcopy(regList[reg])                        
                        new_reg_list.append(temp_reg)



        new_tab_list = []
        iterated_list = []
        for mode in objDict:            
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]                
                for reg in range(len(regList)):

                    if regList[reg]._table_struct_name.upper() in iterated_list:
                        continue

                    iterated_list.append(regList[reg]._table_struct_name.upper())
                    
                    (sameNameTabModeList, same_name_tab_list) = self.is_in_sameNameTabList(regList[reg]._table_struct_name.upper())                    


                    if sameNameTabModeList != []:
                        
                        # assume no expand, all multi-addr                             
                        baseAddr_list = []
                        for reg_i in same_name_tab_list:
                            baseAddr_list += reg_i._regBaseAddr # merge the base address to one list

                        temp_reg = copy.deepcopy(regList[reg])
                        temp_reg._regName = temp_reg._table_struct_name
                        temp_reg._regBaseAddr = baseAddr_list
                        new_tab_list.append(temp_reg)
                                
                    else: # single addr
                        temp_reg = copy.deepcopy(regList[reg])                        
                        temp_reg._regName = temp_reg._table_struct_name                        
                        new_tab_list.append(temp_reg)
                        

        self.reg_list = new_reg_list
        self.tab_list = new_tab_list

        return (new_reg_list, new_tab_list)


   
    def find_same_reg_in_different_mode_by_name(self, sameModeObjsDict, name, sameNameList, i):
          
        for item in sameNameList:
            if name == item[1] :
                return [[], []]

        modes = []
        reg_list = []
        j = -1
        for mode in sameModeObjsDict:
            j = j+1
            if j < i:                
                continue
            
            # for reg
            for reg in sameModeObjsDict[mode][1][1]:                
                if reg._regName == name:
                    #mode__ = "%s->" % reg._excelName + mode
                    mode__ = mode
                    modes.append(mode__)
                    reg_list.append(reg)
                    break

        return (modes, reg_list)


    def is_in_table_excel(self, name):

        if name.find("egress_table_csr") != -1 :
            return 1            
        if name.find("hirar_table_csr") != -1 :
            return 1
        if name.find("ingress1_table_csr") != -1 :
            return 1
        if name.find("ingress2_table_csr") != -1 :
            return 1
        if name.find("ingress3_table_csr") != -1 :
            return 1
        if name.find("tcam_wrapper_CSR") != -1 :
            return 1
        
        return 0

    def show_the_same_name_register_in_different_mode(self, sameModeObjsDict, soc):
        print "show_the_same_name_register_in_different_mode "
        i = -1
        
        for mode in sameModeObjsDict:
            i = i+1
            for reg in sameModeObjsDict[mode][1][1]:                
                #if self.is_in_table_excel(reg._excelName) == 1:                    
                #    continue                    
                                
                (modes, reg_list) = self.find_same_reg_in_different_mode_by_name(sameModeObjsDict, reg._regName, self.sameNameRegList, i)                
                                
                if len(modes) > 1:                    
                    item = [modes, reg._regName, reg_list]                                        
                    self.sameNameRegList.append(item)


        f = file("./tmp/" + soc + "_" + 'same_name_reg_in_different_mode', 'w')
        for i in range(200):            
            f.write("########## Register in %d modes\n" % i)
            for item in self.sameNameRegList:
                if len(item[0]) == i:
                    str  =  "reg %-40s \n" % item[1]
                    str += "%s \n" % item[0]
                    for reg in item[2]:
                        #str += "%s --- > %s\n" % (reg._sheetName, reg._regName)
                        pass
                    str += "\n"
                    f.write(str)


        f.close()

        

    def find_same_table_in_different_mode_by_struct_name(self, sameModeObjsDict, table_struct_name, sameNameList, i):

        for item in sameNameList:
            if table_struct_name == item[1] :
                return [[], []]

        modes = []
        tab_list = []
        j = -1
        for mode in sameModeObjsDict:
            j = j+1
            if j < i:                
                continue
            
            # for table
            for reg in sameModeObjsDict[mode][2][1]:                
                if reg._table_struct_name == table_struct_name:
                    #mode__ = "%s->" % reg._excelName + mode
                    mode__ = mode
                    modes.append(mode__)
                    tab_list.append(reg)
                    break

        return (modes, tab_list)
    

    def show_the_same_name_table_in_different_mode(self, sameModeObjsDict, soc):        
        print "show_the_same_name_table_in_different_mode"
        i = -1
        
        for mode in sameModeObjsDict:
            i = i+1
            for reg in sameModeObjsDict[mode][2][1]:                
                (modes, tab_list) = self.find_same_table_in_different_mode_by_struct_name(sameModeObjsDict, reg._table_struct_name, self.sameNameTabList, i)
                
                
                if len(modes) > 1:                    
                    item = [modes, reg._table_struct_name, tab_list]                    
                    self.sameNameTabList.append(item)                    

        f = file("./tmp/" + soc + "_" + 'same_name_table_in_different_mode', 'w')
        
        
        for i in range(100):            
            f.write("########## table in %d modes\n" % i)
            for item in self.sameNameTabList:
                if len(item[0]) == i:
                    str  =  "tab %-40s \n" % item[1]
                    str += "%s \n\n" % item[0]
                    f.write(str)              

        
        f.close()
       
      

    def get_all_filed_in_regs_and_tables(self, objDict, soc):

        print "get_all_filed_in_regs_and_tables ...\n"
        
        allFieldNameList = []

        
        for mode in objDict:            
            if objDict[mode][1][0] > 0:
                regList = objDict[mode][1][1]
                for reg in range(len(regList)):        
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        if field._fieldName.lower() not in allFieldNameList:
                            allFieldNameList.append(field._fieldName.lower())

        for mode in objDict:            
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]
                for reg in range(len(regList)): # regList only have one table. (but the table maybe divided to key or data table.)
                    
                    fieldInfoList = regList[reg]._regFieldList
                    nKeyType = len(fieldInfoList)
                    
                    if nKeyType > 1:
                        continue                  

                    else:
                        fieldList = regList[reg]._regFieldList[0][1]                        
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            if field._fieldName.lower() not in allFieldNameList:
                                allFieldNameList.append(field._fieldName.lower())                            

        # deal with the table with different key type
        for mode in objDict:            
            if objDict[mode][2][0] > 0:
                regList = objDict[mode][2][1]
                for reg in range(len(regList)):
                    
                    fieldInfoList = regList[reg]._regFieldList
                    nKeyType = len(fieldInfoList)
                    
                    if nKeyType == 1:
                        continue

                    else:
                        for info in fieldInfoList :
                            key = info[0]
                            fieldList = info[1]
                    
                            for fd in range(len(fieldList)):
                                field = fieldList[fd]
                                if field._fieldName.lower() not in allFieldNameList:
                                    allFieldNameList.append(field._fieldName.lower())


        f = file("./tmp/" + soc + "_" + 'all_field_name', 'w')                  
        for name in allFieldNameList:                
            f.write("%sf\n" % name.upper())
        f.close()


        self.allFieldNameList = allFieldNameList


    def get_reg_type(self, type):

        if type not in self.reg_type_list:
            self.reg_type_list.append(type)            
        
        #type_list = ["SOC_REG_RW",    "SOC_REG_RO",   "SOC_REG_IPSC", "SOC_REG_IPSC2", "SOC_REG_BPSC", "SOC_REG_BPSC2", "SOC_REG_NTWC", "SOC_REG_LOGF", "SOC_REG_LOGL",  "SOC_REG_TAB", "SOC_REG_CAM"]

        if type == "R0" : # some error in the excel
            type = "RO"

        if type == "":
            type = "UNKNOWN"
            
        return "SOC_REG_" + type



    def get_tab_type(self, type):

        if type not in self.tab_type_list:
            self.tab_type_list.append(type)            
        
        #type_list = ["SOC_TAB_DIRECT", "SOC_TAB_HASH", "SOC_TAB_TCAM"]

        if type in ["DIRECT", "TCAM", "HASH", ]:
            return "SOC_TAB_" + type
        
        if type == "CAM":
            return "SOC_TAB_TCAM"


        return "SOC_TAB_DIRECT"


    def get_reg_default_value(self, reg):

        default = 0
        fieldList = reg._regFieldList
        for fd in fieldList:            
            default = default | (fd._default<<fd._fieldBp)
        #if default != 0:
        #    print "%s --- %s ---- %s = %x" % (reg._excelName, reg._sheetName, reg._regName, default) 
        return default

    def GenerateAllRegFile(self, reg_list, soc):
        print "Generate the allreg.h File."

        if soc != "": # if soc not been given, we can't give the prefix for the field name
            soc = soc + "_"
            
        f = file("./tmp/" + soc + 'allreg.h', 'w')

        time_ = ("%s-%s-%s %d:%d:%d" % (time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday, time.gmtime().tm_hour ,time.gmtime().tm_min ,time.gmtime().tm_sec))
                
        str = """
/** @file 
  * @note Shenzhen Forward Industry Co.Ltd - Copyright (c) 2017.
  * @brief    
  * 
  * @author   lijun
  * @date     %s
  * @version  1.0
  * 
  * @note     THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANUALLY!!! 
  * $LastChangedDate$
  * $LastChangedRevision$
  * $LastChangedBy$
  */
"""  % ("")

        f.write(str)      

        f.write("\n#ifdef SF_9564\n")
        

        f.write("#ifndef __SF9564_ALLREG_H__\n")
        f.write("#define __SF9564_ALLREG_H__\n\n")

        f.write("\n#include \"./soc/service/reg_tab/soc_field.h\"\n")
        f.write("\n#include \"./soc/service/reg_tab/soc_register.h\"\n")
        f.write("\n#include \"./soc/service/reg_tab/groot/soc_groot_allfield.h\"\n")


        """            
        regList = []
        # import extern variable field
        if 1 == 1:            
            if 1 == 1:
                regList = reg_list
                for reg in range(len(regList)):
                    f.write("extern soc_field_info_t %sf[];\n" %((regList[reg]._regName).lower()))

        f.write("\n\n")

        """


        table_pool_reg_list = []
        # create the address 
        if 1 == 1:            
            if 1 == 1:
                regList = reg_list                
                for reg in regList:

                    if reg._modeName in table_pool_dict:                

                        if reg._old_regName.upper() in table_pool_reg_list:
                            continue
                        table_pool_reg_list.append(reg._old_regName.upper())

                        reg_name = "TABLEPOOL_" + reg._old_regName.upper()                

                    else :
                        reg_name = reg._regName.upper()

                    if reg._regName.upper() in multi_addr_reg_list: # multi-addr
                        
                        f.write("soc_csr_addr_t %s_addr[] = \n{\n" %(reg_name.lower()))        
                        for addr in range(len(reg._regBaseOffsetAddr)):                        
                            str = "    {%d, 0x%x, 0x%x},\n" % (reg._reg_bar, reg._regBaseOffsetAddr[addr][0], reg._regBaseOffsetAddr[addr][1])
                            
                            if addr + 1 == len(reg._regBaseOffsetAddr):
                                str = "    {%d, 0x%x, 0x%x}\n" % (reg._reg_bar, reg._regBaseOffsetAddr[addr][0], reg._regBaseOffsetAddr[addr][1])
                            f.write(str)
            
                        f.write("};\n\n")

                    else:

                        f.write("soc_csr_addr_t %s_addr[] = \n{\n" %(reg_name.lower()))        
                        for addr in range(len(reg._regBaseAddr)):                        
                            str = "    {%d, 0x%x, 0x%x},\n" % (reg._reg_bar, reg._regBaseAddr[addr], reg._regOffsetAddr)
                            
                            if addr + 1 == len(reg._regBaseAddr):
                                str = "    {%d, 0x%x, 0x%x}\n" % (reg._reg_bar, reg._regBaseAddr[addr], reg._regOffsetAddr)
                            f.write(str)
            
                        f.write("};\n\n")
                        



        table_pool_reg_list = []
        f.write("\n\n")
        # create the register     
        if 1 == 1:            
            if 1 == 1:
                regList = reg_list                
                for reg in regList:

                    if reg._modeName in table_pool_dict:                

                        if reg._old_regName.upper() in table_pool_reg_list:
                            continue
                        table_pool_reg_list.append(reg._old_regName.upper())

                        reg_name = "TABLEPOOL_" + reg._old_regName.upper()                

                    else :
                        reg_name = reg._regName.upper()

                    
                    reg_type = self.get_reg_type(reg._regType.upper())

                    default_value = self.get_reg_default_value(reg)
                    
                    str = "soc_reg_info_t %s_reg  = {\"%s\", %s, %s, %d, %s_addr, %d, %sf, 0, NULL, %dULL};\n" % (reg_name.upper(), reg_name.lower(), reg_type, reg._reg_flag, len(reg._regBaseAddr),reg_name.lower(), len(reg._regFieldList), reg_name.lower(), default_value)
                    f.write(str)
        
        #print self.reg_type_list
        
        # create the soc_sf9564_reg_list
        f.write("\nsoc_reg_info_t *soc_sf9564_reg_list[SF9564_MAX_REG_ID] = {\n")

        table_pool_reg_list = []
        i = 0
        if 1 == 1:            
            if 1 == 1:
                regList = reg_list
                for reg in range(len(regList)):
                    
                    if regList[reg]._modeName in table_pool_dict:                

                        if regList[reg]._old_regName.upper() in table_pool_reg_list:
                            continue
                        table_pool_reg_list.append(regList[reg]._old_regName.upper())

                        reg_name = "TABLEPOOL_" + regList[reg]._old_regName.upper()                

                    else :
                        reg_name = regList[reg]._regName.upper()

                    
                    #f.write("%d  %d   &%s_reg,\n" % (self.max_reg_id, i, regList[reg]._regName.upper()))
                    if i < self.max_reg_id - 1:
                        f.write("    &%s_reg,\n" % (reg_name.upper()))
                        i +=1
                    else:
                        f.write("    &%s_reg\n};\n" % (reg_name.upper()))


        f.write("#endif\n")

        f.write("""\n#endif /* SF_9564 */\n""")
        
        f.close()

        

    def GenerateAllMemFile(self, tab_list, soc):
        print "Generate the alltable.h File."

        if soc != "": # if soc not been given, we can't give the prefix for the field name
            soc = soc + "_"
            
        f = file("./tmp/" + soc + 'alltable.h', 'w')
        
        time_ = ("%s-%s-%s %d:%d:%d" % (time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday, time.gmtime().tm_hour ,time.gmtime().tm_min ,time.gmtime().tm_sec))
                
        str = """
/** @file 
  * @note Shenzhen Forward Industry Co.Ltd - Copyright (c) 2017.
  * @brief    
  * 
  * @author   lijun
  * @date     %s
  * @version  1.0
  * 
  * @note     THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANUALLY!!! 
  * $LastChangedDate$
  * $LastChangedRevision$
  * $LastChangedBy$
  */
"""  % ("")

        f.write(str)      

        f.write("\n#ifdef SF_9564\n")
        
        f.write("#ifndef __SF9564_ALLTAB_H__\n")
        f.write("#define __SF9564_ALLTAB_H__\n\n")


        f.write("\n#include \"./soc/service/reg_tab/soc_field.h\"\n")
        f.write("\n#include \"./soc/service/reg_tab/soc_table.h\"\n")
        f.write("\n#include \"./soc/service/reg_tab/groot/soc_groot_allfield.h\"\n")
        

        #f.write("\n#include \"table_depth.h\" \n\n")


        """
        # below if is to store the info of key type for a table which have different keytypes
        for struct_name in key_type_field_info_dict:            
            f.write("extern soc_field_info_t %s_keytype_f;\n" %((struct_name).lower()))  


        regList = []
        # import extern variable field
        if 1 == 1:     
            if 1 == 1:
                regList = tab_list               
                for reg in range(len(regList)):
                    
                    nKeyType = len(regList[reg]._regFieldList)
                    if nKeyType == 1:
                        f.write("extern soc_field_info_t %sf[];\n" %((regList[reg]._regName).lower()))
                    else :
                        for info in regList[reg]._regFieldList:
                            key = info[0]
                            f.write("extern soc_field_info_t %s_%sf[];\n" %((regList[reg]._regName).lower(), key))

        """
        

        f.write("\n\n")
        # create the address 
        if 1 == 1:            
            if 1 == 1:
                regList = tab_list                
                for reg in regList:
                    f.write("soc_csr_addr_t %s_addr[] = \n{\n" %(reg._regName.lower()))        
                    for addr in range(len(reg._regBaseOffsetAddr)):                        
                        str = "    {%d, 0x%x, 0x%x},\n" % (reg._reg_bar, reg._regBaseOffsetAddr[addr][0], reg._regBaseOffsetAddr[addr][1])
                        
                        if addr + 1 == len(reg._regBaseOffsetAddr):
                            str = "    {%d, 0x%x, 0x%x}\n" % (reg._reg_bar, reg._regBaseOffsetAddr[addr][0], reg._regBaseOffsetAddr[addr][1])
                        f.write(str)
        
                    f.write("};\n\n")

                for reg in self.physical_table_list:
                    f.write("soc_csr_addr_t %s_addr[] = \n{\n" %(reg._regName.lower()))
                    f.write("    {%d, 0x%x, 0x%x}\n" % (reg._reg_bar, reg._regBaseAddr[0], reg._regOffsetAddr))
                    f.write("};\n\n")
                    


        f.write("\n\n")
        # create the table fileds info
        if 1 == 1:     
            if 1 == 1:
                regList = tab_list

                #if mode == "CB_CNT":
                #    for _reg in  regList :
                #        print "%s  %s  %s  %s " % (_reg._excelName, _reg._sheetName, _reg._regName, _reg._regFieldList)

                for reg in range(len(regList)):
                    
                    nKeyType = len(regList[reg]._regFieldList)
                    if nKeyType == 1:
                        key = "0"
                        table_witdh = regList[reg]._regFieldList[0][2]
                        if regList[reg]._regFieldList[0][0] != "NULL":
                            key = copy.deepcopy(regList[reg]._regFieldList[0][0])

                        str = "soc_tab_fields_info_t %smf[]  = {\n    {%s, %d, %d, %sf}\n};\n\n" % (regList[reg]._regName.lower(), key, table_witdh, len(regList[reg]._regFieldList[0][1]), (regList[reg]._regName).lower())
                        f.write(str)
                        
                    else :

                        f.write("soc_tab_fields_info_t %smf[]  = {\n" %(regList[reg]._regName.lower()))                        

                        len_ = 0
                        for info in regList[reg]._regFieldList:
                            key = info[0]
                            table_witdh = info[2]
                            
                            str = "    { %s, %d, %d, %s_%sf},\n" % (key, table_witdh, len(info[1]), regList[reg]._regName.lower(), key)
                            
                            len_ += 1
                            if len_ == len(regList[reg]._regFieldList):
                                str = "    { %s, %d, %d, %s_%sf}\n" % (key, table_witdh, len(info[1]), regList[reg]._regName.lower(), key)
                            f.write(str)

                        f.write("};\n\n")

        f.write("\n\n")
        # initialize all the table
        if 1 == 1:     
            if 1 == 1:
                regList = tab_list
                for reg in regList:                        
                    nKeyType = len(reg._regFieldList)
                    if nKeyType == 1 or (reg._table_struct_name.upper() in no_key_type_field_info_dict):
                        key_type_fields = "NULL"
                    else :
                        key_type_fields = "&%s_keytype_f" % reg._table_struct_name.lower()

                    reg_type = self.get_tab_type(reg._regType.upper())

                    if reg._table_struct_name.upper() in table_pool_dict:
                        str = "soc_tab_info_t %sm  = { SOC_TAB_FLAG_TABLE_POOL, NULL, NULL, %d, %d, %d, %s, \"%s\", %d, %s_addr, %d, %smf, %s, 0, 0, NULL};\n" % (reg._regName.lower(), reg._tab_idx_min, reg._tab_idx_max, reg._regFieldList[0][3], reg_type, reg._regName.lower(), len(reg._regBaseAddr), reg._regName.lower(), nKeyType, reg._regName.lower(), key_type_fields)
                    else:
                        str = "soc_tab_info_t %sm  = { %s, NULL, NULL, %d, %d, %d, %s, \"%s\", %d, %s_addr, %d, %smf, %s, 0, 0, NULL};\n" % (reg._regName.lower(), reg._reg_flag, reg._tab_idx_min, reg._tab_idx_max, reg._regFieldList[0][3], reg_type, reg._regName.lower(), len(reg._regBaseAddr), reg._regName.lower(), nKeyType, reg._regName.lower(), key_type_fields)

                    f.write(str)

                
                for reg in self.physical_table_list:
                    reg_type = self.get_tab_type(reg._regType.upper())                    
                    str = "soc_tab_info_t %sm  = { %s, NULL, NULL, %d, %d, %d, %s, \"%s\", %d, %s_addr, %d, NULL, %s, 0, 0, NULL};\n" % (reg._regName.lower(), reg._reg_flag, reg._tab_idx_min, reg._tab_idx_max, reg._nBits, reg_type, reg._regName.lower(), len(reg._regBaseAddr), reg._regName.lower(), 1, "NULL")
                    f.write(str)

        #print self.tab_type_list

        
        # create the table; hash or tcam                    
        if 1 == 0:     
            if 1 == 1:
                regList = tab_list

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




        # create the soc_sf9564_table_list
        f.write("\nsoc_tab_info_t *soc_sf9564_table_list[SF9564_MAX_TABLE_ID] = {\n")

        i = 0
        if 1 == 1:     
            if 1 == 1:
                regList = tab_list             
                for reg in range(len(regList)):                    
                    #if i < self.max_table_id - 1:
                    #    f.write("    &%sm,\n" % (regList[reg]._regName.lower()))
                    #    i +=1
                    #else:
                    #    f.write("    &%sm\n};\n" % (regList[reg]._regName.lower()))

                    f.write("    &%sm,\n" % (regList[reg]._regName.lower()))                    

                i = 0
                for reg in range(len(self.physical_table_list)):
                    if i < len(self.physical_table_list) - 1:
                        f.write("    &%sm,\n" % (self.physical_table_list[reg]._regName.lower()))
                        i +=1
                    else:
                        f.write("    &%sm\n};\n" % (self.physical_table_list[reg]._regName.lower()))
                        
        f.write("#endif\n")

        f.write("""\n#endif /* SF_9564 */\n""")
        
        f.close()




    def GenerateAllFieldFile(self, reg_list, tab_list, soc):
        print "Generate the allfield.h File."
        
        if soc != "": # if soc not been given, we can't give the prefix for the field name
            soc = soc + "_"
        
        f = file("./tmp/soc_groot_allfield.h", 'w')

        time_ = ("%s-%s-%s %d:%d:%d" % (time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday, time.gmtime().tm_hour ,time.gmtime().tm_min ,time.gmtime().tm_sec))
                
        str = """
/** @file 
  * @note Shenzhen Forward Industry Co.Ltd - Copyright (c) 2017.
  * @brief    
  * 
  * @author   lijun
  * @date     %s
  * @version  1.0
  * 
  * @note     THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANUALLY!!! 
  * $LastChangedDate$
  * $LastChangedRevision$
  * $LastChangedBy$
  */
"""  % ("")

        f.write(str)

        f.write("\n#ifdef SF_GROOT_SUPPORT\n")
        
        f.write("#ifndef __SOC_GROOT_ALLFIELD_H__\n")
        f.write("#define __SOC_GROOT_ALLFIELD_H__\n\n")

        f.write("\n#include \"./soc/service/reg_tab/groot/soc_groot_allsymbol.h\"\n")
        f.write("\n#include \"./soc/service/reg_tab/soc_field.h\"\n")
        
        
        regList = []
        table_pool_reg_list = []
        
        if 1 == 1:            
            if 1 == 1:
                regList = reg_list
                for reg in range(len(regList)):

                    if regList[reg]._modeName in table_pool_dict:                

                        if regList[reg]._old_regName.upper() in table_pool_reg_list:
                            continue
                        table_pool_reg_list.append(regList[reg]._old_regName.upper())

                        reg_name = "TABLEPOOL_" + regList[reg]._old_regName.upper()                

                    else :
                        reg_name = regList[reg]._regName.upper()
                        
                    
                    f.write("soc_field_info_t %sf[] = \n{\n" %(reg_name.lower()))
        
                    for fd in range(len(regList[reg]._regFieldList)):
                        field = regList[reg]._regFieldList[fd]
                        str = "    {\"%s\", %sf, %d, %d, %d},\n" % (field._fieldName.lower(), field._fieldName.upper(), field._fieldLen, field._fieldBp, 0)
                        if fd + 1 == len(regList[reg]._regFieldList):
                            str = "    {\"%s\", %sf, %d, %d, %d}\n" % (field._fieldName.lower(), field._fieldName.upper(), field._fieldLen, field._fieldBp, 0)
                        f.write(str)
        
                    f.write("};\n\n")


        # below is to store the info of key type for a table which have different keytypes
        for struct_name in key_type_field_info_dict:            
            bp   = key_type_field_info_dict[struct_name][0]
            len_ = key_type_field_info_dict[struct_name][1]
            
            f.write("soc_field_info_t %s_keytype_f = {\"%s\", 999999, %d, %d, 0};\n" %(struct_name.lower(), struct_name.lower(), len_, bp))            


                
        if 1 == 1:           
            if 1 == 1:
                regList = tab_list
                for reg in range(len(regList)): # regList only have one table. (but the table maybe divided to key or data table.)
                    
                    fieldInfoList = regList[reg]._regFieldList
                    nKeyType = len(fieldInfoList)
                    
                    if nKeyType > 1:
                        continue                  

                    else:                                                

                        fieldList = regList[reg]._regFieldList[0][1]
                    
                        f.write("soc_field_info_t %sf[] = \n{\n" %(regList[reg]._regName.lower()))
                    
                        for fd in range(len(fieldList)):
                            field = fieldList[fd]
                            str = "    {\"%s\", %sf, %d, %d, %d},\n" % (field._fieldName.lower(), field._fieldName.upper(), field._fieldLen, field._fieldBp, 0)
                            if fd + 1 == len(fieldList):
                                str = "    {\"%s\", %sf, %d, %d, %d}\n" % (field._fieldName.lower(), field._fieldName.upper(), field._fieldLen, field._fieldBp, 0)
                            f.write(str)
                        f.write("};\n\n")


        # deal with the table with different key type                
        if 1 == 1:     
            if 1 == 1:
                regList = tab_list
                for reg in range(len(regList)):
                    
                    fieldInfoList = regList[reg]._regFieldList
                    nKeyType = len(fieldInfoList)
                    
                    if nKeyType == 1:
                        continue                  

                    else:
                        for info in fieldInfoList :
                            key = info[0]
                            fieldList = info[1]                    
                    
                    
                            f.write("soc_field_info_t %s_%sf[] = \n{\n" %(regList[reg]._regName.lower(), key))
                    
                            for fd in range(len(fieldList)):
                                field = fieldList[fd]
                                str = "    {\"%s\", %sf, %d, %d, %d},\n" % (field._fieldName.lower(), field._fieldName.upper(), field._fieldLen, field._fieldBp, 0)
                                if fd + 1 == len(fieldList):
                                    str = "    {\"%s\", %sf, %d, %d, %d}\n" % (field._fieldName.lower(), field._fieldName.upper(), field._fieldLen, field._fieldBp, 0)
                                f.write(str)
                            f.write("};\n\n")

        f.write("#endif\n")
        
        f.write("""\n#endif /* SF_GROOT_SUPPORT */\n""")

        f.close()





