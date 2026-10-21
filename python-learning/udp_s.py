#====[新增]:UDP单词查询服务端====
import socket
#单词表：用字典保存，键是单词，值是单词的解释
word_dict={
    'socket':'套接字，网络编程中用来收发数据的接口',
    'tcp':'传输控制协议，面向连接、可靠、字节流',
    'udp':'用户数据报协议，无连接、不保证可靠、效率高',
    'port':'端口，一台电脑上用来区分不同程序的编号',
    'ip':'网络地址，用来在网络中找到一台主机',
    'bind':'绑定，把套接字和服务器的IP、端口关联起来',
    'echo':'回显，服务器把收到的数据原样返回给客户端',
    'apple':'苹果，一种水果',
    'hello':'你好，见面打招呼用的词',
    'student':'学生，在学校里学习的人',
}
#创建套接字，SOCK_DGRAM表示UDP
sk=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#绑定地址
sk.bind(('127.0.0.1',9000))
print('UDP单词查询服务端已启动，等待客户端查询……')
#====[新增]:循环接收，可以给很多个客户端查单词====
try:
    while True:
        #收发数据，recvfrom一次就能拿到数据和对方的地址
        data,addr=sk.recvfrom(1024)
        msg=data.decode('utf-8').strip()
        print(f'收到来自{addr}的查询：{msg}')
        #自定义的简单应用层协议：请求就是单词本身，应答是解释或者"没有该单词"
        #统一转成小写再查，这样输入 Apple 和 apple 都能查到
        if msg.lower() in word_dict:
            reply=word_dict[msg.lower()]
        else:
            reply='没有该单词'
        #UDP不需要连接，用sendto指定发给谁
        sk.sendto(reply.encode('utf-8'),addr)
        print(f'回复{addr}：{reply}')
except KeyboardInterrupt:
    print('\n服务端退出')
finally:
    #关闭套接字
    sk.close()
