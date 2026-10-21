# -*- coding: utf-8 -*-
"""
生成《网络安全与 CTF 新手起步指南（精修版）》Markdown 与 Word 文档。

运行环境：
    D:\\PBox-full\\python3\\python.exe

依赖：
    python-docx
"""

import os
import re
import sys
from datetime import date

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


OUTPUT_DIR = r"D:\Program Files\Obsidian\zuodebiji\网络安全笔记\CTF比赛\CTF"
DOCX_PATH = os.path.join(OUTPUT_DIR, "网络安全与CTF新手起步指南_精修版.docx")
MD_PATH = os.path.join(OUTPUT_DIR, "网络安全与CTF新手起步指南_精修版.md")
MAGPIE_IMAGE = os.path.join(OUTPUT_DIR, "屏幕截图 2026-10-21 164857.png")

FONT_CN = "微软雅黑"
FONT_BODY = "宋体"
FONT_CODE = "Consolas"
NAVY = "17324D"
TEAL = "1F7A74"
ORANGE = "C66A2B"
TEXT = "29343D"
MUTED = "66737D"
LIGHT_BLUE = "EAF3F7"
LIGHT_TEAL = "E8F4F1"
LIGHT_ORANGE = "FFF3E8"
LIGHT_GRAY = "F3F5F7"
WHITE = "FFFFFF"
BORDER = "CDD8DF"
RED = "A33A3A"
LIGHT_RED = "FBECEC"


BLOCKS = []


def h1(text):
    BLOCKS.append(("h1", text))


def h2(text):
    BLOCKS.append(("h2", text))


def h3(text):
    BLOCKS.append(("h3", text))


def p(text):
    BLOCKS.append(("p", text))


def lead(text):
    BLOCKS.append(("lead", text))


def quote(text):
    BLOCKS.append(("quote", text))


def bullets(items):
    BLOCKS.append(("bullets", items))


def numbers(items):
    BLOCKS.append(("numbers", items))


def code(language, text):
    BLOCKS.append(("code", language, text.strip("\n")))


def placeholder(label, description):
    BLOCKS.append(("placeholder", label, description))


def image(path, caption, width_cm=16.0):
    BLOCKS.append(("image", path, caption, width_cm))


def callout(title, text, tone="blue"):
    BLOCKS.append(("callout", title, text, tone))


def table(headers, rows, widths=None):
    BLOCKS.append(("table", headers, rows, widths))


def link(label, url):
    BLOCKS.append(("link", label, url))


def pagebreak():
    BLOCKS.append(("pagebreak",))


