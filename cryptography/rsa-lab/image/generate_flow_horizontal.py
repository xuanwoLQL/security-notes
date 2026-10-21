# -*- coding: utf-8 -*-
"""生成《实验3 RSA 加密解密算法》横向模块化流程图。

说明：
  1. 采用“主菜单分叉 -> 左(密钥生成) / 中(加密) / 右(解密)”布局，解决纵向过长的问题。
  2. 红色线为“模块内部重试/错误回环”（如 p==q 或密文长度错误）。
  3. 蓝色线为“流程完成/严重失败后，返回主菜单”的外部大循环，视觉醒目不穿框。
  4. 纯 ASCII 兼容，避免 SimHei 缺字。
"""

import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

def pick_font(*candidates):
    for path in candidates:
        if os.path.exists(path):
            return path
    raise SystemExit("未找到可用中文字体")

FONT_PATH = pick_font(r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\simsun.ttc")
FONT_BOLD = pick_font(r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\msyh.ttc")

# 画布：宽 2250，高 1380，横向呈现三列
W, H = 2250, 1380
BG = "white"
PROC_FILL, PROC_LINE = "#E8F1FB", "#2F6FB2"
DEC_FILL, DEC_LINE = "#FFF6E0", "#D9A03A"
TERM_FILL, TERM_LINE = "#E7F6EA", "#3E9E58"
ERR_FILL, ERR_LINE = "#FDECEC", "#C0504D"
TEXT = "#1F1F1F"

# 颜色设定
RED_RETRY = "#C0504D"      # 内部重试和错误
BLUE_RETURN = "#1F77B4"    # 返回主菜单的外循环线

def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_PATH, size)

F_TITLE = font(32, bold=True)
F_BOX = font(20)
F_SMALL = font(18)

def wrap(draw, text, fnt, max_w):
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

def process(draw, cx, cy, w, h, text, fnt=F_BOX, fill=PROC_FILL, line=PROC_LINE, radius=10):
    draw.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                           radius=radius, fill=fill, outline=line, width=3)
    draw.multiline_text((cx, cy), wrap(draw, text, fnt, w - 30), font=fnt, fill=TEXT,
                        anchor="mm", align="center", spacing=6)

def diamond(draw, cx, cy, w, h, text, fnt=F_BOX):
    draw.polygon([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)],
                 fill=DEC_FILL, outline=DEC_LINE, width=3)
    draw.multiline_text((cx, cy), wrap(draw, text, fnt, w * 0.55), font=fnt, fill=TEXT,
                        anchor="mm", align="center", spacing=6)

