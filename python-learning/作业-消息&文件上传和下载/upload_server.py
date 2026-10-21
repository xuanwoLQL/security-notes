# -*- coding: utf-8 -*-
"""
消息 & 文件上传和下载 —— 服务端

需求：
  - 接收客户端连接后，可以一直接收客户端发送的内容；
  - 该客户端连接断开后，可以继续接收其他客户端的连接请求，与其他客户端通信；
  - 定义 recv_data(conn) 完成消息接收，recv_file(conn, save_dir) 完成文件接收，
    run() 完成逻辑功能；
  - 附加：服务端也能向客户端发送消息/文件（协议对称化）。

用法：
  python upload_server.py [端口] [保存目录]
  默认端口 9200，保存目录 = 脚本目录下的 uploads/。
  服务端控制台也可以敲字：直接敲一行 = 发消息；输入  sendfile 路径 = 发文件给客户端。
"""

import os
import socket
import sys
import threading

from file_protocol import (
    TYPE_DATA, TYPE_FILE, TYPE_CLOSE,
    pack_frame, recv_frame, recv_all, read_file,
)

HOST = '0.0.0.0'
PORT = 9200


def send_data(conn, content):
    """发送一条文本消息。"""
    conn.sendall(pack_frame(TYPE_DATA, content.encode('utf-8')))


def send_file(conn, file_path):
    """发送一个文件：负载 = 4 字节文件名长度 + 文件名 + 文件内容。"""
    name = os.path.basename(file_path)
    name_bytes = name.encode('utf-8')
    payload = len(name_bytes).to_bytes(4, 'big') + name_bytes + read_file(file_path)
    conn.sendall(pack_frame(TYPE_FILE, payload))


def recv_data(conn, payload):
    """处理收到的“消息”帧。"""
    text = payload.decode('utf-8')
    print('[客户端消息] %s' % text)
    return text


def recv_file(conn, payload, save_dir):
    """处理收到的“文件”帧：拆出文件名和文件内容，保存到 save_dir。"""
    if len(payload) < 4:
        print('收到不完整的文件帧，丢弃')
        return None
    name_len = int.from_bytes(payload[:4], 'big')
    name = payload[4:4 + name_len].decode('utf-8')
    content = payload[4 + name_len:]
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, os.path.basename(name))
    with open(save_path, 'wb') as f:
        f.write(content)
    print('[收到文件] 已保存 %s（%d 字节）' % (save_path, len(content)))
    return save_path


# 当前在线的会话：{conn: {'addr':..., 'lock':...}}
_sessions_lock = threading.Lock()
_sessions = {}


def console_reader():
    """
    单独一个线程读服务端控制台输入，然后把消息/文件广播给所有在线客户端。

    注意：不要给每个客户端各开一个 input() 线程——多个线程同时抢同一个 stdin
    会互相抢走对方要读的那一行（这正是调试中遇到的坑）。控制台只读一次、统一分发。
    """
    while True:
        try:
            line = input()
        except EOFError:
            return
        line = line.strip()
        if not line:
            continue
        if line.startswith('sendfile '):
            path = line[len('sendfile '):].strip()
            if not os.path.isfile(path):
                print('[服务端] 文件不存在：%s' % path)
                continue
            with _sessions_lock:
                targets = list(_sessions.items())
            for conn, info in targets:
                try:
                    with info['lock']:
                        send_file(conn, path)
                    print('[服务端] 已发送文件 %s 给 %s' % (path, info['addr']))
                except OSError:
                    pass
        else:
            with _sessions_lock:
                targets = list(_sessions.items())
            for conn, info in targets:
                try:
                    with info['lock']:
                        send_data(conn, line)
                except OSError:
                    pass
            print('[服务端] 已广播消息：%s' % line)


def run(conn, addr, save_dir):
    """一个客户端的完整逻辑：循环收帧，直到收到 close / 连接断开。"""
    send_lock = threading.Lock()
    with _sessions_lock:
        _sessions[conn] = {'addr': addr, 'lock': send_lock}
    try:
        while True:
            type_byte, payload = recv_frame(conn)
            if type_byte is None:
                print('客户端 %s 关闭了连接' % (addr,))
                break
            if type_byte == TYPE_DATA:
                recv_data(conn, payload)
            elif type_byte == TYPE_FILE:
                recv_file(conn, payload, save_dir)
            elif type_byte == TYPE_CLOSE:
                print('客户端 %s 请求关闭连接' % (addr,))
                with send_lock:
                    send_data(conn, '再见，连接已关闭')
                break
            else:
                print('收到未知类型，忽略')
    except (ConnectionResetError, BrokenPipeError, OSError) as e:
        print('客户端 %s 异常断开：%s' % (addr, e))
    finally:
        with _sessions_lock:
            _sessions.pop(conn, None)
        try:
            conn.close()
        except OSError:
            pass
        print('与 %s 的会话结束，继续等待新的连接……' % (addr,))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    save_dir = sys.argv[2] if len(sys.argv) > 2 else \
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sk.bind((HOST, port))
    sk.listen(5)
    print('消息&文件服务端已启动，监听 %s:%d，接收文件保存到 %s' % (HOST, port, save_dir))
    print('（服务端控制台也可敲字：一行 = 发消息；sendfile 路径 = 发文件；Ctrl+C 退出）')

    # 控制台只由一个线程读取，再负责把消息/文件分发下去
    threading.Thread(target=console_reader, daemon=True).start()

    try:
        while True:
            conn, addr = sk.accept()
            print('客户端 %s 已连接' % (addr,))
            # 顺序服务：处理完当前客户端再 accept 下一个；
            # 想同时服务多个，把下面的 run() 改成用线程跑即可。
            run(conn, addr, save_dir)
    except KeyboardInterrupt:
        print('\n服务端退出')
    finally:
        sk.close()


if __name__ == '__main__':
    main()