def build_content():
    h1("写在前面：这份指南怎么用")
    lead(
        "你不需要先成为程序员，也不需要把数学、操作系统和汇编全部学完，才有资格打开第一道题。"
        "新手真正需要的，是一个足够小的起点、一条能看见反馈的路线，以及持续复盘的习惯。"
    )
    p(
        "这份指南按“认识方向 → 进入靶场 → 建立习惯 → 接触真实场景 → 借力 AI”的顺序展开。"
        "建议你先通读一遍，再按章节动手；不要把它当成收藏夹里又一份“以后再看”的资料。"
    )
    callout(
        "唯一硬性门槛",
        "遵守法律与授权边界。所有练习都应发生在公开靶场、比赛环境或取得书面授权的系统中。"
        "未经授权扫描、入侵、窃取数据或破坏服务，不属于技术学习。",
        "red",
    )
    h2("学习原则：少一点囤积，多一点闭环")
    bullets(
        [
            "**实践优先**：看十篇教程，不如独立做完一道题并复现一次。",
            "**单点突破**：先选 Misc 或 Web，形成正反馈，再扩展方向。",
            "**每题复盘**：做完不等于学会，能脱离原题重新走通才算掌握。",
            "**合法授权**：只测试自己拥有、平台提供或明确授权的目标。",
            "**长期复利**：把题目、脚本、命令和踩坑记录沉淀成自己的知识库。",
        ]
    )
    quote("不要等“学会了”再动手。你是在动手、卡住、查证和复盘的循环里学会的。")

    pagebreak()
    h1("一、引言：新手如何破局")
    lead(
        "CTF 最有价值的地方，不是让你背下多少 payload，而是把真实安全问题压缩成可重复练习的小任务。"
        "先看清五个方向各自在训练什么，再决定自己的第一站。"
    )

    h2("1.1 一张图看懂 CTF 的五大方向")
    table(
        ["方向", "主要解决什么问题", "核心能力", "入门体感", "常见工具"],
        [
            ["Misc", "编码、隐写、流量、取证、杂项分析", "观察、脚本、信息整理", "容易获得反馈", "CyberChef、Wireshark、Python"],
            ["Crypto", "古典密码、RSA、分组密码、哈希与数学攻击", "数学建模、脚本实现", "前期门槛中等", "Python、SageMath、数论工具"],
            ["Web", "SQL 注入、文件上传、SSRF、SSTI、反序列化等", "HTTP 理解、请求构造、代码审计", "反馈快、应用广", "Burp Suite、浏览器开发者工具、sqlmap"],
            ["Pwn", "栈溢出、堆利用、格式化字符串、沙箱逃逸", "汇编、内存布局、调试", "门槛较高", "GDB、pwntools、checksec"],
            ["Reverse", "静态分析、动态调试、脱壳、算法还原", "程序结构、汇编、调试耐心", "门槛较高", "IDA、x64dbg、dnSpy、JADX"],
        ],
        [2.0, 5.3, 4.0, 3.0, 4.4],
    )

    h2("1.2 五大方向到底在学什么")
    h3("Misc：先学会观察")
    p(
        "Misc 看似“杂”，本质是训练你从文件、图片、流量、日志和异常现象里提取线索。"
        "你会接触 Base 编码、压缩包、图片隐写、音频分析、PCAP 流量和简单取证。"
        "它非常适合零基础，因为题目反馈直接，工具操作也能迅速转化为真实工作中的分析能力。"
    )
    h3("Crypto：用数学和代码还原秘密")
    p(
        "Crypto 不只是“解密”。它要求你理解密钥、随机数、模运算、分组模式和常见攻击前提。"
        "新手不必一上来推导所有公式，先学会识别题型、复现脚本、验证假设，再逐步补数学。"
    )
    h3("Web：理解一个请求如何变成漏洞")
    p(
        "Web 的核心是理解浏览器、HTTP、服务端和数据库之间的数据流。"
        "当你能看懂一个请求的参数、Cookie、响应头和业务逻辑，就能进一步判断注入、越权、上传、"
        "文件包含、SSRF、模板注入和反序列化等问题。Web 也是渗透测试最常见的能力底座之一。"
    )
    h3("Pwn：和内存与程序行为打交道")
    p(
        "Pwn 往往需要 C 语言、汇编、Linux 进程、内存布局和调试器基础。"
        "它的学习曲线更陡，但一旦建立“程序在内存里如何运行”的直觉，很多底层安全问题会变得清晰。"
    )
    h3("Reverse：把程序拆开看")
    p(
        "Reverse 会让你面对二进制、字节码、移动应用或 .NET 程序。"
        "静态分析负责“看结构”，动态调试负责“看行为”，两者结合才能还原校验逻辑、通信协议或恶意行为。"
    )

    h2("1.3 为什么建议从 Misc 和 Web 起步")
    bullets(
        [
            "**Misc 的反馈最快**：一个文件、一次解码、一条流量，就能让你体验“发现线索—验证—拿到 Flag”的完整闭环。",
            "**Web 的知识迁移最广**：HTTP、浏览器、代理、请求重放和代码审计，会持续用于 CTF、渗透测试与日常开发安全。",
            "**工具链容易建立**：Python、浏览器、Burp Suite、Wireshark 和 CyberChef 都能快速上手。",
            "**不意味着永远不碰 Pwn/Reverse**：只是先把基础、调试习惯和复盘能力建立起来，再挑战更高的门槛。",
        ]
    )
    callout(
        "新手破局公式",
        "基础工具 + 20 道入门题 + 20 篇自己的 WP = 第一轮正反馈。"
        "数量不是 KPI，关键是每一道题都能说清楚“我为什么这样做、如何验证、下次怎样更快”。",
        "teal",
    )

    h2("1.4 第一周可以直接照做的安排")
    numbers(
        [
            "第 1 天：安装 Python、浏览器、Burp Suite、Wireshark、CyberChef，建立 Obsidian 知识库。",
            "第 2 天：理解 URL、HTTP 方法、状态码、Cookie、请求头和响应头，用 Burp 拦截并重放一个请求。",
            "第 3 天：练习 Base64、URL 编码、十六进制、压缩包和文件头识别。",
            "第 4 天：用 Wireshark 打开一个练习 PCAP，练习过滤、跟踪 TCP 流和导出对象。",
            "第 5 天：完成 5 道 Misc 入门题，每题只允许查看一次提示。",
            "第 6 天：完成 5 道 Web 入门题，重点记录请求包与响应差异。",
            "第 7 天：给 10 道题各写一篇短 WP，整理常用命令和踩坑点。",
        ]
    )

    pagebreak()
    h1("二、初期：零基础小白的起步路线与靶场")
    lead(
        "初期最怕两件事：平台太多不知道选哪个，以及一上来就做超纲题。"
        "下面三个平台分别承担“系统刷题、英文实战、中文零基础路线”的角色，选一个主平台坚持两周。"
    )

    h2("2.1 西电 CTF 终端：适合系统化刷题")
    link("西电 CTF 终端 · 练习入口", "https://ctf.xidian.edu.cn/training")
    p(
        "西电 CTF 终端的训练区保留了多届比赛题库和练习场，适合按赛事、章节和方向系统推进。"
        "对新手最友好的入口通常是“从此开始”、Misc、Web 基础，以及 MoeCTF 一类的入门赛事题库。"
        "练习场通常没有时间压力，可以反复尝试；但也正因如此，更需要给自己设定时间盒，避免一道题耗掉整晚。"
    )
    placeholder("图1", "西电CTF终端练习场页面截图")
    h3("推荐打开方式")
    numbers(
        [
            "注册并登录后进入“训练”，先浏览练习场列表和赛事归档，不要急着点最难的题。",
            "选择“MoeCTF”或“从此开始”一类入口，按 Misc / Web / Crypto 等方向建立题目地图。",
            "第一轮只做能看懂题面 60% 以上的题；先拿到 20—30 次完整解题反馈。",
            "单题建议：独立思考 15 分钟，查官方知识或提示到 40 分钟，仍无进展再看 WP。",
            "看完 WP 后关闭页面，从空目录重新复现一次，并写下卡住自己的那一步。",
        ]
    )
    callout(
        "不要直接抄答案",
        "看 WP 的目的是补上知识缺口，不是把 Flag 复制到提交框。"
        "复现时应能独立解释每个参数、每条命令和每个判断依据。",
        "orange",
    )

    h2("2.2 CyLab Security Academy：在英文环境里练实战")
    link("CyLab Security Academy · Dashboard", "https://learn.cylabacademy.org/dashboard")
    p(
        "当你能完成中文入门题后，可以逐步进入英文平台。"
        "英文环境的价值不只是“练英语”，更是让你习惯阅读原始文档、工具帮助、错误信息和国际社区讨论。"
        "刚开始不要逐词翻译，先抓住动作词、对象和限制条件，例如 identify、extract、bypass、authorized。"
    )
    placeholder("图2", "CyLab Security Academy仪表盘截图")
    h3("建议的使用节奏")
    bullets(
        [
            "先完成 Dashboard 中的入门模块，再按 Misc / Web 主题挑选挑战。",
            "每周固定 3 道题，保持可持续节奏，比周末一次刷 20 道更有效。",
            "建立“术语—中文解释—本题语境”三列表，积累 HTTP、crypto、forensics 等高频词。",
            "遇到英文报错时，先复制关键短语搜索官方文档，再向 AI 询问错误含义和验证方法。",
            "每完成一个模块，用自己的话写一段英文摘要，训练技术表达。",
        ]
    )

    h2("2.3 好靶场：从 0 到 1 的中文学习路线")
    link("好靶场 · 初学者训练营", "http://hbc.haobachang.com/learn_route?id=1")
    p(
        "好靶场的学习路线更适合“完全不知道从哪里开始”的同学。"
        "从截图中的课程结构可以看到，初学者训练营把内容拆成基础知识、Flag 入门、安全编码、Python 入门、"
        "Linux 命令入门、逻辑漏洞、OWASP Top 10 和信息收集等模块。"
        "它强调从生活场景理解“为什么要学安全”，再逐步过渡到真实靶场操作。"
    )
    placeholder("图3", "好靶场初学者训练营页面截图")
    h3("零基础三步走")
    numbers(
        [
            "先选“初学者训练营”，不要同时开五条学习路线。",
            "优先完成“01-基础知识模块”，包括网络安全常识、Flag 规则、编码、Python 和 Linux 命令。",
            "每完成一个关卡，都在 Obsidian 写三行：做了什么、看到什么、下次如何复用。",
        ]
    )
    p(
        "平台课程和关卡会更新，具体顺序以页面当前显示为准。"
        "如果某个模块要求付费或暂时无法访问，不必卡住，换一个公开题目完成同样的能力训练即可。"
    )

    h2("2.4 资源不是收藏夹，而是你的作战地图")
    placeholder("图4", "CTF学习网站个人汇总Excel表格截图")
    p(
        "学习网站越多，越需要一张自己的资源表。"
        "表格不是为了“证明我收藏了很多”，而是帮助你在需要时快速找到最合适的入口，并知道哪些平台真正用过。"
    )
    table(
        ["资源类型", "可以放什么", "使用目的"],
        [
            ["刷题平台", "西电 CTF 终端、好靶场、picoCTF、BUUCTF、CTFHub", "持续做题与阶段测评"],
            ["知识库", "CTF Wiki、PayloadsAllTheThings、HackTricks", "查概念、查题型、查清单"],
            ["工具与脚本", "GitHub 项目、官方 Release、Python 脚本", "复现、扩展、二次开发"],
            ["赛事信息", "CTFtime、比赛官网、战队公告", "安排比赛与复盘"],
            ["个人资产", "Obsidian、Excel、WP 目录、脚本仓库", "沉淀与检索自己的经验"],
        ],
        [3.0, 9.0, 5.0],
    )
    h3("建议的表格字段")
    bullets(
        [
            "**基础信息**：序号、网站名称、URL、是否收费、资源类型。",
            "**学习状态**：适合阶段、账号、最近使用日期、完成度、是否仍可用。",
            "**个人判断**：一句话评价、最强功能、明显缺点、替代平台。",
            "**下一步**：本周要用的 1—3 个入口，以及具体要完成的题目或章节。",
        ]
    )
    callout(
        "每周做一次资源清理",
        "只保留真正会用的平台；把长期不用的资源移到“归档”；"
        "给最常用的 5 个网站标星。资源表的价值在于减少决策成本，而不是增加整理负担。",
        "blue",
    )

    h2("2.5 初期 30 天训练节奏")
    table(
        ["周次", "重点", "建议产出", "完成标准"],
        [
            ["第 1 周", "工具、HTTP、编码、文件识别", "环境清单 + 5 篇短 WP", "能独立抓包、解码、分析文件"],
            ["第 2 周", "Misc 与 Web 基础题型", "10 道题 + 常用命令表", "能解释每道题的关键线索"],
            ["第 3 周", "按方向集中练习", "10 道题 + 2 个可复用脚本", "同类题不再从零开始"],
            ["第 4 周", "限时小测与复盘", "1 次 2 小时模拟 + 月度总结", "能识别自己的短板并安排下周计划"],
        ],
        [2.5, 5.2, 6.0, 4.3],
    )
    p(
        "不要追求“刷完某个平台”。初期的完成标准是：你能独立打开一个陌生题目，"
        "列出观察点，选择工具，验证假设，并在失败后知道下一步该查什么。"
    )

    pagebreak()
    h1("三、中期：进阶提升与习惯养成")
    lead(
        "从会做几道题，到能在比赛中稳定拿分，中间隔着的不是更多工具，而是可重复的解题流程和高质量复盘。"
        "这一章的两个习惯，会决定你后面成长得多快。"
    )

    h2("3.1 进阶路线：主动挑战困难模式")
    p(
        "困难模式不是一上来就挑全场最难的题，而是持续选择“略高于当前能力、但可以通过查证完成”的题目。"
        "如果一道题你完全看不懂题面，说明缺的是前置知识；如果看得懂但做不出，说明需要练习分析和验证。"
    )
    table(
        ["阶段", "选题策略", "训练目标", "建议退出条件"],
        [
            ["入门期", "有明确提示、单一知识点", "建立完整解题闭环", "独立完成 20—30 道题"],
            ["巩固期", "同方向中等题、少看提示", "形成题型识别与工具组合", "同类题 30 分钟内找到方向"],
            ["突破期", "跨知识点、困难题、比赛真题", "训练拆解、验证和取舍", "能写出可复现的完整 WP"],
            ["比赛期", "限时组队、分工协作", "训练沟通、优先级和心态", "赛后 24 小时内完成复盘"],
        ],
        [2.6, 5.2, 5.6, 4.6],
    )
    bullets(
        [
            "使用 **45/90 分钟规则**：45 分钟没有有效进展就查提示，90 分钟仍卡住就看 WP，但必须复现。",
            "每次只增加一个难度维度：要么换题型，要么加限制，不要同时挑战新领域和新工具。",
            "把“不会”拆成更具体的问题：不会读流量、不会构造请求、不会写脚本，还是不会定位关键代码。",
            "比赛后不要只看排名，统计自己在哪些题型上耗时、在哪些步骤上犹豫。",
        ]
    )

    h2("3.2 核心习惯一：每道题必写 WP")
    p(
        "WP 不是答案誊抄，而是一份“未来自己可以照着复现”的操作手册。"
        "它应该保留你的判断过程，包括错误方向、关键转折和最终验证，而不是只留下最后一条命令。"
        "统一使用 `.md` 格式书写，便于搜索、链接、版本管理和迁移。"
    )
    numbers(
        [
            "题目元信息：平台、赛事、题型、难度、日期、状态。",
            "题面重述：用自己的话写清楚目标、输入、输出和限制。",
            "初始观察：文件类型、请求特征、报错、异常字段、可用工具。",
            "尝试与失败：记录走过的弯路，以及为什么放弃该方向。",
            "最终路径：从线索到利用的完整因果链。",
            "关键命令与脚本：保证可以复制运行，并标注依赖和参数含义。",
            "Flag 与验证：记录结果是否正确，以及如何确认不是猜测。",
            "迁移与防御：同类题如何识别，真实系统中如何修复或检测。",
            "参考资料：官方文档、优秀 WP、工具链接。",
        ]
    )
    code(
        "markdown",
        """
---
title: 题目名称
platform: 平台名称
event: 赛事名称
category: Misc
difficulty: easy
date: 2026-10-21
status: solved
tags: [ctf, misc, encoding]
---

# 题目名称

## 1. 题目信息
- 目标：
- 附件 / 地址：
- 限制条件：

## 2. 初始观察
- 文件类型：
- 关键现象：
- 初步假设：

## 3. 解题过程
1. 
2. 
3. 

## 4. 关键脚本 / 命令
```bash
# 在这里放可复现命令
```

## 5. Flag
`flag{...}`

## 6. 卡点与复盘
- 卡在哪里：
- 为什么卡住：
- 下次如何更快：

## 7. 迁移与防御
- 同类题识别：
- 真实场景中的修复 / 检测：

## 8. 参考资料
- 
""",
    )
    callout(
        "24 小时复现法",
        "解题后的第二天，不看 WP 再过一遍关键步骤。"
        "如果中途卡住，说明 WP 里缺少可复现信息；补完后再尝试一次。",
        "teal",
    )

    h2("3.3 核心习惯二：用 Obsidian 搭建本地知识库")
    p(
        "Obsidian 把笔记保存为本地 Markdown 文件，适合长期积累。"
        "它的双向链接、标签、搜索和图谱能帮助你把“题目”连接成“题型”，再把“题型”连接成“方法论”。"
        "对 CTF 学习者来说，最重要的不是插件数量，而是笔记结构是否让下一次检索更快。"
    )
    h3("推荐目录结构")
    code(
        "text",
        """
CTF-Vault/
├─ 00-Inbox/                 临时收集，每周清空
├─ 01-Platforms/             平台入口与使用说明
├─ 02-Topics/
│  ├─ Misc/
│  ├─ Crypto/
│  ├─ Web/
│  ├─ Pwn/
│  └─ Reverse/
├─ 03-Writeups/              按年份或赛事归档
├─ 04-Templates/             WP、题解、复盘模板
├─ 05-Tools/                 工具配置与命令速查
├─ 06-Scripts/               个人脚本与片段
└─ 07-Review/                周复盘、月总结、比赛复盘
""",
    )
    h3("笔记模板的推荐字段")
    bullets(
        [
            "`category`、`difficulty`、`platform`、`event`、`date`、`status`：用于筛选与统计。",
            "`tags`：既写题型，也写技术点，例如 `web/sqli`、`misc/pcap`、`tool/burp`。",
            "`source`：保留题目链接或附件路径，避免半年后找不到上下文。",
            "`next_review`：安排复现日期，让 WP 真正进入复习流程。",
        ]
    )
    p(
        "只启用自己真正会用的核心插件：模板、反向链接、搜索、标签面板即可起步。"
        "需要统计时再加 Dataview，需要快速录入时再加 QuickAdd。"
        "不要花两天研究主题和图标，却一题没做。"
    )
    callout(
        "三个不要",
        "不要把知识库做成资料回收站；不要把所有内容塞进一篇巨型笔记；不要只收藏不写自己的判断。"
        "每篇笔记至少要有一个“我下次会怎么做”的句子。",
        "orange",
    )

    h2("3.4 每周复盘：把经验变成可复用资产")
    table(
        ["复盘问题", "建议输出"],
        [
            ["本周完成了哪些题？", "题目列表、方向分布、平均耗时"],
            ["哪些题真正独立完成？", "独立 / 提示 / WP 三档标记"],
            ["最常卡在哪一步？", "一个具体短板，不写“太菜”"],
            ["学到了哪个可复用技巧？", "命令、脚本、检查清单或判断规则"],
            ["下周只改哪一件事？", "一个可执行动作，例如“每道 Web 题先画数据流”"],
        ],
        [8.0, 9.0],
    )
    p(
        "每周留 45 分钟做复盘，比再多刷两道题更有价值。"
        "复盘的目标不是评价自己，而是让下一周少走一点重复的弯路。"
    )

    h2("3.5 核心竞争力从哪里来")
    bullets(
        [
            "**流程能力**：面对陌生题，知道先观察什么、再验证什么，而不是随机试 payload。",
            "**检索能力**：能把模糊问题拆成准确关键词，在文档、源码和社区中找到答案。",
            "**验证能力**：不把“看起来像”当成结论，能用日志、回显、调试或对照实验证明。",
            "**表达能力**：能写出别人可复现的 WP，也能把风险讲给非技术同学听。",
            "**边界意识**：知道什么能做、什么不能做，以及何时需要停下来确认授权。",
        ]
    )
    quote("工具会更新，题型会变化；稳定的解题流程和复盘能力，才是你真正带走的东西。")

    h2("3.6 搜索技巧：把“不会”拆成能搜到的问题")
    lead(
        "高手并不是什么都记得，而是知道如何快速找到可靠答案。"
        "搜索能力不是“会复制关键词”，而是把模糊的困惑拆成环境、现象、目标和限制，再用准确的关键词逐步缩小范围。"
    )
    h3("3.6.1 先把问题写成一句可检索的话")
    table(
        ["需要补充的信息", "示例", "为什么重要"],
        [
            ["环境", "Windows 11、Python 3.12、Burp Suite 2025", "避免搜到不同系统或版本的答案"],
            ["操作", "运行 sqlmap 时出现报错", "说明问题发生在哪一步"],
            ["完整现象", "ModuleNotFoundError: No module named 'pkg_resources'", "原始报错比“运行失败”更容易命中"],
            ["预期结果", "希望脚本正常启动并监听 8080", "帮助判断答案是否适用"],
            ["已尝试方案", "已执行 pip install setuptools", "避免重复无效建议"],
        ],
        [3.8, 8.0, 5.0],
    )
    p(
        "一个好搜索词通常包含“产品名 + 版本 + 动作 + 原始报错 + 平台”。"
        "例如，不要搜“Python 用不了”，而应搜 "
        "`Python 3.12 ModuleNotFoundError pkg_resources Windows`。"
    )

    h3("3.6.2 Google 高级搜索语法与百度高级语法")
    p(
        "搜索引擎的高级语法可以显著减少噪音。国外常把这类用法称为 Google Hacking，"
        "在学习场景中，我们只把它当作精准检索工具：限定站点、文件类型、标题和排除词，而不是扫描互联网。"
    )
    table(
        ["语法", "示例", "适合解决的问题"],
        [
            ["双引号", "\"No module named pkg_resources\"", "完整匹配一段报错或固定短语"],
            ["site:", "site:docs.python.org urllib.parse", "只搜索官方文档或指定站点"],
            ["filetype:", "filetype:pdf CTF writeup web", "查找 PDF 教材、讲义或报告"],
            ["intitle:", "intitle:CTF writeup Web", "限定网页标题中的关键词"],
            ["inurl:", "inurl:writeup SQL注入", "查找 URL 中含特定词的页面"],
            ["减号排除", "Python 报错 -csdn -转载", "排除重复或低质量结果"],
            ["组合限定", "site:github.com \"BrokenPipeError\" Python", "在 GitHub 中查找同类报错"],
        ],
        [3.0, 8.0, 6.0],
    )
    p(
        "百度同样支持 `site:`、`filetype:`、引号精确匹配和部分标题限定语法，"
        "但具体支持范围会调整。"
    )
    callout(
        "搜索顺序建议",
        "官方文档 → 官方 Issue / 更新日志 → 高质量社区文章 → 视频教程。"
        "越靠前的来源越接近事实，越靠后的来源越适合建立直觉和补充案例。",
        "blue",
    )

    h3("3.6.3 官方文档应该怎么读")
    numbers(
        [
            "先确认产品、版本和运行环境，避免拿旧版本文档套新版本。",
            "先看 Getting Started / Quickstart，跑通最小示例，再进入 API 和高级配置。",
            "使用文档站内搜索定位函数、参数和错误码，不要从第一页硬读到最后一页。",
            "看到示例代码时，先判断输入、输出和依赖，再复制到隔离环境测试。",
            "把关键命令、版本号和官方链接记进 Obsidian，写成自己的“最小可用笔记”。",
        ]
    )

    h3("3.6.4 在 Stack Overflow 和 GitHub Issues 中找报错")
    p(
        "报错搜索的关键是保留原始信息，同时去掉只属于你本机的路径、用户名、Token 和目标地址。"
        "在 Stack Overflow 中优先看被采纳答案、评论补充和版本说明；在 GitHub Issues 中先看是否已修复、"
        "涉及哪个版本、维护者是否给出临时方案。"
    )
    bullets(
        [
            "**精确报错**：先用双引号包住最关键的一整句错误信息。",
            "**补版本**：把语言、库、操作系统和依赖版本加入搜索词。",
            "**找最小复现**：去掉业务代码，只保留能触发问题的最短示例。",
            "**看时间与状态**：优先阅读近期、仍开放或已合并修复的 Issue。",
            "**保护隐私**：提问前删除 API Key、Cookie、内网 IP、客户名称和真实数据。",
        ]
    )
    code(
        "text",
        """
"ModuleNotFoundError: No module named 'pkg_resources'" setuptools Python 3.12
site:stackoverflow.com "BrokenPipeError" Python requests
site:github.com "<项目名>" issues "Connection refused" version 1.2.3
site:docs.python.org "urllib.parse" query parameters
""",
    )
    callout(
        "搜索结果必须回到证据",
        "一条命令看起来能解决问题，不等于它适合你的环境。"
        "先读它在做什么，再在可回滚的本地环境中验证；涉及下载、提权、关闭安全软件的命令尤其要谨慎。",
        "orange",
    )

    h2("3.7 社区与交流：不要闭门造车")
    p(
        "安全圈的知识更新很快，很多经验不会完整写在教材里。"
        "看雪、先知社区和 FreeBuf 聚集了大量逆向、Web、漏洞分析和实战复盘内容。"
        "读别人的文章、参与开源项目、加入战队，能让你更快知道自己缺什么。"
    )
    table(
        ["社区 / 平台", "适合关注的内容", "新手使用建议"],
        [
            ["看雪", "逆向工程、二进制、移动安全、软件保护", "先读基础专题，再带着具体问题搜索"],
            ["先知社区", "Web 安全、漏洞分析、渗透测试、实战复盘", "重点看复现步骤和修复思路，不只收藏结论"],
            ["FreeBuf", "安全资讯、攻防案例、工具介绍、行业动态", "筛选高质量长文，警惕过时工具和营销内容"],
            ["GitHub", "开源工具、POC、脚本、Issue 讨论", "先读 README 和 Issues，再做最小化验证"],
        ],
        [3.6, 7.4, 7.0],
    )
    h3("参与社区的三条原则")
    bullets(
        [
            "**先自己查，再提问**：贴出环境、目标、已尝试方案和完整报错，节省双方时间。",
            "**参与而不是潜水**：可以从修文档、写工具使用说明、复现公开漏洞开始。",
            "**找战队也要看匹配度**：优先选择愿意复盘、愿意分享、尊重规则的队伍，而不是只看排名。",
            "**公开内容注明来源**：引用文章、脚本和截图时保留作者与链接，不把别人的成果包装成自己的。",
        ]
    )
    h3("高质量提问模板")
    code(
        "text",
        """
【环境】Windows 11 / Python 3.12 / 工具版本
【目标】我想完成什么，最终希望看到什么结果
【操作】我执行了哪些命令，按什么顺序执行
【现象】完整报错、截图或日志，不要只写“失败了”
【已尝试】我查过哪些资料，试过哪些方法，结果如何
【边界】这是公开靶场 / 授权环境 / 个人实验环境
""",
    )
    callout(
        "比赛期间注意信息边界",
        "不要在任何社区公开正在进行的比赛题目、Flag、队伍内部信息或未授权目标数据。"
        "赛后分享 WP 时，也应遵守赛事规则和平台条款。",
        "red",
    )

    pagebreak()
    h1("四、后期：接触渗透测试与应急响应")
    lead(
        "CTF 是受控环境，渗透测试和应急响应面对的是真实业务、真实数据和真实责任。"
        "技术动作可能相似，但目标、约束和交付物完全不同。进入这一阶段，第一课永远是授权与边界。"
    )
    callout(
        "先确认授权，再打开工具",
        "只测试书面授权范围内的资产；不做破坏性操作；不访问与任务无关的数据；"
        "发现高风险问题时先报告，不擅自扩大影响。真实环境没有“重置靶机”按钮。",
        "red",
    )

    h2("4.1 CTF、渗透测试与应急响应的区别")
    table(
        ["维度", "CTF", "渗透测试", "应急响应"],
        [
            ["目标", "拿 Flag、拿分", "验证风险并给出修复建议", "还原事实、控制影响、恢复业务"],
            ["范围", "平台给定题目", "合同与授权范围", "受影响系统与证据边界"],
            ["时间", "通常数小时", "按项目计划", "分秒必争，但仍需保全证据"],
            ["产出", "Flag、WP", "测试报告、风险等级、修复建议", "时间线、IOC、处置报告、复盘"],
            ["核心约束", "比赛规则", "授权、保密、最小影响", "证据链、业务连续性、合规"],
        ],
        [3.0, 4.2, 5.3, 5.3],
    )
    callout(
        "重要提醒：不要把 CTF 成绩等同于真实攻防能力",
        "CTF 更像是一场开卷考试，而真实渗透是一场与真实防御体系的博弈，"
        "你需要补齐网络协议、操作系统底层、甚至社会工程学等海量知识，"
        "切勿产生“CTF 打得好就能随便打穿内网”的错觉。",
        "red",
    )
    p(
        "从 CTF 转向真实场景，需要补上的不是更多“攻击技巧”，而是范围管理、风险评估、"
        "证据意识、沟通能力和报告能力。"
    )

    h2("4.2 PBox：先用集成包跨过环境地狱")
    p(
        "PBox 一类渗透测试集成包把信息收集、WebShell 管理、漏洞扫描、后渗透、抓包代理和隧道工具集中在一起，"
        "适合新手快速建立工具地图，避免在依赖、路径和版本问题上消耗过多时间。"
        "使用时仍要逐项阅读工具说明，知道每个按钮背后实际执行什么命令。"
    )
    numbers(
        [
            "在隔离虚拟机或专用测试环境中使用，先创建快照。",
            "把工具包放在固定目录，避免中文路径、空格和权限问题。",
            "按官方说明启动，不要随意双击来源不明的可执行文件。",
            "每次使用新工具前先看帮助、参数和输出，不把默认配置直接打到目标上。",
            "记录真实命令、目标范围、时间、结果和异常，方便复盘与报告。",
            "任务结束后清理临时文件、关闭监听端口并恢复快照。",
        ]
    )
    callout(
        "集成包不是“外挂”",
        "工具只能放大你的判断，不能替代你的判断。"
        "不知道一条命令会做什么时，先在本地靶场验证，再考虑是否用于授权目标。",
        "orange",
    )

    h2("4.3 Maye Lite：工具管理的关键是“可找到、可解释、可复现”")
    p(
        "工具越装越多，真正的问题会从“没有工具”变成“不知道用哪个版本、参数是什么、上次为什么失败”。"
        "Maye Lite 适合把常用工具统一收纳、分类和快速启动。"
        "建议按任务阶段而不是按软件名称分类，让工具栏和你的工作流一致。"
    )
    code(
        "text",
        """
D:\\Tools\\
├─ 01-Recon\\          信息收集、资产测绘、目录扫描
├─ 02-Web\\            代理、请求重放、Web 漏洞验证
├─ 03-AD\\             域环境与凭据相关工具
├─ 04-Forensics\\      流量、内存、日志、文件分析
├─ 05-Tunnels\\        隧道与代理
├─ 06-Scripts\\        自写脚本与常用片段
├─ 07-Docs\\           帮助文档、版本说明、校验值
└─ _Inbox\\            新工具暂存区，每周整理
""",
    )
    bullets(
        [
            "同一工具只保留一个主版本，旧版本移入归档。",
            "为每个条目写一句用途说明和典型命令，避免“图标认识、用法忘记”。",
            "保留官方下载地址、版本号、哈希值和许可证信息。",
            "定期备份 Maye Lite 配置，换机时能快速恢复工作区。",
            "不把破解工具、来源不明二进制和客户数据混放在同一目录。",
        ]
    )

    h2("4.4 GitHub + Watt Toolkit：获取资源，也要识别风险")
    link("GitHub", "https://github.com/")
    link("Watt Toolkit（瓦特工具箱）", "https://github.com/BeyondDimension/SteamTools")
    p(
        "GitHub 是获取安全工具、POC、脚本和学习资料的重要入口。"
        "国内访问不稳定时，可以使用 Watt Toolkit 进行网络加速；它解决的是访问体验问题，不代表仓库内容自动可信。"
        "下载任何工具前，都要检查项目活跃度、Issue、Release、许可证和代码来源。"
    )
    h3("寻找工具的四步法")
    numbers(
        [
            "明确任务：信息收集、Web 验证、流量分析还是取证，不要先囤工具再找用途。",
            "在 GitHub 搜索关键词，优先查看近期更新、Issue 回复和 Release 说明。",
            "阅读 README、安装方式、依赖和示例，确认它能解决你的具体问题。",
            "在隔离环境运行小样本测试，观察网络连接、文件写入和权限变化。",
        ]
    )
    table(
        ["风险信号", "应该怎么做"],
        [
            ["仓库没有说明、没有提交历史、只有一个陌生二进制", "不要直接运行，先找官方来源或替代项目"],
            ["要求关闭杀毒软件、添加大量白名单", "提高警惕，优先在隔离虚拟机测试"],
            ["安装命令经过多层编码或下载后直接执行", "先解码、阅读并确认下载域名与内容"],
            ["Release 无校验值、无版本说明、长期不更新", "降低信任等级，避免用于真实环境"],
            ["要求输入账号、API Key 或浏览器 Cookie", "确认数据去向，使用最小权限和临时凭据"],
        ],
        [9.0, 8.0],
    )
    callout(
        "加速不等于免检",
        "网络能打开，只说明资源可访问；代码是否可信、是否适合当前任务，仍需要你自己验证。",
        "blue",
    )

    h2("4.5 应急响应：从“找漏洞”切换到“还原事实”")
    p(
        "应急响应的核心不是立刻删除可疑文件，而是先控制影响、保全证据，再通过日志、进程、网络、"
        "持久化和文件痕迹还原攻击链。过早重启、清理或覆盖日志，可能让关键证据永久丢失。"
    )
    numbers(
        [
            "**隔离**：先限制网络连接和横向传播，非必要不要直接关机。",
            "**取证**：记录系统时间、内存、磁盘、关键日志和文件哈希，保持证据链。",
            "**排查**：检查账号、进程、服务、计划任务、启动项、Web 目录和网络连接。",
            "**分析**：围绕初始入口、执行链、持久化、横向移动和数据外传建立时间线。",
            "**处置**：清除恶意对象、修复入口、重置凭据，并验证没有残留。",
            "**恢复**：分批恢复业务，持续监控异常，避免二次入侵。",
            "**报告**：写清事实、证据、影响、处置动作和后续改进，不把猜测写成结论。",
        ]
    )
    p(
        "优秀的应急报告应该让读者看懂：什么时候发生了什么、依据是什么、影响了什么、"
        "做了哪些处置、还剩哪些风险。它考验的是证据组织和表达，而不只是工具熟练度。"
    )

    h2("4.6 学习与授权边界")
    bullets(
        [
            "开始前确认书面范围、时间窗口、允许的技术和禁止的动作。",
            "优先使用本地靶场、公开演练环境和比赛平台。",
            "不对互联网上的随机站点做扫描、爆破、上传或漏洞验证。",
            "不下载、复制或传播与任务无关的个人数据和业务数据。",
            "发现敏感信息时停止扩展，按流程报告并最小化留存。",
            "把“能否解释、能否复现、能否负责”作为使用一项技术前的自检。",
        ]
    )

    pagebreak()
    h1("五、AI 时代的前沿玩法")
    lead(
        "AI 降低了入门门槛，也抬高了区分度。"
        "会问、会验证、会沉淀的人，能把 AI 变成放大器；只会复制答案的人，会得到更多看似正确、实际不可用的结论。"
    )

    h2("5.1 AI 的正确位置：副驾驶，不是代打")
    table(
        ["适合让 AI 做", "不应该直接交给 AI 做"],
        [
            ["解释概念、比较工具、生成检查清单", "替你确认目标是否授权"],
            ["把报错翻译成可验证的假设", "未经阅读就执行生成的命令"],
            ["整理日志、归纳时间线、生成报告初稿", "把 AI 的推测当成证据"],
            ["提供同类题思路和检索关键词", "直接复制 Flag 或提交答案"],
            ["辅助写脚本、补测试和注释", "把敏感数据、密钥或客户信息发给模型"],
        ],
        [8.5, 8.5],
    )
    p(
        "高质量使用 AI 的流程是：先自己观察并描述问题，再让 AI 给出多个假设，"
        "然后选择成本最低的验证方式，最后把结果写回自己的知识库。"
        "AI 负责扩展思路，你负责证据和结论。"
    )

    h2("5.2 Magpie：获取免费 Token，但把成本和密钥管住")
    p(
        "Magpie 这类平台可以帮助学习者获取大模型 Token，用于文档问答、脚本辅助和知识库检索。"
        "具体免费额度、模型列表、调用方式和地区限制会变化，应以平台当前官方规则为准。"
    )
    callout(
        "平台生命周期提示",
        "这类获取免费 Token 的平台生命周期通常不稳定，政策和可用性可能随时变化，"
        "重点掌握调用 API 的逻辑，而不是依赖单一平台。",
        "orange",
    )
    p(
        "下图展示的是 Magpie 的模型路由与 API Key 配置界面。"
        "你真正需要理解的是请求如何被路由到模型、Key 如何鉴权，以及额度与错误响应如何查看，"
        "而不是记住某个平台按钮的位置。"
    )
    image(
        MAGPIE_IMAGE,
        "图5：Magpie 模型路由与 API Key 调用界面（本机示例）",
        16.0,
    )
    numbers(
        [
            "通过官方入口注册，确认服务条款、隐私政策和可用模型。",
            "单独创建一个学习用途的 API Key，不要复用工作或生产密钥。",
            "把密钥放在环境变量或本地密钥管理工具中，不写进 WP、截图和 Git 仓库。",
            "设置预算、调用上限和日志，定期检查异常消耗。",
            "出现泄露迹象时立即撤销并重建密钥。",
            "不要把真实目标数据、客户信息、账号密码或未公开漏洞细节发送给第三方模型。",
        ]
    )
    code(
        "powershell",
        """
# 仅作示例：实际变量名和调用方式以平台文档为准
$env:MAGPIE_API_KEY = "你的临时学习密钥"

# 不要把真实密钥提交到 Git；可在本地 .env 中管理并加入 .gitignore
""",
    )
    callout(
        "免费额度不是无限试错",
        "把 Token 用在“解释、对比、生成验证步骤”上，而不是让模型反复猜 Flag。"
        "先写清问题和已有证据，通常比多调用十次更有效。",
        "teal",
    )

    h2("5.3 用高质量 WP 打造专属 AI Agent")
    lead(
        "你可以把 Agent 想象成一个住在你电脑里的实习生，你提供的 WP 就是给他的《员工手册》，"
        "他学得越像你，帮你解题就越顺手。"
    )
    p(
        "专属 AI Agent 的上限，取决于你的语料质量。"
        "把多年收藏的杂乱题解直接丢给模型，得到的是噪音；把经过结构化整理、能够复现的 WP 变成知识库，"
        "才可能得到真正懂你解题习惯的助手。"
    )
    h3("第一步：把 WP 变成可检索的知识资产")
    bullets(
        [
            "统一 Markdown 结构，补全题型、技术点、工具、环境和结果。",
            "把内容拆成三类卡片：事实卡（概念/命令）、方法卡（流程/判断）、案例卡（具体题目）。",
            "为每篇笔记补充标签和一句话摘要，方便按语义检索。",
            "删除无法复现、来源不明或包含敏感信息的旧笔记。",
        ]
    )
    h3("第二步：先做检索，再考虑微调")
    p(
        "新手不必一开始就训练模型。更实用的路线是“知识库 + 检索 + 强约束提示词”："
        "先把问题分类，检索最相关的 3—5 篇笔记，再让模型基于这些材料给出假设和验证步骤。"
        "当语料足够稳定、评测集足够明确后，再考虑微调或更复杂的 Agent 工作流。"
    )
    code(
        "text",
        """
ctf-agent/
├─ knowledge/
│  ├─ misc/
│  ├─ web/
│  ├─ crypto/
│  ├─ writeups/
│  └─ checklists/
├─ agent/
│  ├─ SKILL.md
│  ├─ prompts/
│  └─ tools/
├─ evals/
│  ├─ questions.jsonl
│  └─ expected/
├─ app.py
└─ README.md
""",
    )
    h3("第三步：写一份有边界的 Skill")
    code(
        "markdown",
        """
---
name: ctf-coach
description: 基于个人 WP 知识库的 CTF 解题教练，负责题型识别、线索整理和验证步骤设计。
---

你是我的 CTF 解题教练，不是自动答题器。

工作流程：
1. 先复述题目目标、输入、限制和已知线索。
2. 判断最可能的 2—3 个方向，并说明依据。
3. 从知识库检索相似案例，列出可复用的方法，而不是直接给最终答案。
4. 为每个假设设计最小验证步骤，明确预期现象。
5. 如果证据不足，明确说“不确定”，并给出下一步查证建议。

安全边界：
- 只讨论公开靶场、比赛题目或已授权环境。
- 不生成针对未授权真实目标的攻击步骤。
- 不编造命令输出、文件内容或 Flag。
- 涉及高风险操作时，先解释影响并要求人工确认。

输出格式：
- 已知事实
- 可能方向与依据
- 下一步验证
- 可用命令 / 脚本
- 需要记录的 WP 要点
""",
    )
    h3("第四步：建立评测集，防止“感觉很好用”")
    bullets(
        [
            "准备 30—50 道你已知答案的题，覆盖不同方向和难度。",
            "为每次回答设置指标：方向是否正确、步骤是否可执行、是否编造、是否遵守边界。",
            "每周固定回归测试，记录模型升级或提示词修改后的变化。",
            "把人工修正反馈写回知识库，而不是只改一次对话。",
        ]
    )
    callout(
        "幻觉检查三连",
        "这条命令在我的环境里存在吗？它的每个参数会产生什么影响？"
        "我能否在一个可重置的靶场中先验证？三个问题答不上来，就不要直接执行。",
        "red",
    )

    h2("5.4 AI 时代真正的技术护城河")
    bullets(
        [
            "**问题定义**：把模糊的“帮我看看”拆成可验证的问题，是 AI 无法替代的起点。",
            "**证据意识**：能区分现象、假设和结论，知道用什么实验证明。",
            "**知识资产**：拥有结构化、可检索、可持续更新的个人语料，而不是临时搜索结果。",
            "**工具编排**：知道何时用脚本、何时用现成工具、何时应该手工分析。",
            "**安全判断**：能识别越权、破坏、隐私和供应链风险，并为自己的操作负责。",
            "**表达与协作**：能把复杂问题讲清楚，让队友、客户和管理者做出正确决策。",
        ]
    )
    p(
        "AI 会越来越擅长给出“平均答案”，但真实问题往往缺数据、缺上下文、充满矛盾。"
        "你的优势来自更敏锐的观察、更可靠的验证和更长期的积累。"
    )

    h2("5.5 12 周行动清单")
    table(
        ["周期", "重点任务", "阶段产出"],
        [
            ["第 1—2 周", "工具环境、HTTP、编码、文件分析、Obsidian", "环境清单 + 5 篇 WP"],
            ["第 3—4 周", "Misc 与 Web 入门题", "20 道题 + 常用命令表"],
            ["第 5—6 周", "WP 模板、周复盘、同题型归纳", "个人 WP 知识库 v1"],
            ["第 7—8 周", "中等题、限时训练、参加一次比赛", "比赛复盘 + 短板清单"],
            ["第 9—10 周", "授权靶场、渗透流程、应急响应基础", "一份模拟测试 / 应急报告"],
            ["第 11—12 周", "Magpie、个人 AI Agent、评测集", "可检索的 CTF 助手 v1"],
        ],
        [3.0, 8.5, 6.0],
    )
    callout(
        "今天就开始",
        "注册一个靶场，完成一道最简单的题，写下一篇三行 WP。"
        "30 天后你不会突然成为高手，但会拥有一个可以继续迭代的系统。",
        "orange",
    )
    p(
        "最后请记住：CTF 的终点不是某个排行榜，也不是收集多少工具，而是你能否面对一个陌生问题，"
        "保持好奇、守住边界、提出假设、验证事实，并把经验留给下一次的自己。"
    )
    quote("从第一道 Flag 开始，但不要只停在 Flag。")


