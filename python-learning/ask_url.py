import socket
ck=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print(ck)
#连接服务器
ck.connect(('www.baidu.com', 80))
print(ck)
#收发数据：发送http:请求-->接收返回数据
ck.send(b'GET / HTTP/1.1\r\nHost: www.baidu.com\r\nConnection: close\r\n\r\n')
buffer=[]
while True:
    d=ck.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
ck.close()