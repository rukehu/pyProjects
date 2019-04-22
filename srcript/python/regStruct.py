# -*- coding: utf-8 -*-
__author__ = 'LI JUN'

REG_NAME                        = 0
REG_OFFSET_ADDR                 = 1
REG_TYPE                        = 2
FIELD_NAME_OR_TABLE_WIDTH       = 3
FIELD_OR_INDEX_RANGE            = 4
DATA_VALID_WIDTH                = 5
SUGGEST_CFG                     = 6


ERROR_OK                   = 'error ok'
ERROR_XML_FORMAT           = 'file(template.xml) format error'

# verlog标识符正则表达式
matchRuleStr = '^[A-Za-z_][\w_]+$'

# 基地址与寄存器偏移量地址总共占（DEFAULT_BIT_COUNT*4）位数
DEFAULT_BIT_COUNT = 3
NEW_LINE = '\n'

FPGA_ID = 0
BAR_ID  = 10

SAVE_CSR_CFG_COMMAND_FILE_NAME = "csr_cfg.command"
