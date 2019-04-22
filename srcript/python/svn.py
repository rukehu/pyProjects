# -*- coding: utf-8 -*-

__author__ = 'LI JUN'


import sys
import os


file_ = file("../../debug_tool/cli/svn.h", 'w')


str="""#ifndef __SVN_H__
#define __SVN_H__

"""

file_.write(str)


line_list=[]
str = os.popen("svn info")

line_ = str.readline()
while line_ :
    line_list.append(line_)
    line_ = str.readline()


    
for line in line_list:
    line = line.replace("\n", "")
    if line.find("Revision") != -1:        
        rev = "char_t code_version[]=\"%s\";\n" % line
        file_.write(rev)

    if line.find("Last Changed Date") != -1:
        date = "char_t code_date[]=\"%s\";\n" % line
        file_.write(date)


file_.write("\n#endif\n")
file_.close()

