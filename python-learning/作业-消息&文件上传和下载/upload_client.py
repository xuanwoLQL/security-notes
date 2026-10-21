# -*- coding: utf-8 -*-
"""
消息 & 文件上传和下载 —— 客户端

需求：
  - 定义 send_data(conn, content) 完成消息发送；
  - send_file(conn, file_path)   完成文件发送；
  - run() 完成逻辑功能；
  - 解决粘包问题，循环接收消息，避免信息接收不完整；
  - 发送的信息有三类：消息 / 文件 / close（表示关闭连接），
    能一直发消息或文件，直到发送 close 关闭链接。

用法：
  python upload_client.py [服务器IP] [端口]
  默认 127.0.0.1 9200。
  交互：直接敲一行 = 发消息；send 文件路径 = 发文件；close = 关闭链接退出；
        quit = 直接断开（不发 close 帧）。
"""

import os
import socket
import sys
import threading
import time

from file_protocol import (
    TYPE_DATA, TYPE_FILE, TYPE_CLOSE,
    pack_frame, recv_frame, recv_all, read_file,
)


def send_data(conn, content):
    """发送一条文本消息。"""
    conn.sendall(pack_frame(TYPE_DATA, content.encode('utf-8')))


def send_file(conn, file_path):
    """发送一个文件：负载 = 4 字节文件名长度 + 文件名 + 文件内容。"""
    name = os.path.basename(file_path)
    name_bytes = name.encode('utf-8')
    payload = len(name_bytes).to_bytes(4, 'big') + name_bytes + read_file(file_path)
    conn.sendall(pack_frame(TYPE_FILE, payload))


def handle_incoming(conn, stop_event):
    """后台线程：接收服务端发来的消息/文件并显示/保存，避免信息接收不完整。"""
    while not stop_event.is_set():
        type_byte, payload = recv_frame(conn)
        if type_byte is None:
            print('\n[服务端已关闭连接]')
            stop_event.set()
            return
        if type_byte == TYPE_DATA:
            print('[服务端消息] %s' % payload.decode('utf-8'))
        elif type_byte == TYPE_FILE:
            name_len = int.from_bytes(payload[:4], 'big')
            name = payload[4:4 + name_len].decode('utf-8')
            content = payload[4 + name_len:]
            save = 'recv_' + os.path.basename(name)
            with open(save, 'wb') as f:
                f.write(content)
            print('[收到文件] %s -> %s（%d 字节）' % (name, save, len(content)))


def run(conn):
    """客户端主逻辑。"""
    stop_event = threading.Event()
    threading.Thread(target=handle_incoming, args=(conn, stop_event), daemon=True).start()

    print('已连接。直接敲一行=发消息；send 文件路径=发文件；close=关闭链接；quit=直接退出')
    try:
        while not stop_event.is_set():
            try:
                line = input()
            except EOFError:
                break
            line = line.strip()
            if not line:
                continue
            try:
                if line == 'close':
                    # 第三类信息：close，告诉服务端关闭链接
                    conn.sendall(pack_frame(TYPE_CLOSE, b''))
                    print('已发送 close，等待服务端关闭……')
                    time.sleep(0.3)
                    break
                elif line == 'quit':
                    break
                elif line.startswith('send '):
                    path = line[len('send '):].strip()
                    if os.path.isfile(path):
                        send_file(conn, path)
                        print('文件已发送：%s' % path)
                    else:
                        print('文件不存在：%s' % path)
                else:
                    send_data(conn, line)
            except OSError:
                print('[发送失败，连接可能已断开]')
                break
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
        try:
            conn.close()
        except OSError:
            pass
        print('客户端退出')


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 9200
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host, port))
    except ConnectionRefusedError:
        print('连接失败：服务端没有启动，请先运行 upload_server.py')
        conn.close()
        return
    try:
        run(conn)
    finally:
        try:
            conn.close()
        except OSError:
            pass


if __name__ == '__main__':
    main()
