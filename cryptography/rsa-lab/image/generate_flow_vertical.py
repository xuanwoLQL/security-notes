# -*- coding: utf-8 -*-
"""生成《实验3 RSA 加密解密算法》流程图（真实绘制，非截图）。

说明：
  1. 文字统一使用 SimHei / 微软雅黑，因此框内文字不使用 ⁻¹、φ、≠ 等可能缺失的
     特殊符号，改用 ^(-1)、phi、!=、ceil 这类 ASCII 写法，避免出现方块乱码；
  2. 画布右侧预留空白，错误提示框位于 x=940 一列，"是/否" 分支标签紧贴菱形外侧；
  3. 失败回环使用左侧竖线（x=100、x=55）回到"生成 p、q"与"取明文分块"节点，
     不会穿过任何图形内部；
  4. 默认把图片保存到脚本所在目录（可用参数指定其它目录）。
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont


def pick_font(*candidates):
    """按顺序挑选第一个存在的字体文件，避免某个字体缺失时脚本直接报错。"""
    for path in candidates:
        if os.path.exists(path):
            return path
    raise SystemExit("未找到可用中文字体：" + "、".join(candidates))


FONT_PATH = pick_font(r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\simsun.ttc")
FONT_BOLD = pick_font(r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\msyh.ttc",
                      r"C:\Windows\Fonts\simhei.ttf")

# 画布：高度需要容纳"密钥生成 + 加密 + 解密 + 校验"四段主流程
W, H = 1180, 3020
BG = "white"
PROC_FILL, PROC_LINE = "#E8F1FB", "#2F6FB2"
DEC_FILL, DEC_LINE = "#FFF6E0", "#D9A03A"
TERM_FILL, TERM_LINE = "#E7F6EA", "#3E9E58"
ERR_FILL, ERR_LINE = "#FDECEC", "#C0504D"
TEXT = "#1F1F1F"

CX = 450          # 主流程中心线
BOX_W = 620       # 普通处理框宽度
DIA_W = 440       # 菱形宽度
ERR_CX = 940      # 错误提示框中心
ERR_W, ERR_H = 300, 90


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_PATH, size)


F_TITLE = font(30, bold=True)
F_BOX = font(20)
F_SMALL = font(18)


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


def error_box(draw, cx, cy, text, fnt=F_SMALL):
    process(draw, cx, cy, ERR_W, ERR_H, text, fnt=fnt,
            fill=ERR_FILL, line=ERR_LINE, radius=8)


def arrow(draw, p1, p2, color="#333333", width=3):
    x1, y1 = p1
    x2, y2 = p2
    draw.line([x1, y1, x2, y2], fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 12
    pts = [(x2, y2),
           (x2 - size * math.cos(ang - 0.4), y2 - size * math.sin(ang - 0.4)),
           (x2 - size * math.cos(ang + 0.4), y2 - size * math.sin(ang + 0.4))]
    draw.polygon(pts, fill=color)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

d.text((W / 2, 42), "RSA 加解密算法流程图", font=F_TITLE, fill="#1F3A5F", anchor="mm")

# ---------- 各节点纵向中心坐标 ----------
Y_START   = 130
Y_BITS    = 221
Y_CKBITS  = 339
Y_GENPQ   = 464
Y_CKPQ    = 594
Y_NPHI    = 724
Y_CKGCD   = 852
Y_CALCD   = 979
Y_SAVE    = 1084
Y_INP     = 1184
Y_NBYTES  = 1282
Y_CHUNK   = 1380
Y_MC      = 1480
Y_CWRITE  = 1580
Y_CKPT    = 1705
Y_OUTC    = 1830
Y_INC     = 1930
Y_CKLEN   = 2060
Y_CCHUNK  = 2185
Y_DECM    = 2305
Y_MBYTES  = 2430
Y_CKCT    = 2560
Y_OUTP    = 2685
Y_VERIFY  = 2810
Y_END     = 2933

L = CX - BOX_W / 2            # 主流程框左边缘 140
R = CX + BOX_W / 2            # 主流程框右边缘 760
DL = CX - DIA_W / 2           # 菱形左顶点 230
DR = CX + DIA_W / 2           # 菱形右顶点 670
LOOP_X1 = 100                 # 左侧内圈回环
LOOP_X2 = 55                  # 左侧外圈回环

# ==================== 节点绘制 ====================
terminal(d, CX, Y_START, 200, 56, "开始")

process(d, CX, Y_BITS, BOX_W, 56, "输入密钥位数 bits（默认 512，32~1024 的偶数）")

diamond(d, CX, Y_CKBITS, DIA_W, 110, "bits 是 32~1024 的偶数 ?")
error_box(d, ERR_CX, Y_CKBITS, "提示：位数非法\n要求重新输入")

process(d, CX, Y_GENPQ, BOX_W, 70, "随机生成两个 bits/2 位素数 p、q")
diamond(d, CX, Y_CKPQ, DIA_W, 120, "p != q 且 |p - q| 足够大 ?")

process(d, CX, Y_NPHI, BOX_W, 70, "计算 n = p * q，phi = (p-1)*(q-1)")
diamond(d, CX, Y_CKGCD, DIA_W, 114, "gcd(e = 65537, phi) = 1 ?")

process(d, CX, Y_CALCD, BOX_W, 70,
        "计算 d = e^(-1) mod phi 及 CRT 参数 dp、dq、qinv")
process(d, CX, Y_SAVE, BOX_W, 70,
        "保存 public.txt（n, e）与 private.txt（含 d、CRT 参数）")

process(d, CX, Y_INP, BOX_W, 60, "输入明文 P（字符串或十六进制）")
process(d, CX, Y_NBYTES, BOX_W, 65,
        "nbytes = ceil(bitlen(n) / 8)，每块 block = nbytes - 1")
process(d, CX, Y_CHUNK, BOX_W, 60, "取明文中的下一个分块（不超过 block 字节）")
process(d, CX, Y_MC, BOX_W, 70, "m = fromBytes(chunk)，c = m^e mod n")
process(d, CX, Y_CWRITE, BOX_W, 60, "将 c 按 nbytes 字节大端序写入密文缓冲区")
diamond(d, CX, Y_CKPT, DIA_W, 120, "明文已全部分块处理完 ?")
process(d, CX, Y_OUTC, BOX_W, 60, "输出密文 C（HEX）")

process(d, CX, Y_INC, BOX_W, 70, "输入密文 C（HEX），按 nbytes 字节分块")
diamond(d, CX, Y_CKLEN, DIA_W, 120, "len(C) 是 nbytes 的整数倍 ?")
error_box(d, ERR_CX, Y_CKLEN, "提示错误：密文长度\n必须是 nbytes 的整数倍")

process(d, CX, Y_CCHUNK, BOX_W, 60, "取下一个密文分块 c")
process(d, CX, Y_DECM, BOX_W, 110,
        "m1 = c^dp mod p，m2 = c^dq mod q\n"
        "h = qinv * (m1 - m2) mod p，m = m2 + h*q\n"
        "（无 CRT 参数时改用 m = c^d mod n）")
process(d, CX, Y_MBYTES, BOX_W, 70,
        "将 m 转为字节，去掉前导 0 后追加到明文缓冲区")
diamond(d, CX, Y_CKCT, DIA_W, 120, "密文已全部分块处理完 ?")

process(d, CX, Y_OUTP, BOX_W, 60, "输出明文 P'")
diamond(d, CX, Y_VERIFY, DIA_W, 120, "P' 与 P 完全一致 ?")
error_box(d, ERR_CX, Y_VERIFY, "提示错误：\n检查密钥与分块处理")

terminal(d, CX, Y_END, 200, 56, "结束")

# ==================== 主干连线 ====================
arrow(d, (CX, 158), (CX, 193))                 # 开始 -> 输入 bits
arrow(d, (CX, 249), (CX, 284))                 # 输入 bits -> 判断 bits
arrow(d, (CX, 394), (CX, 429))                 # 判断 bits(是) -> 生成 p、q
arrow(d, (CX, 499), (CX, 534))                 # 生成 p、q -> 判断 p、q
arrow(d, (CX, 654), (CX, 689))                 # 判断 p、q(是) -> 计算 n、phi
arrow(d, (CX, 759), (CX, 795))                 # 计算 n、phi -> 判断 gcd
arrow(d, (CX, 909), (CX, 944))                 # 判断 gcd(是) -> 计算 d
arrow(d, (CX, 1014), (CX, 1049))               # 计算 d -> 保存密钥
arrow(d, (CX, 1119), (CX, 1154))               # 保存密钥 -> 输入明文
arrow(d, (CX, 1214), (CX, 1249))               # 输入明文 -> 计算 nbytes
arrow(d, (CX, 1315), (CX, 1350))               # nbytes -> 取明文分块
arrow(d, (CX, 1410), (CX, 1445))               # 取分块 -> m、c 计算
arrow(d, (CX, 1515), (CX, 1550))               # m、c -> 写密文缓冲
arrow(d, (CX, 1610), (CX, 1645))               # 写缓冲 -> 判断明文完
arrow(d, (CX, 1765), (CX, 1800))               # 判断明文完(是) -> 输出密文
arrow(d, (CX, 1860), (CX, 1895))               # 输出密文 -> 输入密文
arrow(d, (CX, 1965), (CX, 2000))               # 输入密文 -> 判断长度
arrow(d, (CX, 2120), (CX, 2155))               # 判断长度(是) -> 取密文分块
arrow(d, (CX, 2215), (CX, 2250))               # 取密文分块 -> 解密计算 m
arrow(d, (CX, 2360), (CX, 2395))               # 解密 m -> 转字节
arrow(d, (CX, 2465), (CX, 2500))               # 转字节 -> 判断密文完
arrow(d, (CX, 2620), (CX, 2655))               # 判断密文完(是) -> 输出明文
arrow(d, (CX, 2715), (CX, 2750))               # 输出明文 -> 一致性校验
arrow(d, (CX, 2870), (CX, 2905))               # 校验(是) -> 结束

# ==================== 右侧错误分支 ====================

# 1) bits 非法：错误框 -> 绕回"输入 bits"
arrow(d, (DR, Y_CKBITS), (ERR_CX - ERR_W / 2 - 2, Y_CKBITS))
d.line([ERR_CX + ERR_W / 2, Y_CKBITS,
        W - 50, Y_CKBITS,
        W - 50, Y_BITS,
        R + 2, Y_BITS], fill="#C0504D", width=3)
arrow(d, (W - 50, Y_BITS), (R + 2, Y_BITS), color="#C0504D")

# 2) 判断 p、q 失败：内圈回环 -> 生成 p、q
arrow(d, (DL, Y_CKPQ), (LOOP_X1, Y_CKPQ))
d.line([LOOP_X1, Y_CKPQ, LOOP_X1, Y_GENPQ, L - 2, Y_GENPQ], fill="#C0504D", width=3)
arrow(d, (LOOP_X1, Y_GENPQ), (L - 2, Y_GENPQ), color="#C0504D")

# 3) 判断 gcd 失败：外圈回环 -> 生成 p、q
arrow(d, (DL, Y_CKGCD), (LOOP_X2, Y_CKGCD))
d.line([LOOP_X2, Y_CKGCD, LOOP_X2, Y_GENPQ, L - 2, Y_GENPQ], fill="#C0504D", width=3)
arrow(d, (LOOP_X2, Y_GENPQ), (L - 2, Y_GENPQ), color="#C0504D")

# 4) 密文长度非法：错误框 -> 提示返回主菜单
arrow(d, (DR, Y_CKLEN), (ERR_CX - ERR_W / 2 - 2, Y_CKLEN))
d.text((ERR_CX, Y_CKLEN + ERR_H / 2 + 22), "-> 返回主菜单，重新输入密文",
       font=F_SMALL, fill="#C0504D", anchor="mm")

# 5) 明文一致性校验失败：错误框 -> 提示返回主菜单
arrow(d, (DR, Y_VERIFY), (ERR_CX - ERR_W / 2 - 2, Y_VERIFY))
d.text((ERR_CX, Y_VERIFY + ERR_H / 2 + 22), "-> 返回主菜单，检查密钥与分块",
       font=F_SMALL, fill="#C0504D", anchor="mm")

# ==================== 左侧分块循环回环 ====================

# 6) 明文未处理完 -> 回到"取明文分块"
arrow(d, (DL, Y_CKPT), (LOOP_X1, Y_CKPT))
d.line([LOOP_X1, Y_CKPT, LOOP_X1, Y_CHUNK, L - 2, Y_CHUNK], fill="#333333", width=3)
arrow(d, (LOOP_X1, Y_CHUNK), (L - 2, Y_CHUNK))

# 7) 密文未处理完 -> 回到"取密文分块"
arrow(d, (DL, Y_CKCT), (LOOP_X1, Y_CKCT))
d.line([LOOP_X1, Y_CKCT, LOOP_X1, Y_CCHUNK, L - 2, Y_CCHUNK], fill="#333333", width=3)
arrow(d, (LOOP_X1, Y_CCHUNK), (L - 2, Y_CCHUNK))

# ==================== 分支标签 ====================
RED, GREEN = "#C0504D", "#3E9E58"


def lab(x, y, text, color, anchor):
    d.text((x, y), text, font=F_SMALL, fill=color, anchor=anchor)


# 判断 bits
lab(DR + 10, Y_CKBITS - 18, "否", RED, "lm")
lab(CX + 16, Y_CKBITS + 66, "是", GREEN, "lm")

# 判断 p、q
lab(DL - 10, Y_CKPQ - 18, "否", RED, "rm")
lab(CX + 16, Y_CKPQ + 66, "是", GREEN, "lm")

# 判断 gcd
lab(DL - 10, Y_CKGCD - 18, "否", RED, "rm")
lab(CX + 16, Y_CKGCD + 64, "是", GREEN, "lm")

# 判断明文是否处理完
lab(DL - 10, Y_CKPT - 18, "否", RED, "rm")
lab(CX + 16, Y_CKPT + 66, "是", GREEN, "lm")

# 判断密文长度
lab(DR + 10, Y_CKLEN - 18, "否", RED, "lm")
lab(CX + 16, Y_CKLEN + 66, "是", GREEN, "lm")

# 判断密文是否处理完
lab(DL - 10, Y_CKCT - 18, "否", RED, "rm")
lab(CX + 16, Y_CKCT + 66, "是", GREEN, "lm")

# 一致性校验
lab(DR + 10, Y_VERIFY - 18, "否", RED, "lm")
lab(CX + 16, Y_VERIFY + 66, "是", GREEN, "lm")

# 段落小标题（可选，帮助阅读）
d.text((60, Y_GENPQ - 60), "【密钥生成】", font=F_SMALL, fill="#2F6FB2", anchor="lm")
d.text((60, Y_INP - 46), "【加密】", font=F_SMALL, fill="#2F6FB2", anchor="lm")
d.text((60, Y_INC - 46), "【解密】", font=F_SMALL, fill="#2F6FB2", anchor="lm")

# ==================== 保存 ====================
out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "rsa_flow.png")
img.save(out, "PNG")
print("已保存：", out, img.size)