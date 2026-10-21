# 网络安全与 CTF 新手起步指南（精修版）

一份面向零基础学习者的网络安全与 CTF 入门路线，内容覆盖五大方向、靶场选择、Writeup 与 Obsidian 知识库、搜索技巧、安全社区、授权渗透、应急响应以及 AI Agent。

> 本文档仅用于公开靶场、比赛环境和个人实验环境中的合法学习。

## 文件说明

| 文件 | 说明 |
| --- | --- |
| [Word 精修版](<./网络安全与CTF新手起步指南_精修版.docx>) | 已排版、含自动目录和插图的最终版本 |
| [Markdown 全文](<./网络安全与CTF新手起步指南_精修版.md>) | 可编辑、便于检索和二次整理的全文 |
| [生成脚本](./generate_ctf_guide_refined_docx.py) | 使用 `python-docx` 生成 Word 的完整代码 |
| [Magpie 截图](./assets/magpie-route.png) | Markdown 中第 5.2 节引用的界面截图 |

## 主要内容

- CTF 五大核心方向：Misc、Crypto、Web、Pwn、Reverse
- 西电 CTF 终端、CyLab Security Academy、好靶场的起步路线
- 每道题写 WP、用 Obsidian 搭建个人知识库
- 高效搜索、官方文档阅读、Stack Overflow 与 GitHub Issues 检索
- 看雪、先知社区、FreeBuf 等安全社区与交流方法
- PBox、Maye Lite、GitHub 与 Watt Toolkit 的工具管理
- 渗透测试、应急响应的边界和认知纠偏
- Magpie Token 使用、个人 AI Agent 与 Skill 构建思路

## 重新生成 Word

生成脚本默认输出到作者本机的 Obsidian 目录。迁移到其他电脑时，先修改脚本顶部的 `OUTPUT_DIR`：

```python
OUTPUT_DIR = r"D:\你的目标目录"
```

然后使用已安装 `python-docx` 的 Python 环境运行：

```powershell
python generate_ctf_guide_refined_docx.py
```

脚本会同时生成 Markdown 和 Word；Word 目录打开后可按提示更新域以刷新页码。
