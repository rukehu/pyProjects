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
        pass

    def __writ_hand_info(self, hand_info):
        """
        写入寄存器总体信息
        :param hand_info:
        :return:
        """
        tab_cnt = 'Table Count:' + hand_info['tab_cnt']
        tab_bitwidth = 'Table Bit Width:' + hand_info['tab_bit_width']
        tab_type = 'Table Type:' + hand_info['tab_type']
        tab_disc = 'Table Discription:'
        self._word_doc.add_heading(hand_info['key_type'], level=1)    # 写入寄存器表名

    def open_word(self, word_path):
        try:
            self._word_doc = Document(word_path)
        except:
            logger.info('Can not open this file:', word_path)
            self._word_doc = None
            return

    def write_register_toword(self, reg_info):
        if self._word_doc == None:
            logger.info('The document is not open.')
            return

        head_info = reg_info['head_info']





    def write_word_end(self):
        pass
