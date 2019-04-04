# Excel转Word软件模块设计

软件主要涉及以下三个模块  

## excel数据读取模块

### 功能设计

1. 读取数据，excel表格通过读取页（sheet）、读取行（row）的方式对数据进行提取；

2. 解析并封装，根据表格中特定位置的字段对数据进行解析，然后封装成一个寄存器所需要的数据结构；

3. 数据输出，解析一页（sheet）为一个寄存器数据结构（应该为一个寄存器字典形式）输出。

### 软件实现

软件主要涉及以下类型与提供接口。

1. ExcelHandl：该类型为excel控制类，对excel的所有操作进行封装；

2. 对外提供接口：  
    open_excel(self, excel_path):根据excel路径打开这个表格；

    get_excel_sheets(self):获取excel所有的页名，以list()类型输出;

    get_register_info(self, sheet_name):根据sheet name 获取一个寄存器信息，信息以字dic()类型输出。

    read_excel_end(self):关闭退出excel操作。

## world数据写入模块

### 功能设计

1. 写入字段，根据提供的寄存器数据信息（为一个字典），获取对应的字段并将该字段写入Word指点的位置。

2. 插入表格，将需要写入表格的字段信息使用表格的形式写入Word。


### 软件实现

软件涉及类型封装与提供接口。

1. WordHandler：该类型为Word控制类，对Word所有操作进行封装；

2. 对外提供接口：  
    open_word(self, word_path)：打开（不存在则创建）Word文档；

    write_register_toword(self, reg_info):将给与的寄存器信息写入Word特定位置。

    write_word_end(self):保存并关闭Word操作。

## main控制模块

main功能模块调用其他模块，建立模块之间的数据通信与控制，完成excel转Word格式功能。