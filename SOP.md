# 📋 日常灵感工作流 — 标准操作流程 (SOP)

> **目标**: 将社交媒体/视频网站的 AI 学习灵感，自动转化为结构化的知识资产
> **版本**: v2.0 (三层架构 + 成本优化)
> **更新**: 2026-06-09

---

## 目录

1. [架构总览](#1-架构总览)
2. [日常使用流程](#2-日常使用流程)
3. [环境维护](#3-环境维护)
4. [故障排查](#4-故障排查)
5. [成本控制](#5-成本控制)
6. [附录](#6-附录)

---

## 1. 架构总览

```
┌────────────────────────────────────────────────────────────┐
│ 🌀 自动化层 (n8n — 本地)                                    │
│                                                             │
│  定时抓 B站热门 → 格式化 → POST Webhook                      │
│  (可选) 截图监听 → PaddleOCR → 提取文字                      │
│               ↓                                              │
├────────────────────────────────────────────────────────────┤
│ ⚙️  GitHub Actions (云端 — 免费)                             │
│                                                             │
│  auto-process.yml  → 更新 memory_index + graph_data         │
│  auto-analyze.yml  → AI 三档回退分析 (免费→低价→付费)        │
│  deploy-pages.yml  → 发布知识图谱到 GitHub Pages            │
│               ↓                                              │
├────────────────────────────────────────────────────────────┤
│ 🧠  决策层 (AI 助手 — 可选)                                  │
│                                                             │
│  读取分析结果 → 撰写知识文档 → 更新 facts.md + 知识图谱       │
└────────────────────────────────────────────────────────────┘
```

---

## 2. 日常使用流程

### 2.1 快速模式（推荐）

只需**发截图或文字**给 AI 助手，我会自动走完整流程。

```
你: [发截图/描述灵感]
AI: 保存到 01_原始灵感/ → 分析 → 搜索 → 写文档 → 更新图谱
你: [可选] 调整或补充
```

**适合**: 日常碎片灵感、单条处理

### 2.2 半自动模式（n8n + AI）

n8n 定时抓 B站，AI 分析入库。

```
n8n: 每12h 抓 B站热门 → 写入 01_原始灵感/
GitHub: 自动触发 AI 分析 (auto-analyze.yml)
你:  打开 GitHub 确认分析结果
AI:  深入补充知识文档
```

**适合**: 想批量采集不想手动找灵感

### 2.3 全自动模式（n8n + GitHub Actions）

完全无人值守，灵感自动采集→分析→入库。

```
n8n: 抓取 → 写入 → push
GitHub: auto-process → auto-analyze → deploy-pages
你:   只需每周看一下知识图谱进展
```

**适合**: 长期积累知识库

---

## 3. 环境维护

### 3.1 本地服务启动

```bash
# 启动 n8n (工作流引擎)
n8n start
# 访问: http://localhost:5678
# 账号: qiqinmodgut@gmail.com / Dgut7HHH

# 启动 Webhook 接收器 (n8n→本地仓库)
pip install flask
python _scripts/webhook_server.py
# 服务: http://localhost:5677/webhook/inspiration
```

### 3.2 更新 n8n 工作流

```bash
# 如果 n8n_workflow.json 有更新:
n8n import:workflow --input=_scripts/n8n_workflow.json
```

### 3.3 推送到 GitHub

```bash
git add -A
git commit -m "新灵感: 标题"
git push
```

### 3.4 查看知识库状态

```bash
python _scripts/process_inspiration.py status
```

---

## 4. 故障排查

### 4.1 Webhook 连接被拒绝

```bash
# 检查 webhook 是否运行
curl -X POST http://localhost:5677/webhook/inspiration \
  -H "Content-Type: application/json" \
  -d '{"test":true}'

# 没运行则启动
python _scripts/webhook_server.py
```

### 4.2 n8n 工作流执行报错

常见原因：

| 错误 | 原因 | 解决 |
|------|------|------|
| `Unsupported language: javascript` | Code 节点语言参数错误 | 改为 `javaScript` (大写 S) |
| `Connection refused` | Webhook 地址不对 | 检查 n8n 中 URL 是否为 `http://localhost:5677/webhook/inspiration` |
| 401 Unauthorized | Cookie 过期 | 重新登录 n8n |

### 4.3 GitHub Actions 不触发

- 检查是否已 push 到 `main` 分支
- 检查 push 的文件路径是否在 `paths` 列表中
- 去 GitHub → Actions 标签页查看运行日志

### 4.4 AI 分析失败

| 现象 | 原因 | 解决 |
|------|------|------|
| 三个 tier 都失败 | 所有 API Key 不可用 | 检查 GitHub Secrets 配置 |
| 只有 GitHub Models 失败 | Token 无免费额度 | 确认 GITHUB_TOKEN 有权限 |
| 分析结果为空 | 输入文本太短 | 确保 description.md 有内容 |

---

## 5. 成本控制

### 5.1 当前成本为零的项目

| 项目 | 免费额度来源 |
|------|-------------|
| GitHub Actions | 公开仓库：**2000 分钟/月** 免费 |
| GitHub Pages | **无限流量**，完全免费 |
| GitHub Models (GPT-4o-mini) | 通过 GITHUB_TOKEN **免费调用** |
| n8n | 本地运行，**免费开源** |
| B站 API | **无需 Token**，公开接口 |

### 5.2 建议配置的 API Key

配置到 GitHub Secrets，仅在免费额度用尽时降级使用：

```
DEEPSEEK_API_KEY  — DeepSeek Chat ¥0.5/百万token
OPENAI_API_KEY    — GPT-4o 兜底（极少用到）
```

配置路径: GitHub → Settings → Secrets and variables → Actions

### 5.3 Actions 分钟省着用

当前防护措施：

```
✅ 去掉了定时触发器        → 不空跑
✅ concurrency 防排队     → 新提交取消旧排队
✅ paths-ignore 防循环    → auto-process 自己的提交不触发二次运行
```

按当前使用频率（每天 3-5 次灵感），月消耗约 **50-100 分钟**，远低于免费额度。

---

## 6. 附录

### 6.1 目录结构速查

```
日常灵感工作流/
├── 01_原始灵感/          # 截图 + description.md
├── 02_灵感分析/          # analysis.md
├── 03_知识文档/          # 按分类的结构化文档
│   ├── 01_Agent与AI编程/
│   ├── 02_模型与API/
│   ├── 03_工作流与自动化/
│   ├── 04_提示词工程/
│   └── 05_多模态与工具链/
├── 04_知识网络/          # graph_data.json + knowledge_graph.md
├── 05_模板/              # 文档模板
├── _memory/              # memory_index.json + facts.md
├── _scripts/             # 处理脚本
├── docs/                 # GitHub Pages 页面
└── .github/workflows/    # 3 个 Actions 工作流
```

### 6.2 常用脚本速查

```bash
# 查看知识库状态
python _scripts/process_inspiration.py status

# OCR 截图→文字
python _scripts/ocr_helper.py 截图路径

# n8n webhook 接收器
python _scripts/webhook_server.py

# AI 三档回退分析
python _scripts/ai_analyzer.py --file description.md
```

### 6.3 n8n 登录信息

| 项目 | 内容 |
|------|------|
| 地址 | http://localhost:5678 |
| 邮箱 | qiqinmodgut@gmail.com |
| 密码 | Dgut7HHH |

---

> **📌 关键原则**: 能免费的绝不付费，能自动的绝不手动。
> GitHub Models 免费额度先用，DeepSeek 兜底，OpenAI 最后保底。
