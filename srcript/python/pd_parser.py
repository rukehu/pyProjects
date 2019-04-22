#-*- coding: utf-8 -*-
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import os
import xlrd
register_to_pd = []
pd_field_dict = {}
pd_line_name = ["slice_to_pa_f_0",      "slice_to_pa_f_1",      "pa2tt_0",              "pa2tt_1",              "pa_mpls2tt_pd_0",
                "pa_mpls2tt_pd_1",      "tt2pa_mpls_data_0",    "tt2pa_mpls_data_1",    "tt2vcap_0",            "tt2vcap_1",
                "tt_vlan_pd_0",         "tt_vlan_pd_1",         "tt_l2_r_0",            "tt_l2_r_1",            "tt_l3_fifo_0",
                "tt_l3_fifo_1",         "tt_icap_fifo_dout_0",  "tt_icap_fifo_dout_1",  "TT2PD_EDITOR_f_0",     "TT2PD_EDITOR_f_1",
                "tt_mpls_ifc_0",        "tt_mpls_ifc_1",        "tt_port_ifc_0",        "tt_port_ifc_1",        "TT_IMDA_SOP_0",
                "TT_IMDA_SOP_1",        "vcap_vlan_pd_0",       "vcap_vlan_pd_1",       "vcap_vfp_ifc_0",       "vcap_vfp_ifc_1",
                "vlan_ifc_0",           "vlan_ifc_1",           "vlan_vxlat_ifc_0",     "vlan_vxlat_ifc_1",     "rtag_l3_fifo_0",
                "rtag_l3_fifo_1",       "ra_l2_r_0",            "ra_l2_r_1",            "l2_l3_pd_0",           "l2_l3_pd_1",
                "l2_svp_ifc_0",         "l2_svp_ifc_1",         "l2_vfi_ifc_0",         "l2_vfi_ifc_1",         "l3_icap_pd_0",
                "l3_icap_pd_1",         "l3_entry_ifc_0",       "l3_entry_ifc_1",       "l3_def_ifc_0",         "l3_def_ifc_1",
                "l3_iif_ifc_0",         "l3_iif_ifc_1",         "l3_vrf_ifc_0",         "l3_vrf_ifc_1",         "IM2DA_r_0",
                "IM2DA_r_1",            "Post_QD_r_0",          "Post_QD_r_1",          "PRE_PD_r_0",           "PRE_PD_r_1",
                "EL32EVLAN_r_0",        "EL32EVLAN_r_1",        "el3_to_pea_fifo_0",    "el3_to_pea_fifo_1",    "el3_port_efc_0",
                "el3_port_efc_1",       "el3_nh_efc_0",         "el3_nh_efc_1",         "el3_dvp_efc_0",        "el3_dvp_efc_1",
                "evlan_vxlate_efc_0",   "evlan_vxlate_efc_1",   "mirror_to_pea_pd_0",   "mirror_to_pea_pd_1",   "pab_ecap_pd_0",
                "pab_ecap_pd_1",        "pea_to_pac_pd_0",      "pea_to_pac_pd_1",      "PAC2PEB_f_0",          "PAC2PEB_f_1",
                "EVLAN_FILTER2PEB_r_0", "EVLAN_FILTER2PEB_r_1"]

