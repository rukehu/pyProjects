#!/usr/bin/python
# -*- coding: UTF-8 -*-

from PySide2 import QtCore
from PySide2.QtWidgets import *
from ui.designer.UI_infowidget import Ui_Form
import logging


class InfoWidget(QWidget, Ui_Form):
    new_message = QtCore.Signal(object)

    class LogHandler(logging.Handler):
        def __init__(self, fun):
            logging.Handler.__init__(self)
            self.fun = fun
            self.setFormatter(logging.Formatter('%(name)-12s %(levelname)8s %(message)s'))

        def emit(self, record):
            if self.fun != None:
                self.fun(record)

    def __init__(self):
        super(InfoWidget, self).__init__()
        self.setupUi(self)

        self.log_handler = InfoWidget.LogHandler(self.setTipInfo)
        self.log_handler.setLevel(logging.NOTSET)
        logging.getLogger().addHandler(self.log_handler)

        self.new_message.connect(self.on_message)

    def setTipInfo(self, record):
        self.new_message.emit(record)

    def on_message(self, record):
        msg = self.log_handler.format(record)
        self.textEdit.append(msg)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    MainWidget = InfoWidget()
    MainWidget.setWindowTitle("control")
    MainWidget.show()
    logger = logging.getLogger('test')
    logger.debug('hello')
    sys.exit(app.exec_())
