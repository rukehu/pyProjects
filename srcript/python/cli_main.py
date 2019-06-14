# -*- coding: utf-8 -*-


__author__ = 'GalaxyWind'

from cli_cmdTree import CCmdTree
from parse_main import start
from pd_parser import pd_init
import shutil
import logging

logging.basicConfig(level=logging.NOTSET, format='[%(filename)s:%(lineno)d]-%(levelname)s %(message)s')
logger = logging.getLogger('main')

if __name__ == '__main__':

    print ("This is cli_main.py __main__ function")


    start()
    pd_init()


    if 1 == 1:
        shutil.copy("./config.xml",             "./tmp/")
        shutil.copy("./interface.xml",          "./tmp/")
        shutil.copy("./openflow.xml",           "./tmp/")
        shutil.copy("./pktgen.xml",             "./tmp/")
        shutil.copy("./vlan_test.xml",          "./tmp/")
        shutil.copy("./l3_lpm_tcam.xml",        "./tmp/")
        shutil.copy("./port.xml",               "./tmp/")
        shutil.copy("./l2table.xml",            "./tmp/")
        shutil.copy("./counter.xml",            "./tmp/")
        shutil.copy("./test.xml",               "./tmp/")
        shutil.copy("./fp.xml",                 "./tmp/")
        shutil.copy("./soc.xml",                "./tmp/")
        

        cmdTree = CCmdTree("./tmp/")
        cmdTree.parseXml()
        cmdTree.generCode_funcDef_h()
        cmdTree.generCode_funcArray_h()
        cmdTree.generCode_funcExtern_h()
        cmdTree.generCode_cli_view_h()
        cmdTree.generCode_cli_gen_c()

    print "Copying the files to specified folders........\n"
    
    # copy files to specified folder

    if 1 == 0:
        shutil.copy("./tmp/soc_groot_direct.c",        "../../../source/soc/service/reg_tab/groot/")
        shutil.copy("./tmp/soc_groot_hash_tcam.c",     "../../../source/soc/service/reg_tab/groot/")
        shutil.copy("./tmp/soc_groot_reg.c",           "../../../source/soc/service/reg_tab/groot/")
        shutil.copy("./tmp/soc_groot_table_pool.c",    "../../../source/soc/service/reg_tab/groot/")


        shutil.copy("./tmp/sf9564_allreg.h",        "../../../header/soc/service/reg_tab/groot/sf9564/")
        shutil.copy("./tmp/sf9564_alltable.h",      "../../../header/soc/service/reg_tab/groot/sf9564/")

        shutil.copy("./tmp/soc_groot_allfield.h",      "../../../header/soc/service/reg_tab/groot/")        
        shutil.copy("./tmp/soc_groot_allsymbol.h",     "../../../header/soc/service/reg_tab/groot/")        
        shutil.copy("./tmp/soc_groot_direct.h",        "../../../header/soc/service/reg_tab/groot/")
        shutil.copy("./tmp/soc_groot_hash_tcam.h",     "../../../header/soc/service/reg_tab/groot/")
        shutil.copy("./tmp/soc_groot_reg.h",           "../../../header/soc/service/reg_tab/groot/")
        shutil.copy("./tmp/soc_groot_table_pool.h",    "../../../header/soc/service/reg_tab/groot/")


    if 1 == 0:
        shutil.copy("./tmp/cli_gen.c",              "../../debug_tool/cli/")
        shutil.copy("./tmp/reg_mem_interface.c",    "../../debug_tool/cli/")
        shutil.copy("./tmp/cli_mode.h",             "../../debug_tool/cli/")
        shutil.copy("./tmp/cli_view.h",             "../../debug_tool/cli/")
        shutil.copy("./tmp/funcDef.h",              "../../debug_tool/cli/")
        shutil.copy("./tmp/kernelFuncArray.h",      "../../debug_tool/cli/")
        shutil.copy("./tmp/kernelFuncExtern.h",     "../../debug_tool/cli/")
        shutil.copy("./tmp/pd_info.c",              "../../debug_tool/cli/")
        shutil.copy("./tmp/pd_info.h",              "../../debug_tool/cli/")
        shutil.copy("./tmp/userFuncExtern.h",       "../../debug_tool/cli/")
        shutil.copy("./tmp/userFuncArray.h",        "../../debug_tool/cli/")




    

    