pd_desciption =	["Input to PA",         "Input to PA",          "PA to TT",             "PA to TT",             "PA MPLS to TT",
                 "PA MPLS to TT",       "TT to PA MPLS",        "TT to PA MPLS",        "TT to VCAP",           "TT to VCAP",
                 "TT to VLAN",          "TT to VLAN",           "TT to L2",             "TT to L2",             "TT to L3",
                 "TT to L3",            "TT to ICAP",           "TT to ICAP",           "TT to PD_EDITOR",      "TT to PD_EDITOR",
                 "TT MPLS to IFC",      "TT MPLS to IFC",       "TT PORT to IFC",       "TT PORT to IFC",       "TT to IMDA",
                 "TT to IMDA",          "VCAP to VLAN",         "VCAP to VLAN",         "VCAP VFP to IFC",      "VCAP VFP to IFC",
                 "VLAN to IFC",         "VLAN to IFC",          "VLAN VXLAT to IFC",    "VLAN VXLAT to IFC",    "RTAG to L3",
                 "RTAG to L3",          "RA to L2",             "RA to L2",             "L2 to L3",             "L2 to L3",
                 "L2 SVP to IFC",       "L2 SVP to IFC",        "l2 VFI to IFC",        "l2 VFI to IFC",        "L3 to ICAP",
                 "L3 to ICAP",          "L3 ENTRY to IFC",      "L3 ENTRY to IFC",      "L3 DEF to IFC",        "L3 DEF to IFC",
                 "L3 IIF to IFC",       "L3 IIF to IFC",        "L3 VRF to IFC",        "L3 VRF to IFC",        "IM to DA",
                 "IM to DA",            "Input to EL3",         "Input to EL3",         "Input to EL3",         "Input to EL3",
                 "EL3 to EVLAN",        "EL3 to EVLAN",         "EL3 to PEA",           "EL3 to PEA",           "EL3 PORT to EFC",
                 "EL3 PORT to EFC",     "EL3 Next Hop to EFC",  "EL3 Next Hop to EFC",  "EL3 DVP to EFC",       "EL3 DVP to EFC",
                 "EVLAN VXLAT to EFC",  "EVLAN VXLAT to EFC",   "MIRROR to PEA",        "MIRROR to PEA",        "PAB to ECAP",
                 "PAB to ECAP",         "PEA to PAC",           "PEA to PAC",           "PAC to PEB",           "PAC to PEB",
                 "EVLAN Filter to PEB", "EVLAN Filter to PEB"]


def copy_file_to_file(src_file_name, dest_file):
    with open(src_file_name, "r") as file:
        line = file.readline()
        while(line):
            dest_file.write(line)
            line = file.readline()

class Pd_field(object):
    global register_to_pd
    def __init__(self):
        self.start_bit = ""
        self.end_bit = ""
        self.field_name = ""
    def __str__(self):
        str_temp  = ""
        str_temp += "field_name: %s " % self.field_name
        str_temp += "start_bit: %s " % self.start_bit
        str_temp += "end_bit: %s " % self.end_bit
        return str_temp

class Register(object):
    def __init__(self):
        self.base_addr = ""
        self.start_offset_addr = ""
        self.register_num = 0
        self.pd_name = ""
        self.pd_field_num = 0
        self.pd_field_list = []
        self.line_name = ""

    def __eq__(self, line_name):
        return self.line_name == line_name

    def __str__(self):
        str_temp  = ""
        str_temp += "line_name: %s\n" % self.line_name
        str_temp += "   pd_name: %s\n" % self.pd_name
        str_temp += "   base_addr: %s\n" % self.base_addr
        str_temp += "   start_offset_addr: %s\n" % self.start_offset_addr
        str_temp += "   register_num : %d\n" % self.register_num
        str_temp += "   pd_field_num: %d\n" % self.pd_field_num
        str_temp += "   pd_field_list:\n"
        for i in range(len(self.pd_field_list)):
            str_temp += "       " + str(self.pd_field_list[i]) + "\n"
        return str_temp

