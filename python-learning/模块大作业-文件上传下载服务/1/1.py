# -*- coding: utf-8 -*-
"""
按 1.py 的风格，根据《TCP 网盘》客户端 / 服务端真实源码绘制算法流程图。
生成：
    图1 TCP 网盘客户端流程图.png
    图2 TCP 网盘服务端流程图.png
"""

import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = r"C:\Windows\Fonts\simhei.ttf"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

BG = "white"
PROC_FILL, PROC_LINE = "#E8F1FB", "#2F6FB2"      # 处理框
DEC_FILL,  DEC_LINE  = "#FFF6E0", "#D9A03A"      # 判断框
TERM_FILL, TERM_LINE = "#E7F6EA", "#3E9E58"      # 起止框
ERR_FILL,  ERR_LINE  = "#FDECEC", "#C0504D"      # 错误/异常
TEXT = "#1F1F1F"
LINE = "#333333"


# ------------------------------------------------------------------
#                              基础绘图工具
# ------------------------------------------------------------------
def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """按宽度对中文文本做简单换行（支持手动 \n）。"""
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur)
            cur = ""
            continue
        if draw.textlength(cur + ch, font=fnt) > max_w and cur:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def process(draw, cx, cy, w, h, text, fnt=None,
            fill=PROC_FILL, line=PROC_LINE, radius=10):
    fnt = fnt or _font(FONT_PATH, 19)
    draw.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                           radius=radius, fill=fill, outline=line, width=3)
    draw.multiline_text((cx, cy), wrap(draw, text, fnt, w - 30), font=fnt,
                        fill=TEXT, anchor="mm", align="center", spacing=6)


def diamond(draw, cx, cy, w, h, text, fnt=None):
    fnt = fnt or _font(FONT_PATH, 19)
    draw.polygon([(cx, cy - h / 2), (cx + w / 2, cy),
                  (cx, cy + h / 2), (cx - w / 2, cy)],
                 fill=DEC_FILL, outline=DEC_LINE, width=3)
    draw.multiline_text((cx, cy), wrap(draw, text, fnt, w * 0.58), font=fnt,
                        fill=TEXT, anchor="mm", align="center", spacing=6)


