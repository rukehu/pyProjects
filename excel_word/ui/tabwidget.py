#!/usr/bin/python
# -*- coding: UTF-8 -*-


import os, logging
from PySide2 import QtCore
from PySide2.QtWidgets import *
from ui.designer.UI_tablewidget import Ui_ExcelWgt
import json
import config

logger = logging.getLogger('ExcelWidget')

class ExcelWidget(QWidget, Ui_ExcelWgt):
    signal_start_switch = QtCore.Signal(list)

    def __init__(self):
        super(ExcelWidget, self).__init__()
        self.setupUi(self)

        self.table_widget.verticalHeader().setHidden(True)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.horizontalScrollBar().setEnabled(False)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)    # 关闭水平表头拖动

        self._set_width = False
        self._box_list = list()

        self.table_widget.setDragDropMode(QAbstractItemView.DragDrop)
        self.table_widget.setDragEnabled(True)
        self.table_widget.setAcceptDrops(True)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.select_btn.clicked.connect(self.__select_btn_clicked)
        self.remove_btn.clicked.connect(self.__remove_btn_clicked)
        self.reset_btn.clicked.connect(self.__reset_btn_clicked)
        self.save_btn.clicked.connect(self.__save_btn_clicked)
        self.start_btn.clicked.connect(self.__start_btn_clicked)

    def __select_btn_clicked(self):
        for box in self._box_list:
            box.setChecked(True)

    def __remove_btn_clicked(self):
        idx_list = list()

        for idx in range(len(self._box_list)):
            if self._box_list[idx].isChecked():
                idx_list.append(idx)

        # table widget须倒序删除
        idx_list = sorted(idx_list, reverse=True)
        for idx in idx_list:
            self._box_list.pop(idx)
            self.table_widget.removeRow(idx)

        for idx in range(len(self._box_list)):
            self.table_widget.item(idx, 1).setText(str(idx))

    def __reset_btn_clicked(self):
        for idx in range(len(self._box_list)):
            self.table_widget.item(idx, 3).setText(u'自动编号')

    def __save_btn_clicked(self):
        f_path = QFileDialog.getSaveFileName(self, '保存配置', dir='sequence.json', filter='json (*.json)')
        print(f_path)

        sequen_list = list()
        for idx in range(len(self._box_list)):
            sequen_dct = {}
            item = self.table_widget.item(idx, 2)
            sequen_dct['url'] = config.EXCEL_DIR + '/' + item.text()
            item = self.table_widget.item(idx, 3)
            num_str = item.text()
            if num_str.isdigit():
                sequen_dct['table_number'] = int(num_str)
            else:
                sequen_dct['table_number'] = -1

            sequen_list.append(sequen_dct)

        if len(f_path) > 0:
            with open(f_path[0], 'w') as f_json:
                json_str = json.dumps(sequen_list, indent=4)
                f_json.write(json_str)

    def __start_btn_clicked(self):
        sequen_list = list()
        for idx in range(len(self._box_list)):
            if self._box_list[idx].isChecked():
                sequen_dct = {}
                item = self.table_widget.item(idx, 2)
                sequen_dct['url'] = config.EXCEL_DIR + '/' + item.text()
                item = self.table_widget.item(idx, 3)
                num_str = item.text()
                if num_str.isdigit():
                    sequen_dct['table_number'] = int(num_str)
                else:
                    sequen_dct['table_number'] = -1

                sequen_list.append(sequen_dct)

        if len(sequen_list) > 0:
            self.signal_start_switch.emit(sequen_list)

    def resize_table_widget(self):
        width = self.table_widget.width() / 5

        if self._set_width:
            self.table_widget.setColumnWidth(0, width)
            self.table_widget.setColumnWidth(1, width)
            self.table_widget.setColumnWidth(2, width)
            self.table_widget.setColumnWidth(3, width)
        self._set_width = True


    def load_excel_info(self, load_list):
        row_idx = 0
        print('hello')
        for excel_info in load_list:
            self.table_widget.setRowCount(row_idx + 1)
            wgt = QWidget(self)
            layout_h = QHBoxLayout()
            chk_box = QCheckBox()
            chk_box.setChecked(True)
            layout_h.addWidget(chk_box)
            layout_h.setContentsMargins(0, 0, 0, 0)
            layout_h.setAlignment(chk_box, QtCore.Qt.AlignCenter)
            wgt.setLayout(layout_h)
            self.table_widget.setCellWidget(row_idx, 0, wgt)
            self._box_list.append(chk_box)

            item = QTableWidgetItem()
            item.setText(str(row_idx))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(item.flags() & (~QtCore.Qt.ItemIsEditable))
            self.table_widget.setItem(row_idx, 1, item)

            item = QTableWidgetItem()
            excel = excel_info['url'].split('/').pop()
            item.setText(excel)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(item.flags() & (~QtCore.Qt.ItemIsEditable))
            self.table_widget.setItem(row_idx, 2, item)

            item = QTableWidgetItem()
            num = excel_info['table_number']
            if num > -1:
                item.setText(str(num))
            else:
                item.setText(u'自动编号')
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table_widget.setItem(row_idx, 3, item)

            wgt = QWidget(self)
            layout_h = QHBoxLayout()
            pgr_bar = QProgressBar()
            pgr_bar.setOrientation(QtCore.Qt.Horizontal)
            pgr_bar.setValue(0)
            pgr_bar.setFormat("0%")
            pgr_bar.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            layout_h.addWidget(pgr_bar)
            layout_h.setMargin(0)
            layout_h.setAlignment(pgr_bar, QtCore.Qt.AlignCenter)
            wgt.setLayout(layout_h)
            self.table_widget.setCellWidget(row_idx, 4, wgt)

            row_idx += 1