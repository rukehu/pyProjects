#!/usr/bin/python
# -*- coding: UTF-8 -*-

import openpyxl
import logging
import config

logger = logging.getLogger('ExcelHeadl')

class ExcelHeadl(object):
    def __init__(self):
        self._excel_wb = None

    def open_excel(self, excel_path):
        state = False
        logger.debug(excel_path)
        if '.xlsx' in excel_path:
            try:
                self._excel_wb = openpyxl.load_workbook(excel_path)
            except:
                logger.info('Can not open this file:', excel_path)
                self._excel_wb = None
            else:
                state = True

        return state

    def get_excel_sheets(self):
        """
        获取excel所有的sheet name
        :return: name list()
        """
        sheets = list()
        if self._excel_wb != None:
            sheets = self._excel_wb.sheetnames

        return sheets

    def get_registers_info(self, sheet_name):
        """
        获取sheet中的一个寄存器信息
        :param sheet_name:
        :return:寄存器信息dict :{'head_info', 'reg_list'};
                 head_info:{'tab_cnt', 'tab_bit_width', 'tab_type', 'hash_algorithm',
                            'csr_mod', 'csr_addr', 'tab_share', 'tab_description'}
                 reg_list:[{'key_type', 'bit_list'}, {'key_type', 'bit_list'}...]   # 寄存器信息描述list
                        bit_list:[{'filed_name', 'filed_bits', 'sub_filed_name', 'sub_filed_bits',
                            'description', 'default_val', 'notes'}, ...]
        """
        key_idx = None
        sheet = None
        reg_info = dict()
        head_info = dict()
        tab_list = list()
        tab_len = 0
        row_idx = 0
        reg_list = list()
        bit_list = list()

        try:
            sheet = self._excel_wb[sheet_name]
        except:
            logger.info('the sheet not exist :')
            return

        for row in sheet.rows:
            # row = 0,1 获取寄存器表头总体信息, row = 2 获取寄存器表头信息
            if row_idx == 0 or row_idx == 2:
                key_idx = {}
                tab_list = []
                idx = 0

                for tup in row:
                    val = tup.value
                    if val != None:
                        tab_list.append(val)
                        key_idx[val] = idx
                    idx += 1

                tab_len = len(tab_list)
                logger.debug(tab_list)

            elif row_idx == 1:
                for _key in tab_list:
                    head_info[_key] = row[key_idx[_key]].value
                reg_info['head_info'] = head_info
                logger.debug(head_info)

            else:
                # 获取寄存器信息
                tab_name = row[0].value
                if tab_name != None or row_idx == 3:
                    key_dct = dict()
                    if tab_name == None:
                        tab_name = sheet_name

                    key_dct[tab_list[0]] =tab_name
                    bit_list = list()
                    key_dct['bit_list'] = bit_list
                    reg_list.append(key_dct)
                    reg_info['reg_list'] = reg_list

                bit_dct = dict()
                for cloumn_idx in range(tab_len):
                    if cloumn_idx > 0:
                        bit_dct[tab_list[cloumn_idx]] = row[cloumn_idx].value
                if bit_dct['FIELD_NAME'] or bit_dct['SUB_FIELD_NAME']:
                    bit_list.append(bit_dct)
            row_idx += 1

        return reg_info

    def read_excel_end(self):
        self._excel_wb.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET)
    excel_headl = ExcelHeadl()
    excel_headl.open_excel(config.EXCEL_URL)
    sheets = excel_headl.get_excel_sheets()
    logger.debug(sheets)
    reg_info = excel_headl.get_registers_info(sheets[7])
    logger.debug(reg_info)
    excel_headl.read_excel_end()
