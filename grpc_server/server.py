#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/23 15:44
# @Author  : LUO YING
# @Site    : 
# @File    : server.py
# @Detail    :
import time
from concurrent import futures

import grpc

from grpc_server.views import helloworld_pb2_grpc
from grpc_server.views.impl import MessageQueryImpl

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'
_PORT = '7070'


def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(MessageQueryImpl(), grpcServer)
    grpcServer.add_insecure_port(_HOST + ':' + _PORT)
    grpcServer.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)


if __name__ == '__main__':
    serve()
