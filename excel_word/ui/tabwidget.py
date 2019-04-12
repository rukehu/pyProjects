#!/usr/bin/python
# -*- coding: UTF-8 -*-


from PySide2.QtWidgets import *
from ui.designer.UI_tablewidget import Ui_ExcelWgt

class ExcelWidget(QWidget, Ui_ExcelWgt):

    def __init__(self):
        super(ExcelWidget, self).__init__()
        self.setupUi(self)