#!/usr/bin/python
# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from ui.designer.UI_TerminalWidget import Ui_Terminal
from ui.ctlwidget import ControlWidget
from ui.tabwidget import ExcelWidget
from ui.infowidget import InfoWidget
import logging

logger = logging.getLogger('Terminal')

class Terminal(QWidget, Ui_Terminal):

    def __init__(self):
        super(Terminal, self).__init__()
        self.setupUi(self)

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


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MainWidget = Terminal()
    MainWidget.setWindowTitle("control")
    MainWidget.show()
    sys.exit(app.exec_())
