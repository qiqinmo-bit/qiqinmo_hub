# 📋 日常灵感工作流 — 标准操作流程 (SOP)

> **目标**: 将碎片化灵感自动转化为结构化的知识资产
> **版本**: v2.1 (收图夹 + 一键自动化)
> **更新**: 2026-06-12

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
│ 🌀 自动化层 (收图夹 + n8n)                                  │
│                                                             │
│  收图夹: 截图拖入 → 自动OCR(rapidocr) → 入库 → push         │
│  n8n:   定时抓B站热门 → POST Webhook → 写入灵感             │
│               ↓                                              │
├────────────────────────────────────────────────────────────┤
│ ⚙️  GitHub Actions (云端 — 免费)                             │
│                                                             │
│  auto-process.yml  → 更新 memory_index + graph_data         │
│  auto-analyze.yml  → AI 三档回退分析 (免费→低价→付费)        │
│  deploy-pages.yml  → 发布知识图谱到 GitHub Pages            │
│               ↓                                              │
├────────────────────────────────────────────────────────────┤
│ 🧠  决策层 (AI 助手 — 按需)                                  │
│                                                             │
│  读取分析结果 → 撰写知识文档 → 更新 facts.md + 知识图谱       │
└────────────────────────────────────────────────────────────┘
```

---

## 2. 日常使用流程

### 2.1 收图夹模式（推荐）

```
① 双击「收图夹_启动.bat」          ← 后台常驻，最小化即可
② 截图 → Ctrl+C → 进收图夹/ → Ctrl+V
     ↓ 自动 (5秒内)
    rapidocr 识别文字 → 创建 description.md → 入库
    → 更新索引+图谱 → git push → GitHub
③ GitHub Actions 自动 AI 分析
④ 打开 GitHub Pages 看知识图谱
```

**适合**: 日常碎片灵感、最省事

### 2.2 拖拽模式

```
把截图拖到「process.bat」上
→ 自动 OCR → 入库 → git push
→ 完事
```

**适合**: 偶尔用一次，不想开后台

### 2.3 AI 助手模式

```
你: [发截图/描述灵感]
AI: 保存到 01_原始灵感/ → 分析 → 搜索 → 写文档 → 更新图谱
你: git push
```

**适合**: 深度分析，需要 AI 写知识文档

### 2.4 n8n 半自动模式

```
n8n: 每12h 抓 B站热门 → 写入 01_原始灵感/
GitHub: 自动触发 AI 分析 (auto-analyze.yml)
你:  看看分析结果，补充知识文档
```

**适合**: 批量采集不想手动找灵感

---

## 3. 环境维护

### 3.1 本地服务启动

```bash
# 收图夹（推荐）
python _scripts/watcher.py         # 或双击 收图夹_启动.bat

# n8n (工作流引擎)
n8n start                          # http://localhost:5678
python _scripts/webhook_server.py  # Webhook 接收器
```

### 3.2 推送到 GitHub

```bash
git add -A
git commit -m "新灵感: 标题"
git push                           # Clash 代理自动配端口
```

### 3.3 查看知识库状态

```bash
python _scripts/process_inspiration.py status
```

### 3.4 一键处理（不启动后台）

```bash
# 把截图拖到 process.bat 上
# 或命令行:
python _scripts/one_click.py 截图路径
```

---

## 4. 故障排查

### 4.1 OCR 识别失败

| 现象 | 原因 | 解决 |
|------|------|------|
| 识别不到文字 | 图片不清晰/非文字截图 | 手动创建 description.md |
| DLL 加载失败 | onnxruntime 版本问题 | `pip install onnxruntime==1.17.0` |
| numpy 冲突 | numpy 版本过高 | `pip install "numpy<2"` |

### 4.2 Git 推送失败

```bash
# 检查网络
curl https://github.com -m 5

# 手动配代理
git config --local http.proxy http://127.0.0.1:7897
git push
git config --local --unset http.proxy
```

### 4.3 GitHub Actions 不触发

- 检查是否 push 到 `main` 分支
- 检查 push 的文件路径是否在 `paths` 列表中
- 去 GitHub → Actions 标签页查看运行日志

### 4.4 AI 分析失败

| 现象 | 原因 | 解决 |
|------|------|------|
| 三个 tier 都失败 | 所有 API Key 不可用 | 检查 GitHub Secrets |
| 只有 GitHub Models 失败 | Token 无额度 | 确认 GITHUB_TOKEN 有权限 |
| 分析结果为空 | 输入文本太短 | 确保 description.md 有内容 |

---

## 5. 成本控制

### 5.1 当前成本为零的项目

| 项目 | 免费额度来源 |
|------|-------------|
| GitHub Actions | 公开仓库：2000 分钟/月 免费 |
| GitHub Pages | 无限流量，完全免费 |
| GitHub Models (GPT-4o-mini) | 通过 GITHUB_TOKEN 免费调用 |
| OCR (rapidocr) | 本地运行，免费开源 |
| n8n | 本地运行，免费开源 |
| B站 API | 无需 Token，公开接口 |

### 5.2 建议配置的 API Key

配置到 GitHub Secrets，仅在免费额度用尽时降级使用：

```
DEEPSEEK_API_KEY  — DeepSeek Chat ¥0.5/百万token
OPENAI_API_KEY    — GPT-4o 兜底（极少用到）
```

配置路径: GitHub → Settings → Secrets and variables → Actions

### 5.3 Actions 分钟省着用

```
✅ 去掉了定时触发器        → 不空跑
✅ concurrency 防排队     → 新提交取消旧排队
✅ paths-ignore 防循环    → auto-process 自己的提交不触发二次运行
```

按当前使用频率，月消耗约 50-100 分钟，远低于免费额度。

---

## 6. 附录

### 6.1 目录结构速查

```
日常灵感工作流/
├── 收图夹/               # 🗂️ 截图丢这里，自动处理
├── 收图夹_启动.bat        # 🚀 双击启动后台监听
├── process.bat            # 🖱️ 拖拽一键处理
│
├── 01_原始灵感/          # 截图 + description.md
├── 02_灵感分析/          # analysis.md
├── 03_知识文档/          # 按分类的结构化文档
├── 04_知识网络/          # graph_data.json + knowledge_graph.md
├── 05_模板/              # 文档模板
├── _memory/              # memory_index.json + facts.md
├── _scripts/             # 处理脚本
├── docs/                 # GitHub Pages 页面
└── .github/workflows/    # 3 个 Actions 工作流
```

### 6.2 常用脚本速查

```bash
# 启动收图夹
python _scripts/watcher.py

# 一键处理截图
python _scripts/one_click.py 截图路径

# 查看知识库状态
python _scripts/process_inspiration.py status

# AI 三档回退分析
python _scripts/ai_analyzer.py --file description.md

# n8n webhook 接收器
python _scripts/webhook_server.py
```

### 6.3 n8n 登录信息

| 项目 | 内容 |
|------|------|
| 地址 | http://localhost:5678 |
| 邮箱 | qiqinmodgut@gmail.com |
| 密码 | Dgut7HHH |

---

> **关键原则**: 能免费的绝不付费，能自动的绝不手动。
> GitHub Models 免费额度先用，DeepSeek 兜底，OpenAI 最后保底。
