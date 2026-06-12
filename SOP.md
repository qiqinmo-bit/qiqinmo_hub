# 日常灵感工作流 — 标准操作流程 (SOP)

> 目标：将碎片化灵感自动转化为结构化的知识资产
> 版本：v3.0 (完整人机交互管道)
> 更新：2026-06-13

---

## 1. 架构总览

```
┌──────────────────────────────────────────────────────────────┐
│ 🌀 自动化层 (本地)                                             │
│                                                              │
│  收图夹: 截图拖入 → 自动OCR(rapidocr) → 入库(01) → git push  │
│  仪表盘: http://localhost:5677 实时查看进度+模型层级           │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ ⚙️ 处理层 (GitHub Actions)                                    │
│                                                              │
│  1. batch_analyze.py     → AI 分析 → 02_灵感分析              │
│  2. promote_knowledge.py → 知识文档 → 03_知识文档             │
│  3. process_inspiration.py → 索引+图谱 → _memory + 04        │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ 🧠 决策层 (AI 助手 — 按需)                                     │
│                                                              │
│  读取分析结果 → 撰写知识文档 → 更新 facts.md + 知识图谱         │
│  AI 分析三档回退: GitHub Models(免费) → DeepSeek(低价) → OpenAI(兜底) │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. 日常使用流程

### 2.1 收图夹模式（推荐日常）

```
① 双击「收图夹_启动.bat」      ← 后台常驻
② 截图 → 放入 收图夹/          ← 自动处理，5秒内完成
③ 打开仪表盘看进度              ← http://localhost:5677
④ 等 GitHub Actions 自动跑完    ← 看仪表盘模型层级 绿=API成功 黄=本地规则
⑤ 打开 GitHub Pages 看知识图谱
```

**自动完成**: OCR → 入库 → git push → GitHub Actions 全自动分析 → 知识文档 → 图谱

### 2.2 拖拽模式（偶尔用）

```
把截图拖到「process.bat」上
→ 自动 OCR → 入库 → git push
→ 完事
```

### 2.3 Dashboard 实时监控

启动仪表盘：
```bash
python _scripts/web_dashboard.py
# 或双击 仪表盘_启动.bat
```

**仪表盘功能：**
- 进度条：1-6 步实时显示当前处理到哪一步
- 模型徽章：🟢 DeepSeek / 🟡 本地规则 / ⚫ 等待中
- 实时日志：SSE 推送日志，处理完成自动刷新
- GitHub Actions 状态：最新工作流运行结果
- 卡住检测：超过 45 秒无更新会黄色告警

### 2.4 AI 助手模式（深度分析）

当你主动要求分析某篇灵感时：

```
你: "分析这个灵感"
AI: 1. 读取 01_原始灵感/description.md
    2. 调用 DeepSeek API 分析
    3. 生成分析结果 → 02_灵感分析/
    4. 生成知识文档 → 03_知识文档/
    5. 更新 facts.md + 知识图谱
你: 审阅并确认
```

---

## 3. 完整管道详解

### 截图到知识图谱的全链路

```
截图
  → one_click.py / watcher.py      [本地] OCR + 入库
  → git push                        [本地] 推送到 GitHub
  → pipeline.yml (GitHub Actions) [云端]
    ├─ batch_analyze.py → ai_analyzer.py → 02_灵感分析/
    │   └─ 三档回退: GitHub Models → DeepSeek → OpenAI → 本地规则
    ├─ promote_knowledge.py --auto  → 03_知识文档/
    └─ process_inspiration.py --auto → _memory/index + 04/graph
```

### AI 分析三档回退策略

| 优先级 | 来源 | 模型 | 成本 | 条件 |
|--------|------|------|------|------|
| 1 | GitHub Models | GPT-4o-mini | 免费 | 需 GITHUB_TOKEN |
| 2 | DeepSeek | deepseek-chat | ¥0.5/百万Token | 需 DEEPSEEK_API_KEY |
| 3 | OpenAI | GPT-4o | 付费 | 极少用到 |
| 兜底 | 本地规则 | 关键词提取 | 免费 | 无 API 时的保底 |

### 单张截图成本

| 环节 | 成本 | 说明 |
|------|------|------|
| OCR 识别 | ¥0 | 本地 rapidocr-onnxruntime |
| AI 分析(quick) | ~¥0.0012 | 输入600 + 输出500 tokens |
| 知识文档生成(full) | ~¥0.0023 | 输入800 + 输出1000 tokens |
| 索引更新 | ¥0 | 本地脚本 |
| Git 推送 | ¥0 | 本地操作 |
| GitHub Actions | ¥0 | 免费额度内 |
| **合计** | **~¥0.0035/张** | **约 0.35 分** |

**参考**: 1000 张截图 ≈ ¥3.50

---

## 4. 环境维护

### 4.1 本地服务启动

```bash
# 收图夹（推荐）
python _scripts/watcher.py         # 或双击 收图夹_启动.bat