def set_run_font(run, name=FONT_CN, size=None, bold=None, color=None):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)


def set_paragraph_spacing(paragraph, before=0, after=6, line=1.5):
    fmt = paragraph.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    fmt.line_spacing = line


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=100, start=120, bottom=100, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_cell_border(cell, color=BORDER, size=4, left_color=None, left_size=None):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    specs = {
        "top": (color, size),
        "left": (left_color or color, left_size or size),
        "bottom": (color, size),
        "right": (color, size),
        "insideH": (color, size),
        "insideV": (color, size),
    }
    for edge, (edge_color, edge_size) in specs.items():
        tag = borders.find(qn(f"w:{edge}"))
        if tag is None:
            tag = OxmlElement(f"w:{edge}")
            borders.append(tag)
        tag.set(qn("w:val"), "single")
        tag.set(qn("w:sz"), str(edge_size))
        tag.set(qn("w:space"), "0")
        tag.set(qn("w:color"), edge_color)


def set_row_cant_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    if tr_pr.find(qn("w:cantSplit")) is None:
        tr_pr.append(OxmlElement("w:cantSplit"))


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    if tr_pr.find(qn("w:tblHeader")) is None:
        header = OxmlElement("w:tblHeader")
        header.set(qn("w:val"), "true")
        tr_pr.append(header)


