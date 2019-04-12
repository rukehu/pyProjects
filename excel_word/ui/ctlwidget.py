#!/usr/bin/python
# -*- coding: UTF-8 -*-

from PySide2.QtCore import QFileInfo
from PySide2.QtWidgets import *
from ui.designer.UI_controlwidget import Ui_ControlWgt
import config
import logging

logger = logging.getLogger('controlwgt')

class ControlWidget(QWidget, Ui_ControlWgt):

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
        path_dct = dict()

        if file_path[1] == json_f:
            _path = file_path[0]
            path_dct['json'] = _path
            self.path_edit.setText(_path)
            return path_dct

        elif file_path[1] == excels:
            paths = file_path[0]
            path_dct['excels'] = paths

            if len(paths) == 1:
                self.path_edit.setText(paths[0])
            else:
                f_info = QFileInfo(paths[0])
                self.path_edit.setText(f_info.absolutePath())

            return path_dct

        return None

    def __select_btn_clicked(self):
        dir = QFileDialog.getExistingDirectory()
        if len(dir) > 0:
            self.export_edit.setText(dir)
            config.WORD_URL = dir + '/' + config.TABLES_NAME
            config.WORD_DIR = dir

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MainWidget = ControlWidget()
    MainWidget.setWindowTitle("control")
    MainWidget.show()
    sys.exit(app.exec_())
