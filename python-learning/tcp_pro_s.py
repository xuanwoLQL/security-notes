#解决Tcp粘包问题
from socket import *
import struct
sk=socket(AF_INET,SOCK_STREAM)
sk.bind(('127.0.0.1',8888))
sk.listen()
conn,addr=sk.accept()

#先接收4字节
n=conn.recv(4)
#转换成长度值
str_n=struct.unpack('i',n)[0]
#接收数据
data1=conn.recv(str_n).decode('utf-8')

#先接受4字节
n=conn.recv(4)
#转换成长度值
str_n=struct.unpack('i',n)[0]
#接收数据
data2=conn.recv(str_n).decode('utf-8')

print('----->',data1)
print('----->',data2)
conn.close()