def add_hyperlink(paragraph, text, url, color=TEAL, font=FONT_CN, size=10.5, bold=False):
    part = paragraph.part
    relationship_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), relationship_id)
    new_run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    color_node = OxmlElement("w:color")
    color_node.set(qn("w:val"), color)
    r_pr.append(color_node)
    if bold:
        r_pr.append(OxmlElement("w:b"))
    size_node = OxmlElement("w:sz")
    size_node.set(qn("w:val"), str(int(size * 2)))
    r_pr.append(size_node)
    size_cs = OxmlElement("w:szCs")
    size_cs.set(qn("w:val"), str(int(size * 2)))
    r_pr.append(size_cs)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    r_pr.append(underline)
    r_fonts = OxmlElement("w:rFonts")
    r_fonts.set(qn("w:ascii"), font)
    r_fonts.set(qn("w:hAnsi"), font)
    r_fonts.set(qn("w:eastAsia"), font)
    r_pr.append(r_fonts)
    new_run.append(r_pr)
    text_node = OxmlElement("w:t")
    text_node.text = text
    new_run.append(text_node)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def add_field(paragraph, instruction):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.append(begin)
    run._r.append(instr)
    run._r.append(separate)
    run._r.append(end)
    return run


def add_rich_text(paragraph, text, size=10.5, color=TEXT, bold=False):
    parts = re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            set_run_font(run, FONT_BODY, size, True, color)
        elif part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            set_run_font(run, FONT_CODE, max(size - 0.5, 8.5), bold, ORANGE)
        else:
            run = paragraph.add_run(part)
            set_run_font(run, FONT_BODY, size, bold, color)


