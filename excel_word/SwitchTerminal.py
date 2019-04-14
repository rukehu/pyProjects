#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from PySide2.QtWidgets import *
from ui.designer.UI_TerminalWidget import Ui_Terminal
from ui.ctlwidget import ControlWidget
from ui.tabwidget import ExcelWidget
from ui.infowidget import InfoWidget
from source.excel import ExcelHeadl
from source.word import WrodHandl
import config
import logging


logger = logging.getLogger('Terminal')

class Terminal(QWidget, Ui_Terminal):

    def __init__(self):
        super(Terminal, self).__init__()
        self.setupUi(self)

        self._excel_headl = ExcelHeadl()
        self._word_headl = WrodHandl()

        self._ctl_widget = ControlWidget()
        layout_v = QVBoxLayout()
        layout_v.addWidget(self._ctl_widget)
        layout_v.setContentsMargins(0, 0, 0, 0)
        self.ControlFrame.setLayout(layout_v)

        self._excel_widget = ExcelWidget()
        layout_v = QVBoxLayout()
        layout_v.addWidget(self._excel_widget)
        layout_v.setContentsMargins(0, 0, 0, 0)
        self.TableFrame.setLayout(layout_v)

        self._info_widget = InfoWidget()
        layout_v = QVBoxLayout()
        layout_v.addWidget(self._info_widget)
        layout_v.setContentsMargins(0, 0, 0, 0)
        self.InforFrame.setLayout(layout_v)

        self._ctl_widget.signal_inport_excels.connect(self._excel_widget.load_excel_info)
        self._excel_widget.signal_start_switch.connect(self.start_excel_to_word)

    def resizeEvent(self, evt):
        self._excel_widget.resize_table_widget()

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

        excel_name = excel_url.split('/').pop()
        word_name = excel_name.split('.')[0] + '.docx'

        word_url = word_dir + '/' + word_name
        self._word_headl.write_word_end(word_url)

    def excels_to_words(self, excels_dct, word_dir):
        logger.info(excels_dct)
        for e_dct in excels_dct:
            num = e_dct['table_number']
            if num > 0:
                self._word_headlset_table_number(num)
            self.excel_to_word(e_dct['url'], word_dir)

    def excels_to_word(self, excels_dct, word_url):
        """
        :param excels_url:
        :param word_path:
        :return:
        """
        self._word_headl.open_word(None)
        logger.info(excels_dct)

        for excel in excels_dct:
            if not self._excel_headl.open_excel(excel['url']):
                continue
            self._word_headl.set_table_number( excel['table_number'])

            sheets = self._excel_headl.get_excel_sheets()
            if len(sheets) > 0 and sheets[0] == u'版本说明':
                sheets.pop(0)

            for sheet in sheets:
                logger.debug(sheet)
                reg_info = self._excel_headl.get_registers_info(sheet)
                logger.debug(reg_info['head_info'])
                logger.debug(reg_info['reg_list'])
                self._word_headl.write_register_toword(sheet, reg_info)

            self._excel_headl.read_excel_end()

        self._word_headl.write_word_end(word_url)

    def start_excel_to_word(self, sequen_list):
        sw_state = self._ctl_widget.get_file_select_state()
        if not os.path.isdir(config.WORD_DIR):
            os.makedirs(config.WORD_DIR)

        if sw_state['files']:
            self._word_headl.set_table_number(1)
            self.excels_to_words(sequen_list, config.WORD_DIR)
            logger.info('excels to words end...')

        if sw_state['once']:
            self._word_headl.set_table_number(1)
            self.excels_to_word(sequen_list, config.WORD_URL)
            logger.info('excels to word end...')

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MainWidget = Terminal()
    MainWidget.setWindowTitle('Excel转word')
    MainWidget.show()
    sys.exit(app.exec_())
