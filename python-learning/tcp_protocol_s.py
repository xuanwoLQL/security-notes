#====[新增]:带自定义协议（长度前缀）的TCP服务端，用来解决粘包问题====
#自定义协议：每条消息 = 4字节长度(大端序) + 消息体，消息体是JSON
import socket
import struct
import json
import time

HEAD_LEN=4          #协议头的长度：4个字节
MAX_LEN=1024*1024   #消息体最大长度，防止收到乱码时申请一个超大的内存

def send_msg(connsk,sender,content):
    """按自定义协议发送一条消息：先发4字节长度，再发消息体"""
    msg={'sender':sender,'content':content,'time':time.strftime('%H:%M:%S')}
    #ensure_ascii=False 是为了让中文直接以utf-8编码，而不是写成\uXXXX
    body=json.dumps(msg,ensure_ascii=False).encode('utf-8')
    #!I表示按网络字节序（大端）打包成4字节无符号整数，len()算的是字节数
    head=struct.pack('!I',len(body))
    connsk.send(head+body)

def recv_all(connsk,n):
    """一次recv不一定能收满n个字节，要循环收，收满为止"""
    buf=b''
    while len(buf)<n:
        part=connsk.recv(n-len(buf))
        if not part:
            return None     #对方关闭了连接
        buf=buf+part
    return buf

def recv_msg(connsk):
    """按自定义协议接收一条完整的消息，返回字典；对方关闭连接时返回None"""
    head=recv_all(connsk,HEAD_LEN)
    if head is None:
        return None
    #先读协议头，知道这条消息有多长
    length=struct.unpack('!I',head)[0]
    if length>MAX_LEN:
        print(f'收到不合理的长度{length}，直接断开连接')
        return None
    #再按这个长度把消息体读完，这样就不会把两条消息粘在一起
    body=recv_all(connsk,length)
    if body is None:
        return None
    return json.loads(body.decode('utf-8'))

#创建套接字
sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#绑定地址
sk.bind(('127.0.0.1',8082))
#设置监听
sk.listen(5)
print('带自定义协议的服务端已启动，等待客户端连接……')
try:
    while True:
        connsk,addr=sk.accept()
        print(f'客户端{addr}已连接')
        try:
            while True:
                msg=recv_msg(connsk)
                if msg is None:
                    print(f'客户端{addr}关闭连接')
                    break
                print(f'收到[{msg["sender"]}] {msg["content"]} ({msg["time"]})')
                if msg['content'].upper()=='QUIT':
                    send_msg(connsk,'服务器','拜拜')
                    break
                send_msg(connsk,'服务器',f'已收到[{msg["content"]}]')
        #====[新增]:异常处理，客户端断开、数据不合法都不会让服务端崩溃====
        except (ConnectionResetError,BrokenPipeError) as e:
            print(f'客户端{addr}异常断开:{e}')
        except json.JSONDecodeError:
            print(f'客户端{addr}发来的内容不是合法的JSON，这条消息被丢弃')
        finally:
            connsk.close()
            print(f'客户端{addr}已退出，服务端继续等待新的连接')
except KeyboardInterrupt:
    print('\n服务端退出')
finally:
    sk.close()