class Excel(object):
    def __init__(self, excel_name_input):
        self.excel_name = excel_name_input
        self.excel_fd =None

    def open_excel(self):
        if self.excel_name == "":
            print "None excel name, please check"
        else:
            self.excel_fd = xlrd.open_workbook(self.excel_name)

    def get_info(self):
        for sheet_name in self.excel_fd.sheet_names():
            register = Register()
            table = self.excel_fd.sheet_by_name(sheet_name)
            register.line_name = sheet_name
            self.get_register_info(table, register)
            if sheet_name == "TT_IMDA_SOP_0" or sheet_name == "TT_IMDA_SOP_1": 
                #print "TT_IMDA_SOP_0 or TT_IMDA_SOP_1" 
                register.pd_name = "SOP_1024"
                register.pd_field_num = 1
                pd_field = Pd_field()
                pd_field.start_bit = "0"
                pd_field.end_bit = "1023"
                pd_field.field_name = "SOP_1024"
                register.pd_field_list.append(pd_field)
                if True == pd_field_dict.has_key(pd_field.field_name):
                    pd_field_dict[pd_field.field_name] += 100
                else:
                    pd_field_dict[pd_field.field_name] = 1
            else:
                self.get_pd_name(table, register)
                self.get_pd_field(register)
            register_to_pd.append(register)

    def get_pd_field(self, register):
        current_dir = os.getcwd()
        pipeline_dir = current_dir + "\\" + "PIPELINE"
        pipeline_file_list = os.listdir(pipeline_dir)
        for file_name in pipeline_file_list:
            pipeline_file_path = os.path.join(pipeline_dir, file_name)
            pipeline_fd = xlrd.open_workbook(pipeline_file_path)
            for sheet_name in pipeline_fd.sheet_names():
                if sheet_name == register.pd_name:
                    table = pipeline_fd.sheet_by_name(sheet_name)
                    row = 1
                    col = 0
                    while table.nrows > row and 0 != table.cell_type(row, col):
                        register.pd_field_num +=1
                        pd_field = Pd_field()
                        pd_field.field_name = table.cell(row, col).value
                        if pd_field.field_name.find("/") != -1:
                           pd_field.field_name = pd_field.field_name.replace("/", "_")
                        if pd_field.field_name.find(" ") != -1:
                           pd_field.field_name = pd_field.field_name.replace(" ", "_")
                        if pd_field.field_name.find("(") != -1:
                           pd_field.field_name = pd_field.field_name.replace("(", "_")
                        if pd_field.field_name.find(")") != -1:
                           pd_field.field_name = pd_field.field_name.replace(")", "_")
                        if pd_field.field_name.find("+") != -1:
                           pd_field.field_name = pd_field.field_name.replace("+", "_")
                        pd_field.end_bit = table.cell(row, col+1).value
                        pd_field.start_bit = table.cell(row, col+2).value
                        #print (pd_field.field_name, pd_field.start_bit, pd_field.end_bit)
                        register.pd_field_list.append(pd_field)
                        if True == pd_field_dict.has_key(pd_field.field_name):
                            pd_field_dict[pd_field.field_name] += 100
                        else:
                            pd_field_dict[pd_field.field_name] = 1
                        row += 1
                    #print register.pd_field_num

    def get_pd_name(self, table, register):
        row = 0
        col = 8
        count = 2
        while count > 0:
            if 0 != table.cell_type(row, col):
                pd_name = table.cell(row, col).value
                if pd_name != u"对应PD/FIFO结构名":
                    print pd_name
                    register.pd_name = pd_name
                count -=1
            row += 1

    def get_register_info(self, table, register):
        register.base_addr = table.cell(0, 1).value
        is_offset_found = 0
        row = 2
        col = 0
        while table.nrows > row:
            if 0 == table.cell_type(row, col):
                row += 1
                continue
            data = table.cell(row, col+1).value
            index_n = data.find("n")
            if -1 != index_n:
                index_m = data.find("*")
                register.register_num += int(data[index_n+1: index_m])
                if is_offset_found == 0:
                    index_p = data.find("+")
                    register.start_offset_addr = data[:index_p]
                    is_offset_found = 1
            else:
                register.register_num += 1
                if is_offset_found != 1:
                    register.start_offset_addr = data
                    is_offset_found = 1
            row += 1  

