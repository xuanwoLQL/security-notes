import socket
import threading
import json
import os
import hashlib
import re
#-------------------------------------------------------------------
#全局配置
#-------------------------------------------------------------------
HOST = '0.0.0.0' #监听全部网卡地址
PORT = 8888

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'server_data')#用户网盘数据存储目录
USERS_FILE = os.path.join(BASE_DIR, 'users.json')#用户账号密码存储文件

os.makedirs(DATA_DIR, exist_ok=True)
#多个线程会同时读写user.json,必须加锁保证一致性
lock = threading.Lock()

#--------------------------------------------------------------------
#               一、用户表读写与工具
#--------------------------------------------------------------------
def load_users():
    #读取用户表;文件不存在则返回空字典
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_users(users):
    #吧用户表写回磁盘(带缩进，方便人工查看)
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def hash_pwd(pwd):
    #密码只存sha256摘要，不存明文
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest()


def recv_line(conn):
    """按字节读取一行，避免和后续文件二进制数据粘包"""
    #返回None表示对端已关闭
    data = b''
    while True:
        ch = conn.recv(1)
        if not ch:
            return None
        if ch == b'\n':
            break
        data += ch
    return data.decode('utf-8')


def send_json(conn, obj):
    #把字典序列成一行json(末尾\\n)发送
    line = json.dumps(obj, ensure_ascii=False) + '\n'
    conn.sendall(line.encode('utf-8'))


def safe_name(name):
    """
    文件名安全处理:
        只取最后一段(去掉任何目录成分)
        jujue''/'.'/'..'
    防止客户端用../../之类的路劲穿越攻击
    """
    name = os.path.basename(name)
    if name in ('', '.', '..') or '..' in name:
        return None
    return name


def user_dir(username):
    #返回某个用户的网盘目录路径
    return os.path.join(DATA_DIR, username)

