#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, os
from source.excel import ExcelHeadl
from source.word import WrodHandl
import config
import logging

logger = logging.getLogger('main')
logging.basicConfig(level=logging.NOTSET)

if __name__ == '__main__':
    excel_headl = ExcelHeadl()
    word_headl = WrodHandl()

    excel_headl.open_excel(config.EXCEL_URL)
    word_headl.open_word(None)

    sheets = excel_headl.get_excel_sheets()
    # 第一个表格为版本说明，将其移出
    if len(sheets) > 0:
        sheet = sheets.pop(0)

    reg_info = excel_headl.get_registers_info(sheets[0])
    logger.debug(reg_info)
    word_headl.write_register_toword(reg_info)

    # for sheet in sheets:
    #     excel_headl.get_registers_info(sheets[1])

    excel_headl.read_excel_end()
    word_headl.write_word_end()