def terminal(draw, cx, cy, w, h, text, fnt=None):
    fnt = fnt or _font(FONT_PATH, 19)
    draw.ellipse([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                 fill=TERM_FILL, outline=TERM_LINE, width=3)
    draw.multiline_text((cx, cy), text, font=fnt, fill=TEXT,
                        anchor="mm", align="center")


def arrow(draw, p1, p2, color=LINE, width=3):
    x1, y1 = p1
    x2, y2 = p2
    draw.line([x1, y1, x2, y2], fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 12
    pts = [(x2, y2),
           (x2 - size * math.cos(ang - 0.4), y2 - size * math.sin(ang - 0.4)),
           (x2 - size * math.cos(ang + 0.4), y2 - size * math.sin(ang + 0.4))]
    draw.polygon(pts, fill=color)


def polyline(draw, pts, color=LINE, width=3):
    draw.line(pts, fill=color, width=width)


# ==================================================================
#                         图 1：客户端
# ==================================================================
def draw_client(out_dir):
    W, H = 1520, 1420
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    FT = _font(FONT_BOLD, 30)
    FB = _font(FONT_PATH, 19)
    FS = _font(FONT_PATH, 17)
    FX = _font(FONT_PATH, 16)

    d.text((W / 2, 42), "图1  TCP 网盘客户端流程图",
           font=FT, fill="#1F3A5F", anchor="mm")

    CX = 420          # 主流程中心线
    BUS_L = 860       # 分支左侧总线
    RX = 1120         # 右侧功能框中心
    RW = 400          # 右侧功能框宽度
    BUS_R = 1420      # 回环右侧总线

    # ------------------------- 主流程 -------------------------
    terminal(d, CX, 100, 220, 56, "开始", FB)
    process(d, CX, 175, 640, 50, "打印：=====TCP网盘客户端=====", FB)
    process(d, CX, 245, 640, 50, "current_user = None", FB)
    process(d, CX, 320, 640, 62,
            "循环入口：显示主菜单\n1 注册  2 登录  3 查看文件  4 上传  5 下载  0 退出", FB)
    process(d, CX, 400, 640, 50, "输入 op 选择功能", FB)
    diamond(d, CX, 515, 440, 150, "op 分支", FB)

    arrow(d, (CX, 128), (CX, 150))
    arrow(d, (CX, 200), (CX, 220))
    arrow(d, (CX, 270), (CX, 289))
    arrow(d, (CX, 351), (CX, 375))
    arrow(d, (CX, 425), (CX, 440))

    # ------------------------- 功能分支 -------------------------
    branches = [
        (430, 120, "[1] 注册  register()\n连接服务器 → 输入用户名 / 密码\n"
                   "发送 register 请求 → 接收响应 → 打印 msg"),
        (575, 120, "[2] 登录  current_user = login()\n连接服务器 → 发送 login 请求\n"
                   "成功返回用户名，失败返回 None"),
        (715, 100, "[3] 查看网盘文件\n未登录 → 提示「请先登录」\n"
                   "已登录 → list_file() 发送 listfile 并打印列表"),
        (845, 120, "[4] 上传文件  upload_file()\n输入本地路径 → 校验文件存在\n"
                   "发送 文件名 / 大小 → 分块发送 → 接收结果"),
        (985, 130, "[5] 下载文件  download_file()\n发送 download_info 获取文件大小\n"
                   "判断是否断点续传 → 按 offset 下载 → 直到 __EOF__"),
        (1115, 60, "其他 → 不做任何处理，回到菜单"),
        (1205, 60, "[0] 打印「退出客户端」，break"),
    ]

    for y, h, txt in branches:
        f = FX if h >= 100 else FS
        process(d, RX, y, RW, h, txt, fnt=f)

    # 菱形 → 左侧总线
    arrow(d, (CX + 220, 515), (BUS_L, 515))
    polyline(d, [(BUS_L, 430), (BUS_L, 1205)])
    for y, _, _ in branches:
        arrow(d, (BUS_L, y), (RX - RW / 2 - 2, y))

    # 功能框执行完 → 回环 → 循环入口
    polyline(d, [(BUS_R, 320), (BUS_R, 1115)])
    for y, _, _ in branches[:-1]:
        polyline(d, [(RX + RW / 2, y), (BUS_R, y)])
    arrow(d, (BUS_R, 320), (CX + 322, 320))

    # 退出分支 → 结束
    arrow(d, (RX, 1235), (RX, 1284))
    terminal(d, RX, 1312, 200, 56, "结束", FB)

    out = os.path.join(out_dir, "图1 TCP 网盘客户端流程图.png")
    img.save(out, "PNG")
    print("saved:", out, img.size)


# ==================================================================
#                         图 2：服务端
# ==================================================================
def draw_server(out_dir):
    W, H = 1720, 1800
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    FT = _font(FONT_BOLD, 30)
    FB = _font(FONT_PATH, 19)
    FS = _font(FONT_PATH, 17)
    FX = _font(FONT_PATH, 16)

    d.text((W / 2, 42), "图2  TCP 网盘服务端流程图",
           font=FT, fill="#1F3A5F", anchor="mm")

    CX = 480           # 主流程中心线
    BUS_L = 940        # 命令分支总线
    RX = 1250          # 命令处理框中心
    RW = 400           # 命令处理框宽度
    BUS_R = 1600       # 右侧汇聚总线

    # ------------------------- 主流程 -------------------------
    terminal(d, CX, 100, 220, 56, "开始", FB)
    process(d, CX, 175, 640, 50, "确保 server_data 目录存在（BASE_DIR）", FB)
    process(d, CX, 240, 640, 50, "users = load_users()  读取 userinfo.json", FB)
    process(d, CX, 305, 640, 50, "创建 TCP socket(AF_INET, SOCK_STREAM)", FB)
    process(d, CX, 370, 640, 50, "bind((127.0.0.1, 8888)) 绑定端口", FB)
    process(d, CX, 435, 640, 50, "listen(5) 开始监听", FB)
    process(d, CX, 500, 640, 50, "打印：网盘服务端启动，端口8888", FB)
    process(d, CX, 575, 640, 58, "accept() 阻塞等待客户端连接", FB)
    process(d, CX, 650, 640, 50, "打印：客户端连接 addr", FB)
    process(d, CX, 720, 640, 50, "data = conn.recv(1024).decode()", FB)
    process(d, CX, 790, 640, 58,
            'req = json.loads(data)   action = req["action"]', FB)
    diamond(d, CX, 910, 440, 150, "action 分支", FB)

    arrow(d, (CX, 128), (CX, 150))
    arrow(d, (CX, 200), (CX, 215))
    arrow(d, (CX, 265), (CX, 280))
    arrow(d, (CX, 330), (CX, 345))
    arrow(d, (CX, 395), (CX, 410))
    arrow(d, (CX, 460), (CX, 475))
    arrow(d, (CX, 525), (CX, 546))
    arrow(d, (CX, 604), (CX, 625))
    arrow(d, (CX, 675), (CX, 695))
    arrow(d, (CX, 745), (CX, 761))
    arrow(d, (CX, 819), (CX, 835))

    # ------------------------- 命令分支 -------------------------
    cmds = [
        (780, 130, "action == 'register'\n· 用户名已存在 → 回复「用户名已存在」\n"
                   "· 否则写入 users 并保存 userinfo.json\n  创建用户目录 → 回复「注册成功」"),
        (930, 120, "action == 'login'\n· 账号不存在或密码错误 → 回复「账号密码错误」\n"
                   "· 校验通过 → 回复「登录成功」"),
        (1060, 90, "action == 'listfile'\n· os.listdir(用户目录)\n"
                   "· 回复 {code:0, data: 文件列表}"),
        (1190, 130, "action == 'upload'\n· 先回 ok → 循环接收 filesize 字节\n"
                    "· 以 wb 写入 用户目录/文件名\n· 完成后回复「上传完成」"),
        (1330, 110, "action == 'download_info'\n· 文件存在 → 回复文件大小 size\n"
                    "· 不存在 → 回复「文件不存在」"),
        (1470, 110, "action == 'download_data'\n· 打开文件并 seek(offset)\n"
                    "· 循环发送 4096 字节 → 最后发送 __EOF__"),
    ]
    for y, h, txt in cmds:
        process(d, RX, y, RW, h, txt, fnt=FX)

    # 菱形 → 命令总线 → 各命令框
    arrow(d, (CX + 220, 910), (BUS_L, 910))
    polyline(d, [(BUS_L, 780), (BUS_L, 1470)])
    for y, _, _ in cmds:
        arrow(d, (BUS_L, y), (RX - RW / 2 - 2, y))

    # 各命令框右侧 → 右侧汇聚总线
    polyline(d, [(BUS_R, 780), (BUS_R, 1620)])
    for y, _, _ in cmds:
        polyline(d, [(RX + RW / 2, y), (BUS_R, y)])

    # ------------------------- 异常分支 -------------------------
    process(d, CX, 1180, 560, 92,
            "except Exception as e:\n打印异常信息 e", fnt=FS,
            fill=ERR_FILL, line=ERR_LINE)
    arrow(d, (CX, 985), (CX, 1132), color=ERR_LINE)
    d.text((CX + 14, 1050), "任意请求处理出错", font=FS,
           fill=ERR_LINE, anchor="lm")

    # ------------------------- 关闭连接 & 回环 -------------------------
    process(d, RX, 1620, 440, 62, "finally: conn.close() 关闭连接", fnt=FS)
    arrow(d, (BUS_R, 1620), (RX + 222, 1620))

    # 异常框 → 关闭连接
    polyline(d, [(CX, 1226), (CX, 1710), (RX, 1710)], color=ERR_LINE)
    arrow(d, (RX, 1710), (RX, 1653), color=ERR_LINE)

    # 关闭连接 → 回到 accept 循环
    polyline(d, [(RX - 220, 1620), (100, 1620), (100, 575)])
    arrow(d, (100, 575), (CX - 322, 575))
    d.text((118, 1560), "循环处理下一个客户端连接", font=FX,
           fill="#2F6FB2", anchor="lm")

    out = os.path.join(out_dir, "图2 TCP 网盘服务端流程图.png")
    img.save(out, "PNG")
    print("saved:", out, img.size)


# ------------------------------------------------------------------
def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out_dir, exist_ok=True)
    draw_client(out_dir)
    draw_server(out_dir)


if __name__ == "__main__":
    main()