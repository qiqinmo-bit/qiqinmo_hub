---
创建时间: 2026-06-13
来源灵感: [[02_灵感分析/2026-06-12_灵感_006]]
关键词: [模型不从指令, RAG, Rerank, AgenticRAG, Memory, Claude Code]
分类: 02_模型与API
---

# 📚 模型指令遵从与 RAG 系统优化

## 概述

AI 工程中的两个核心难题：如何让模型遵循指令，以及如何构建高效的 RAG 系统。本文从面试真题出发，整理实际工程中的解决思路和优化方案。

## 核心内容

### 模型不听话怎么办？

**Badcase 定位流程：**
1. 确认是 Prompt 问题还是模型能力问题
2. Prompt 层面：拆解指令、加示例、明确约束
3. 模型参数：调整 temperature（低=更确定）、top_p、frequency_penalty
4. 后处理：输出格式校验、正则约束、二次校验
5. 流程约束：引入人工确认环节、多轮校验

**证明解决有效：**
- 建立评测数据集，定量对比修正前后
- A/B 测试线上效果
- 注意：反思结果不要污染上下文，避免模型混淆

### Claude Code 分层记忆机制

Claude Code 的 Memory 采用三层架构：
- **项目级规则**：`CLAUDE.md` / `AGENTS.md`，长期稳定的项目规范
- **用户偏好**：个人工作习惯、常用设置
- **会话上下文**：当前对话的短期记忆，用完即弃

**隔离原则：** 层级之间不能污染，项目规则不能被对话内容覆盖

**上下文过长处理：**
- 滑动窗口：丢弃最早的历史
- 摘要压缩：用 LLM 压缩长对话
- 优先级裁剪：保留关键决策记录，丢弃噪音

### RAG 优化实战

**为什么需要 Rerank？**
- 向量检索 Top-K 中可能混入噪声
- Rerank 用更精细的模型重新排序，提高精确度

**Recall@K vs Precision@K 取舍：**
- 需要高召回：增大 K + Rerank 兜底
- 需要高精度：减小 K + 强 Rerank
- 通用推荐：K=20 用 Rerank 取 Top-5

**Top-K 动态调整策略：**
- 根据 query 长度：短 query 多搜，长 query 少搜
- 根据历史效果：记录每个 K 值下的用户满意率
- 根据领域：高精度领域（医疗、法律）用更小的 K

**BM25 vs 向量检索：**
- BM25 精确匹配强，适合专有名词、编号
- 向量检索语义理解强，适合同义改写
- 最佳实践：**混合检索**（Hybrid Search），两个结果合并 Rerank

### Agentic RAG vs 传统 RAG

| 维度 | 传统 RAG | Agentic RAG |
|------|---------|-------------|
| 检索次数 | 1次 | 多轮，根据结果调整 |
| Query处理 | 直接检索 | Query Rewrite 优化 |
| 失败处理 | 返回空 | 调整策略重新检索 |
| 工具使用 | 仅检索 | 可调用多个工具 |

**Query Rewrite 是否算 Agentic？**
- 简单改写不算，Agentic 的关键是：**自主判断检索结果是否满足需求，不满足则调整策略**

**多轮检索设计：**
1. 首轮：Broad retrieval，覆盖范围大
2. 判断：Check 结果是否满足
3. 调整：缩小范围/换关键词/换检索源
4. 深度：对关键点做追问式检索

## 推荐工具/项目

| 项目 | 说明 | 链接 |
|------|------|------|
| Cohere Rerank | 生产级 Rerank 模型 | [cohere.com](https://cohere.com/rerank) |
| BGE-Reranker | 开源 Rerank 模型 | [HuggingFace](https://huggingface.co/BAAI/bge-reranker-v2-m3) |
| LangChain | RAG 全链路框架 | [langchain.com](https://langchain.com) |
| LlamaIndex | 数据索引+RAG 专业框架 | [llamaindex.ai](https://llamaindex.ai) |

## 最佳实践

- 模型不从指令：先从 Prompt 入手，再加后处理，最后上流程约束
- RAG 标配：Embedding + BM25 混合检索 → Rerank
- Agentic RAG 适合复杂多步推理场景，简单问答传统 RAG 就够了
- Memory 分层：Rule > Preference > Context，严格隔离

## 关联知识

- [[RAG 系统设计与优化]]
- [[短期记忆与长期记忆：GraphRAG 方案]]
- [[AI Agent 系统设计核心问题]]
