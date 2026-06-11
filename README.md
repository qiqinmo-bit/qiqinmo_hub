# 🧠 日常灵感工作流

> **将碎片化灵感自动转化为结构化知识资产**
>
> 截图丢进「收图夹」→ 自动 OCR → 入库 → 推送 GitHub → AI 分析 → 知识图谱

[![🧠 灵感自动处理](https://github.com/qiqinmo-bit/qiqinmo_hub/actions/workflows/auto-process.yml/badge.svg)](https://github.com/qiqinmo-bit/qiqinmo_hub/actions/workflows/auto-process.yml)
[![🤖 灵感自动分析](https://github.com/qiqinmo-bit/qiqinmo_hub/actions/workflows/auto-analyze.yml/badge.svg)](https://github.com/qiqinmo-bit/qiqinmo_hub/actions/workflows/auto-analyze.yml)
[![🕸️ 知识图谱 Pages](https://github.com/qiqinmo-bit/qiqinmo_hub/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/qiqinmo-bit/qiqinmo_hub/actions/workflows/deploy-pages.yml)

---

## 📋 目录

- [工作流全览](#-工作流全览)
- [三层架构](#-三层架构)
- [快速开始](#-快速开始)
- [使用模式](#-使用模式)
- [目录结构速查](#-目录结构速查)
- [本地服务启动](#-本地服务启动)
- [成本控制](#-成本控制)

---

## 🔄 工作流全览

```
灵感源                             知识资产
────────                            ────────
┌─────────┐   ┌──────────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ B站热门  │→  │ 01_原始灵感/  │→  │ AI 分析   │→  │03_知识文档│→  │ 可视化   │
│  n8n抓  │   │              │   │ 三档回退  │   │ 按分类   │   │ 知识图谱 │
└─────────┘   │ description  │   └──────────┘   │ 结构化   │   │ Mermaid  │
┌─────────┐   │   .md        │                  └──────────┘   │ + Pages  │
│ 截图拖  │→  │              │   ┌──────────┐                  └──────────┘
│ 进收图夹 │   │ 截图.jpg     │   │04_知识网络│
└─────────┘   └───────┬──────┘   │ graph    │
                      │           │ .json    │
                      │ push 触发 │ facts.md │
                      v           └──────────┘
                ┌──────────────┐
                │ GitHub       │  自动: auto-process
                │ Actions      │  自动: auto-analyze
                │              │  自动: deploy-pages
                └──────────────┘
```

---

## 🏗️ 三层架构

```
┌─────────────────────────────────────────────────────────────┐
│  🌀 自动化层 (n8n + 收图夹)                                  │
│                                                             │
│  n8n:   每12h抓B站热门 → POST到Webhook → 写入灵感            │
│  收图夹: 截图丢进去 → 自动OCR(rapidocr) → 入库               │
│               ↓                                              │
│         写入 01_原始灵感/ + git push                           │
├─────────────────────────────────────────────────────────────┤
│  ⚙️  处理层 (GitHub Actions · 免费)                          │
│                                                             │
│  auto-process.yml  → 更新 memory_index + graph_data          │
│  auto-analyze.yml  → AI 三档回退分析                         │
│  deploy-pages.yml  → 发布知识图谱到 GitHub Pages              │
│                                                             │
│  💰 成本策略:                                               │
│    1. GitHub Models (免费) — GPT-4o-mini，零成本              │
│    2. DeepSeek (低价)       — ¥0.5/百万 token 兜底            │
│    3. OpenAI (付费)         — 极少用到                        │
├─────────────────────────────────────────────────────────────┤
│  🧠  决策层 (AI 助手 · 按需)                                  │
│                                                             │
│  读取分析结果 → 撰写知识文档 → 建立双向链接                      │
│  更新 facts.md → 更新知识图谱                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 玩法一：放截图自动处理（推荐）

```
① 双击「收图夹_启动.bat」          ← 后台监听开机
② 截图 → 丢进「收图夹」文件夹     ← 自动 OCR + 入库 + 推送到 GitHub
③ 打开 GitHub Pages 看结果        ← 自动 AI 分析
```

只需两步，后台全自动，连命令都不用敲。

### 玩法二：拖拽到 process.bat

```
把截图拖到「process.bat」上
→ 自动 OCR → 入库 → git push
→ 完事
```

### 玩法三：给 AI 处理

```
直接把截图/文字发给 AI
→ AI 帮你保存 → 分析 → 写知识文档
→ 你最后 git push
```

---

## 🛠️ 本地服务启动

### 收图夹（推荐）

```bash
# 方式1: 双击 收图夹_启动.bat
# 方式2: 命令行
python _scripts/watcher.py
```

### n8n（批量采集B站）

```bash
n8n start                   # 访问 http://localhost:5678
python _scripts/webhook_server.py   # Webhook 接收器
```

### 查看知识库状态

```bash
python _scripts/process_inspiration.py status
```

### 推送到 GitHub

```bash
git push    # Clash 代理自动配端口 7897/7890/7891
```

---

## 📁 目录结构速查

```
qiqinmo_hub/
├── 收图夹/                  # 🗂️ 把截图放这里！自动处理
├── 收图夹_启动.bat           # 🚀 双击启动后台监听
├── process.bat              # 🖱️ 截图拖上去一键处理
│
├── 01_原始灵感/              # 📥 灵感入口
│   └── 日期_标题/
│       ├── description.md
│       └── 截图.jpg
│
├── 02_灵感分析/              # 🔍 AI 分析
├── 03_知识文档/              # 📚 结构化知识库
│   ├── 01_Agent与AI编程/
│   ├── 02_模型与API/
│   ├── 03_工作流与自动化/
│   ├── 04_提示词工程/
│   └── 05_多模态与工具链/
│
├── 04_知识网络/              # 🕸️ 知识图谱
├── 05_模板/                  # 📄 文档模板
├── _memory/                  # 🧠 索引 + 事实库
├── _scripts/                 # 🔧 核心脚本
│   ├── process_inspiration.py
│   ├── ai_analyzer.py
│   ├── one_click.py          ← 一键处理
│   ├── watcher.py            ← 收图夹监听
│   └── webhook_server.py
│
├── .github/workflows/        # ⚙️ GitHub Actions
└── docs/                     # 🌐 GitHub Pages
```

---

## 💰 成本控制

| 项目 | 免费额度 | 当前消耗 |
|------|---------|---------|
| GitHub Actions | 公开仓库 2000 分钟/月 | ~50-100 分钟/月 |
| GitHub Pages | 无限流量 | 基本为零 |
| GitHub Models (GPT-4o-mini) | GITHUB_TOKEN 免费调用 | 零成本 |
| n8n | 本地运行，免费开源 | 零成本 |
| B站 API | 无需 Token | 零成本 |

**防护措施**（已内置）：
- ✅ GitHub Actions 去掉了定时触发器 → 不空跑
- ✅ concurrency 防排队 → 新提交自动取消旧排队
- ✅ paths-ignore 防循环 → auto-process 自己的提交不触发二次运行

---

> **核心原则:** 能免费的绝不付费，能自动的绝不手动。

<p align="center"><sub>日常灵感工作流 · qiqinmo-bit</sub></p>
