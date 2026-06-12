---
创建时间: 2026-06-13
来源灵感: [[02_灵感分析/2026-06-12_灵感_002]]
关键词: [LangGraph, AutoGen, CrewAI, Agent框架, 低代码平台]
分类: 01_Agent与AI编程
---

# 📚 Agent 框架对比：LangGraph vs AutoGen vs CrewAI

## 概述

当前主流 Agent 开发框架的选型对比，从架构设计、扩展性、低代码平台等维度分析 LangGraph、AutoGen、CrewAI 的优劣，以及与扣子等低代码 Agent 平台的适用场景。

## 核心内容

### LangGraph（LangChain 出品）

**核心概念：State / Node / Edge**
- **State**：全局状态对象，所有 Node 共享读写，驱动整个图执行
- **Node**：逻辑单元，每个 Node 接收 State、处理、返回更新后的 State
- **Edge**：控制流，定义 Node 之间的跳转条件和顺序

**优势：**
- 与 LangChain 生态完美集成，链式思维自然
- State 驱动的设计让复杂工作流清晰可控
- 支持条件分支、循环、并行执行
- 可自定义 reducer 控制状态更新逻辑

**劣势：**
- 学习曲线陡，State 管理容易引入复杂度
- 调试困难，Graph 执行过程难以可视化

### AutoGen（微软）

**核心优势：**
- 多Agent 对话模式，天然支持 Agent 间通信
- AssistantAgent（助手） + UserProxyAgent（用户代理）两层模型
- 内置代码执行沙箱

**劣势：**
- Agent 间通信效率低，对话过长时性能下降
- 适用于聊天类场景，不适合结构化工作流

### CrewAI

**核心概念：Agent / Task / Crew**
- Agent：角色定义（role、goal、backstory）
- Task：任务描述+预期输出
- Crew：Agent+Task 的组合编排

**优势：**
- 最易上手，配置式定义，代码量最少
- 角色化设计让多Agent 协作自然
- 内置任务委派和流程管理

**劣势：**
- 灵活性受限，复杂工作流不够灵活
- 对底层模型的控制力较弱

### 低代码平台（扣子/Coze）

**优势：**
- 零代码搭建 Agent，快速验证
- 内置大量插件和工具
- 适合非技术人员

**劣势：**
- 定制化能力有限
- 不适合生产级、需要深入定制的场景
- 数据安全可控性差

### 选型建议

| 场景 | 推荐框架 |
|------|---------|
| 复杂工作流/状态驱动 | LangGraph |
| 多Agent 对话/协作 | AutoGen |
| 快速原型/简单Agent | CrewAI |
| 非技术人员/快速验证 | 扣子/Coze |
| 需要极致定制 | 手写状态机 |

## 推荐工具/项目

| 项目 | 说明 | 链接 |
|------|------|------|
| LangGraph | 状态驱动 Agent 框架 | [GitHub](https://github.com/langchain-ai/langgraph) |
| AutoGen | 微软多Agent 框架 | [GitHub](https://github.com/microsoft/autogen) |
| CrewAI | 角色化 Agent 协作 | [GitHub](https://github.com/crewAIInc/crewAI) |
| 扣子/Coze | 字节跳动低代码 Agent 平台 | [coze.cn](https://www.coze.cn) |

## 最佳实践

- LangGraph 选 LangChain 生态，CrewAI 选快速验证
- 框架能力不足时，用 Custom Node / Tool 扩展，不换框架
- 低代码平台只适合原型，生产环境用代码框架
- 无论选哪个框架，都需要：错误重试、日志审计、状态持久化

## 关联知识

- [[AI Agent 系统设计核心问题]]
- [[AI编程工具进化：从补全到Agent]]
