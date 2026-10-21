# -*- coding: utf-8 -*-
"""按 2.py 的风格，真实绘制《TCP 网盘》客户端 / 服务端算法流程图。"""

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


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """按宽度对中文文本做简单换行。"""
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
    draw.multiline_text((cx, cy), wrap(draw, text, fnt, w * 0.55), font=fnt,
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


# ============================================================
#                        图 1：客户端
# ============================================================
def draw_client(out_dir):
    W, H = 1360, 1400
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    FT = _font(FONT_BOLD, 30)
    FB = _font(FONT_PATH, 19)
    FS = _font(FONT_PATH, 17)

    d.text((W / 2, 42), "图1  TCP 网盘客户端流程图",
           font=FT, fill="#1F3A5F", anchor="mm")

    CX = 430     # 主流程中心线

    # ---------------- 节点 ----------------
    terminal(d, CX, 100, 220, 56, "开始", FB)
    process(d, CX, 180, 620, 50, "输入服务器 IP（默认 127.0.0.1）", FB)
    process(d, CX, 250, 620, 50, "输入端口号（默认 8888）", FB)
    process(d, CX, 320, 620, 50, "创建 TCP socket 套接字", FB)
    process(d, CX, 390, 620, 50, "connect() 连接服务器", FB)
    diamond(d, CX, 490, 400, 120, "连接成功 ?", FB)

    process(d, 980, 490, 340, 76, "输出：连接失败",
            fnt=FS, fill=ERR_FILL, line=ERR_LINE)
    terminal(d, 980, 610, 200, 56, "结束", FB)

    process(d, CX, 615, 620, 56, "循环入口：清屏刷新 + 显示主菜单", FB)
    process(d, CX, 690, 620, 50, "输入 choice 选择", FB)
    diamond(d, CX, 800, 360, 140, "choice 分支", FB)

    opt_x, opt_w = 1000, 340
    opts = [
        (700,  "[1] 注册        do_register()"),
        (780,  "[2] 登录        do_login()"),
        (860,  "[3] 查看文件    do_list()"),
        (940,  "[4] 上传文件    do_upload()"),
        (1020, "[5] 下载文件    do_download()"),
        (1100, "其他 → 提示「无效选择」"),
        (1180, "[0] 退出（发送 quit）"),
    ]
    for y, txt in opts:
        process(d, opt_x, y, opt_w, 56, txt, fnt=FS)

    terminal(d, 1000, 1300, 200, 56, "结束", FB)

    # ---------------- 连线 ----------------
    # 主干
    arrow(d, (CX, 128), (CX, 155))
    arrow(d, (CX, 205), (CX, 225))
    arrow(d, (CX, 275), (CX, 295))
    arrow(d, (CX, 345), (CX, 365))
    arrow(d, (CX, 415), (CX, 428))

    # 「连接失败」分支
    arrow(d, (630, 490), (806, 490), color=ERR_LINE)
    d.text((660, 470), "否", font=FS, fill=ERR_LINE, anchor="lm")
    arrow(d, (980, 528), (980, 580), color=ERR_LINE)

    # 「连接成功」分支
    arrow(d, (CX, 550), (CX, 585))
    d.text((CX + 14, 566), "是", font=FS, fill=TERM_LINE, anchor="lm")

    arrow(d, (CX, 643), (CX, 663))
    arrow(d, (CX, 715), (CX, 728))

    # choice 分支：菱形 -> 竖直总线 -> 各功能框
    arrow(d, (CX + 180, 800), (700, 800))
    d.line([700, 700, 700, 1100], fill=LINE, width=3)
    for y, _ in opts[:-1]:                     # 除「退出」外都连出去
        arrow(d, (700, y), (828, y))

    # 各功能执行完 -> 回到循环入口（右侧回环）
    d.line([1270, 615, 1270, 1100], fill=LINE, width=3)
    for y, _ in opts[:-1]:
        d.line([1170, y, 1270, y], fill=LINE, width=3)
    arrow(d, (1270, 615), (742, 615))

    # 「退出」-> 结束
    arrow(d, (1000, 1208), (1000, 1270))

    out = os.path.join(out_dir, "图1 TCP 网盘客户端流程图.png")
    img.save(out, "PNG")
    print("saved:", out, img.size)


# ============================================================
#                        图 2：服务端
# ============================================================
def draw_server(out_dir):
    W, H = 1620, 2220
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    FT = _font(FONT_BOLD, 30)
    FB = _font(FONT_PATH, 19)
    FS = _font(FONT_PATH, 17)
    FX = _font(FONT_PATH, 16)

    d.text((W / 2, 42), "图2  TCP 网盘服务端流程图",
           font=FT, fill="#1F3A5F", anchor="mm")

    # ==================== 面板 A：主线程 ====================
    MCX = 550
    d.text((40, 105), "【主线程 main()】", font=FB, fill="#1F3A5F", anchor="lm")

    terminal(d, MCX, 150, 240, 56, "开始", FB)
    process(d, MCX, 225, 560, 50, "确保 server_data 目录存在", FB)
    process(d, MCX, 295, 560, 50, "初始化线程锁 lock = threading.Lock()", FB)
    process(d, MCX, 365, 560, 50, "创建 socket 并设置 SO_REUSEADDR", FB)
    process(d, MCX, 435, 560, 50, "bind 绑定 0.0.0.0:8888", FB)
    process(d, MCX, 505, 560, 50, "listen(5) 开始监听", FB)
    process(d, MCX, 575, 560, 50, "打印：服务器启动，监听 0.0.0.0:8888", FB)
    process(d, MCX, 655, 560, 56, "accept() 阻塞等待客户端连接", FB)
    process(d, MCX, 745, 560, 56, "创建 daemon 线程执行 handle_client(conn, addr)", FB)

    arrow(d, (MCX, 178), (MCX, 200))
    arrow(d, (MCX, 250), (MCX, 270))
    arrow(d, (MCX, 320), (MCX, 340))
    arrow(d, (MCX, 390), (MCX, 410))
    arrow(d, (MCX, 460), (MCX, 480))
    arrow(d, (MCX, 530), (MCX, 550))
    arrow(d, (MCX, 600), (MCX, 627))
    arrow(d, (MCX, 683), (MCX, 717))

    # accept 循环回环
    d.line([830, 745, 900, 745, 900, 655, 832, 655], fill=LINE, width=3)
    arrow(d, (900, 655), (832, 655))
    d.text((910, 700), "循环\n处理", font=FS, fill=LINE, anchor="lm")

    # ==================== 面板 B：客户端处理线程 ====================
    NCX = 550
    d.text((40, 850), "【客户端处理线程 handle_client()】",
           font=FB, fill="#1F3A5F", anchor="lm")

    terminal(d, NCX, 900, 360, 56, "handle_client 新线程开始", FB)
    process(d, NCX, 975, 560, 50, "打印 [+] 客户端连接 日志", FB)
    process(d, NCX, 1040, 560, 50, "state = {'user': None}（记录登录状态）", FB)
    process(d, NCX, 1120, 600, 56, "recv_line(conn) 读取一行（循环入口）", FB)
    diamond(d, NCX, 1230, 420, 110, "line 为 None（对端断开）?", FB)
    process(d, NCX, 1340, 520, 50, "json.loads(line) 解析请求", FB)
    diamond(d, NCX, 1440, 380, 110, "JSON 解析成功 ?", FB)
    diamond(d, NCX, 1560, 340, 120, "按 cmd 分支", FB)

    # cmd 分支对应的处理框
    cmd_x, cmd_w = 1250, 380
    cmds = [
        (1450, 110,
         "cmd == 'register'\n· 正则校验用户名\n· 加锁读写 users.json\n"
         "· 已存在 → 报错\n· 否则存 sha256(密码)\n  并创建用户目录"),
        (1580, 100,
         "cmd == 'login'\n· 读取 users.json\n· 比对 sha256(密码)\n"
         "· 成功 → 记录 state['user']"),
        (1700, 90,
         "cmd == 'list'\n· 遍历用户目录\n· 返回文件 / 子目录信息"),
        (1810, 100,
         "cmd == 'upload'\n· 校验文件名与登录态\n· 以 wb 覆盖写入\n"
         "· 接收 size 字节数据"),
        (1930, 100,
         "cmd == 'download'\n· 按 offset 定位文件\n· 循环发送文件内容"),
        (2050, 80,
         "cmd == 'quit'\n· 回复「再见」并退出循环"),
        (2150, 70,
         "未知命令 → 回复 error"),
    ]
    for y, h, txt in cmds:
        process(d, cmd_x, y, cmd_w, h, txt, fnt=FX)

    # 「断开」分支
    process(d, 1250, 1230, 360, 76, "关闭连接，打印断开日志",
            fnt=FS, fill=ERR_FILL, line=ERR_LINE)
    terminal(d, 1250, 1350, 200, 56, "结束", FB)

    # 「JSON 出错」分支
    process(d, 200, 1440, 260, 80, "回复：\nJSON 格式错误",
            fnt=FX, fill=ERR_FILL, line=ERR_LINE)

    # ---------------- 面板 B 连线 ----------------
    arrow(d, (NCX, 928), (NCX, 950))
    arrow(d, (NCX, 1000), (NCX, 1015))
    arrow(d, (NCX, 1065), (NCX, 1092))
    arrow(d, (NCX, 1148), (NCX, 1175))
    arrow(d, (NCX, 1285), (NCX, 1315))
    arrow(d, (NCX, 1365), (NCX, 1385))
    arrow(d, (NCX, 1495), (NCX, 1500))

    # 对端断开 -> 关闭连接
    arrow(d, (760, 1230), (1066, 1230), color=ERR_LINE)
    d.text((790, 1210), "是", font=FS, fill=ERR_LINE, anchor="lm")
    arrow(d, (1250, 1268), (1250, 1320), color=ERR_LINE)

    # JSON 解析失败 -> 错误提示 -> 回到读取循环
    arrow(d, (360, 1440), (332, 1440), color=ERR_LINE)
    d.text((368, 1420), "否", font=FS, fill=ERR_LINE, anchor="lm")
    d.line([200, 1400, 200, 1120], fill=ERR_LINE, width=3)
    arrow(d, (200, 1120), (248, 1120), color=ERR_LINE)

    # JSON 解析成功
    arrow(d, (NCX, 1495), (NCX, 1500))
    d.text((NCX + 14, 1508), "是", font=FS, fill=TERM_LINE, anchor="lm")

    # cmd 分支总线
    arrow(d, (NCX + 170, 1560), (900, 1560))
    d.line([900, 1450, 900, 2150], fill=LINE, width=3)
    for y, _, _ in cmds:
        arrow(d, (900, y), (1058, y))

    # 各命令处理完 -> 回到读取循环
    d.line([1520, 1120, 1520, 2150], fill=LINE, width=3)
    for y, _, _ in cmds:
        d.line([1440, y, 1520, y], fill=LINE, width=3)
    arrow(d, (1520, 1120), (852, 1120))

    # 读取循环入口标识
    d.text((870, 1090), "循环读取", font=FX, fill="#2F6FB2", anchor="lm")

    out = os.path.join(out_dir, "图2 TCP 网盘服务端流程图.png")
    img.save(out, "PNG")
    print("saved:", out, img.size)


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out_dir, exist_ok=True)
    draw_client(out_dir)
    draw_server(out_dir)


if __name__ == "__main__":
    main()