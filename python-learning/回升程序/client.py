# -*- coding: utf-8 -*-
# 客户端：连接服务端，发一条消息过去
import socket

# 1. 创建 TCP 套接字
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2. 连接服务端
sk.connect(('127.0.0.1', 9000))

# 3. 发送一条消息
msg = 'hello, 我是客户端'
sk.send(msg.encode('utf-8'))
print('已发送：', msg)

# 4. 关闭连接
sk.close()
