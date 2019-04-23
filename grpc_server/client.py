#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/19 10:43
# @Author  : LUO YING
# @Site    : 
# @File    : helloworld_grpc_client.py.py
# @Detail    :
import grpc

import grpc_server.views.helloworld_pb2 as helloworld_pb2
import grpc_server.views.helloworld_pb2_grpc as helloworld_pb2_grpc


def run():
    # 连接 rpc 服务器
    channel = grpc.insecure_channel('localhost:7070')
    # 调用 rpc 服务
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='ying'))
    print("Greeter client received: " + response.message)
    response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='ying'))
    print("Greeter client received: " + response.message)
    response = stub.ListFeature(helloworld_pb2.HelloRequest())

    for feature in response:
        print("Feature called {name} have body {body}".format(name=feature.name, body=feature.body))
    # print(response)
    response = stub.query(helloworld_pb2.HelloRequest(id=2))
    print("Greeter client ListFeature received: ")
    print(response.message)
    print(response.data)


if __name__ == '__main__':
    run()