def add_para(doc, text, style=None, size=10.5, color=TEXT, align=None, before=0, after=6, indent_first=True):
    paragraph = doc.add_paragraph(style=style)
    if align is not None:
        paragraph.alignment = align
    set_paragraph_spacing(paragraph, before, after, 1.5)
    if indent_first and style is None:
        paragraph.paragraph_format.first_line_indent = Pt(21)
    add_rich_text(paragraph, text, size, color)
    return paragraph


def style_document(doc):
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.3)
    section.bottom_margin = Cm(2.2)
    section.left_margin = Cm(2.4)
    section.right_margin = Cm(2.3)
    section.header_distance = Cm(1.0)
    section.footer_distance = Cm(1.0)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = FONT_BODY
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_BODY)
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor.from_string(TEXT)
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_after = Pt(6)

    h1_style = styles["Heading 1"]
    h1_style.font.name = FONT_CN
    h1_style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_CN)
    h1_style.font.size = Pt(20)
    h1_style.font.bold = True
    h1_style.font.color.rgb = RGBColor.from_string(NAVY)
    h1_style.paragraph_format.space_before = Pt(10)
    h1_style.paragraph_format.space_after = Pt(14)
    h1_style.paragraph_format.keep_with_next = True

    h2_style = styles["Heading 2"]
    h2_style.font.name = FONT_CN
    h2_style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_CN)
    h2_style.font.size = Pt(14.5)
    h2_style.font.bold = True
    h2_style.font.color.rgb = RGBColor.from_string(TEAL)
    h2_style.paragraph_format.space_before = Pt(14)
    h2_style.paragraph_format.space_after = Pt(7)
    h2_style.paragraph_format.keep_with_next = True

    h3_style = styles["Heading 3"]
    h3_style.font.name = FONT_CN
    h3_style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_CN)
    h3_style.font.size = Pt(11.5)
    h3_style.font.bold = True
    h3_style.font.color.rgb = RGBColor.from_string(ORANGE)
    h3_style.paragraph_format.space_before = Pt(9)
    h3_style.paragraph_format.space_after = Pt(4)
    h3_style.paragraph_format.keep_with_next = True

    for style_name in ("List Bullet", "List Number"):
        style = styles[style_name]
        style.font.name = FONT_BODY
        style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_BODY)
        style.font.size = Pt(10.5)
        style.paragraph_format.line_spacing = 1.4
        style.paragraph_format.space_after = Pt(4)

    for style_name, indent, size in (("TOC 1", 0.0, 10.2), ("TOC 2", 0.8, 9.4)):
        try:
            toc_style = styles[style_name]
        except KeyError:
            toc_style = styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
            toc_style.base_style = styles["Normal"]
        toc_style.font.name = FONT_CN
        toc_style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_CN)
        toc_style.font.size = Pt(size)
        toc_style.font.color.rgb = RGBColor.from_string(TEXT)
        toc_style.paragraph_format.left_indent = Cm(indent)
        toc_style.paragraph_format.space_before = Pt(3 if style_name == "TOC 1" else 0)
        toc_style.paragraph_format.space_after = Pt(2 if style_name == "TOC 1" else 1)
        toc_style.paragraph_format.line_spacing = 1.05


