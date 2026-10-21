import socket
sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#连接服务器，下面括号里面的东西是一个元组
try:
    sk.connect(('127.0.0.1',8081))
except ConnectionRefusedError:
    #====[新增]:服务端没启动时给个提示就退出，而不是报一大堆红字====
    print("连接失败：服务端没有启动，请先运行 tcp_s.py")
    sk.close()
else:
    print("已连接，输入quit退出")
    #循环收发数据
    while True:
        try:
            msg=input("你:").strip()
            if not msg:
                continue
            #====[新增]:粘包现象演示，把三条消息拼在一起只send一次====
            if msg=='sticky':
                sk.send(b'aa'+b'bb'+b'cc')
                print("已把[aa][bb][cc]三条消息拼成一段一次性发出")
                print(f"服务端:{sk.recv(1024).decode('utf-8').strip()}")
                continue
            #编辑成字节流
            sk.send(msg.encode('utf-8'))
            reply=sk.recv(1024)
            #====[新增]:recv收到空字节串，说明服务端已经退出了====
            if not reply:
                print("服务端已关闭连接")
                break
            reply=reply.decode('utf-8').strip()
            print(f"服务端:{reply}")
            if reply=='Goodebye':
                break
        #====[新增]:服务端先退出时客户端优雅退出，而不是崩溃====
        except OSError as e:
            print(f"与服务端的连接已断开：{e}")
            break
        #====[新增]:Ctrl+C也能正常退出====
        except KeyboardInterrupt:
            print("\n你按了Ctrl+C")
            break
    #关闭套接字
    sk.close()
    print("客户端退出")
