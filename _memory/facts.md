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
