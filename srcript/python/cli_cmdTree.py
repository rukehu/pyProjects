# -*- coding: utf-8 -*-
__author__ = 'GalaxyWind'

import os
from xml.etree import ElementTree
from cli_view import CView
from cli_command import CCommand

class CCmdTree(object):
    """define a type for CLI"""
    __slots__ = ('_viewDict', '_xmlFilePath', '_funcIdToName', '_funcNameToId', '_nextKernelFuncId', '_nextUserFuncId')
    def __init__(self, xmlFilePath):
        self._viewDict              = dict()                # a dict(key:viewName, value: CView)
        self._xmlFilePath           = xmlFilePath           #命令注册xml文件所在目录
        self._funcIdToName          = dict()
        self._funcNameToId          = dict()
        self._nextKernelFuncId       = 200000                   #从101开始编号，内核空间命令回调函数########################################
        self._nextUserFuncId         = 0                     #从0开始编号，用户空间命令回调函数

    @property
    def viewDict(self):
        return self._viewDict

    @viewDict.setter
    def viewDict(self, value):
        self._viewDict = value

    @property
    def xmlFilePath(self):
        return self._xmlFilePath

    @xmlFilePath.setter
    def xmlFilePath(self, value):
        self._xmlFilePath = value

    def _AddView(self, viewName):
        self.viewDict[viewName] = CView(viewName)

    def _GetView(self, viewName):
        if viewName not in self.viewDict:
            self._AddView(viewName)
        return self.viewDict[viewName]

    def parseXml(self):
        curListDir = os.listdir(self.xmlFilePath)
        xmlList = [fileName for fileName in curListDir if fileName[-3:] == "xml"]
        xmlFilePathList = [os.path.join(self.xmlFilePath,fileName) for fileName in xmlList]

        #print "\n xmlList is %s \n" % xmlList
        #print "\n xmlFilePathList is %s \n" % xmlFilePathList
        for xmlfile in xmlFilePathList:

            #print xmlfile
            xmlInfo=ElementTree.parse(xmlfile)
            viewList=xmlInfo.findall('./view')
            #print "\n viewList is: %s \n" % viewList
			
            for view in viewList:                
                viewName = view.attrib["name"].strip().upper()
                viewObject = self._GetView(viewName)
                #print "\n view name is: %s \n" % viewName
				
                commandList = view.getchildren()
                #print "\n commandList is %s \n" % commandList
                for command in commandList:
                    cmdStr          = ""
                    helpInfoList    = []
                    funcId          = 0
                    funcName        = ""
                    newMode         = ""
                    cliType         = ""
                    funcType        = ""
                    if "type" in command.attrib:
                        cliType = command.attrib["type"].strip()
                    else:
                        #CLI命令默认为一般类型
                        cliType = "normal"

                    for member in command.getchildren():
                        if member.text != None:
                            if member.tag == "cli":
                                cmdStr = member.text.strip()
                            elif member.tag == "help":
                                for helpInfo in member.getchildren():
                                    helpStr = helpInfo.text.strip()
                                    helpInfoList.append(helpStr)
                            elif member.tag == "funcName":
                                funcName = member.text.strip()
                                if funcName in self._funcNameToId:
                                    funcId = self._funcNameToId[funcName]
                                else:
                                    if "type" in member.attrib:
                                        funcType = member.attrib["type"].strip()
                                    else:
                                        #CLI命令默认为一般类型
                                        funcType = "kenerl"

                                    if funcType == "kenerl":
                                        funcId = self._nextKernelFuncId
                                        self._nextKernelFuncId += 1
                                    elif funcType == "user":
                                        funcId = self._nextUserFuncId
                                        self._nextUserFuncId += 1
                                    else:
                                        pass

                                    self._funcNameToId[funcName]    = funcId
                                    self._funcIdToName[funcId]      = funcName
                            elif member.tag == "newMode":
                                newMode = member.text.strip().upper()
                            else:
                                pass

                    viewObject.AddCommand(CCommand(cmdStr, helpInfoList, funcId, funcName, newMode, cliType))

    def generCode_funcDef_h(self):
        with open("./tmp/funcDef.h","w") as file:
            file.write("#ifndef _FUNC_DEF_H_\n")
            file.write("#define _FUNC_DEF_H_\n\n")

            #file.write("#define _KERNEL_FUNC_START_ \n\n")

            index = 0
            while index < self._nextUserFuncId:
                funcstr = self._funcIdToName[index].upper()
                strTemp = "#define  %-50s  %d\n"%(funcstr, index)
                file.write(strTemp)
                index += 1

            index = 200000
            while index < self._nextKernelFuncId:
                funcstr = self._funcIdToName[index].upper()
                strTemp = "#define  %-50s  %d\n"%(funcstr, index)
                file.write(strTemp)
                index += 1

            file.write("\n\n\n#endif /* _FUNC_DEF_H_ */")

    def generCode_funcArray_h(self):
        with open("./tmp/kernelFuncArray.h","w") as file:
            strTemp = "#ifndef _KERNEL_FUNC_ARRAY_H_\n"
            strTemp += "#define _KERNEL_FUNC_ARRAY_H_\n\n"
            strTemp += "#include \"kernelFuncExtern.h\"\n"
            strTemp += "#define FUNC_NUM_MAX 200000\n\n"

            strTemp += "typedef int32_t (*CLI_FUNC)(int32_t module_id, int32_t argc, char_t *args[]);\n"
            strTemp += "CLI_FUNC kernelFuncArray[FUNC_NUM_MAX] = {\n"
            file.write(strTemp)


            index = 200000
            while index < self._nextKernelFuncId:
                strTemp = "    %-50s  /* %d */"%(self._funcIdToName[index], index - 101)
                if index != (self._nextKernelFuncId - 1):
                    strTemp += ","
                strTemp += "\n"
                file.write(strTemp)
                index += 1

            file.write("};\n")
            file.write("\n\n\n#endif /* _KERNEL_FUNC_ARRAY_H_ */")

        with open("./tmp/userFuncArray.h","w") as file:
            strTemp = "#ifndef _USER_FUNC_ARRAY_H_\n"
            strTemp += "#define _USER_FUNC_ARRAY_H_\n\n"
            strTemp += "#include \"userFuncExtern.h\"\n"
            strTemp += "#define FUNC_NUM_MAX 200000\n\n" 

            strTemp += "typedef int32_t (*CLI_FUNC)(int32_t module_id, int32_t argc, char_t *args[]);\n"
            strTemp += "CLI_FUNC userFuncArray[FUNC_NUM_MAX] = {\n"
            file.write(strTemp)


            index = 0
            while index < self._nextUserFuncId:
                strTemp = "    %-50s  /* %d */"%(self._funcIdToName[index], index)
                if index != (self._nextUserFuncId - 1):
                    strTemp += ","
                strTemp += "\n"
                file.write(strTemp)
                index += 1

            file.write("};\n")
            file.write("\n\n\n#endif /* _USER_FUNC_ARRAY_H_ */")

    def generCode_funcExtern_h(self):
        with open("./tmp/kernelFuncExtern.h","w") as file:
            file.write("#ifndef _KERNEL_FUNC_EXTERN_H_\n")
            file.write("#define _KERNEL_FUNC_EXTERN_H_\n\n\n")

            index = 200000
            while index < self._nextKernelFuncId:
                strTemp = "extern int32_t %s(int32_t module_id, int32_t argc, char_t *args[]);  /* %d */\n"\
                          %(self._funcIdToName[index], index - 101)
                file.write(strTemp)
                index += 1

            file.write("\n\n\n#endif /* _KERNEL_FUNC_EXTERN_H_ */")

        with open("./tmp/userFuncExtern.h","w") as file:
            file.write("#ifndef _USER_FUNC_EXTERN_H_\n")
            file.write("#define _USER_FUNC_EXTERN_H_\n\n\n")

            index = 0
            while index < self._nextUserFuncId:
                strTemp = "extern int32_t %s(int32_t module_id, int32_t argc, char_t *args[]);  /* %d */\n"\
                          %(self._funcIdToName[index], index)
                file.write(strTemp)
                index += 1

            file.write("\n\n\n#endif /* _USER_FUNC_EXTERN_H_ */")

    def generCode_cli_view_h(self):
        with open("./tmp/cli_view.h","w") as file:
            file.write("#ifndef _CLI_VIEW_H_\n")
            file.write("#define _CLI_VIEW_H_\n\n\n")
            index = 1
            
            for key in self.viewDict.keys():
                if key == "CONFIG_MODE":
                    strTemp = "#define  %-20s  0\n"%(key)                    
                    file.write(strTemp)
                    continue                    
                
                strTemp = "#define  %-20s  %d\n"%(key, index)
                index += 1
                file.write(strTemp)

            strTemp = "#define  %-20s  %d\n"%("MAX_MODE", index)
            index += 1			
            strTemp += "#define  %-20s  %d\n"%("MODIFIER_MODE", index)
            index += 1
            strTemp += "#define  %-20s  %d\n"%("EXEC_MODE", index)
			
            file.write(strTemp)
            file.write("\n\n\n#endif /* _CLI_VIEW_H_ */")

            
            
    def generCode_cli_gen_c(self):
        with open("./tmp/cli_gen.c","w") as file:
            file.write("#include \"cli_view.h\"\n")
            file.write("#include \"cli.h\"\n")
            file.write("#include \"funcDef.h\"\n\n\n")
            for viewTemp in self.viewDict.values():
                for command in viewTemp.commandList:
                    strTemp = "CLI(%s_cmd,\n"%command.funcName  \
                        + "    \"%s\",\n"%command.cmdStr
                    strTemp = strTemp + "    " + command.funcName.upper() + ",\n"
                    for helpInfo in command.helpInfoList:
                        strTemp += "    \"%s\",\n"%helpInfo

                    strTemp = strTemp[:-2] # delete last ", \n"
                    strTemp += ");\n\n\n"
                    file.write(strTemp.encode("utf-8"))

            strTemp = "void cli_gen (struct cli_tree *ctree)\n{\n"
            file.write(strTemp)
            for viewName in self.viewDict:
                viewTemp = self.viewDict[viewName]
                strTemp = ""
                for command in viewTemp.commandList:
                    if command.cliType == "normal":
                        strTemp += "    cli_install_gen(ctree, %s, PRIVILEGE_VR_MAX, 0, &%s_cmd);\n\n"\
                                  %(viewName.upper(), command.funcName)
                    elif command.cliType == "global":
                        for key in self.viewDict.keys():
                            strTemp += "    cli_install_gen(ctree, %s, PRIVILEGE_VR_MAX, 0, &%s_cmd);\n\n"\
                                      %(key.upper(), command.funcName)
                    else:
                        pass

                file.write(strTemp)

            file.write("}\n")



    def __str__(self):
        return 'CViewManager object(viewDict: %s)' \
                    %(str(self.viewDict))

    __repr__ = __str__
