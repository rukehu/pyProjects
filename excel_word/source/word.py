#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, os
from docx import Document
from docx.shared import Inches


class WrodHandl(object):
    def __init__(self):
        self._word_doc = Document()
        pass