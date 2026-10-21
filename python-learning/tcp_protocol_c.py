#====[新增]:带自定义协议（长度前缀）的TCP客户端，用来测试粘包问题====
#自定义协议：每条消息 = 4字节长度(大端序) + 消息体，消息体是JSON
import socket
import struct
import json
import time

HEAD_LEN=4          #协议头的长度：4个字节
MAX_LEN=1024*1024   #消息体最大长度
SENDER='客户端'      #消息里记录的发送者

def make_body(content):
    """把一条消息拼成JSON字节串"""
    msg={'sender':SENDER,'content':content,'time':time.strftime('%H:%M:%S')}
    return json.dumps(msg,ensure_ascii=False).encode('utf-8')

def send_msg(sk,content):
    """按自定义协议发送一条消息：先发4字节长度，再发消息体"""
    body=make_body(content)
    #!I表示按网络字节序（大端）打包成4字节无符号整数
    head=struct.pack('!I',len(body))
    sk.send(head+body)

def recv_all(sk,n):
    """一次recv不一定能收满n个字节，要循环收，收满为止"""
    buf=b''
    while len(buf)<n:
        part=sk.recv(n-len(buf))
        if not part:
            return None     #服务端关闭了连接
        buf=buf+part
    return buf

def recv_msg(sk):
    """按自定义协议接收一条完整的消息，返回字典；服务端关闭连接时返回None"""
    head=recv_all(sk,HEAD_LEN)
    if head is None:
        return None
    length=struct.unpack('!I',head)[0]
    if length>MAX_LEN:
        return None
    body=recv_all(sk,length)
    if body is None:
        return None
    return json.loads(body.decode('utf-8'))

#创建套接字
sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#连接服务端
try:
    sk.connect(('127.0.0.1',8082))
except ConnectionRefusedError:
    print('连接失败：服务端没有启动，请先运行 tcp_protocol_s.py')
    sk.close()
else:
    print('已连接，输入消息发送给服务端；输入 burst 演示粘包；输入 quit 退出')
    while True:
        try:
            text=input('我:').strip()
            if not text:
                continue
            if text=='burst':
                #====[新增]:把三条消息按协议拼成一段，只send一次，故意做出粘包====
                data=b''
                for word in ['aa','bb','cc']:
                    body=make_body(word)
                    data=data+struct.pack('!I',len(body))+body
                sk.send(data)
                print('已把aa、bb、cc三条消息拼在一起一次性发出')
                for i in range(3):
                    reply=recv_msg(sk)
                    print(f'服务端回复{i+1}:{reply["content"]}')
                continue
            #正常发送一条消息
            send_msg(sk,text)
            reply=recv_msg(sk)
            if reply is None:
                print('服务端已关闭连接')
                break
            print(f'服务端:{reply["content"]}  （{reply["time"]}）')
            if text=='quit':
                break
        except OSError as e:
            print(f'与服务端的连接已断开：{e}')
            break
        except KeyboardInterrupt:
            print('\n你按了Ctrl+C')
            break
    #关闭套接字
    sk.close()
    print('客户端退出')