def add_header_footer(doc):
    section = doc.sections[0]
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_paragraph_spacing(hp, 0, 0, 1.0)
    run = hp.add_run("网络安全与 CTF 新手起步指南（精修版）")
    set_run_font(run, FONT_CN, 8.5, False, MUTED)
    hp.add_run("\t")
    run2 = hp.add_run("LEARN · PRACTICE · REVIEW")
    set_run_font(run2, FONT_CODE, 8, False, MUTED)
    hp.paragraph_format.tab_stops.add_tab_stop(Cm(15.9), alignment=2)
    bottom = OxmlElement("w:pBdr")
    bottom_line = OxmlElement("w:bottom")
    bottom_line.set(qn("w:val"), "single")
    bottom_line.set(qn("w:sz"), "4")
    bottom_line.set(qn("w:space"), "4")
    bottom_line.set(qn("w:color"), BORDER)
    bottom.append(bottom_line)
    hp._p.get_or_add_pPr().append(bottom)

    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(fp, 0, 0, 1.0)
    run = fp.add_run("第 ")
    set_run_font(run, FONT_CN, 8.5, False, MUTED)
    page_run = add_field(fp, "PAGE")
    set_run_font(page_run, FONT_CN, 8.5, False, MUTED)
    run = fp.add_run(" 页")
    set_run_font(run, FONT_CN, 8.5, False, MUTED)


