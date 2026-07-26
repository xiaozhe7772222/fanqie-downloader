---
name: fanqie_downloader
description: 番茄小说搜索·状态查询·下载 — 全安卓端三合一工具，Skill 版内置搜索、查状态、下载、榜单浏览
version: 1.1
author: @小哲
dependencies:
  - requests
  - beautifulsoup4
  - tqdm
  - gmssl
---

# 🍅 番茄小说搜索 · 状态 · 下载（Skill 版）

## 给 AI 的指令

**本 Skill 提供番茄小说的搜索、状态查询、下载功能。**
**AI 必须通过终端执行 `fanqie_txt.py` 脚本来完成操作，不支持 package_proxy 方式调用。**

## 可用命令

```bash
# 搜索小说（返回 JSON）
python3 fanqie_txt.py --search <关键词>

# 查看书籍详情（返回 JSON，含字数/状态/在读/分类/简介）
python3 fanqie_txt.py --check <book_id>

# 下载小说（保存到配置的路径）
python3 fanqie_txt.py --book_id <book_id>

# 交互式菜单（搜索/榜单/批量/工具箱/设置）
python3 fanqie_txt.py
```

## 执行位置

**脚本路径：`/sdcard/Download/Operit/skills/fanqie_downloader/fanqie_txt.py`**
**依赖文件：`abogus.py`（必须与 fanqie_txt.py 在同一目录）**

**执行方式：**
```bash
cd /sdcard/Download/Operit/skills/fanqie_downloader && python3 fanqie_txt.py --search 关键词
```

## 功能说明

| 功能 | 命令 | 说明 |
|:---|:---|:---|
| 🔍 搜索 | `--search` | 搜索番茄小说，返回JSON（书名、作者、book_id、字数） |
| ℹ️ 状态 | `--check` | 查看书籍详情，返回JSON（字数、连载状态、在读、分类、简介） |
| 📥 下载 | `--book_id` | 多线程并发下载，自动解密，保存为TXT |
| 📊 榜单 | 交互菜单 `ph` | 浏览男频/女频各类榜单 |
| 📂 路径 | 交互菜单 `s` | 设置中可切换保存路径，默认 `/storage/emulated/0/番茄小说下载/` |

## 默认保存路径

**默认：`/storage/emulated/0/番茄小说下载/`**
**可在设置中切换为任意可写目录（如 `/storage/emulated/0/Podcasts/` 等）。**

## 技术说明

- 番茄小说搜索 API 返回的字符经过自定义加密，脚本内置了解密引擎（已修复 370/372 个映射）
- 搜索功能需要 `abogus.py` 模块生成 a_bogus 参数绕过反爬
- 下载采用多线程并发，支持断点续传
- 章节内容通过 `__INITIAL_STATE__` 提取并自动解密

## 注意事项

**本项目基于 MIT 协议开源，仅供学习交流。**
**请尊重番茄小说的版权，仅用于个人离线阅读。**
**首次使用前需要安装依赖：`pip install requests beautifulsoup4 tqdm gmssl`**
