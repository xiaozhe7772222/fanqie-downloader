# 唯一 · 番茄小说搜索 · 状态 · 下载 · 全安卓端
# The One · Fanqie Novel Search · Status · Download · Full Android

> **@小哲** — 唯一一个为安卓设计的番茄小说三合一工具：搜索 + 查状态 + 下载
> **@小哲** — The only Android-first Fanqie Novel tool that does it all: search + status + download

---

**🏷️ 标签 · Tags**

`番茄小说` `fanqie` `番茄小说下载` `fanqie-novel-downloader` `安卓` `Android` `Termux` `Pydroid3` `Skill` `Python` `小说下载` `novel-downloader` `离线阅读` `offline-reading` `开源` `open-source` `MIT` `移动端` `mobile` `全安卓` `Full-Android` `搜索` `search` `状态查询` `status-check` `三合一` `all-in-one` `番茄免费小说` `fanqie-novel` `爬虫` `crawler` `a-bogus` `多线程` `multi-thread` `断点续传` `resume-download` `TXT` `电子书`

---

## 它是什么 · What It Is

**番茄小说搜索、状态查询与下载工具，全安卓端适配。**
**Fanqie Novel search, status check, and downloader — fully adapted for Android.**

**不是网页工具，不是桌面软件，是三个真正跑在安卓手机上的版本。**
**Not a web tool, not a desktop app — three versions that actually run on your Android phone.**

**它会搜索、它会告诉你这本书更没更、它会下载到本地让你离线看。**
**It searches, it tells you if the book has updated, it downloads for offline reading.**

**默认保存到 `/storage/emulated/0/番茄小说下载/`，也可在设置中自由切换。**
**Default save path: `/storage/emulated/0/番茄小说下载/`, freely switchable in settings.**

**就这三件事，做到极致。**
**Just these three things, done to the extreme.**

---

## 唯一 · The One

**同类工具很多，但唯一一个同时满足这三条的，只有这个。**
**There are many similar tools, but only one meets all three criteria.**

| 对比项 Comparison | 同类工具 Others | 本工具 This One |
|:---|:---|:---|
| **全安卓端 Full Android** | ❌ 大多需要 PC 或服务器 | ✅ 手机直接跑 |
| **搜索 Search** | ❌ 只给下载链接 | ✅ 内置搜索，返回 book_id |
| **状态查询 Status check** | ❌ 下完才知道 | ✅ 先查再下，避免白跑 |
| **下载 Download** | ⚠️ 单线程慢 | ✅ 多线程并发 + 断点续传 |
| **加密解密 Decryption** | ❌ 下完乱码 | ✅ 自动解密 |
| **多版本 Three versions** | ❌ 只有一个版本 | ✅ Skill / Termux / Pydroid3 |
| **路径自定义 Custom path** | ❌ 固定目录 | ✅ 默认 `/storage/emulated/0/番茄小说下载/`，随时切换 |
| **开源 Open source** | ⚠️ 部分闭源 | ✅ MIT 全开源 |

---

## 三个版本 · Three Versions

### 🧠 Skill 版
**适用场景：自动化集成环境。**
**Use case: Automated integration environment.**

```bash
git clone https://github.com/xiaozhe7772222/fanqie-downloader.git
pip install requests beautifulsoup4 tqdm gmssl
cd fanqie_downloader/skill
python3 fanqie_txt.py --search 关键词
python3 fanqie_txt.py --check 7575757575757575757
python3 fanqie_txt.py --book_id 7575757575757575757
```

### 📱 Termux 版
**适用场景：Android Termux 终端环境。**
**Use case: Android Termux terminal environment.**

```bash
# 一键安装
git clone https://github.com/xiaozhe7772222/fanqie-downloader.git
cd fanqie_downloader/termux
bash install.sh
fanqie --search 关键词
fanqie --check 7575757575757575757
fanqie --book_id 7575757575757575757

# 手动安装
pkg install python
pip install requests beautifulsoup4 tqdm gmssl
cd /path/to/termux
python3 fanqie_txt.py
```

### 🐍 Pydroid3 版
**适用场景：Pydroid3 移动端 Python IDE。**
**Use case: Pydroid3 mobile Python IDE.**

```bash
pip install requests beautifulsoup4 tqdm gmssl
git clone https://github.com/xiaozhe7772222/fanqie-downloader.git
cd fanqie_downloader/pydroid3
python3 fanqie_txt.py
```

---

## 快速开始 · Quick Start

```bash
python3 fanqie_txt.py --search 北齐天可汗          # 搜索
python3 fanqie_txt.py --check 7635758880567348249  # 查状态
python3 fanqie_txt.py --book_id 7635758880567348249 # 下载
python3 fanqie_txt.py                               # 交互菜单
```

---

## 功能特性 · Features

| 功能 Feature | 说明 Description |
|:---|:---|
| 🔍 **搜索 Search** | 内置搜索，返回 JSON 结构化结果 |
| ℹ️ **状态 Status** | 查字数、连载状态、在读人数、分类 |
| 📥 **下载 Download** | 多线程并发，自动解密，保存为 TXT |
| ↺ **断点续传 Resume** | 中断后继续，不重复下载 |
| 📂 **路径自定义 Custom path** | 默认 `/storage/emulated/0/番茄小说下载/`，随时切换 |
| 📊 **榜单 Ranking** | 男频/女频各类榜单浏览 |
| 📚 **批量 Batch** | 多本书一次下载 |
| 🛠️ **工具箱 Toolbox** | 章节范围、字数统计、追更检测 |

---

## 项目结构 · Project Structure

```
fanqie_downloader/
├── README.md
├── skill/          # Skill 集成版
│   ├── fanqie_txt.py      # 主程序
│   └── abogus.py          # 反爬模块
├── termux/         # Termux 终端版
│   ├── fanqie_txt.py      # 主程序
│   ├── abogus.py          # 反爬模块
│   └── install.sh         # 一键安装脚本
└── pydroid3/       # Pydroid3 移动 IDE 版
    ├── fanqie_txt.py      # 主程序
    └── abogus.py          # 反爬模块
```

---

## 安装依赖 · Install Dependencies

```bash
pip install requests beautifulsoup4 tqdm gmssl
```

---

## 技术细节 · Technical Details

**番茄小说使用自定义字符编码保护章节内容，下载器内置了解密引擎。**
**Fanqie Novel uses custom character encoding; the downloader has a built-in decryption engine.**

**搜索功能基于 a_bogus 参数签名绕过反爬机制。**
**Search uses a_bogus parameter signing to bypass anti-crawling.**

**下载采用多线程并发，支持断点续传和缓存管理。**
**Download uses multi-threading with resume and cache support.**

**默认保存路径 `/storage/emulated/0/番茄小说下载/`，可在设置中切换为任意可写目录。**
**Default save path `/storage/emulated/0/番茄小说下载/`, switchable to any writable directory in settings.**

---

## 📄 开源许可 · License

**MIT License · 仅供学习交流 · 请尊重番茄小说的版权，仅用于个人离线阅读。**
**MIT License · For educational purposes only · Respect Fanqie Novel's copyright, use only for personal reading.**

---

**⭐ 如果这个项目对你有帮助，欢迎 Star！**
**⭐ Star if you find this project helpful!**