class Hfile(object):
    def generate(self, file_name):
        c_file = open(file_name, "w")

        c_file.write("#ifndef _PD_INFO_H_\n")
        c_file.write("#define _PD_INFO_H_\n")
        
        c_file.write('#include"common.h"\n')
        c_file.write('#include"cli.h"\n')
        c_file.write('#include"sal/sal_core.h"\n')
        c_file.write('#include <fcntl.h>\n\n')
        
        copy_file_to_file("pd_macro_and_header", c_file)

        c_file.write("\n\n")

        c_file.write("typedef struct pd_field_info\n")
        c_file.write("{\n")
        c_file.write("  uint32_t start_bit;\n")
        c_file.write("  uint32_t end_bit;\n")
        c_file.write("  char_t *field_name;\n")
        c_file.write("  struct pd_field_info *next;\n")
        c_file.write("}pd_field_info;")
        c_file.write("\n\n")

        c_file.write("typedef struct pd\n")
        c_file.write("{\n")
        c_file.write("  uint32_t base_addr;\n")
        c_file.write("  uint32_t start_offset_addr;\n")
        c_file.write("  uint32_t register_num;\n")
        c_file.write("  char_t *line_name;\n")
        c_file.write("  char_t *pd_name;\n")
        c_file.write("  struct pd *next;\n")
        c_file.write("  struct pd_field_info *pd_field_list;\n")
        c_file.write("}pd;\n\n")
        c_file.write("struct pd *pd_list;\n\n")
        for i in range(len(register_to_pd)):
            c_file.write("//%s\n" % register_to_pd[i].line_name)
            j = register_to_pd[i].pd_field_num - 1
            while j >= 0:
                pd_field_name = register_to_pd[i].pd_field_list[j].field_name
                if pd_field_dict[pd_field_name] > 1:
                    pd_field_name +="_%d" % pd_field_dict[pd_field_name]
                    pd_field_dict[register_to_pd[i].pd_field_list[j].field_name] -= 100
                if j == register_to_pd[i].pd_field_num - 1:
                    c_file.write('static struct pd_field_info %s = {%d, %d, "%s", NULL};\n' % (pd_field_name, int(register_to_pd[i].pd_field_list[j].start_bit), int(register_to_pd[i].pd_field_list[j].end_bit), register_to_pd[i].pd_field_list[j].field_name))
                    register_to_pd[i].pd_field_list[j].field_name = pd_field_name
                else:
                    c_file.write('static struct pd_field_info %s = {%d, %d , "%s", &%s};\n' % (pd_field_name, int(register_to_pd[i].pd_field_list[j].start_bit), int(register_to_pd[i].pd_field_list[j].end_bit), register_to_pd[i].pd_field_list[j].field_name,  register_to_pd[i].pd_field_list[j+1].field_name))                
                    register_to_pd[i].pd_field_list[j].field_name = pd_field_name
                j -= 1
            if 0 == register_to_pd[i].pd_field_num:
                print "The pd field of %s has not found" % register_to_pd[i].line_name
            else:
                c_file.write('static struct pd %s = {%s, %s, %d, "%s", "%s", NULL, &%s};\n' % (register_to_pd[i].line_name, register_to_pd[i].base_addr, register_to_pd[i].start_offset_addr, register_to_pd[i].register_num, register_to_pd[i].line_name.lower(), register_to_pd[i].pd_name,register_to_pd[i].pd_field_list[0].field_name))                
            c_file.write("\n\n")
            c_file.flush()

        #c_file.write("static struct pd *pd_list_head = &%s;\n\n" % register_to_pd[len(register_to_pd) - 1].line_name)

        c_file.write('#ifdef __cplusplus\nextern "C"{\n#endif\n')
        c_file.write("static void init_pd_list();\n")
        c_file.write("static int32_t pd_probe_get(struct pd *pd_probe);\n\n")
        c_file.write("static void write_log(int32_t fd, char_t *fmt, ...);\n\n")
        c_file.write("static int32_t dump_all_pd_probe(struct pd *pd_list);\n\n")
        c_file.write("static int32_t set_all_pd_probe_enable();\n\n")
        c_file.write("int32_t cli_debug_mode(int32_t module_id, int32_t argc, char_t *args[]);\n\n")
        c_file.write("int32_t set_pd_probe_enable(int32_t module_id, int32_t argc, char_t *args[]);\n")
        c_file.write("int32_t dump_pd_probe(int32_t module_id, int32_t argc, char_t *args[]);\n")
        for i in range(len(register_to_pd)):
            c_file.write("int32_t get_pd_probe_%s(int32_t module_id, int32_t argc, char_t *args[]);\n" % register_to_pd[i].line_name.lower())
        c_file.write('#ifdef __cplusplus\n}\n#endif\n\n')
        
        c_file.write("#endif\n")

        c_file.close()