def add_cover(doc):
    top_table = doc.add_table(rows=1, cols=1)
    top_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = top_table.cell(0, 0)
    set_cell_shading(cell, NAVY)
    set_cell_margins(cell, top=140, start=180, bottom=140, end=180)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run("BEGINNER TO BUILDER  /  2026")
    set_run_font(run, FONT_CODE, 9, True, WHITE)

    spacer = doc.add_paragraph()
    set_paragraph_spacing(spacer, 0, 0, 1.0)
    spacer.paragraph_format.space_before = Pt(44)

    label = doc.add_paragraph()
    label.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_paragraph_spacing(label, 0, 10, 1.0)
    run = label.add_run("零基础 · 可执行 · 长期主义 · 精修版")
    set_run_font(run, FONT_CN, 11, True, TEAL)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_paragraph_spacing(title, 0, 6, 1.12)
    run = title.add_run("网络安全与 CTF")
    set_run_font(run, FONT_CN, 31, True, NAVY)

    title2 = doc.add_paragraph()
    title2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_paragraph_spacing(title2, 0, 18, 1.12)
    run = title2.add_run("新手起步指南")
    set_run_font(run, FONT_CN, 31, True, NAVY)

    subtitle = doc.add_paragraph()
    set_paragraph_spacing(subtitle, 0, 30, 1.5)
    run = subtitle.add_run("从第一道 Flag，到 AI 时代的技术护城河")
    set_run_font(run, FONT_BODY, 14, False, TEXT)

    line = doc.add_paragraph()
    set_paragraph_spacing(line, 0, 24, 1.0)
    p_pr = line._p.get_or_add_pPr()
    border = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "16")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), ORANGE)
    border.append(bottom)
    p_pr.append(border)

    info = doc.add_table(rows=3, cols=2)
    info.alignment = WD_TABLE_ALIGNMENT.LEFT
    info.autofit = False
    rows = [
        ("适用人群", "零基础 / 转专业 / 刚进战队的新同学"),
        ("建议周期", "8—12 周完成第一轮学习闭环"),
        ("学习原则", "合法授权 · 动手优先 · 每题复盘 · 长期复利"),
    ]
    for idx, (key, value) in enumerate(rows):
        c1, c2 = info.rows[idx].cells
        c1.width = Cm(3.0)
        c2.width = Cm(12.0)
        for c in (c1, c2):
            set_cell_margins(c, top=80, start=0, bottom=80, end=120)
            set_cell_border(c, color=WHITE, size=0)
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p1 = c1.paragraphs[0]
        set_paragraph_spacing(p1, 0, 0, 1.1)
        r1 = p1.add_run(key)
        set_run_font(r1, FONT_CN, 9.5, True, MUTED)
        p2 = c2.paragraphs[0]
        set_paragraph_spacing(p2, 0, 0, 1.1)
        r2 = p2.add_run(value)
        set_run_font(r2, FONT_CN, 10.5, False, TEXT)

    spacer2 = doc.add_paragraph()
    set_paragraph_spacing(spacer2, 0, 0, 1.0)
    spacer2.paragraph_format.space_before = Pt(45)
    note = doc.add_paragraph()
    set_paragraph_spacing(note, 0, 0, 1.2)
    run = note.add_run("版本 2026.10  ·  本地学习资料  ·  请仅用于合法授权环境")
    set_run_font(run, FONT_CN, 9, False, MUTED)

    doc.add_page_break()


def add_toc(doc):
    h = doc.add_paragraph()
    set_paragraph_spacing(h, 0, 12, 1.1)
    run = h.add_run("目录")
    set_run_font(run, FONT_CN, 20, True, NAVY)

    note = doc.add_paragraph()
    set_paragraph_spacing(note, 0, 8, 1.2)
    run = note.add_run("提示：在 Word 中右键目录并选择“更新域”，可刷新页码。")
    set_run_font(run, FONT_CN, 9, False, MUTED)

    toc_p = doc.add_paragraph()
    set_paragraph_spacing(toc_p, 0, 0, 1.3)
    add_field(toc_p, 'TOC \\o "1-2" \\h \\z \\u')
    doc.add_page_break()


