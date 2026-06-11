# AGENTS.md — 给 AI 的工作指令

当你（AI）在此仓库中时，请遵循以下规则：

---

## 🏗️ 三层架构总览

```
┌─────────────────────────────────────────────────────────────┐
│  🌀 自动化层 (n8n) — 数据抓取                               │
│                                                             │
│  · 定时抓 B站热门 → 写入 01_原始灵感/                        │
│  · 收图夹轮询监听 → rapidocr 提取文字                        │
│  · 调用 webhook_server.py 或直写 JSON 到仓库                 │
├─────────────────────────────────────────────────────────────┤
│  ⚙️  处理层 (GitHub Actions) — 索引更新                      │
│                                                             │
│  · Push 到 01_原始灵感/ 时自动触发                            │
│  · 运行 process_inspiration.py --auto                        │
│  · 更新 _memory/memory_index.json + 04_知识网络/graph_data   │
├─────────────────────────────────────────────────────────────┤
│  🧠 决策层 (AI) — 分析+写作                                  │
│                                                             │
│  · 读取 description.md → 分析技术要点                        │
│  · 搜索开源方案 → 撰写知识文档 → 建立双向链接                 │
│  · 更新 facts.md 持久化事实库                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧠 你的核心职责（决策层）

当用户说「分析」或提到某篇灵感时，你的工作流：

### Step 1 — 定位灵感源
- 检查 `01_原始灵感/` 中最新的 `description.md`
- 如果有 OCR 提取的文字（`> OCR 提取文字`），直接阅读
- 如果只有截图（`.jpg/.png`），询问用户描述或尝试 OCR

### Step 2 — 分析梳理
- 解读截图/文字中的核心观点
- 拆解**实现路径**与**技术要点**
- 搜索相关开源项目（用 web_search）
- 保存分析文档到 `02_灵感分析/当天日期_主题/analysis.md`

### Step 3 — 撰写知识文档
- 按 `05_模板/knowledge_doc_template.md` 模板整理
- 保存到 `03_知识文档/` 对应分类下
- 分类参考:
  - `01_Agent与AI编程` — Cursor/Codex/AutoGPT/Multi-Agent
  - `02_模型与API` — GPT/Claude/API/微调/Embedding/RAG
  - `03_工作流与自动化` — n8n/Zapier/CI-CD/爬虫/RPA ← **本仓库自身**
  - `04_提示词工程` — Prompt 技巧/Chain-of-Thought
  - `05_多模态与工具链` — 音视频/多模态模型/LangChain/Dify

### Step 4 — 更新知识网络
- 更新 `_memory/facts.md` — 记录核心结论、配置、代码片段
- 更新 `04_知识网络/knowledge_graph.md` — 添加新节点和关联

---

## 📄 文档规范

- 所有文档使用 **Markdown** 格式
- 知识文档间使用 `[[双向链接]]` 相互引用
- 知识网络使用 Mermaid 语法绘制
- 每个知识文档必须标注：`创建时间`、`关键词`、`关联知识`

---

## 🗂️ 记忆系统

| 文件 | 用途 |
|------|------|
| `_memory/memory_index.json` | 全局搜索索引（自动层维护，你只读） |
| `_memory/facts.md` | 持久化事实库 — 你每次分析后更新 |
| `04_知识网络/graph_data.json` | 知识图谱数据（自动层维护，你只读） |
| `04_知识网络/knowledge_graph.md` | 可视化 Mermaid 图谱（你手动更新） |

---

## 🔧 脚本工具参考

| 脚本 | 用途 | 谁来用 |
|------|------|--------|
| `_scripts/process_inspiration.py` | 核心处理（n8n/Auto/手动） | GitHub Actions / n8n |
| `_scripts/one_click.py` | 一键处理：OCR→入库→git push | 用户拖拽/命令行 |
| `_scripts/watcher.py` | 收图夹轮询监听 | 后台常驻 |
| `_scripts/webhook_server.py` | n8n 本地 webhook 接收器 | n8n |
| `_scripts/n8n_workflow.json` | 可导入 n8n 的工作流模板 | 用户导入 n8n |
