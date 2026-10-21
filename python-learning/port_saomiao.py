import socket
import time
for port in range(8880,9000):
    ck=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    n=ck.connect_ex(('127.0.0.1',port))
    print(n)
    if(n==0):
        print('端口号为：',port,'的服务已开启')
    ck.close()