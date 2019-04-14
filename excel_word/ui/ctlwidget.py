#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from PySide2 import QtCore
from PySide2.QtWidgets import *
from ui.designer.UI_controlwidget import Ui_ControlWgt
import config
import logging, json

logger = logging.getLogger('controlwgt')

class ControlWidget(QWidget, Ui_ControlWgt):
    signal_inport_excels = QtCore.Signal(list)

    def __init__(self):
        super(ControlWidget, self).__init__()
        self.setupUi(self)

        self.inport_btn.clicked.connect(self.__inport_btn_clicked)
        self.select_btn.clicked.connect(self.__select_btn_clicked)

    def __inport_btn_clicked(self):
        excels = 'excel (*.xlsx)'
        json_f = 'json (*.json)'

        file_path = QFileDialog.getOpenFileNames(self, '选择.xlsx/.json文件', filter=excels + ';;' + json_f)
        logger.debug(file_path[0])
        load_list = list()

        if file_path[1] == json_f:
            _path = file_path[0]
            self.path_edit.setText(_path[0])

            with open(_path[0], 'r') as f_json:
                load_list = json.load(f_json)

        elif file_path[1] == excels:
            paths = file_path[0]

            if len(paths) == 1:
                self.path_edit.setText(paths[0])
            else:
                f_info = QtCore.QFileInfo(paths[0])
                self.path_edit.setText(f_info.absolutePath())
                config.EXCEL_DIR = f_info.absolutePath()

            for _path in paths:
                path_dct = {}
                path_dct['url'] = _path
                path_dct['table_number'] = -1
                load_list.append(path_dct)

        print(load_list)

        if len(load_list):
            self.signal_inport_excels.emit(load_list)

    def __select_btn_clicked(self):
        dir = QFileDialog.getExistingDirectory()
        if len(dir) > 0:
            self.export_edit.setText(dir)
            config.WORD_URL = dir + '/' + 'tables.docx'
            config.WORD_DIR = dir

    def get_file_select_state(self):
        state_dct = dict()
        if self.files_box.isChecked():
            state_dct['files'] = True
        else:
            state_dct['files'] = False

        if self.once_box.isChecked():
            state_dct['once'] = True
        else:
            state_dct['once'] = False

        return state_dct

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MainWidget = ControlWidget()
    MainWidget.setWindowTitle("control")
    MainWidget.show()
    sys.exit(app.exec_())
