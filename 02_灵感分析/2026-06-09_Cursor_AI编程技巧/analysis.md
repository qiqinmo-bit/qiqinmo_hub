# 📝 灵感分析文档

**日期**: 2026-06-09
**来源**: B站视频评论区
**主题**: Cursor AI编程 — Composer 多文件编辑 + Agent 模式

---

## 1️⃣ 核心观点

- Cursor 的 **Composer**（编写器）模式允许同时编辑多个文件，比传统单文件补全效率高得多
- **Agent 模式**让 AI 能自主理解任务、规划步骤、跨文件修改
- 二者结合 = 从"逐行补全"升级为"任务级自动编程"
- 很多人只用 Tab 补全，没意识到 Composer + Agent 才是 Cursor 的核心杀手锏

## 2️⃣ 技术栈

- **Cursor** — 基于 VS Code 的 AI 优先 IDE（闭源商业产品）
- **Composer** — 多文件并行编辑界面（Ctrl/⌘+I）
- **Agent 模式** — 自动规划 + 执行 + 修复的智能体
- **底层模型** — 支持 Claude、GPT-4o、DeepSeek 等多种模型切换

## 3️⃣ 实现路径

### 方法一：Cursor Composer 工作流
1. 安装 Cursor → 打开项目
2. 按 `Ctrl+Shift+I`（或 `⌘+Shift+I`）打开 Composer
3. 描述你想实现的功能（如 "添加用户登录页面，包括前端表单和后端 API"）
4. Composer 自动创建/修改多个文件
5. 使用 `Ctrl+Enter` 接受全部更改，或逐文件 Review
6. 切换到 **Agent 模式**（Composer 右下角开关）
7. Agent 自动读取项目结构 → 执行命令 → 修复错误

### 方法二：开源替代方案对比
- **Aider**：终端工具，git 感知，自动 commit，多文件编辑
- **Cline**：VS Code 扩展，自主 Agent，支持 Plan/Act 模式
- **Continue.dev**：VS Code/JetBrains 扩展，模块化，可自定义模型

## 4️⃣ 开源项目搜索

| 项目 | 功能 | 链接 | 匹配度 |
|------|------|------|--------|
| **Aider** | 终端 AI 结对编程，git 原生集成，自动多文件编辑 | [GitHub](https://github.com/Aider-AI/aider) | ⭐⭐⭐⭐⭐ |
| **Cline** | VS Code 开源自主编码 Agent，跨文件理解+修改 | [GitHub](https://github.com/cline/cline) | ⭐⭐⭐⭐⭐ |
| **Continue.dev** | VS Code/JetBrains 开源扩展，自定义模型+上下文 | [官网](https://docs.continue.org.cn/) | ⭐⭐⭐⭐ |
| **Copilot** | GitHub 官方，Tab补全+Chat，闭源 | [GitHub](https://github.com/features/copilot) | ⭐⭐⭐ |

## 5️⃣ 个人思考

- Cursor 的 Composer + Agent 组合是目前 AI 编程工具中体验最顺滑的，尤其适合**全栈功能开发**和**大型重构**
- 但它是**闭源商业产品**，有定价和模型限制
- **Cline** 作为开源替代，在 Agent 能力上非常接近，且支持任意模型（本地模型也可）
- **Aider** 更适合偏好终端工作流、习惯 git 精细控制的开发者
- 未来趋势：从"AI 补全代码" → "AI 理解项目 → 规划 → 执行"，Agent 模式是分水岭

## 6️⃣ 关键词

`Cursor` `Composer` `Agent模式` `AI编程` `多文件编辑` `Aider` `Cline` `Continue.dev`

## 7️⃣ 关联知识

- [[AI编程工具对比：Cursor vs Cline vs Aider]]
