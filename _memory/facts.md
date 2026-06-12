# 🧠 持久化事实库

> 这里记录关键结论、常用配置、代码片段等可复用的知识。
> 每次新增知识文档后，同步更新此处。

---

## 📊 项目总进度 (2026-06-12)

### 已完成 ✅

**1. 三层架构搭建**
- 🌀 **自动化层**: n8n 工作流「灵感自动抓取」已激活（每12h抓B站热门）
- ⚙️ **处理层**: 3 个 GitHub Actions 工作流就绪（auto-process / auto-analyze / deploy-pages）
- 🧠 **决策层**: AI 助手按需分析写作

**2. 一键收图功能**
- ✅ `收图夹/` 文件夹 + 轮询监听 `watcher.py`
- ✅ 截图放进去自动 OCR → 入库 → git push
- ✅ rapidocr-onnxruntime 轻量 OCR 引擎

**3. 成本优化**
- GitHub Actions: 去定时 + concurrency 防排队 + paths-ignore 防循环
- AI API: GitHub Models (免费) → DeepSeek (低价) → OpenAI (付费兜底)
- GitHub Pages: 免费无限流量
- Dependabot: 每周自动维护依赖

**4. 知识库**
- 第1篇知识文档: 「AI编程工具进化：从补全到Agent」
- `_memory/index.json` 已建立完整索引
- `04_知识网络/knowledge_graph.md` Mermaid 可视化图谱
- 总条目: 7 篇

**5. 文档**
- `SOP.md`: 标准操作流程
- `AGENTS.md`: AI 行为指令
- `README.md`: 项目总说明
- `process.bat`: 拖拽一键处理
- `收图夹_启动.bat`: 后台监听启动器

**6. 版本管理**
- 本地 git → GitHub: `qiqinmo-bit/qiqinmo_hub`
- Clash 代理自动配端口: `7897, 7890, 7891`

### 待完成 ⏳

- 更多灵感分析和知识文档撰写
- GitHub Pages 知识图谱正式上线

---

## 🔧 服务配置快照

### n8n
| 项目 | 内容 |
|------|------|
| 地址 | http://localhost:5678 |
| 邮箱 | qiqinmodgut@gmail.com |
| 密码 | Dgut7HHH |
| 工作流 | 灵感自动抓取 (每12h) |

### 灵感处理
| 项目 | 内容 |
|------|------|
| 收图夹 | 项目根目录 `收图夹/` |
| 监听脚本 | `_scripts/watcher.py` |
| 启动器 | `收图夹_启动.bat` |
| 一键拖拽 | `process.bat` |
| OCR | rapidocr-onnxruntime |

### GitHub
| 项目 | 内容 |
|------|------|
| 仓库 | https://github.com/qiqinmo-bit/qiqinmo_hub |
| Pages | https://qiqinmo-bit.github.io/qiqinmo_hub/ |
| Clash 代理 | 7897 / 7890 / 7891 |

---

## 💡 常用命令

```bash
# 启动 n8n
n8n start

# 启动收图夹
python _scripts/watcher.py

# 拖拽处理截图
# 把截图拖到 process.bat 上

# 查看知识库状态
python _scripts/process_inspiration.py status

# 推送
git push
```

---

## 🤖 AI 编程知识

### Cursor Composer + Agent 模式
- **Composer** (`Ctrl+Shift+I`) = 多文件同时编辑
- **Agent 模式** = AI 自主规划→执行→修复
- 二者组合是 Cursor 的杀手锏

### 开源替代
- **Cline** (github.com/cline/cline) — VS Code 自主 Agent
- **Aider** (github.com/Aider-AI/aider) — 终端工具，git 原生集成
- **Continue.dev** — 模块化扩展

---

### AI Agent 系统设计核心问题 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 01_Agent与AI编程 |
| **来源** | 字节 AiAgent 二面面试题 |
| **核心** | 工作流拆解 / Tool Calling / 多Agent 协作 / 状态管理 |

### Agent 框架对比 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 01_Agent与AI编程 |
| **核心** | LangGraph (状态驱动) vs AutoGen (对话) vs CrewAI (角色化) / 低代码平台选型 |