def terminal(draw, cx, cy, w, h, text, fnt=F_BOX):
    draw.ellipse([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                 fill=TERM_FILL, outline=TERM_LINE, width=3)
    draw.multiline_text((cx, cy), text, font=fnt, fill=TEXT, anchor="mm", align="center")

def error_box(draw, cx, cy, text, fnt=F_SMALL, w=220, h=70):
    process(draw, cx, cy, w, h, text, fnt=fnt, fill=ERR_FILL, line=ERR_LINE, radius=8)

def arrow(draw, p1, p2, color="#333333", width=3):
    x1, y1 = p1
    x2, y2 = p2
    draw.line([x1, y1, x2, y2], fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 14
    pts = [(x2, y2),
           (x2 - size * math.cos(ang - 0.4), y2 - size * math.sin(ang - 0.4)),
           (x2 - size * math.cos(ang + 0.4), y2 - size * math.sin(ang + 0.4))]
    draw.polygon(pts, fill=color)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
d.text((W / 2, 50), "RSA 加解密算法流程图（分模块菜单版）", font=F_TITLE, fill="#1F3A5F", anchor="mm")

# ==================== 坐标与节点全局定义 ====================
# 顶部菜单区
MENU_X = 1125
Y_START = 100
Y_MENU = 180
Y_DIA = 300

# 列中心 X 坐标
CX_KG = 400     # 密钥生成
CX_ENC = 1125   # 加密
CX_DEC = 1800   # 解密

# 各个模块的 Y 坐标（高度 130，上下相距适当）
Y1 = 380
Y2 = 480
Y3 = 600
Y4 = 700
Y5 = 820
Y6 = 920
Y7 = 1040
Y8 = 1140
Y9 = 1260

# ==================== 绘制节点 ====================
# 顶部主干
terminal(d, MENU_X, Y_START, 180, 56, "开始")
process(d, MENU_X, Y_MENU, 320, 56, "显示主菜单，等待用户选择")
diamond(d, MENU_X, Y_DIA, 280, 100, "选择功能 (1/2/3/0)")

# ----- 左列：密钥生成 -----
process(d, CX_KG, Y1, 360, 56, "输入密钥位数 bits (默认 512)")
diamond(d, CX_KG, Y2, 340, 100, "bits 是 32~1024 的偶数 ?")
error_box(d, CX_KG + 340, Y2, "提示：位数非法\n要求重新输入")

process(d, CX_KG, Y3, 360, 56, "随机生成两个 bits/2 位素数 p、q")
diamond(d, CX_KG, Y4, 340, 100, "p != q 且 |p - q| 足够大 ?")

process(d, CX_KG, Y5, 360, 56, "计算 n = p * q, phi = (p-1)*(q-1)")
diamond(d, CX_KG, Y6, 340, 100, "gcd(e = 65537, phi) = 1 ?")

process(d, CX_KG, Y7, 420, 56, "计算 d = e^(-1) mod phi 及 CRT 参数")
process(d, CX_KG, Y8, 360, 56, "保存 public.txt 和 private.txt")
process(d, CX_KG, Y9, 240, 50, "生成完成", fill="#F0F0F0", line="#888888")

# ----- 中列：加密 -----
process(d, CX_ENC, Y1, 360, 56, "输入明文 P (字符串或十六进制)")
process(d, CX_ENC, Y2, 420, 56, "nbytes = ceil(bitlen(n) / 8), block = nbytes - 1")
process(d, CX_ENC, Y3, 360, 56, "取明文下一个分块 (<= block 字节)")
process(d, CX_ENC, Y4, 360, 56, "m = fromBytes, c = m^e mod n")
process(d, CX_ENC, Y5, 360, 56, "将 c 按 nbytes 字节大端序写缓冲区")
diamond(d, CX_ENC, Y6, 340, 100, "明文已全部分块处理完 ?")
process(d, CX_ENC, Y7, 360, 56, "输出密文 C (HEX)")
process(d, CX_ENC, Y8, 240, 50, "加密完成", fill="#F0F0F0", line="#888888")

# ----- 右列：解密 -----
process(d, CX_DEC, Y1, 360, 56, "输入密文 C (HEX)")
diamond(d, CX_DEC, Y2, 340, 100, "len(C) 是 nbytes 的整数倍 ?")
error_box(d, CX_DEC + 340, Y2, "提示错误：长度非法\n要求重新输入")

process(d, CX_DEC, Y3, 360, 56, "取下一个密文分块 c")
process(d, CX_DEC, Y4, 440, 86, "m1 = c^dp mod p, m2 = c^dq mod q\nh = qinv*(m1-m2) mod p, m = m2+h*q\n(无 CRT 时改用 m = c^d mod n)")
process(d, CX_DEC, Y5, 360, 56, "将 m 转字节，去前导 0 追加缓冲区")
diamond(d, CX_DEC, Y6, 340, 100, "密文已全部分块处理完 ?")

process(d, CX_DEC, Y7, 360, 56, "输出明文 P'")
diamond(d, CX_DEC, Y8, 340, 100, "P' 与 P 完全一致 ?")
error_box(d, CX_DEC + 340, Y8, "提示错误：\n检查密钥与分块处理")
process(d, CX_DEC, Y9, 240, 50, "解密完成", fill="#F0F0F0", line="#888888")

# ==================== 主干连线 ====================
# 开始 -> 菜单 -> 选择
arrow(d, (MENU_X, 128), (MENU_X, 152))
arrow(d, (MENU_X, 208), (MENU_X, 250))

# 分叉到三列
# 左：密钥生成
d.line([(MENU_X - 140, Y_DIA), (CX_KG, Y_DIA), (CX_KG, Y1 - 28)], fill="#333333", width=3)
arrow(d, (CX_KG, Y1 - 50), (CX_KG, Y1 - 28))
d.text((CX_KG + 30, Y_DIA - 15), "选 1", font=F_SMALL, fill="#333333")

# 中：加密
arrow(d, (MENU_X, Y_DIA + 50), (MENU_X, Y1 - 28))
d.text((MENU_X + 15, Y_DIA + 60), "选 2", font=F_SMALL, fill="#333333")

# 右：解密
d.line([(MENU_X + 140, Y_DIA), (CX_DEC, Y_DIA), (CX_DEC, Y1 - 28)], fill="#333333", width=3)
arrow(d, (CX_DEC, Y1 - 50), (CX_DEC, Y1 - 28))
d.text((CX_DEC - 80, Y_DIA - 15), "选 3", font=F_SMALL, fill="#333333")

# ==================== 左列连线 (密钥生成) ====================
arrow(d, (CX_KG, Y1 + 28), (CX_KG, Y2 - 50))
arrow(d, (CX_KG, Y2 + 50), (CX_KG, Y3 - 28)) # 是
arrow(d, (CX_KG, Y3 + 28), (CX_KG, Y4 - 50))
arrow(d, (CX_KG, Y4 + 50), (CX_KG, Y5 - 28)) # 是
arrow(d, (CX_KG, Y5 + 28), (CX_KG, Y6 - 50))
arrow(d, (CX_KG, Y6 + 50), (CX_KG, Y7 - 28)) # 是
arrow(d, (CX_KG, Y7 + 28), (CX_KG, Y8 - 28))
arrow(d, (CX_KG, Y8 + 28), (CX_KG, Y9 - 25))

# 左列内部红色回环
# bits 非法 -> 错误 -> 回退
arrow(d, (CX_KG + 170, Y2), (CX_KG + 230, Y2), color=RED_RETRY)
d.line([(CX_KG + 340, Y2 - 35), (CX_KG + 340, Y1), (CX_KG + 180, Y1)], fill=RED_RETRY, width=3)
arrow(d, (CX_KG + 230, Y1), (CX_KG + 180, Y1), color=RED_RETRY)
d.text((CX_KG + 180, Y2 - 15), "否", font=F_SMALL, fill=RED_RETRY)

# p,q / gcd 失败 -> 回退到 Y3
arrow(d, (CX_KG - 170, Y4), (CX_KG - 220, Y4), color=RED_RETRY)
d.line([(CX_KG - 220, Y4), (CX_KG - 220, Y3), (CX_KG - 180, Y3)], fill=RED_RETRY, width=3)
arrow(d, (CX_KG - 220, Y3), (CX_KG - 180, Y3), color=RED_RETRY)
d.text((CX_KG - 180, Y4 - 15), "否", font=F_SMALL, fill=RED_RETRY)

arrow(d, (CX_KG - 170, Y6), (CX_KG - 260, Y6), color=RED_RETRY)
d.line([(CX_KG - 260, Y6), (CX_KG - 260, Y3), (CX_KG - 180, Y3)], fill=RED_RETRY, width=3)
# 箭头已在上一段画过，这里直接合并即可
d.text((CX_KG - 180, Y6 - 15), "否", font=F_SMALL, fill=RED_RETRY)

# ==================== 中列连线 (加密) ====================
arrow(d, (CX_ENC, Y1 + 28), (CX_ENC, Y2 - 28))
arrow(d, (CX_ENC, Y2 + 28), (CX_ENC, Y3 - 28))
arrow(d, (CX_ENC, Y3 + 28), (CX_ENC, Y4 - 28))
arrow(d, (CX_ENC, Y4 + 28), (CX_ENC, Y5 - 28))
arrow(d, (CX_ENC, Y5 + 28), (CX_ENC, Y6 - 50))
arrow(d, (CX_ENC, Y6 + 50), (CX_ENC, Y7 - 28)) # 是
arrow(d, (CX_ENC, Y7 + 28), (CX_ENC, Y8 - 25))

# 明文未处理完 -> 红色回环
arrow(d, (CX_ENC - 170, Y6), (CX_ENC - 250, Y6), color=RED_RETRY)
d.line([(CX_ENC - 250, Y6), (CX_ENC - 250, Y3), (CX_ENC - 180, Y3)], fill=RED_RETRY, width=3)
arrow(d, (CX_ENC - 250, Y3), (CX_ENC - 180, Y3), color=RED_RETRY)
d.text((CX_ENC - 180, Y6 - 15), "否", font=F_SMALL, fill=RED_RETRY)

# ==================== 右列连线 (解密) ====================
arrow(d, (CX_DEC, Y1 + 28), (CX_DEC, Y2 - 50))
arrow(d, (CX_DEC, Y2 + 50), (CX_DEC, Y3 - 28)) # 是
arrow(d, (CX_DEC, Y3 + 28), (CX_DEC, Y4 - 43))
arrow(d, (CX_DEC, Y4 + 43), (CX_DEC, Y5 - 28))
arrow(d, (CX_DEC, Y5 + 28), (CX_DEC, Y6 - 50))
arrow(d, (CX_DEC, Y6 + 50), (CX_DEC, Y7 - 28)) # 是
arrow(d, (CX_DEC, Y7 + 28), (CX_DEC, Y8 - 50))
arrow(d, (CX_DEC, Y8 + 50), (CX_DEC, Y9 - 25)) # 是

# 解密内部红色回环
# 密文长度错误 -> 往外抛（由蓝色线接管，这侧不画闭环）
arrow(d, (CX_DEC + 170, Y2), (CX_DEC + 230, Y2), color=RED_RETRY)
d.text((CX_DEC + 180, Y2 - 15), "否", font=F_SMALL, fill=RED_RETRY)

# 密文未处理完 -> 红色回环
arrow(d, (CX_DEC + 170, Y6), (CX_DEC + 250, Y6), color=RED_RETRY)
d.line([(CX_DEC + 250, Y6), (CX_DEC + 250, Y3), (CX_DEC + 180, Y3)], fill=RED_RETRY, width=3)
arrow(d, (CX_DEC + 250, Y3), (CX_DEC + 180, Y3), color=RED_RETRY)
d.text((CX_DEC + 180, Y6 - 15), "否", font=F_SMALL, fill=RED_RETRY)

# 校验失败 -> 往外抛（由蓝色线接管）
arrow(d, (CX_DEC + 170, Y8), (CX_DEC + 230, Y8), color=RED_RETRY)
d.text((CX_DEC + 180, Y8 - 15), "否", font=F_SMALL, fill=RED_RETRY)


# ==================== 蓝色外部返回线（核心解决） ====================
# 左侧返回线：完成 -> 一路走到最左侧，然后向上回到菜单菱形左侧
d.line([(CX_KG, Y9 + 25), (CX_KG, Y9 + 60), (50, Y9 + 60), (50, Y_DIA), (MENU_X - 140, Y_DIA)], fill=BLUE_RETURN, width=4)
arrow(d, (MENU_X - 140 - 10, Y_DIA), (MENU_X - 140, Y_DIA), color=BLUE_RETURN, width=4)
d.text((CX_KG, Y9 + 75), "返回主菜单", font=F_SMALL, fill=BLUE_RETURN, anchor="mm")

# 中间返回线：完成 -> 往右走，绕开节点，向上回到菜单框的右侧
d.line([(CX_ENC, Y8 + 25), (CX_ENC, Y8 + 60), (1450, Y8 + 60), (1450, Y_MENU), (MENU_X + 160, Y_MENU)], fill=BLUE_RETURN, width=4)
arrow(d, (MENU_X + 160 + 10, Y_MENU), (MENU_X + 160, Y_MENU), color=BLUE_RETURN, width=4)
d.text((CX_ENC + 50, Y8 + 75), "返回主菜单", font=F_SMALL, fill=BLUE_RETURN, anchor="lm")

# 右侧返回线
# 1. 完成返回
d.line([(CX_DEC, Y9 + 25), (CX_DEC, Y9 + 60), (2200, Y9 + 60), (2200, Y_DIA), (MENU_X + 140, Y_DIA)], fill=BLUE_RETURN, width=4)
arrow(d, (MENU_X + 140 + 10, Y_DIA), (MENU_X + 140, Y_DIA), color=BLUE_RETURN, width=4)
d.text((CX_DEC, Y9 + 75), "返回主菜单", font=F_SMALL, fill=BLUE_RETURN, anchor="mm")

# 2. 长度错误，抛出到最右侧蓝线并打上箭头
d.line([(CX_DEC + 340, Y2 + 35), (CX_DEC + 340, Y2 + 50), (2200, Y2 + 50)], fill=BLUE_RETURN, width=3)
arrow(d, (2200 - 15, Y2 + 50), (2200, Y2 + 50), color=BLUE_RETURN, width=3)
d.text((CX_DEC + 230, Y2 + 60), "返回主菜单重试", font=F_SMALL, fill=BLUE_RETURN, anchor="lm")

# 3. 一致性校验失败，抛出到最右侧蓝线并打上箭头
d.line([(CX_DEC + 340, Y8 + 35), (CX_DEC + 340, Y8 + 50), (2200, Y8 + 50)], fill=BLUE_RETURN, width=3)
arrow(d, (2200 - 15, Y8 + 50), (2200, Y8 + 50), color=BLUE_RETURN, width=3)
d.text((CX_DEC + 230, Y8 + 60), "返回主菜单重试", font=F_SMALL, fill=BLUE_RETURN, anchor="lm")


# ==================== 保存 ====================
out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "rsa_flow_horizontal.png")
img.save(out, "PNG")
print("已保存：", out, img.size)