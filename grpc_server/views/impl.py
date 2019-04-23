#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/23 10:15
# @Author  : LUO YING
# @Site    : 
# @File    : impl.py
# @Detail    :


import json

from grpc_server.tool.db_connet import MessageHandler
from .helloworld_pb2 import HelloReply, HelloRequest, MessageInfo
from .helloworld_pb2_grpc import GreeterServicer


class MessageQueryImpl(GreeterServicer):
    drh = MessageHandler()

    def query(self, request, context):
        return self._query(request.id)

    def _query(self, uid: int) -> HelloReply:
        """根据ID查询信息"""
        try:
            ret = self.drh.query(uid)

            if len(ret) == 1:
                r = HelloRequest(name=ret[0]['name'], body=ret[0]['body'])
                return HelloReply(code=0, message=json.dumps(ret), data=r)
            return HelloReply(code=0, message=json.dumps(ret), )

        except Exception as e:
            return HelloReply(code=500, message="failed: {}".format(e))

    def _query_all(self, ):
        ret = self.drh.query()
        return ret

        # 实现 proto 文件中定义的 rpc 调用

    def SayHello(self, request, context):
        return HelloReply(message='hello {msg}'.format(msg=request.name))

    def SayHelloAgain(self, request, context):
        return HelloReply(message='hello {msg}'.format(msg=request.name))

    def _read_query(self):
        feature_list = []
        for item in self._query_all():
            feature = MessageInfo(
                name=item['name'],
                body=item['body']
            )
            feature_list.append(feature)
        return feature_list

    def ListFeature(self, request, context):
        db = self._read_query()
        for feature in db:
            yield feature
