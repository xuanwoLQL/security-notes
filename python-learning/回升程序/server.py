# -*- coding: utf-8 -*-
# 服务端：等客户端连上来，收到它发来的一条消息，打印出来
import socket

# 1. 创建 TCP 套接字
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2. 绑定本机地址和端口
sk.bind(('127.0.0.1', 9000))
# 3. 开始监听，等待客户端连接
sk.listen(5)
print('服务端已启动，等待客户端连接……')

# 4. 阻塞等待，直到有客户端连上来
conn, addr = sk.accept()
print('客户端已连接：', addr)

# 5. 接收客户端发来的数据，并打印
data = conn.recv(1024)
print('收到的消息：', data.decode('utf-8'))

# 6. 关闭连接
conn.close()
sk.close()