def add_quote(doc, text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_row_cant_split(tbl.rows[0])
    set_cell_shading(cell, LIGHT_TEAL)
    set_cell_margins(cell, top=150, start=220, bottom=150, end=220)
    set_cell_border(cell, color=LIGHT_TEAL, size=0, left_color=TEAL, left_size=24)
    para = cell.paragraphs[0]
    set_paragraph_spacing(para, 0, 0, 1.4)
    run = para.add_run("“")
    set_run_font(run, FONT_BODY, 18, True, TEAL)
    run = para.add_run(text)
    set_run_font(run, FONT_BODY, 10.5, False, TEXT)
    run = para.add_run("”")
    set_run_font(run, FONT_BODY, 18, True, TEAL)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_callout(doc, title, text, tone="blue"):
    palette = {
        "blue": (LIGHT_BLUE, NAVY, "TIPS"),
        "teal": (LIGHT_TEAL, TEAL, "KEY"),
        "orange": (LIGHT_ORANGE, ORANGE, "NOTE"),
        "red": (LIGHT_RED, RED, "WARNING"),
    }
    fill, accent, label = palette.get(tone, palette["blue"])
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_row_cant_split(tbl.rows[0])
    set_cell_shading(cell, fill)
    set_cell_margins(cell, top=150, start=220, bottom=150, end=220)
    set_cell_border(cell, color=fill, size=0, left_color=accent, left_size=24)

    label_p = cell.paragraphs[0]
    set_paragraph_spacing(label_p, 0, 3, 1.0)
    run = label_p.add_run(f"{label}  /  {title}")
    set_run_font(run, FONT_CN, 9.5, True, accent)

    text_p = cell.add_paragraph()
    set_paragraph_spacing(text_p, 0, 0, 1.4)
    run = text_p.add_run(text)
    set_run_font(run, FONT_BODY, 10, False, TEXT)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_placeholder(doc, label, description):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_row_cant_split(tbl.rows[0])
    set_cell_shading(cell, LIGHT_GRAY)
    set_cell_margins(cell, top=220, start=220, bottom=220, end=220)
    set_cell_border(cell, color="9AA8B2", size=8)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(p, 0, 0, 1.3)
    run = p.add_run(f"【{label}：{description}】")
    set_run_font(run, FONT_CN, 10.5, True, NAVY)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_image_block(doc, image_path, caption, width_cm=16.0):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(paragraph, 6, 4, 1.0)
    paragraph.paragraph_format.keep_with_next = True
    run = paragraph.add_run()
    run.add_picture(image_path, width=Cm(width_cm))

    caption_p = doc.add_paragraph()
    caption_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(caption_p, 0, 10, 1.2)
    caption_run = caption_p.add_run(caption)
    set_run_font(caption_run, FONT_CN, 9, False, MUTED)


def add_code_block(doc, language, text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_row_cant_split(tbl.rows[0])
    set_cell_shading(cell, "F6F8FA")
    set_cell_margins(cell, top=140, start=180, bottom=140, end=180)
    set_cell_border(cell, color="D8DEE4", size=4)
    p = cell.paragraphs[0]
    set_paragraph_spacing(p, 0, 0, 1.05)
    if language:
        run = p.add_run(f"{language}\n")
        set_run_font(run, FONT_CODE, 8, True, MUTED)
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        run = p.add_run(line)
        set_run_font(run, FONT_CODE, 8.5, False, TEXT)
        if idx != len(lines) - 1:
            run.add_break(WD_BREAK.LINE)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_table(doc, headers, rows, widths=None):
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.style = "Table Grid"
    set_row_cant_split(tbl.rows[0])
    set_repeat_table_header(tbl.rows[0])
    hdr = tbl.rows[0].cells
    for idx, text in enumerate(headers):
        cell = hdr[idx]
        set_cell_shading(cell, NAVY)
        set_cell_margins(cell, top=90, start=100, bottom=90, end=100)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(para, 0, 0, 1.1)
        run = para.add_run(text)
        set_run_font(run, FONT_CN, 9, True, WHITE)
        if widths:
            cell.width = Cm(widths[idx])

    for row_idx, row in enumerate(rows):
        new_row = tbl.add_row()
        set_row_cant_split(new_row)
        cells = new_row.cells
        for col_idx, text in enumerate(row):
            cell = cells[col_idx]
            if row_idx % 2 == 1:
                set_cell_shading(cell, "F7F9FA")
            set_cell_margins(cell, top=85, start=100, bottom=85, end=100)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            para = cell.paragraphs[0]
            set_paragraph_spacing(para, 0, 0, 1.25)
            add_rich_text(para, text, 9.2, TEXT)
            if widths:
                cell.width = Cm(widths[col_idx])

    # Keep short tables together; Word may still split if a table is taller than a page.
    for row in tbl.rows[:-1]:
        for cell in row.cells:
            for para in cell.paragraphs:
                para.paragraph_format.keep_with_next = True
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def render_docx():
    doc = Document()
    doc.core_properties.title = "网络安全与 CTF 新手起步指南（精修版）"
    doc.core_properties.subject = "零基础网络安全与 CTF 学习路线"
    doc.core_properties.author = "网络安全学习资料"
    doc.core_properties.keywords = "网络安全, CTF, Misc, Web, Crypto, Pwn, Reverse, 渗透测试, 应急响应, AI Agent"
    doc.core_properties.comments = "面向零基础学习者的本地学习指南精修版。"

    style_document(doc)
    add_header_footer(doc)
    add_cover(doc)
    add_toc(doc)

    for block_index, block in enumerate(BLOCKS):
        kind = block[0]
        if kind == "h1":
            para = doc.add_heading(level=1)
            run = para.add_run(block[1])
            set_run_font(run, FONT_CN, 20, True, NAVY)
        elif kind == "h2":
            para = doc.add_heading(level=2)
            run = para.add_run(block[1])
            set_run_font(run, FONT_CN, 14.5, True, TEAL)
        elif kind == "h3":
            para = doc.add_heading(level=3)
            run = para.add_run(block[1])
            set_run_font(run, FONT_CN, 11.5, True, ORANGE)
        elif kind == "p":
            paragraph = add_para(doc, block[1])
            next_kind = BLOCKS[block_index + 1][0] if block_index + 1 < len(BLOCKS) else None
            if next_kind == "image":
                paragraph.paragraph_format.keep_with_next = True
        elif kind == "lead":
            add_para(doc, block[1], size=11.5, color=NAVY, after=10, indent_first=False)
        elif kind == "quote":
            add_quote(doc, block[1])
        elif kind == "bullets":
            for item in block[1]:
                para = doc.add_paragraph(style="List Bullet")
                set_paragraph_spacing(para, 0, 4, 1.4)
                add_rich_text(para, item)
        elif kind == "numbers":
            for idx, item in enumerate(block[1], 1):
                para = doc.add_paragraph()
                set_paragraph_spacing(para, 0, 4, 1.4)
                para.paragraph_format.left_indent = Cm(0.72)
                para.paragraph_format.first_line_indent = Cm(-0.58)
                number_run = para.add_run(f"{idx}. ")
                set_run_font(number_run, FONT_CODE, 10, True, ORANGE)
                add_rich_text(para, item)
        elif kind == "code":
            add_code_block(doc, block[1], block[2])
        elif kind == "placeholder":
            add_placeholder(doc, block[1], block[2])
        elif kind == "image":
            add_image_block(doc, block[1], block[2], block[3])
        elif kind == "callout":
            add_callout(doc, block[1], block[2], block[3])
        elif kind == "table":
            add_table(doc, block[1], block[2], block[3])
        elif kind == "link":
            para = doc.add_paragraph()
            set_paragraph_spacing(para, 0, 4, 1.3)
            run = para.add_run("链接  ")
            set_run_font(run, FONT_CN, 9.5, True, MUTED)
            add_hyperlink(para, block[1], block[2])
            run = para.add_run(f"  {block[2]}")
            set_run_font(run, FONT_CODE, 8.5, False, MUTED)
        elif kind == "pagebreak":
            doc.add_page_break()
        else:
            raise ValueError(f"Unknown block type: {kind}")

    doc.save(DOCX_PATH)


def postprocess_hyperlinks(path=DOCX_PATH):
    """Restore clickable URL text after Word has updated the TOC field."""
    doc = Document(path)
    restored = 0
    for paragraph in doc.paragraphs:
        if paragraph._p.find(qn("w:hyperlink")) is not None:
            continue
        match = re.search(r"https?://[^\s]+", paragraph.text)
        if not match:
            continue
        url = match.group(0).rstrip(".,;，。；")
        target_run = None
        for run in reversed(paragraph.runs):
            if url in run.text:
                target_run = run
                break
        if target_run is None:
            continue
        prefix, _, suffix = target_run.text.partition(url)
        if suffix.strip():
            continue
        target_run.text = prefix
        add_hyperlink(
            paragraph,
            url,
            url,
            color=MUTED,
            font=FONT_CODE,
            size=8.5,
        )
        restored += 1
    if restored:
        doc.save(path)
    print(f"HYPERLINKS_RESTORED={restored}")
    return restored


def markdown_escape_table(text):
    return str(text).replace("|", "\\|").replace("\n", "<br>")


def render_markdown():
    lines = [
        "---",
        "title: 网络安全与 CTF 新手起步指南（精修版）",
        "subtitle: 从第一道 Flag，到 AI 时代的技术护城河",
        f"date: {date.today().isoformat()}",
        "tags: [网络安全, CTF, 新手, 学习路线, AI]",
        "---",
        "",
        "# 网络安全与 CTF 新手起步指南（精修版）",
        "",
        "> 面向零基础学习者的本地学习资料。请仅在合法授权环境中练习。",
        "",
        "## 目录",
        "",
        "> 提示：Word 版本使用自动生成目录；打开 Word 后右键目录并选择“更新域”可刷新页码。",
        "",
        "1. [写在前面](#写在前面这份指南怎么用)",
        "2. [一、引言：新手如何破局](#一引言新手如何破局)",
        "3. [二、初期：零基础小白的起步路线与靶场](#二初期零基础小白的起步路线与靶场)",
        "4. [三、中期：进阶提升与习惯养成](#三中期进阶提升与习惯养成)",
        "5. [四、后期：接触渗透测试与应急响应](#四后期接触渗透测试与应急响应)",
        "6. [五、AI 时代的前沿玩法](#五ai-时代的前沿玩法)",
        "",
    ]
    for block in BLOCKS:
        kind = block[0]
        if kind == "h1":
            lines.extend([f"# {block[1]}", ""])
        elif kind == "h2":
            lines.extend([f"## {block[1]}", ""])
        elif kind == "h3":
            lines.extend([f"### {block[1]}", ""])
        elif kind in ("p", "lead"):
            lines.extend([block[1], ""])
        elif kind == "quote":
            lines.extend([f"> {block[1]}", ""])
        elif kind == "bullets":
            lines.extend([f"- {item}" for item in block[1]])
            lines.append("")
        elif kind == "numbers":
            lines.extend([f"{idx}. {item}" for idx, item in enumerate(block[1], 1)])
            lines.append("")
        elif kind == "code":
            lines.extend([f"```{block[1]}", block[2], "```", ""])
        elif kind == "placeholder":
            lines.extend([f"【{block[1]}：{block[2]}】", ""])
        elif kind == "image":
            relative_path = os.path.relpath(block[1], OUTPUT_DIR).replace("\\", "/")
            lines.extend([f"![{block[2]}](<{relative_path}>)", "", f"*{block[2]}*", ""])
        elif kind == "callout":
            lines.extend([f"> **{block[1]}**", f"> {block[2]}", ""])
        elif kind == "table":
            headers, rows, _ = block[1], block[2], block[3]
            lines.append("| " + " | ".join(markdown_escape_table(h) for h in headers) + " |")
            lines.append("| " + " | ".join("---" for _ in headers) + " |")
            for row in rows:
                lines.append("| " + " | ".join(markdown_escape_table(c) for c in row) + " |")
            lines.append("")
        elif kind == "link":
            lines.extend([f"[{block[1]}]({block[2]})", ""])
        elif kind == "pagebreak":
            lines.extend(["---", ""])
        else:
            raise ValueError(f"Unknown block type: {kind}")
    with open(MD_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    build_content()
    render_markdown()
    render_docx()
    postprocess_hyperlinks()
    print(f"MARKDOWN={MD_PATH}")
    print(f"DOCX={DOCX_PATH}")


if __name__ == "__main__":
    if "--restore-links-only" in sys.argv:
        postprocess_hyperlinks()
    else:
        main()
