---
创建时间: 2026-06-13
来源灵感: [[02_灵感分析/2026-06-12_灵感_001]]
关键词: [Agent, Tool Calling, 多Agent, 状态管理, 面试]
分类: 01_Agent与AI编程
---

# 📚 AI Agent 系统设计核心问题

## 概述

从字节跳动 AI Agent 二面真题中提炼的 Agent 系统设计核心问题清单，涵盖工作流拆解、Tool Calling 设计、多Agent 协作、模型指令遵从等关键考点。

## 核心内容

### 1. Agent 工作流设计

**确定性 Workflow vs LLM 决策节点的划分原则：**
- 确定性节点：数据清洗、格式校验、权限检查、日志记录等规则明确的操作
- LLM 决策节点：意图识别、内容生成、代码编写、方案选择等需要理解的场景
- 关键：明确失败分支和重试机制，LLM 决策节点必须有超时 + 降级策略

### 2. 状态管理

Agent 状态的保存与恢复是系统稳定的基础：
- **会话状态**：Redis/数据库持久化，支持断点续跑
- **中间状态**：LLM 调用过程中的 partial result 需要缓存
- **审计日志**：每次 Agent 决策和操作都记录，便于调试

### 3. Tool Calling 设计

**Schema 设计原则：**
- 输入输出参数必须有明确类型约束和校验规则
- 工具描述要精确，避免歧义导致模型误调用
- 参数错误兜底：参数校验前置 + 失败时返回明确错误码

**安全措施：**
- 危险工具隔离：敏感操作走服务端审批/二次确认
- Tool 分发架构：推荐通过服务端做分发，不直接暴露给模型
- 调用频率限制和并发控制

### 4. 多Agent 协作

**分工与通信：**
- 明确 Agent 职责边界，避免功能重叠
- 通过共享状态/消息队列通信
- Leader Agent 协调+终止机制防止死循环

### 5. 模型指令遵从

**Badcase 定位流程：**
1. 区分是 Prompt 问题还是模型能力问题
2. Prompt 层面：清晰指令 + 示例 + 约束条件
3. 后处理层面：输出校验 + 格式约束
4. 流程层面：人工确认环节 + 降级策略

## 推荐工具/项目

| 项目 | 说明 | 链接 |
|------|------|------|
| LangGraph | 状态驱动 Agent 框架，State/Node/Edge 模型 | [GitHub](https://github.com/langchain-ai/langgraph) |
| AutoGen | 微软多Agent 对话框架 | [GitHub](https://github.com/microsoft/autogen) |
| CrewAI | 角色化多Agent 协作 | [GitHub](https://github.com/crewAIInc/crewAI) |

## 关键代码/配置

```python
# Tool Schema 示例
tool_schema = {
    "name": "search_knowledge",
    "description": "搜索知识库获取相关信息",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词"}
        },
        "required": ["query"]
    }
}
```

## 最佳实践

- Agent 工作流：确定性节点用代码实现，不确定性节点交给 LLM
- Tool Calling 必须做输入校验和失败重试，不能信任模型输出
- 多Agent 场景：明确 Leader-Follower 关系，Leader 负责终止决策
- 状态管理：会话级状态存 Redis，任务级状态存 DB，审计日志 append-only
- Prompt vs 模型能力：建立测试用例集，定期回归

## 关联知识

- [[LangGraph vs AutoGen：Agent 框架选型]]
- [[AI编程工具进化：从补全到Agent]]
- [[RAG 系统设计与优化]]