### AI 模型选型指南 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 02_模型与API |
| **核心** | 编程→Opus/GPT-5.5/GLM / 学术→GPT-5.5thinking / 办公→Kimi / 中文→DeepSeek V4 |

### 模型指令遵从与 RAG 优化 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 02_模型与API |
| **核心** | Badcase定位→Prompt→参数→后处理→流程 / RAG: BM25+向量 混合→Rerank / Agentic RAG |

### AI 视频制作与多模态工具链 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 05_多模态与工具链 |
| **核心** | 首帧生成(香蕉/即梦) → 动作迁移(Wan/Kling/Runway) / ComfyUI 生态 |

### 短期记忆与长期记忆 GraphRAG (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 03_工作流与自动化 |
| **核心** | 短期(<100天)=向量DB / 长期(>100天)=GraphRAG / 最佳方案 |

### Vibe Coding 工具链 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 04_提示词工程 |
| **核心** | Superpower→需求 / Stitch→设计 / Codex→开发 / MCP 桥接 |

---

### AI Agent 系统设计核心问题 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 01_Agent与AI编程 |
| **来源** | 字节 AiAgent 二面面试题 |
| **核心** | 工作流拆解 / Tool Calling / 多Agent 协作 / 状态管理 |

### Agent 框架对比 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 01_Agent与AI编程 |
| **核心** | LangGraph (状态驱动) vs AutoGen (对话) vs CrewAI (角色化) / 低代码平台选型 |

### AI 模型选型指南 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 02_模型与API |
| **核心** | 编程→Opus/GPT-5.5/GLM / 学术→GPT-5.5thinking / 办公→Kimi / 中文→DeepSeek V4 |

### 模型指令遵从与 RAG 优化 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 02_模型与API |
| **核心** | Badcase定位→Prompt→参数→后处理→流程 / RAG: BM25+向量 混合→Rerank / Agentic RAG |

### AI 视频制作与多模态工具链 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 05_多模态与工具链 |
| **核心** | 首帧生成(香蕉/即梦) → 动作迁移(Wan/Kling/Runway) / ComfyUI 生态 |

### 短期记忆与长期记忆 GraphRAG (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 03_工作流与自动化 |
| **核心** | 短期(<100天)=向量DB / 长期(>100天)=GraphRAG / 最佳方案 |

### Vibe Coding 工具链 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 04_提示词工程 |
| **核心** | Superpower→需求 / Stitch→设计 / Codex→开发 / MCP 桥接 |


### AI Agent 系统设计核心问题 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 01_Agent与AI编程 |
| **来源** | 字节 AiAgent 二面面试题 |
| **核心** | 工作流拆解 / Tool Calling / 多Agent 协作 / 状态管理 |

### Agent 框架对比 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 01_Agent与AI编程 |
| **核心** | LangGraph (状态驱动) vs AutoGen (对话) vs CrewAI (角色化) / 低代码平台选型 |

### AI 模型选型指南 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 02_模型与API |
| **核心** | 编程:Opus/GPT-5.5/GLM / 学术:GPT-5.5thinking / 办公:Kimi / 中文:DeepSeek V4 |

### 模型指令遵从与 RAG 优化 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 02_模型与API |
| **核心** | Badcase定位/Prompt/参数/后处理/流程 / RAG: BM25+向量 混合+Rerank / Agentic RAG |

### AI 视频制作与多模态工具链 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 05_多模态与工具链 |
| **核心** | 首帧生成(香蕉/即梦) 动作迁移(Wan/Kling/Runway) / ComfyUI 生态 |

### 短期记忆与长期记忆 GraphRAG (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 03_工作流与自动化 |
| **核心** | 短期(<100天)=向量DB / 长期(>100天)=GraphRAG / 最佳方案 |

### Vibe Coding 工具链 (2026-06-13)

| 项目 | 内容 |
|------|------|
| **分类** | 04_提示词工程 |
| **核心** | Superpower=需求 / Stitch=设计 / Codex=开发 / MCP 桥接 |
