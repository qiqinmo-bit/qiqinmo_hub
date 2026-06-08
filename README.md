# 🧠 日常灵感工作流

> 将视频评论区/社交媒体上的 AI 学习灵感，自动转化为结构化的知识资产。

---

## 🏗️ 三层架构

```
  ┌──────────────────────────────────────────────────────────────┐
  │ 🌀 n8n (自动化层)                                            │
  │                                                              │
  │  定时任务 ──→ B站 API ──→ 提取评论区/热门                      │
  │  文件监听 ──→ PaddleOCR ──→ 截图→文字                         │
  │               ↓                                              │
  │       写入 01_原始灵感/description.md                          │
  │               ↓ Push                                         │
  ├──────────────────────────────────────────────────────────────┤
  │ ⚙️ GitHub Actions (处理层)                                    │
  │                                                              │
  │  自动检测新灵感 → 更新 memory_index.json                       │
  │                → 更新 graph_data.json (知识图谱)               │
  │                → 自动 Commit 回仓库                            │
  │               ↓                                              │
  ├──────────────────────────────────────────────────────────────┤
  │ 🧠 Reasonix AI (决策层)                                       │
  │                                                              │
  │  读取描述 → 分析技术要点 → 搜索开源方案                        │
  │         → 撰写知识文档 → 更新 facts.md + 知识图谱              │
  └──────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 方式 1：纯手动（无需配置）

直接发截图给我，我会：

```
📸 你发截图 → 我分析 → 我搜索 → 我写文档 → 我更新图谱
```

### 方式 2：开启 n8n 自动抓取（推荐）

```bash
# 1. 安装 n8n（已有则跳过）
npm install -g n8n

# 2. 启动 n8n
n8n start

# 3. 启动本地 webhook 接收器
pip install flask
python _scripts/webhook_server.py

# 4. 在 n8n 中导入工作流模板
#    打开 http://localhost:5678 → 设置 → 导入 → 选择 _scripts/n8n_workflow.json
```

之后 n8n 会**定时自动抓取** B站热门内容并写入仓库。

### 方式 3：开启 GitHub Actions 自动索引

将仓库推送到 GitHub 后：

1. 进入 GitHub 仓库 → **Actions** 选项卡
2. 确保 `🧠 灵感自动处理` workflow 已启用（默认启用）
3. 每次 push 新灵感到 `01_原始灵感/` 时，它会自动更新索引和图谱

---

## 📂 完整目录结构

```
日常灵感工作流/
├── README.md                    # 本文件
├── AGENTS.md                    # AI 行为指令（重要！）
│
├── 01_原始灵感/                  # 原始截图与描述
│   └── YYYY-MM-DD_主题/
│       ├── description.md       # 描述文本 + OCR 文字
│       └── *.jpg / *.png        # 原始截图
│
├── 02_灵感分析/                  # 详细分析文档
│   └── YYYY-MM-DD_主题/
│       └── analysis.md          # AI 写的分析
│
├── 03_知识文档/                  # 结构化知识库
│   ├── 01_Agent与AI编程/
│   ├── 02_模型与API/
│   ├── 03_工作流与自动化/
│   ├── 04_提示词工程/
│   └── 05_多模态与工具链/
│
├── 04_知识网络/                  # 知识图谱
│   ├── knowledge_graph.md       # 可视化 Mermaid 图谱
│   └── graph_data.json          # 图谱数据（自动维护）
│
├── 05_模板/                     # 文档模板
│   ├── analysis_template.md
│   ├── knowledge_doc_template.md
│   └── knowledge_graph_template.md
│
├── _memory/                     # 记忆系统
│   ├── memory_index.json        # 全局搜索索引（自动维护）
│   └── facts.md                 # 持久化事实库（AI 维护）
│
├── _scripts/                    # 辅助脚本
│   ├── process_inspiration.py   # 核心处理脚本
│   ├── ocr_helper.py            # PaddleOCR 封装
│   ├── webhook_server.py        # n8n 本地 Webhook 接收器
│   └── n8n_workflow.json        # 可导入 n8n 的工作流模板
│
└── .github/workflows/           # GitHub Actions
    └── auto-process.yml         # 自动索引更新
```

---

## ⚙️ 配置指南

### 1. PaddleOCR（截图→文字）

```bash
pip install paddleocr
```

安装后，`_scripts/ocr_helper.py` 会自动启用 OCR 功能。

```bash
# 测试
python _scripts/ocr_helper.py 01_原始灵感/2026-06-09_xxx/截图.jpg
```

> 没安装也会优雅降级，只是返回提示信息。

### 2. n8n 工作流配置

导入 `_scripts/n8n_workflow.json` 到 n8n 后：

- **定时触发**：默认每 12 小时运行一次，可在 Schedule Trigger 节点调整
- **B站 API**：读取热门内容，无需登录
- **评论扩展**：如要抓特定视频的评论区，把 `bilibili-api` 节点 URL 改为:
  ```
  https://api.bilibili.com/x/v2/medialist/resource/list?type=1&biz_id=你的合集ID
  ```
  或按 `https://api.bilibili.com/x/v2/reply?oid={视频aid}&type=1` 抓评论

### 3. GitHub Actions 配置

推送到 GitHub 后**无需额外配置**。如需调整定时:

```yaml
# .github/workflows/auto-process.yml 中的 cron 表达式
on:
  schedule:
    - cron: "0 2 * * *"   # 每天 UTC 2:00（北京时间 10:00）
```

---

## 🔧 脚本速查

```bash
# 查看知识库状态
python _scripts/process_inspiration.py status

# OCR 截图并自动入库（等待 AI 分析）
python _scripts/process_inspiration.py --ocr 截图路径

# 从 n8n JSON 文件导入
python _scripts/process_inspiration.py --n8n payload.json

# 手动启动自动更新（同 GitHub Actions 逻辑）
python _scripts/process_inspiration.py --auto

# 启动 webhook 服务（供 n8n 调用）
python _scripts/webhook_server.py
```

---

## 📊 项目状态

[![🧠 灵感自动处理](https://github.com/YOUR_NAME/YOUR_REPO/actions/workflows/auto-process.yml/badge.svg)](https://github.com/YOUR_NAME/YOUR_REPO/actions/workflows/auto-process.yml)
<!-- ↑ 推送到 GitHub 后替换 YOUR_NAME/YOUR_REPO -->

| 层级 | 状态 | 说明 |
|------|------|------|
| 🧠 决策层 (AI) | ✅ 就绪 | 截图→分析→文档，全程 AI 驱动 |
| ⚙️ 处理层 (GitHub Actions) | ✅ 就绪 | 自动更新索引和图谱 |
| 🌀 自动化层 (n8n) | ⏸️ 可选 | 需本地安装 n8n + 配置 API |
| 🔍 OCR (本地模型) | ⏸️ 可选 | 需安装 PaddleOCR |

---

*✨ 将日常碎片灵感，沉淀为可检索、可关联的知识资产*
