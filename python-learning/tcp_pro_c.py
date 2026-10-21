import socket
import struct
ck=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ck.connect(('127.0.0.1',8888))
#先求发送数据的长度
str_n=len(b'Hello, World!')
#用struct模块把长度值转换成4字节的二进制数据
n=struct.pack('i',str_n)
#发送长度
ck.send(n)
#发送数据
ck.send(b'Hello, World!')

#先求发送数据的长度
str_n=len(b'dog')
#用struct模块把长度值转换成4字节的二进制数据
n=struct.pack('i',str_n)
#发送长度
ck.send(n)
#发送数据
ck.send(b'dog')

ck.close()