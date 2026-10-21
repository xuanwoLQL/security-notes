# -*- coding: utf-8 -*-
"""
TCP 网盘 —— 客户端
协议：控制命令用「一行 JSON + \n」传输，
      文件数据紧随其后按裸字节流传输（8KB 一块）。
"""

import socket
import json
import os

# ----------------------------------------------------------------------
# 全局配置：默认服务器地址 / 端口
# ----------------------------------------------------------------------
HOST = '127.0.0.1'
PORT = 8888


# ======================================================================
#                      一、屏幕与交互工具函数
# ======================================================================
def clear_screen():
    """
    【刷新屏幕】
    等价于 main.cpp 里的 system("cls")：
      - Windows 使用 cls
      - Linux / macOS 使用 clear
    每次回到菜单或进入某个功能前调用，保证界面干净、不刷屏。
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """
    【暂停等待】
    等价于 main.cpp 里的 wait()：
    让用户看完操作结果后按回车，再回到主菜单。
    """
    input('\n按回车键继续...')


# ======================================================================
#                      二、底层收发工具
# ======================================================================
def recv_line(sock):
    """
    按「一个字节一个字节」读取，直到遇到换行符 \\n 为止。

    为什么不能直接用 sock.recv(1024)？
    因为文件二进制数据里也可能出现 \\n，
    如果一次性读一大块，很容易把「JSON 控制行」和
    「后续的文件二进制」粘在一起。逐字节读可以精确地
    在 \\n 处停下来，保证协议边界清晰。
    """
    data = b''
    while True:
        ch = sock.recv(1)
        if not ch:                 # 对端关闭
            return None
        if ch == b'\n':            # 读到行尾
            break
        data += ch
    return data.decode('utf-8')


def send_json(sock, obj):
    """把 Python 字典序列化成一行 UTF-8 JSON，末尾补 \\n 后发送。"""
    line = json.dumps(obj, ensure_ascii=False) + '\n'
    sock.sendall(line.encode('utf-8'))


def request(sock, obj):
    """
    一问一答式请求：
      1. 发送 JSON 命令
      2. 读取服务器返回的一行 JSON
      3. 反序列化成字典返回
    """
    send_json(sock, obj)
    line = recv_line(sock)
    if line is None:
        raise ConnectionError('服务器断开连接')
    return json.loads(line)


# ======================================================================
#                      三、进度条
# ======================================================================
def progress_bar(done, total, prefix=''):
    """
    在控制台同一行刷新显示进度条。
    \\r 回到行首 + end='' 不换行 + flush=True 立即输出，
    就实现了「原地刷新」的效果。
    """
    if total <= 0:
        total = 1
    percent = min(done / total, 1.0)
    length = 40
    filled = int(length * percent)
    bar = '#' * filled + '-' * (length - filled)
    print(f'\r{prefix} [{bar}] {done}/{total} {percent * 100:6.2f}%',
          end='', flush=True)
    if done >= total:
        print()                    # 完成时补一个换行


# ======================================================================
#                      四、各功能实现
# ======================================================================
def do_register(sock):
    """【功能 1】注册：把用户名、明文密码发给服务器，由服务器做哈希存储。"""
    username = input('用户名: ').strip()
    password = input('密码: ').strip()
    resp = request(sock, {'cmd': 'register',
                          'username': username,
                          'password': password})
    print(resp.get('msg', resp))


def do_login(sock):
    """【功能 2】登录：服务器校验通过后，本次连接会记住登录状态。"""
    username = input('用户名: ').strip()
    password = input('密码: ').strip()
    resp = request(sock, {'cmd': 'login',
                          'username': username,
                          'password': password})
    print(resp.get('msg', resp))
    return resp.get('status') == 'ok'


def do_list(sock):
    """【功能 3】查看网盘一级目录下的文件与子目录。"""
    resp = request(sock, {'cmd': 'list'})
    if resp.get('status') != 'ok':
        print(resp.get('msg'))
        return

    files = resp.get('files', [])
    if not files:
        print('网盘为空')
        return

    print('网盘文件（一级目录）:')
    for f in files:
        if f.get('is_dir'):
            print(f"  {f['name']}")
        else:
            print(f"  {f['name']}  {f['size']} 字节")


def do_upload(sock):
    """
    【功能 4】上传（覆盖式）
    协议顺序：
      1) 先发 {"cmd":"upload","filename":...,"size":...}
      2) 服务器回 {"status":"ok"} 后，客户端紧接着发送 size 字节裸数据
    """
    local_path = input('本地文件路径: ').strip().strip('"')
    if not os.path.isfile(local_path):
        print('本地文件不存在')
        return

    filename = os.path.basename(local_path)      # 只取文件名，避免路径穿越
    size = os.path.getsize(local_path)

    # 第一步：协商（告诉服务器要传什么、多大）
    resp = request(sock, {'cmd': 'upload', 'filename': filename, 'size': size})
    if resp.get('status') != 'ok':
        print(resp.get('msg'))
        return

    # 第二步：按 8KB 分块发送文件内容
    sent = 0
    with open(local_path, 'rb') as f:
        while sent < size:
            chunk = f.read(8192)
            if not chunk:
                break
            sock.sendall(chunk)
            sent += len(chunk)
            progress_bar(sent, size, prefix=f'上传 {filename}')

    if sent == size:
        print('上传完成')
    else:
        print('上传中断')


def do_download(sock):
    """
    【功能 5】下载（支持断点续传）
    协议顺序：
      1) 发送 {"cmd":"download","filename":...,"offset":本地已有字节数}
      2) 服务器回 {"status":"ok","size":总大小,"offset":...}
      3) 客户端按 offset 追加写（ab）或覆盖写（wb）
    """
    filename = os.path.basename(input('要下载的网盘文件名: ').strip())
    local_dir = input('本地保存目录（默认当前目录）: ').strip().strip('"') or '.'
    os.makedirs(local_dir, exist_ok=True)

    local_path = os.path.join(local_dir, filename)

    # ---------- 判断本地是否已有同名文件，询问是否续传 ----------
    offset = 0
    if os.path.exists(local_path):
        local_size = os.path.getsize(local_path)
        print(f'本地已存在该文件，大小 {local_size} 字节。')
        choice = input('是否续传？(y=续传 / n=从头开始): ').strip().lower()
        if choice == 'y':
            offset = local_size      # 从已有字节处继续
        else:
            offset = 0               # 从头重下

    # ---------- 向服务器发起下载请求 ----------
    resp = request(sock, {'cmd': 'download',
                          'filename': filename,
                          'offset': offset})
    if resp.get('status') != 'ok':
        print(resp.get('msg'))
        return

    total = int(resp['size'])

    if offset > total:
        print('本地文件比服务器文件大，无法续传。')
        return
    if offset == total:
        print('文件已完整，无需下载')
        return

    # ---------- 接收数据 ----------
    mode = 'ab' if offset > 0 else 'wb'     # 续传用追加，否则覆盖
    received = offset

    with open(local_path, mode) as f:
        while received < total:
            chunk = sock.recv(min(8192, total - received))
            if not chunk:
                break
            f.write(chunk)
            received += len(chunk)
            progress_bar(received, total, prefix=f'下载 {filename}')

    if received == total:
        print('下载完成')
    else:
        print('下载中断')


# ======================================================================
#                      五、主程序
# ======================================================================
def main():
    # ---------- 连接服务器 ----------
    host = input(f'服务器IP（默认 {HOST}）: ').strip() or HOST
    port = input(f'端口（默认 {PORT}）: ').strip()
    port = int(port) if port else PORT

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, port))
    except Exception as e:
        print('连接服务器失败:', e)
        return

    clear_screen()                       # 【刷新】连接成功，清掉输入提示
    print('已连接服务器')

    # ---------- 主菜单循环 ----------
    while True:
        clear_screen()                   # 【刷新】每轮先清屏，重新画菜单

        print('===== TCP 网盘 =====')
        print('1. 注册')
        print('2. 登录')
        print('3. 查看文件')
        print('4. 上传文件')
        print('5. 下载文件（支持断点续传）')
        print('0. 退出')

        choice = input('请选择: ').strip()

        clear_screen()                   # 【刷新】清掉菜单，只留操作结果

        try:
            if choice == '1':
                do_register(sock)
            elif choice == '2':
                do_login(sock)
            elif choice == '3':
                do_list(sock)
            elif choice == '4':
                do_upload(sock)
            elif choice == '5':
                do_download(sock)
            elif choice == '0':
                # 优雅通知服务器后断开
                try:
                    request(sock, {'cmd': 'quit'})
                except Exception:
                    pass
                break
            else:
                print('无效选择')
        except (ConnectionError, OSError) as e:
            print('连接错误:', e)
            break

        # 【暂停】等用户看完结果再回到菜单（对应 main.cpp 的 wait()）
        pause()

    sock.close()


if __name__ == '__main__':
    main()