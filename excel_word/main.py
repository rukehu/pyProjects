#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, os
import json
from source.excel import ExcelHeadl
from source.word import WrodHandl
import logging
import config

logger = logging.getLogger('main')
logging.basicConfig(level=logging.DEBUG, format='%(name)s [line:%(lineno)d] %(message)s')

filter=['.xlsx']        # 过滤文件

class SwitchControl(object):
    def __init__(self):
        self._excel_headl = ExcelHeadl()
        self._word_headl = WrodHandl()

    def get_excels_url(self, excel_dir):
        """
        根据指定路径获取excels
        :param excel_dir: 表格所载目录
        :return:list()
        """
        excel_files = list()  # 所有的文件

        if not os.path.isdir(config.EXCEL_DIR):
            logger.info('dir non-exist:', config.EXCEL_DIR)
            return excel_files

        for maindir, subdir, files in os.walk(excel_dir):
            for file_name in files:
                if file_name.find('~$', 0, 2) != -1:
                    continue
                apath = os.path.join(maindir, file_name)  # 合并成一个完整路径
                ext = os.path.splitext(apath)[1]          # 获取文件后缀 [0]获取的是除了文件名以外的内容

                if ext in filter:
                    excel_files.append(apath)

        return excel_files

    def update_sequence_list(self, excels_url):
        """
        更新寄存器顺序表，不存在则生成
        :return:
        """
        load_list = list()
        sequen_list = list()

        if os.path.exists(config.SEQUENCE_URL) and os.path.getsize(config.SEQUENCE_URL) > 0:
            with open(config.SEQUENCE_URL, 'r') as f_json:
                load_list = json.load(f_json)
                sequen_list = load_list
                logger.debug(sequen_list)

        for excel in excels_url:
            url_exist = False
            for load_dct in load_list:
                if excel == load_dct['url']:
                    url_exist = True
                    break

            sequen_dct = {}
            if not url_exist:
                sequen_dct['url'] = excel
                sequen_dct['table_number'] = 0
                sequen_list.append(sequen_dct)

        if len(sequen_list) > 0:
            with open(config.SEQUENCE_URL, 'w') as f_json:
                json_str = json.dumps(sequen_list, indent=4)
                f_json.write(json_str)


    def make_word_dir(self):
        """
        检查word 文档目录是否存在，不存在则创建
        :return:
        """
        if not os.path.isdir(config.WORD_DIR):
            os.makedirs(config.WORD_DIR)

    def excel_to_word(self, excel_url, word_dir):
        if not self._excel_headl.open_excel(excel_url):
            return

        self._word_headl.open_word(None)
        sheets = self._excel_headl.get_excel_sheets()
        # 第一个表格为版本说明，将其移出
        if len(sheets) > 0 and sheets[0] == u'版本说明':
            sheets.pop(0)

        for sheet in sheets:
            logger.debug(sheet)
            reg_info = self._excel_headl.get_registers_info(sheet)
            logger.debug(reg_info['head_info'])
            logger.debug(reg_info['reg_list'])
            self._word_headl.write_register_toword(sheet, reg_info)

        self._excel_headl.read_excel_end()

        excel_name = excel_url.split('\\').pop()
        word_name = excel_name.split('.')[0] + '.docx'

        word_url = word_dir + '\\' + word_name
        self._word_headl.write_word_end(word_url)


    def excels_to_word(self, excels_url, word_path):
        pass



if __name__ == '__main__':
    sw_control = SwitchControl()

    excels_url = sw_control.get_excels_url(config.EXCEL_DIR)
    logger.debug(excels_url)
    sw_control.update_sequence_list(excels_url)
    sw_control.make_word_dir()            # 检查word文档生成目录是否存在

    # for e_url in excels_url:
    #     logger.debug(e_url)
    #     sw_control.excel_to_word(e_url, config.WORD_DIR)
    #     logger.debug('----------------------------------\r\n')

    # 单个文档测试
    # e_url = 'D:\PyProjects\excel_word\ExcelTables\L3.xlsx'
    # sw_control.excel_to_word(e_url, config.WORD_DIR)