#------------------------------------------------------------------
#               二、客户端处理线程
#------------------------------------------------------------------
def handle_client(conn, addr):
    print(f'[+] 客户端连接: {addr}')
    #这条连接的登录状态；未登录时为None
    state = {'user': None}

    try:
        #------命令主循环:一次读一行json,处理完继续读
        while True:
            line = recv_line(conn)
            if line is None: #对端正常/异常断开
                break
            #----解析json------
            try:
                req = json.loads(line)
            except json.JSONDecodeError:
                send_json(conn, {'status': 'error', 'msg': 'JSON格式错误'})
                continue

            cmd = req.get('cmd')
            #---------------
            # 命令1:注册
            #---------------
            if cmd == 'register':
                username = req.get('username', '').strip()
                password = req.get('password', '')
                #用户名只允许字母/数字/下划线，长度1~30
                if not re.fullmatch(r'[A-Za-z0-9_]{1,30}', username):
                    send_json(conn, {'status': 'error', 'msg': '用户名只能包含字母数字下划线，长度1-30'})
                    continue
                #加锁保护user.json的[读-判断-写]整个过程
                with lock:
                    users = load_users()
                    if username in users:
                        exists = True
                    else:
                        users[username] = hash_pwd(password)
                        save_users(users)
                        os.makedirs(user_dir(username), exist_ok=True)
                        exists = False

                if exists:
                    send_json(conn, {'status': 'error', 'msg': '用户已存在'})
                else:
                    send_json(conn, {'status': 'ok', 'msg': '注册成功，已创建用户目录'})
            #-------------
            # 命令2:登录
            #-------------
            elif cmd == 'login':
                username = req.get('username', '').strip()
                password = req.get('password', '')

                with lock:
                    users = load_users()

                if username in users and users[username] == hash_pwd(password):
                    state['user'] = username    #记录本连接已登录
                    os.makedirs(user_dir(username), exist_ok=True)
                    send_json(conn, {'status': 'ok', 'msg': '登录成功'})
                else:
                    send_json(conn, {'status': 'error', 'msg': '用户名或密码错误'})
            #------------------
            # 命令3:查看文件
            #------------------
            elif cmd == 'list':
                if not state['user']:
                    send_json(conn, {'status': 'error', 'msg': '请先登录'})
                    continue

                d = user_dir(state['user'])
                files = []
                if os.path.exists(d):
                    for name in os.listdir(d):
                        p = os.path.join(d, name)
                        if os.path.isfile(p):
                            files.append({'name': name, 'size': os.path.getsize(p)})
                        elif os.path.isdir(p):
                            files.append({'name': name + '/', 'size': 0, 'is_dir': True})

                send_json(conn, {'status': 'ok', 'files': files})
            #-----------------------
            # 命令4:上传：存在则覆盖
            #-----------------------
            elif cmd == 'upload':
                if not state['user']:
                    send_json(conn, {'status': 'error', 'msg': '请先登录'})
                    continue

                filename = safe_name(req.get('filename', ''))
                size = int(req.get('size', 0))

                if not filename:
                    send_json(conn, {'status': 'error', 'msg': '文件名非法'})
                    continue

                path = os.path.join(user_dir(state['user']), filename)
                #同名的目录会冲突，拒绝上传
                if os.path.isdir(path):
                    send_json(conn, {'status': 'error', 'msg': '同名目录已存在，无法上传'})
                    continue

                send_json(conn, {'status': 'ok', 'msg': '开始上传'})

                received = 0
                with open(path, 'wb') as f:  # wb 实现覆盖
                    while received < size:
                        chunk = conn.recv(min(8192, size - received))
                        if not chunk:
                            break
                        f.write(chunk)
                        received += len(chunk)

                if received == size:
                    print(f'[上传完成] {state["user"]}/{filename} {size} 字节')
                else:
                    print(f'[上传中断] {state["user"]}/{filename} {received}/{size}')
            #-------------------------
            # 命令5:下载：支持断点续传
            #-------------------------
            elif cmd == 'download':
                if not state['user']:
                    send_json(conn, {'status': 'error', 'msg': '请先登录'})
                    continue

                filename = safe_name(req.get('filename', ''))
                offset = int(req.get('offset', 0))  #客户端已有字节数

                if not filename:
                    send_json(conn, {'status': 'error', 'msg': '文件名非法'})
                    continue

                path = os.path.join(user_dir(state['user']), filename)

                if not os.path.isfile(path):
                    send_json(conn, {'status': 'error', 'msg': '文件不存在'})
                    continue

                total = os.path.getsize(path)
                #偏移量必须在[0,total]之间
                if offset < 0 or offset > total:
                    send_json(conn, {
                        'status': 'error',
                        'msg': f'偏移量无效，服务器文件大小: {total}'
                    })
                    continue

                send_json(conn, {'status': 'ok', 'size': total, 'offset': offset})

                sent = offset
                with open(path, 'rb') as f:
                    f.seek(offset)#从断电处开始读
                    while sent < total:
                        chunk = f.read(min(8192, total - sent))
                        if not chunk:
                            break
                        conn.sendall(chunk)
                        sent += len(chunk)

                print(f'[下载完成] {state["user"]}/{filename} 从 {offset} 到 {total}')
            #-----------------------
            #命令6:退出
            #-----------------------
            elif cmd == 'quit':
                send_json(conn, {'status': 'ok', 'msg': '再见'})
                break

            else:
                send_json(conn, {'status': 'error', 'msg': '未知命令'})

    except Exception as e:
        print(f'[!] 处理客户端 {addr} 出错: {e}')
    finally:
        conn.close()
        print(f'[-] 客户端断开: {addr}')


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #允许重启后立即复用端口，避免TIME_WAIT报错
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)  #半连接队列长度

    print(f'服务器启动，监听 {HOST}:{PORT}')

    while True:
        conn, addr = s.accept()
        #daemon:主程序推出时自动结束
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()


if __name__ == '__main__':
    main()
