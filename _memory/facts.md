# 🧠 持久化事实库

> 这里记录关键结论、常用配置、代码片段等可复用的知识。
> 每次新增知识文档后，同步更新此处。

---

## 📊 项目总进度 (2026-06-09)

### 已完成 ✅

**1. 三层架构搭建**
- 🌀 **n8n 自动化层**: 本地 n8n v2.23.4 运行中，工作流「灵感自动抓取」已激活（每12h抓B站热门）
- ⚙️ **GitHub Actions 处理层**: 3 个工作流就绪（auto-process / auto-analyze / deploy-pages）
- 🧠 **AI 决策层**: Reasonix 分析 + GitHub Models 三档回退（免费→DeepSeek→付费）

**2. 成本优化**
- GitHub Actions: 去定时 + concurrency 防排队 + paths-ignore 防循环 → 分钟数省~70%
- AI API: GitHub Models (免费) → DeepSeek (低价) → OpenAI (付费兜底) → 尽可能零成本
- GitHub Pages: 知识图谱可视化展示，免费无限流量
- Dependabot: 每周自动维护 Python + Actions 依赖

**3. 飞书集成**
- `feishu_bot.py`: 飞书消息→灵感工作流的转发器，Flask 服务运行在 `:5676`
- `deploy_feishu.py`: 一键部署脚本（自动安装依赖+下载隧道+启动服务）
- `create_feishu_app.mjs`: 一键创建飞书应用（Node SDK registerApp）
- 飞书应用「灵感收集」已创建，App ID/Secret 已配置到 `.env`
- 飞书 CLI (lark-cli v1.0.49) 已安装，profile 已配置

**4. 内网穿透**
- serveo.net SSH 隧道可连接但 502（Windows 防火墙限制）
- 推荐用 natapp（国内友好）替代

**5. 知识库**
- 第1篇知识文档: 「AI编程工具进化：从补全到Agent」 存入 `03_知识文档/01_Agent与AI编程/`
- 覆盖 4 个方案对比: Cursor / Cline / Aider / Continue.dev
- `_memory/index.json` 已建立完整索引
- `04_知识网络/knowledge_graph.md` Mermaid 可视化图谱

**6. 文档**
- `SOP.md`: 标准操作流程（含架构、日常使用、故障排查、成本控制）
- `AGENTS.md`: AI 行为指令（三层架构说明 + 决策层职责）
- `README.md`: 项目总说明 + 配置指南 + 脚本速查

**7. Git 仓库**
- 本地 git 已初始化，远程指向上 GitHub: `qiqinmo-bit/qiqinmo_hub`
- 初始提交已推送（核心文件已上线）
- SOP.md 暂存本地待推送

### 待完成 ⏳

- 飞书开放平台: 配置事件订阅 `im.message.receive_v1` + 回调地址 + 权限 `im:message` + 发布上线
- natapp/公网隧道: 解决飞书回调的访问问题
- 飞书 CLI: 执行 `lark-cli auth login --domain im` 完成用户授权

---

## 🔧 服务配置快照

### n8n
| 项目 | 内容 |
|------|------|
| 地址 | http://localhost:5678 |
| 邮箱 | qiqinmodgut@gmail.com |
| 密码 | Dgut7HHH |
| 工作流 | 灵感自动抓取 (每12h) |

### 飞书 Bot
| 项目 | 内容 |
|------|------|
| 地址 | http://localhost:5676 |
| App ID | cli_aaada99cc778dce2 |
| 回调 | /feishu/webhook |
| Auth Token | 使用 .env 配置 |

### 灵感 Webhook
| 项目 | 内容 |
|------|------|
| 地址 | http://localhost:5677 |
| 端点 | /webhook/inspiration |

### GitHub
| 项目 | 内容 |
|------|------|
| 仓库 | https://github.com/qiqinmo-bit/qiqinmo_hub |
| Pages | 配置中 (docs/index.html) |

---

## 💡 常用命令

```bash
# 启动 n8n
n8n start

# 启动飞书 Bot
python _scripts/feishu_bot.py

# 启动 Webhook
python _scripts/webhook_server.py

# 一键部署飞书
python _scripts/deploy_feishu.py

# 查看知识库状态
python _scripts/process_inspiration.py status

# 飞书 CLI 用户授权
lark-cli auth login --domain im
```

---

## 🤖 AI 编程知识

### Cursor Composer + Agent 模式
- **Composer** (`Ctrl+Shift+I`) = 多文件同时编辑
- **Agent 模式** = AI 自主规划→执行→修复
- 二者组合是 Cursor 的杀手锏，远强于单纯 Tab 补全
- 项目规则配置在 `.cursor/rules/` 目录

### 开源替代
- **Cline** (github.com/cline/cline) — VS Code 自主 Agent，支持任意模型（含本地），Plan/Act 双模式
- **Aider** (github.com/Aider-AI/aider) — 终端工具，git 原生集成，自动 commit，`/web` 命令拉网页
- **Continue.dev** — 模块化扩展，支持自定义模型和上下文引用

### Cursor 常用快捷键
| 功能 | 快捷键 |
|------|--------|
| Chat | `Ctrl+I` |
| Composer | `Ctrl+Shift+I` |
| 接受全部 | `Ctrl+Enter` |
| 逐文件 Review | Composer 面板操作 |
