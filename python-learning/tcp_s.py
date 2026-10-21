import socket
import threading
#创建套接字
sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#绑定地址
sk.bind(('127.0.0.1',8081))
#设置监听
sk.listen(5)
print("服务端已启动，等待客户连接")

#====[新增]:把原来收发数据的代码写成一个函数，参数就是accept得到的connsk和addr====
def handle_client(connsk,addr):
    print(f'客户端{addr}已连接')
    #收发数据
    try:
        while True:
            data=connsk.recv(1024)
            #====[新增]:recv收到空字节串，说明客户端已经关闭了连接====
            if not data:
                print(f'客户端{addr}关闭连接')
                break
            msg=data.decode('utf-8').strip()
            #====[新增]:回显功能====
            if msg.upper()=='QUIT':
                reply='Goodebye'
            else:
                reply=f'{msg}'#服务器原样回显
            connsk.send(reply.encode('utf-8'))
            print(f'回显给客户端{addr}:{repr(reply)}')
            #客户端说退出，回完话就结束这个客户端的服务
            if msg.upper()=='QUIT':
                break
    #====[新增]:客户端直接关窗口会用异常的方式断开，接住它，服务端不崩溃====
    except (ConnectionResetError,BrokenPipeError) as e:
        print(f'客户端{addr}异常断开:{e}')
    finally:
        #只关闭这条连接，监听套接字sk还在，可以继续接受别的客户端
        connsk.close()
        print(f'客户端{addr}已退出，服务端继续等待新的连接')

#====[新增]:循环接受多个客户端，一个客户端退出后服务端不退出====
try:
    while True:
        #阻塞等待客户端请求
        connsk,addr=sk.accept()
        #====[新增]:每个客户端开一个线程来处理，可以同时和多个客户端通信====
        t=threading.Thread(target=handle_client,args=(connsk,addr),daemon=True)
        t.start()
except KeyboardInterrupt:
    #====[新增]:Ctrl+C时优雅退出，而不是报一堆错误====
    print("\n服务端退出")
finally:
    #关闭套接字
    sk.close()
