# 网络安全学习笔记

信息安全专业的学习笔记与 CTF writeup，全部为 Markdown，可在 Obsidian 或直接在 GitHub 上阅读。

> 仓库内容全部来自**公开 CTF 比赛和公开靶场**的练习记录，以及通用的 Web 安全知识整理，不包含任何真实目标的资产或凭据信息。

## 目录

| 目录 | 内容 |
| --- | --- |
| `ctf-writeups/` | CTF 比赛题解 |
| `ctf-writeups/competition-plan/` | 2026 京津冀大学生信息安全网络攻防大赛决赛备赛方案 |
| `web-security/` | Web 漏洞原理与利用的学习笔记 |
| `pentest/` | 公开靶场的内网渗透 writeup |
| `attachments/` | 笔记中引用的图片 |

## CTF 题解

按知识点整理，覆盖 Web 方向常见题型：

| 题目 | 考点 |
| --- | --- |
| `8.一个文件上传漏洞` | `.user.ini` 配合图片马绕过上传限制 |
| `9.非常经典的 php 无参数 RCE 绕过` | 无参数远程代码执行 |
| `12/14.TGCTF2025 文件上传 + 反序列化` | 伪装上传 + PHP 反序列化链 |
| `13.SSRF（服务端请求伪造）` | 内网探测、协议利用与组合攻击 |
| `15.PHP 协议与编码 压缩绕过` | php://filter 链与编码绕过 |
| `16.SQL 注入题目` | `into outfile` / `dumpfile` 写入限制分析 |
| `18.eval（命令注入）` | 命令注入回显利用 |
| `19.fastjson` | WAF 绕过 + JNDI 远程类加载 RCE |
| `3.条件竞争解法` | 文件上传条件竞争 |

## Web 安全学习笔记

覆盖 XXE、SSTI、PHP / Java 反序列化（含 POP 链）、SQL 注入、原型污染、文件包含、文件上传、WAF 绕过、内网横向、应急响应等主题，另有 Wireshark、dirsearch、hashcat、蚁剑等工具的使用记录。

## 靶场渗透 writeup

- `1.bug库渗透测试1 wp` — Docker 靶场，外网打点 → 权限提升 → 内网横向，11/11 FLAG
- `2.bug库渗透测试2`
- `3.LingJing 的 vulntarget-b`

## 关于脱敏

- 所有目标地址均为 CTF 比赛 / 靶场的一次性临时环境，**公网 IP 已统一替换为 RFC 5737 文档地址段 `203.0.113.0/24`**，无法用于复现或攻击。
- 笔记中的账号口令均为靶场内预置的演示凭证。

