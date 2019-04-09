#!/usr/bin/python
# -*- coding: UTF-8 -*-

from docx import Document, table
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Inches, Cm
import logging

logger = logging.getLogger('WordHandl')

FONT_NAME = 'Calibri'        # 设置默认字体
REG_TAB_CLOUMN = 4           # 寄存器表格的列总量
TAB_CNT_BASE = 0             # 表格起始号

class WrodHandl(object):
    def __init__(self):
        self._word_doc = None
        self._tab_cnt = TAB_CNT_BASE

    def __key_type_heading(self, key_list):
        """
        根据多个寄存器KEY_TYPE复用,生成Heading标题
        :param key_list:
        :return:寄存器标题str
        """
        min_len = len(key_list[0])
        cnt = len(key_list)
        ch_eq = False        # 标识含有不相等的字符

        if cnt == 1:
            return key_list[0]

        for key in key_list:
            key_len = len(key)
            if min_len > key_len:
                min_len = key_len

        for idx in range(min_len):
            ch = key_list[0][idx]
            for i in range(cnt):
                if key_list[i][idx] != ch:
                    ch_eq = True
                    break
            if ch_eq:
                break

        if ch_eq:
            heading = key_list[0][0:idx]
            heading += '_t'
        else:
            heading = key_list[0]

        return heading

    def __write_hand_info(self, hand_info):
        """
        写入寄存器总体信息
        :param hand_info:
        :return:
        """
        self._word_doc.add_heading(hand_info['KEY_TYPE'], level=1)  # 写入寄存器表名

        tab_cnt = 'Table Count:' + str(hand_info['TABLE_COUNT'])
        self._word_doc.add_paragraph(tab_cnt)

        tab_bitwidth = 'Table Bit Width:' + str(hand_info['TABLE_BITS_WIDTH'])
        self._word_doc.add_paragraph(tab_bitwidth)

        tab_type = 'Table Type:' + hand_info['TABLE_TYPE']
        self._word_doc.add_paragraph(tab_type)

        if hand_info['TABLE_SHARE']:
            tab_share = 'Table Share:' + hand_info['TABLE_SHARE']
            self._word_doc.add_paragraph(tab_share)

        if hand_info['TABLE_DESCRIPTION']:
            tab_disc = 'Table Discription:' + hand_info['TABLE_DESCRIPTION']
            self._word_doc.add_paragraph(tab_disc)

    def __write_table_reginfo(self, reg_info):
        """
        表格写入寄存器信息
        :param reg_tab:
        :return:
        """
        self._tab_cnt += 1

        # 添加表格标题
        tab_name = 'Table ' + str(self._tab_cnt) + ': ' + reg_info['KEY_TYPE']
        tab_pgr = self._word_doc.add_paragraph()
        tab_pgr.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        tab_run = tab_pgr.add_run(tab_name)
        tab_run.bold = True

        # 添加寄存器表格信息
        bit_list = reg_info['bit_list']
        tab_row = len(bit_list) + 1         # 需添加表头
        tab_cloumn = REG_TAB_CLOUMN
        reg_tab = self._word_doc.add_table(tab_row, tab_cloumn, 'Table Grid')

        # 设置表格宽度
        reg_tab.autofit = False
        for idx in range(tab_row):
            reg_tab.cell(idx, 0).width = Inches(0.8)
            reg_tab.cell(idx, 1).width = Inches(1.8)
            reg_tab.cell(idx, 2).width = Inches(2.2)
            reg_tab.cell(idx, 3).width = Inches(0.8)

        # 写入表头信息
        head_arr = ['Bits', 'Name', 'Description', 'Default']
        for idx in range(tab_cloumn):
            tab_run = reg_tab.cell(0, idx).paragraphs[0].add_run(head_arr[idx])
            tab_run.bold = True
            tab_run.font.italic = True

        row_idx = 1
        for bit_info in bit_list:
            tab_cells = reg_tab.rows[row_idx].cells

            bits = bit_info['FIELD_BITS']
            if bits == None:
                bits = bit_info['SUB_FIELD_BITS']
            tab_cells[0].text = str(bits)
            # tab_cells[0].text().font.name
            # tab_cells[0].width = Inches(4)

            name = bit_info['FIELD_NAME']
            if name == None:
                name = bit_info['SUB_FIELD_NAME']
            tab_cells[1].text = name

            descrip = bit_info['DESCRIPTION']
            if descrip != None:
                tab_cells[2].text = descrip
            default = bit_info['DEFAULT_VALUE']
            if default != None:
                tab_cells[3].text = str(default)

            row_idx += 1


    def open_word(self, word_path):
        """
        打开一个word文档，不存在则创建
        :param word_path:
        :return:
        """
        try:
            self._word_doc = Document(word_path)
        except:
            logger.info('Can not open this file:', word_path)
            self._word_doc = None
            return

        self._word_doc.styles['Normal'].font.name = FONT_NAME

    def write_register_toword(self, reg_info):
        """
        将给与寄存器信息写入word文档
        :param reg_info:
        :return:
        """
        key_list = list()
        index = 0

        if self._word_doc == None:
            logger.info('The document is not open.')
            return

        reg_head = reg_info['head_info']
        reg_list = reg_info['reg_list']
        for reg in reg_list:
            key_list.append(reg['KEY_TYPE'])

        # 根据多个key type 获取寄存器标题
        reg_head['KEY_TYPE'] = self.__key_type_heading(key_list)
        self.__write_hand_info(reg_head)

        # 将寄存器信息写入word表格
        for reg_tab in reg_list:
            self.__write_table_reginfo(reg_tab)

            index += 1
            if index < len(reg_list):
                self._word_doc.add_paragraph()

    def write_word_end(self):
        self._word_doc.add_page_break()
        self._word_doc.save('L3.docx')
