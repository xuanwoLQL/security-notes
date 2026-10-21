# -*- coding: utf-8 -*-
"""
“消息 & 文件上传和下载”公共协议模块

需求要求客户端、服务端都定义 send_data / send_file / recv_data / recv_file。
为了让这些函数既能发消息又能发文件（协议对称化），本模块把收发细节抽出来：

本实验使用的自定义协议（解决粘包问题）：
    每一帧 = 1 字节 类型 + 8 字节 长度(大端) + 负载
    类型 'M' = 消息，负载是 UTF-8 文本
    类型 'F' = 文件，负载 = 4 字节文件名长度 + 文件名 + 文件内容
    类型 'C' = close，表示要关闭链接（负载为空）

收的时候先读 1 字节类型、再读 8 字节长度，然后按长度把负载读满，
所以多条数据粘在一起也能被正确拆开，不会只读到一半。
"""

import struct

TYPE_DATA = b'M'
TYPE_FILE = b'F'
TYPE_CLOSE = b'C'

HEAD = struct.Struct('!cQ')       # !c = 1 字节字符, !Q = 8 字节无符号大端
HEAD_LEN = HEAD.size


def pack_frame(type_byte, payload):
    """把类型和负载打包成一帧。"""
    return HEAD.pack(type_byte, len(payload)) + payload


def recv_all(sock, n):
    """收满 n 个字节；对方关闭连接时返回 None。"""
    buf = b''
    while len(buf) < n:
        part = sock.recv(n - len(buf))
        if not part:
            return None
        buf += part
    return buf


def recv_frame(sock):
    """
    接收一帧，返回 (类型, 负载)。
    对方正常关闭链接时返回 (None, None)。
    """
    head = recv_all(sock, HEAD_LEN)
    if head is None:
        return None, None
    type_byte, length = HEAD.unpack(head)
    payload = b''
    if length:
        payload = recv_all(sock, length)
        if payload is None:
            return None, None
    return type_byte, payload


def read_file(path, chunk=1024 * 4):
    """读文件为字节串（示例文件不大；大文件可以改成分块发送）。"""
    with open(path, 'rb') as f:
        return f.read()
