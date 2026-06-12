---
创建时间: 2026-06-13
来源灵感: [[02_灵感分析/2026-06-12_灵感_003]]
关键词: [Vibe Coding, Superpower, Codex, Stitch, MCP, 无代码开发]
分类: 04_提示词工程
---

# 📚 Vibe Coding 工具链：Superpower + Codex + Stitch

## 概述

"Vibe Coding" 工作流的新范式：通过 Superpower 生成需求文档、Codex 作为开发引擎、Stitch 做 UI 设计，让没有代码基础的人也能开发应用。MCP（Model Context Protocol）作为工具间的桥梁。

## 核心内容

### Vibe Coding 是什么

Vibe Coding 是一种**以自然语言驱动**的编程范式，开发者不再逐行写代码，而是通过描述需求让 AI 完成整个开发流程。核心是"描述 → 生成 → 迭代"。

### 推荐工作流

**Step 1：需求梳理（Superpower）**
- 使用 Superpower（AI 编码辅助工具）生成需求文档
- 输出：PRD / 技术规范 / 记忆文档

**Step 2：UI 设计（Stitch）**
- 用 Stitch 设计界面原型
- 优势：设计效果比 Codex 自带的 Product Design 更好
- 免费可用，适合快速迭代

**Step 3：开发实现（Codex）**
- 通过 MCP 导入 Stitch 的设计
- 让 Codex 直接开发完整应用
- Codex 负责后端逻辑、数据流、部署配置

**Step 4：MCP 桥接**
- MCP（Model Context Protocol）连接设计工具和开发工具
- 设计稿 → MCP → Codex → 最终应用
- 减少人工转换带来的误差

### 工具对比

| 工具 | 职责 | 适合人群 |
|------|------|---------|
| Superpower | 需求分析、文档生成 | 所有人 |
| Stitch | UI/UX 设计 | 设计师、无代码开发者 |
| Codex | 全栈开发 | 开发者、AI 编程用户 |
| Cursor | IDE 级 AI 编程 | 开发者 |
| Bolt/v0 | 快速原型 | 设计师、PM |

## 推荐工具/项目

| 项目 | 说明 | 链接 |
|------|------|------|
| Codex CLI | OpenAI 开源 CLI 编程 Agent | [GitHub](https://github.com/openai/codex) |
| Superpower | AI 编码辅助/需求生成 | [superpower.ai](https://superpower.ai) |
| Stitch | AI 驱动的 UI 设计工具 | [stitch.com](https://stitch.com) |
| MCP | Model Context Protocol | [modelcontextprotocol.io](https://modelcontextprotocol.io) |

## 最佳实践

- Vibe Coding 适合原型快速验证，不适合生产级复杂系统
- 需求文档先行，好的需求 = 好的代码
- 设计工具 + 开发工具分离，通过 MCP 桥接
- 无代码开发者入门路径：Superpower → Stitch → Codex
- 即使有代码基础，Vibe Coding 也能大幅提升效率

## 关联知识

- [[AI编程工具进化：从补全到Agent]]
- [[AI 模型选型场景指南]]
- [[AI Agent 系统设计核心问题]]