class Cfile(object):
    def generate(self, file_name):
        c_file = open(file_name, "w")
        c_file.write('#include"pd_info.h"\n\n')

        copy_file_to_file("pd_function", c_file)
        
        for i in range(len(register_to_pd)):
            c_file.write("int32_t get_pd_probe_%s(int32_t module_id, int32_t argc, char_t *args[])\n" % register_to_pd[i].line_name.lower())
            c_file.write("{\n")
            c_file.write("  pd_probe_get(&%s);\n" % register_to_pd[i].line_name)
            c_file.write("  return 0; \n}\n\n")

        c_file.write("int32_t cli_debug_mode(int32_t module_id, int32_t argc, char_t *args[])\n")
        c_file.write("{\n")
        c_file.write('    ctree->mode = DEBUG_MODE;\n    setPrompt("GalaxyWind(config/debug)#");\n')
        c_file.write('    DEBUGK(DK_TESTS, SAL_LL_INFO, "func: cli_debug_mode excuted!\\n");\n    return 0;\n')
        c_file.write('}\n')

        c_file.write("int32_t cli_debug_exit(int32_t module_id, int32_t argc, char_t *args[])\n")
        c_file.write("{\n")
        c_file.write('    ctree->mode = CONFIG_MODE;\n    setPrompt("GalaxyWind(config)#");\n')
        c_file.write('    DEBUGK(DK_TESTS, SAL_LL_INFO, "func: cli_debug_exit excuted!\\n");\n    return 0;\n')
        c_file.write('}\n')



        

class XMLfile(object):
    def generate(self, file_name):
        xml = open(file_name, "w")
        xml.write('<?xml version="1.0" encoding="utf-8"?>\n\n')
        xml.write('<!--\n')
        xml.write('        Description:\n')
        xml.write('                THE FILE IS GENERATED AUTOMATICLY, DO NOT EDIT BY MANNUAL!!!\n')
        xml.write('-->\n\n\n')
        xml.write('<root>\n')
        xml.write('    <view name="DEBUG_MODE">\n')
        for i in range(len(pd_line_name)):
            j = register_to_pd.index(pd_line_name[i])
            xml.write('        <command type="normal">\n')
            xml.write('            <cli>%s</cli>\n' % register_to_pd[j].line_name.lower())
            xml.write('            <help>\n')
            xml.write('                <helpInfo>%s</helpInfo>\n' % pd_desciption[i])
            xml.write('            </help>\n')
            xml.write('            <funcName type="user">get_pd_probe_%s</funcName>\n' % register_to_pd[j].line_name.lower())
            xml.write('        </command>\n\n')

        xml.write('        <command type="normal">\n')
        xml.write('            <cli>enable_all_pd_probe</cli>\n')
        xml.write('            <help>\n')
        xml.write('                <helpInfo>Set all pd probe force enable bit and global enable bit true</helpInfo>\n')
        xml.write('            </help>\n')
        xml.write('            <funcName type="user">set_pd_probe_enable</funcName>\n')
        xml.write('        </command>\n\n')

        xml.write('        <command type="normal">\n')
        xml.write('            <cli>disable_all_pd_probe</cli>\n')
        xml.write('            <help>\n')
        xml.write('                <helpInfo>Set all pd probe force enable bit and global enable bit false</helpInfo>\n')
        xml.write('            </help>\n')
        xml.write('            <funcName type="user">set_pd_probe_disable</funcName>\n')
        xml.write('        </command>\n\n')


        xml.write('        <command type="normal">\n')
        xml.write('            <cli>dump_all_pd_probe</cli>\n')
        xml.write('            <help>\n')
        xml.write('                <helpInfo>Dump all pd probe into pd.log file</helpInfo>\n')
        xml.write('            </help>\n')
        xml.write('            <funcName type="user">dump_pd_probe</funcName>\n')
        xml.write('        </command>\n\n')


        xml.write('        <command type="normal">\n')
        xml.write('            <cli>exit</cli>\n')
        xml.write('            <help>\n')
        xml.write('                <helpInfo>End current mode and down to previous mode</helpInfo>\n')
        xml.write('            </help>\n')
        xml.write('            <funcName type="user">cli_debug_exit</funcName>\n')
        xml.write('            <newMode></newMode>\n')        
        xml.write('        </command>\n\n')
        
        xml.write('     </view>\n')
        xml.write('</root>\n')

def pd_init():
    current_dir = os.getcwd()
    pd_dir = current_dir + "\\" + "PD"
    excel_list = os.listdir(pd_dir)
    for file_name in excel_list:
        file_path = os.path.join(pd_dir, file_name)
        print "\n%s" % file_name
        excel = Excel(file_path)
        excel.open_excel()
        excel.get_info()
    h_file = Hfile()
    h_file.generate("./tmp/pd_info.h")
    c_file = Cfile()
    c_file.generate("./tmp/pd_info.c")
    xml = XMLfile()
    xml.generate("./tmp/debug.xml")

if __name__ == "__main__":
    pd_init()
