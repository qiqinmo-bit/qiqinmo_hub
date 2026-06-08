---
创建时间: 2026-06-09
来源灵感: [[02_灵感分析/2026-06-09_Cursor_AI编程技巧]]
关键词: [Cursor, Composer, Agent模式, AI编程, Aider, Cline]
分类: 01_Agent与AI编程
---

# 📚 AI编程工具进化：从补全到 Agent

## 概述

Cursor 的 Composer（多文件编辑器） + Agent（自主智能体）模式，代表了 AI 编程工具从"逐行补全"到"任务级自动编程"的关键跃迁。同时，开源社区也涌现出 Aider、Cline 等强力替代方案。

## 实现路径

### 方案一：Cursor（商业首选）

Cursor 是目前体验最完整的 AI 编程 IDE：

| 功能 | 快捷键 | 说明 |
|------|--------|------|
| **Tab 补全** | 自动 | 逐行代码预测 |
| **Chat** | `Ctrl+I` | 对话式代码问答 |
| **Composer** | `Ctrl+Shift+I` | 多文件同时编辑 |
| **Agent 模式** | Composer 内切换 | 自主规划+执行+修复 |
| **项目规则** | `.cursor/rules/` | 项目级 AI 行为配置 |

**适合场景**：全栈功能开发、大型重构、对新代码库的快速探索

### 方案二：Cline（开源 Agent）

[Cline](https://github.com/cline/cline) 是 VS Code 上的开源自主编码 Agent：

- **Plan/Act 模式**：先规划后执行，安全可控
- **跨文件理解**：读取整个项目结构，做出协调修改
- **任意模型**：支持 Claude/GPT/DeepSeek/本地模型
- **终端执行**：可自动运行命令、安装依赖、修复错误
- **CI 集成**：CLI 模式可嵌入脚本和 CI 流程

### 方案三：Aider（终端流）

[Aider](https://github.com/Aider-AI/aider) 是终端中的 AI 结对编程工具：

- **Git 原生集成**：每次修改自动 commit，安全回滚
- **多文件编辑**：理解仓库结构，协调跨文件变更
- **Map 机制**：自动生成仓库地图，帮助 AI 理解项目
- **无 IDE 绑定**：纯终端 + 任意编辑器
- **网页抓取**：支持 `/web <url>` 将网页内容加入上下文

### 方案四：Continue.dev（模块化）

[Continue](https://docs.continue.org.cn/) 是 VS Code/JetBrains 的开源扩展：

- **自定义模型**：支持任何 API 或本地模型
- **上下文管理**：支持 @file、@folder、@codebase 等引用
- **Slash 命令**：可自定义快捷命令
- **Tab 自动补全**：本地模型加速

## 推荐工具/项目

| 项目 | 说明 | 链接 |
|------|------|------|
| **Cursor** | AI 优先 IDE，Composer+Agent 体验最佳 | [cursor.com](https://cursor.com) |
| **Cline** | VS Code 开源自主 Agent | [GitHub](https://github.com/cline/cline) |
| **Aider** | 终端 AI 结对编程，git 原生 | [GitHub](https://github.com/Aider-AI/aider) |
| **Continue.dev** | 开源模块化 AI 代码助手 | [docs.continue.org.cn](https://docs.continue.org.cn/) |

## 关键代码/配置

### Cursor 项目规则 (.cursor/rules/)

```markdown
# .cursor/rules/project.md
你是一个资深全栈工程师。在进行修改前：
1. 先阅读项目结构和现有代码
2. 制定修改计划
3. 与用户确认后执行
```

### Aider 常用命令

```bash
# 启动终端会话
aider --model claude-sonnet-4-20250514

# 添加文件到上下文
aider src/main.py src/utils.py

# 使用 GPT-4o
aider --model gpt-4o

# 开启自动提交
aider --auto-commits
```

## 最佳实践

- **Composer + Agent 黄金组合**：用 Composer 做多文件编辑，Agent 模式做复杂任务
- **小步提交**：无论用哪个工具，保持每次变更聚焦单一目标
- **项目规则先行**：在 `.cursor/rules/` 中定义好 AI 行为规范，事半功倍
- **混合使用**：Cursor 做主要开发 + Cline/Aider 处理 CI 和自动化脚本
- **本地模型保底**：Cline 和 Continue 支持本地模型，API 故障时有备用方案

## 关联知识

- [[AI编程工具对比：Cursor vs Cline vs Aider]]
- [[提示词工程：AI编程中的 Prompt 技巧]]
- [[Agent 模式在编程工具中的应用]]
