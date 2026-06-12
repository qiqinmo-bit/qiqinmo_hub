---
创建时间: 2026-06-13
来源灵感: [[02_灵感分析/2026-06-12_AI模型选择建议]]
关键词: [GPT, Claude, Gemini, DeepSeek, MiniMax, 模型选型, GLM]
分类: 02_模型与API
---

# 📚 AI 模型选型场景指南

## 概述

根据不同使用场景、地区、成本约束下的 AI 模型选择策略。汇总社区一线开发者的实际选型经验，覆盖编程、学术、办公、中文处理等场景。

## 核心内容

### 编程场景

| 条件 | 推荐模型 | 理由 |
|------|---------|------|
| 有 Opus 访问权限 | Claude Opus | 代码理解和生成能力最强 |
| 香港 IP | GPT-5.5 | 可通过香港节点访问 |
| 国内直连 | GLM-5α.1 (智谱) | 国产模型编程能力领先 |
| 写网页/前端 | Gemini 3.1 Pro | 前端代码生成质量好 |
| 学术编程 | GPT-5.5 thinking | 推理能力强，适合科研 |

### 学术研究

- **医学/科研**：Gemini 3.1 Pro 适合文献分析，但有时会"耍小花招"（编造内容）
- **严谨推理**：GPT-5.5 thinking 更可靠，适合需要严格推理的场景
- **学术写作**：Claude 系列在长文档处理上表现好

### 办公与学生场景

- **国内办公首选**：Kimi（月之暗面），长文本能力强
- **指令服从/格式输出**：MiniMax，适合结构化输出要求高的场景
- **中文语言处理**：DeepSeek V4，中文理解和生成质量优秀

### 多维度选型矩阵

| 维度 | 最佳选择 | 备选 |
|------|---------|------|
| 代码质量 | Opus > GPT-5.5 > GLM-5α.1 | Gemini 3.1 Pro |
| 中文理解 | DeepSeek V4 > GLM > Kimi | MiniMax |
| 格式输出 | MiniMax > GPT-4o | Claude Haiku |
| 长文本 | Kimi > Gemini > Claude | GPT-5.5 |
| 成本最低 | DeepSeek V4 | MiniMax |
| 速度最快 | GPT-4o-mini | Claude Haiku |
| 推理最强 | o1/o3 > GPT-5.5 thinking | Claude Opus |

## 推荐工具/项目

| 项目 | 说明 | 链接 |
|------|------|------|
| DeepSeek V4 | 中文最优，性价比极高 | [chat.deepseek.com](https://chat.deepseek.com) |
| MiniMax | 指令服从和格式输出优秀 | [minimax.com](https://minimax.com) |
| Kimi | 国内长文本办公首选 | [kimi.moonshot.cn](https://kimi.moonshot.cn) |
| GLM-5α.1 | 智谱国产编程模型 | [zhipu.ai](https://zhipu.ai) |

## 最佳实践

- **多模型备用**：至少准备 2-3 个模型的 API Key，一个故障立即切换
- **场景专精**：编程用编程强的模型，写作用写作强的，不追求"全能模型"
- **成本分层**：日常简单任务用小模型/便宜模型，复杂任务用旗舰模型
- **国内网络**：香港 IP 可访问大部分海外模型，直连推荐国产模型
- **定期重评**：模型能力更新快，每季度重新评估一次选型

## 关联知识

- [[RAG 系统设计与优化]]
- [[短期记忆与长期记忆：GraphRAG 方案]]
