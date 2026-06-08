# 🧠 持久化事实库

> 这里记录关键结论、常用配置、代码片段等可复用的知识。
> 每次新增知识文档后，同步更新此处。

---

## AI 编程工具

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
