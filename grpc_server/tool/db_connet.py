#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/22 16:03
# @Author  : LUO YING
# @Site    : 
# @File    : db_connet.py
# @Detail    :

from grpc_server.tool._tools import BaseHandler, session_ctx
from grpc_server.tool.models import Message


class MessageHandler(BaseHandler):
    def query(self, unit=-1):
        return self._query_normal(unit)

    def _query_normal(self, unit=-1):
        if unit != -1:
            return self._query_by_id(unit)
        else:
            with session_ctx() as session:
                us = session.query(Message).all()
                us = self.obj_converter.convert_list(us)
                return us

    def _query_by_id(self, unit: int):
        with session_ctx() as session:
            u = session.query(Message).filter(Message.id == unit).all()
            u = self.obj_converter.convert_list(u)
            return u


if __name__ == '__main__':
    m = MessageHandler()
    res = m.query()
    print(res)
