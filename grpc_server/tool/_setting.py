#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/22 14:55
# @Author  : LUO YING
# @Site    : 
# @File    : _setting.py
# @Detail    :
import os

dir = os.path.dirname(os.path.abspath(__file__))
DB_URI = 'sqlite:///{}\database.sqlite3'.format(os.path.dirname(dir))

print(DB_URI)
