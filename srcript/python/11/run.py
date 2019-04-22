# coding=utf-8
import re
import xlrd
import sys
import os
import xlwt
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print "-----------"
        print root   #os.walk()所在目录
        print dirs   #os.walk()所在目录的所有目录名
        print files   #os.walk()所在目录的所有非目录文件名
        print " "
    for file in files:
        print file
        if(file[-2:] == ".v"):
            f = open(file_dir + file)  # 返回一个文件对象
            line = f.readline()  # 调用文件的 readline()方法
            a0 = []
            a1 = []
            a2 = []
            while line:
                if line.find("input") ==0:
                    a2.append('I')
                    if line.find(":") >0:
                        temp1=line[line.find("[")+1:line.find(":")]
                        if len(temp1) >5:
                            temp1=temp1[0:-2]
                            if(temp1[0]=="("):
                                temp1=temp1[1:-1]
                        else:
                            temp1=str(int(temp1)+1)
                        a1.append(temp1)
                        temp2 = line[line.find("]") + 1:line.find(";")].strip()
                        a0.append(temp2)
                    else :
                        a1.append('0')
                        temp2 = line[line.find("put") + 3:line.find(";")].strip()
                        a0.append(temp2)
                elif line.find("output") ==0:
                    a2.append('O')
                    if line.find(":") >0:
                        temp1=line[line.find("[")+1:line.find(":")]
                        if len(temp1) >5:
                            temp1=temp1[0:-2]
                            if(temp1[0]=="("):
                                temp1=temp1[1:-1]
                        else:
                            temp1=str(int(temp1)+1)
                        a1.append(temp1)
                        temp2 = line[line.find("]") + 1:line.find(";")].strip()
                        a0.append(temp2)
                    else :
                        a1.append('0')
                        temp2 = line[line.find("put") + 3:line.find(";")].strip()
                        a0.append(temp2)
                else:
                    pass

                #print line,  # 后面跟 ',' 将忽略换行符

                # print(line, end = '')　     # 在 Python 3 中使用

                line = f.readline()
            f.close()
            name=file[:-2]
            len1 = len(a0)
            print a0
            print len(a0)
            print a1
            print len(a1)
            print a2
            print len(a2)
            save(name,len1,a0,a1,a2)
        else:
            pass

def save(name,len1,a0,a1,a2):
    file = xlwt.Workbook()
    table = file.add_sheet(name)
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'Times New Roman'
    font.bold = True
    style.font = font
    for i in range (0,len1):
        table.write(i, 0, a0[i], style)
        table.write(i, 1, a1[i], style)
        table.write(i, 2, a2[i], style)
    #table = file.add_sheet('sheet1', cell_overwrite_ok=True)
    name=name+'.xls'
    print name
    file.save(name)
def read():
    path=os.getcwd()
    path=path + "\\"
    file_name(path)
    print path

def main():
    read()
if __name__ == '__main__':
    main()