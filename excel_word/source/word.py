#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, os
import docx
from docx import Document
from docx.shared import Inches
import logging

logger = logging.getLogger('WordHandl')

class WrodHandl(object):
    def __init__(self):
        self._word_doc = None
        self._tab_cnt = 0

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

        tab_cnt = 'Table Count:' + hand_info['TABLE_COUNT']
        self._word_doc.add_paragraph(tab_cnt)

        tab_bitwidth = 'Table Bit Width:' + str(hand_info['TABLE_BITS_WIDTH'])
        self._word_doc.add_paragraph(tab_bitwidth)

        tab_type = 'Table Type:' + hand_info['TABLE_TYPE']
        self._word_doc.add_paragraph(tab_type)

        if hand_info['TABLE_SHARE']:
            tab_share = 'Table Sheare:' + hand_info['TABLE_SHARE']
            self._word_doc.add_paragraph(tab_share)

        tab_disc = 'Table Discription:' + hand_info['TABLE_DESCRIPTION']
        self._word_doc.add_paragraph(tab_disc)

    def __write_table_reginfo(self, reg_tab):
        """
        表格写入寄存器信息
        :param reg_tab:
        :return:
        """
        pass



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

    def write_register_toword(self, reg_info):
        key_list = list()
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



    def write_word_end(self):
        self._word_doc.add_page_break()
        self._word_doc.save('L3.docx')
