# 🧠 日常灵感工作流

> **将碎片化灵感自动转化为结构化知识资产**
>
> 从 B站热门、截图、飞书消息 → 自动入库 → AI 分析 → 生成知识文档 → 可视化知识图谱

[![🧠 灵感自动处理](https://github.com/qiqinmo-bit/qiqinmo_hub/actions/workflows/auto-process.yml/badge.svg)](https://github.com/qiqinmo-bit/qiqinmo_hub/actions/workflows/auto-process.yml)
[![🤖 灵感自动分析](https://github.com/qiqinmo-bit/qiqinmo_hub/actions/workflows/auto-analyze.yml/badge.svg)](https://github.com/qiqinmo-bit/qiqinmo_hub/actions/workflows/auto-analyze.yml)
[![🕸️ 知识图谱 Pages](https://github.com/qiqinmo-bit/qiqinmo_hub/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/qiqinmo-bit/qiqinmo_hub/actions/workflows/deploy-pages.yml)

---

## 📋 目录

- [工作流全览](#-工作流全览)
- [三层架构](#-三层架构)
- [如何使用（三种模式）](#-如何使用三种模式)
- [目录结构速查](#-目录结构速查)
- [本地服务启动](#-本地服务启动)
- [成本控制](#-成本控制)
- [文档导航](#-文档导航)

---

## 🔄 工作流全览

整个流程从灵感源到知识资产，经历 **采集 → 入库 → 分析 → 沉淀 → 展示** 五个阶段：

```
灵感源                               知识资产
───────                             ────────
┌─────────┐     ┌──────────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ 📺 B站  │──→  │ 01_原始灵感/ │──→  │ AI 分析  │──→  │03_知识文档│──→  │ 可视化   │
│  热门   │     │              │     │ 三档回退 │     │ 按分类   │     │ 知识图谱 │
└─────────┘     │ description  │     └──────────┘     │ 结构化   │     │ Mermaid  │
┌─────────┐     │   .md        │                      └──────────┘     │ + Pages  │
│ 📷 截图  │──→  │              │                      ┌──────────┐     └──────────┘
│   OCR   │     │ 截图.jpg     │                      │04_知识网络│
└─────────┘     └──────────────┘                      │ graph    │
┌─────────┐         │                                  │ .json    │
│ 💬 飞书  │──→      │ push 触发                        │ facts.md │
│  消息   │         ↓                                  └──────────┘
└─────────┘    ┌──────────────┐
               │ GitHub       │ ← 自动 (auto-process)
               │ Actions      │ ← 自动 (auto-analyze)
               │              │ ← 自动 (deploy-pages)
               └──────────────┘
```

**一句话流程**: 灵感从任何渠道进入 → 自动或手动写入 `01_原始灵感/` → push 到 GitHub → Actions 自动处理索引和 AI 分析 → 知识凝练为结构化文档 → 最终呈现在可视化知识图谱中。

---

## 🏗️ 三层架构

```
┌─────────────────────────────────────────────────────────────┐
│  🌀 自动化层 (n8n · 本地)                                    │
│                                                             │
│  定时抓 B站热门（每12h）→ 格式化 → POST 到 Webhook              │
│  （可选）监听截图文件 → PaddleOCR → 提取文字                    │
│               ↓                                              │
│         写入 01_原始灵感/ + git push                           │
├─────────────────────────────────────────────────────────────┤
│  ⚙️  处理层 (GitHub Actions · 云端 · 免费)                    │
│                                                             │
│  auto-process.yml  → 更新 memory_index + graph_data          │
│  auto-analyze.yml  → AI 三档回退分析                         │
│  deploy-pages.yml  → 发布知识图谱到 GitHub Pages              │
│                                                             │
│  💰 成本策略：                                               │
│    1️⃣ GitHub Models (免费) — GPT-4o-mini，零成本              │
│    2️⃣ DeepSeek (低价)       — ¥0.5/百万 token 兜底            │
│    3️⃣ OpenAI (付费)         — 极少用到                        │
├─────────────────────────────────────────────────────────────┤
│  🧠  决策层 (AI 助手 · 按需)                                  │
│                                                             │
│  读取分析结果 → 撰写知识文档 → 建立双向链接                      │
│  更新 facts.md 持久化事实库 → 更新知识图谱                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 如何使用（三种模式）

### 🟢 模式一：手动快速模式（推荐入门）

**适合**：日常碎片灵感、单条处理、从截图开始

```
你发给 AI 助手一张截图或一段文字
  ↓
AI 自动保存到 01_原始灵感/ → 分析 → 搜索 → 写知识文档 → 更新图谱
  ↓
你确认结果，可调整补充
```

**步骤**：
1. 将灵感截图或文字发给 AI 助手
2. AI 自动完成全部流程（分析→写文档→更新图谱）
3. 完成后用 `git add -A && git commit -m "新灵感" && git push` 推送

### 🟡 模式二：半自动模式（n8n + AI）

**适合**：想批量采集 B站 热门内容，不想手动找灵感

```
n8n 每 12h 自动抓 B站热门 → 写入 01_原始灵感/
  ↓
GitHub Actions 自动触发处理 (auto-process)
  ↓
AI 自动分析 (auto-analyze)
  ↓
你去 GitHub 确认分析结果，或让 AI 补充知识文档
```

**先决条件**：本地启动 n8n + webhook 服务器

### 🔴 模式三：全自动模式（无人值守）

**适合**：长期积累知识库，只需每周查看进展

```
n8n 自动采集 → 自动 push 到 GitHub
  ↓
GitHub Actions 自动处理 + 分析
  ↓
GitHub Pages 自动发布知识图谱
  ↓
你只需每周打开 Pages 看知识库长势
```

**先决条件**：配置好飞书 Bot 或保持 n8n 持续运行

---

### 📥 四种灵感来源对比

| 来源 | 方式 | 自动化程度 | 适合场景 |
|------|------|-----------|---------|
| 📺 **B站热门** | n8n 定时抓取 | 全自动 | 批量采集行业趋势 |
| 📷 **截图** | PaddleOCR 识别 | 半自动 | 课程截图、文章截图 |
| 💬 **飞书消息** | 飞书 Bot 转发 | 全自动（需配置隧道） | 日常随手记录 |
| ✏️ **手动输入** | 直接写 description.md | 手动 | 深度整理 |



## 📁 目录结构速查

```
qiqinmo_hub/
├── 01_原始灵感/              # 📥 灵感入口（截图 + description.md）
│   └── 2026-06-09_标题/
│       ├── description.md     ← 核心：灵感描述文本
│       └── 截图.jpg           ← 可选：来源截图
│
├── 02_灵感分析/              # 🔍 AI 分析结果
│   └── 2026-06-09_标题/
│       └── analysis.md        ← AI 拆解的技术要点、实现路径
│
├── 03_知识文档/              # 📚 结构化知识库（按分类）
│   ├── 01_Agent与AI编程/     ← Cursor/AutoGPT/Multi-Agent
│   ├── 02_模型与API/         ← GPT/Claude/RAG/微调
│   ├── 03_工作流与自动化/    ← n8n/爬虫/CI-CD
│   ├── 04_提示词工程/        ← Prompt 技巧/CoT
│   └── 05_多模态与工具链/    ← 音视频/LangChain/Dify
│
├── 04_知识网络/              # 🕸️ 知识图谱数据
│   ├── graph_data.json        ← 图谱数据（自动更新）
│   ├── knowledge_graph.md     ← Mermaid 可视化图谱
│
├── 05_模板/                  # 📄 文档模板
│   ├── analysis_template.md
│   ├── knowledge_doc_template.md
│   └── knowledge_graph_template.md
│
├── _memory/                  # 🧠 记忆系统
│   ├── memory_index.json      ← 全局搜索索引（自动维护）
│   └── facts.md               ← 持久化事实库（手动更新）
│
├── _scripts/                 # 🔧 核心脚本
│   ├── process_inspiration.py ← 🎯 灵感处理核心（手动/n8n/Auto）
│   ├── ai_analyzer.py         ← 🤖 AI 分析引擎（三档回退）
│   ├── webhook_server.py      ← 🌐 n8n → 本地的 Webhook 接收器
│   ├── feishu_bot.py          ← 💬 飞书 Bot 转发器
│   ├── ocr_helper.py          ← 📸 截图 OCR 识别
│   ├── deploy_feishu.py       ← 🚀 飞书一键部署
│   ├── create_feishu_app.mjs  ← 飞书应用创建
│   └── start_tunnel.mjs       ← 内网穿透启动器
│
├── .github/workflows/        # ⚙️ GitHub Actions
│   ├── auto-process.yml       ← 自动更新索引+图谱
│   ├── auto-analyze.yml       ← AI 三档回退分析
│   └── deploy-pages.yml       ← 知识图谱 Pages 发布
│
├── docs/                     # 🌐 GitHub Pages
│   └── index.html             ← 知识图谱可视化页面
│
├── AGENTS.md                 # 🤖 AI 行为指令
├── SOP.md                    # 📋 详细操作流程
├── 飞书配置教程.md            # 📖 飞书配置指南
└── .env                      # 🔐 本地环境变量（不上传）
```

---

## 🛠️ 本地服务启动

### 1. 启动 n8n（工作流引擎）

```bash
n8n start
# 访问 http://localhost:5678
# 账号: qiqinmodgut@gmail.com / Dgut7HHH
```

### 2. 启动 Webhook 接收器（n8n→本地仓库）

```bash
pip install flask
python _scripts/webhook_server.py
# 服务: http://localhost:5677/webhook/inspiration
```

### 3. （可选）启动飞书 Bot

```bash
python _scripts/feishu_bot.py
# 服务: http://localhost:5676
```

### 4. 查看知识库状态

```bash
python _scripts/process_inspiration.py status
```

### 5. 推送新灵感到 GitHub

```bash
git add -A
git commit -m "新灵感: xxx"
git push
```

---

## 💰 成本控制

| 项目 | 免费额度 | 当前消耗 |
|------|---------|---------|
| GitHub Actions | 公开仓库 **2000 分钟/月** | ~50-100 分钟/月 |
| GitHub Pages | **无限流量** | 基本为零 |
| GitHub Models (GPT-4o-mini) | GITHUB_TOKEN **免费调用** | 零成本 |
| n8n | 本地运行，**免费开源** | 零成本 |
| B站 API | **无需 Token** 的公开接口 | 零成本 |

**防护措施**（已内置）：
- ✅ GitHub Actions 去掉了定时触发器 → 不空跑
- ✅ `concurrency` 防排队 → 新提交自动取消旧排队
- ✅ `paths-ignore` 防循环 → auto-process 自己的提交不触发二次运行

---

## 📚 文档导航

| 文档 | 用途 |
|------|------|
| **[SOP.md](SOP.md)** | 📋 标准操作流程 — 架构详解、日常使用、故障排查、成本控制 |
| **[AGENTS.md](AGENTS.md)** | 🤖 AI 行为指令 — 告诉 AI 如何分析灵感和写作 |
| **[飞书配置教程.md](飞书配置教程.md)** | 📖 飞书 Bot 的完整配置步骤（事件订阅、权限、发布） |
| **[05_模板/](05_模板/)** | 📄 知识文档模板 — 写文档时参考 |

---

> **核心原则:** 能免费的绝不付费，能自动的绝不手动。

<p align="center"><sub>Built with ❤️ by qiqinmo-bit · 日常灵感工作流 v2.0</sub></p>
