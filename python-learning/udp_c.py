#====[新增]:UDP单词查询客户端====
import socket
#创建套接字，SOCK_DGRAM表示UDP
sk=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#====[新增]:设置超时时间，UDP不保证可靠，收不到回复时能提示出来====
sk.settimeout(3)
print('UDP单词查询客户端，输入单词回车查询，直接回车退出')
count=0
#====[新增]:循环输入单词，直到输入空退出====
try:
    while True:
        word=input('请输入要查询的单词：').strip()
        if not word:
            break
        #收发数据，UDP不用connect，直接sendto到服务器的地址
        sk.sendto(word.encode('utf-8'),('127.0.0.1',9000))
        count=count+1
        try:
            data,addr=sk.recvfrom(1024)
            print(f'查询结果:{data.decode("utf-8")}')
        except socket.timeout:
            #====[新增]:超时提示，体现UDP"尽力而为"的特点====
            print('查询超时：没有收到服务端的回复（UDP不保证一定能送到）')
        except ConnectionResetError:
            #====[新增]:Windows下服务端没启动时，系统会说"对方不可达"====
            print('收不到回复：服务端可能没有启动，请先运行 udp_s.py')
except KeyboardInterrupt:
    print('\n你按了Ctrl+C')
finally:
    #关闭套接字
    sk.close()
print(f'客户端退出，一共查询了{count}个单词')