# 仪表盘
python _scripts/web_dashboard.py   # 或双击 仪表盘_启动.bat
# 打开 http://localhost:5677

# 查看知识库状态
python _scripts/process_inspiration.py status
```

### 4.2 推送到 GitHub

```bash
git add -A
git commit -m "新灵感: 标题"
git push
# Clash 代理自动配端口 7897
```

### 4.3 API Key 配置

配置到 GitHub → Settings → Secrets and variables → Actions：

```bash
DEEPSEEK_API_KEY = sk-xxxx...  # 推荐，低价稳定
OPENAI_API_KEY   = sk-xxxx...  # 兜底，极少用到
```

### 4.4 脚本速查

```bash
# 一键处理截图
python _scripts/one_click.py 截图路径

# 查看待提升的知识条目
python _scripts/promote_knowledge.py --status

# 手动提升指定条目
python _scripts/promote_knowledge.py --entry 2026-06-12_主题

# AI 三档回退分析
python _scripts/ai_analyzer.py --file description.md

# 更新索引+图谱
python _scripts/process_inspiration.py --auto
```

---

## 5. Dashboard 详解

### 模型层级指示器

仪表盘顶部显示当前使用的 AI 模型层级：

```
📸 收图夹监控 [运行中] [模型: DeepSeek] ← 新增
              🟢 = API 成功    🟡 = 本地规则    ⚫ = 暂无记录
```

数据来源：`_memory/last_model.json`，每次 AI 分析后自动更新。

### API 端点

| 路径 | 说明 |
|------|------|
| `/` | 仪表盘主页面 |
| `/api/status` | 处理状态 + watcher 状态 |
| `/api/model-info` | 最近一次 AI 模型调用信息 |
| `/api/logs` | 实时日志 |
| `/api/gh-status` | GitHub Actions 运行状态 |
| `/stream` | SSE 实时推送 |

---

## 6. 目录结构

```
日常灵感工作流/
├── 收图夹/               # 截图拖入，自动处理
├── 收图夹_启动.bat        # 后台监听启动
├── 仪表盘_启动.bat        # 仪表盘启动
├── process.bat            # 拖拽一键处理
│
├── 01_原始灵感/          # 截图 + OCR 文字
├── 02_灵感分析/          # AI 分析结果
├── 03_知识文档/          # 结构化知识文档
│   ├── 01_Agent与AI编程/
│   ├── 02_模型与API/
│   ├── 03_工作流与自动化/
│   ├── 04_提示词工程/
│   └── 05_多模态与工具链/
├── 04_知识网络/          # graph_data.json + knowledge_graph.md
├── 05_模板/              # 文档模板
├── _memory/              # 索引 + 事实库 + 运行时状态
├── _scripts/             # 处理脚本
├── templates/            # 仪表盘 HTML
├── docs/                 # GitHub Pages 页面
└── .github/workflows/    # GitHub Actions 工作流
```

---

## 7. 故障排查

### OCR 识别失败

| 现象 | 原因 | 解决 |
|------|------|------|
| 识别不到文字 | 图片不清晰/非文字截图 | 手动创建 description.md |
| DLL 加载失败 | onnxruntime 版本问题 | `pip install onnxruntime==1.17.0` |

### AI 分析失败

| 现象 | 原因 | 解决 |
|------|------|------|
| 三个 tier 全失败 | 所有 API Key 不可用 | 检查 GitHub Secrets |
| rule_fallback | API 全部失败 | 仪表盘显示 🟡 本地规则 |
| DeepSeek 超时 | 国内网络受限 | 配 Clash 代理或加 OPENAI_API_KEY |

### Git 推送失败

```bash
# 手动配代理
git config --local http.proxy http://127.0.0.1:7897
git push
git config --local --unset http.proxy
```

