# 🧠 已安装 Skills 总览

> 共 **160+** 个技能，来源：mattpocock (31) + superpowers (19) + anthropics (93) + trailofbits (27) + other (6)

---

## 目录

- [按场景速查](#按场景速查)
- [mattpocock/skills — 日常工程技能](#1-mattpocockskills--日常工程技能)
- [obra/superpowers — 编程方法论](#2-obrasuperpowers--编程方法论)
- [anthropics/skills — Anthropic 官方](#3-anthropicsskills--anthropic-官方)
- [trailofbits/skills — 安全审计](#4-trailofbitsskills--安全审计)
- [其他技能](#5-其他技能)

---

## 按场景速查

| 场景 | 推荐技能 | 来源 |
|------|---------|------|
| 🆕 **启动对话** | `/using-superpowers` | superpowers |
| 🎯 **明确需求** | `/grill-me` / `/ask-questions-if-underspecified` | mattpocock / superpowers |
| 📝 **写计划** | `/writing-plans` / `/to-prd` | superpowers / mattpocock |
| 🔨 **写代码** | `/tdd` / `/executing-plans` | superpowers / mattpocock |
| 🐛 **调试** | `/diagnose` / `/systematic-debugging` | mattpocock / superpowers |
| 👁️ **代码审查** | `/review` / `/receiving-code-review` | superpowers |
| 🛡️ **安全审计** | `/c-review` / `/security-threat-model` | trailofbits |
| 🔄 **重构** | `/improve-codebase-architecture` / `/request-refactor-plan` | mattpocock |
| 🧪 **测试** | `/tdd` / `/property-based-testing` | superpowers / trailofbits |
| 📊 **拆 Issue** | `/to-issues` / `/triage` | mattpocock |
| 🗣️ **极简模式** | `/caveman` | mattpocock |
| 🚀 **部署** | `/vercel-deploy` / `/netlify-deploy` | anthropics |
| 🎨 **前端设计** | `/frontend-design` / `/figma-use` | anthropics |
| 📄 **文档** | `/docx` / `/pptx` / `/xlsx` | anthropics |

---

## 1. mattpocock/skills — 日常工程技能

**来源**: [github.com/mattpocock/skills](https://github.com/mattpocock/skills) ⭐126k

### 核心工作流

| 技能 | 说明 |
|------|------|
| `/grill-me` | 被 AI 连环追问设计方案，逐条决策树走完 |
| `/grill-with-docs` | 同上 + 建立领域语言、更新 CONTEXT.md 和 ADR |
| `/to-prd` | 把当前讨论转为 PRD 并提交为 GitHub Issue |
| `/to-issues` | 把计划/PRD 拆成可独立执行的 GitHub Issues |
| `/triage` | 用状态机分类 Issue（标签：待评估/待回复/AI可处理/需人工/不处理） |
| `/setup-matt-pocock-skills` | 初始化项目配置（已运行） |

### 代码开发

| 技能 | 说明 |
|------|------|
| `/tdd` | 红绿重构 TDD 循环，逐个垂直切片构建功能 |
| `/diagnose` | 系统性调试：复现→最小化→假设→验证→修复→回归测试 |
| `/prototype` | 快速原型验证（终端/多 UI 方案切换） |
| `/improve-codebase-architecture` | 基于 CONTEXT.md + ADR 发现架构改进机会 |
| `/zoom-out` | 俯瞰不熟悉的代码模块，让 AI 给高层解释 |
| `/review` | 审查从指定点（commit/branch/tag）起的变更 |
| `/receiving-code-review` | 收到审查反馈后，理解意图再改，而不是盲目点掉 |
| `/requesting-code-review` | 完成功能后生成结构化的审查请求 |
| `/qa` | 交互式 QA 会话，用户报 bug，AI 系统化诊断 |

### 效率和工具

| 技能 | 说明 |
|------|------|
| `/caveman` | 极简模式，省 ~75% token，同时保持技术准确 |
| `/handoff` | 把当前对话压缩成交接文档，让另一个 agent 继续 |
| `/teach` | 多轮教学，在当前目录创建教学工作区 |
| `/write-a-skill` | 按照最佳实践创建新技能 |
| `/design-an-interface` | 用并行探索生成多个极端不同的接口设计 |
| `/ubiquitous-language` | 从对话中提取 DDD 通用语言词汇表 |
| `/setup-pre-commit` | 配置 Husky + Prettier + 类型检查 + 测试预提交钩子 |

### 内容创作

| 技能 | 说明 |
|------|------|
| `/writing-beats` | 用"节拍"构建文章，类选择你自己的冒险 |
| `/writing-fragments` | 从用户碎片化想法中挖掘写作素材 |
| `/writing-shape` | 把原始素材塑造成文章 |
| `/edit-article` | 重构文章结构、提升清晰度 |
| `/obsidian-vault` | 搜索、创建、管理 Obsidian 笔记 |

### 其他

| 技能 | 说明 |
|------|------|
| `/git-guardrails-claude-code` | 设置 git hooks 阻止危险命令（push/reset --hard/clean） |
| `/scaffold-exercises` | 创建练习目录结构（章节/问题/解答/讲解） |
| `/migrate-to-shoehorn` | 从 `as` 类型断言迁移到 `@total-typescript/shoehorn` |
| `/request-refactor-plan` | 通过用户访谈创建细粒度重构计划 |

---

## 2. obra/superpowers — 编程方法论

**来源**: [github.com/obra/superpowers](https://github.com/obra/superpowers) ⭐13.5k

### 启动入口

| 技能 | 说明 |
|------|------|
| `/using-superpowers` | **必须先用这个！** 建立工作方式，告诉 AI 如何找技能、问需求、写计划 |

### 需求澄清

| 技能 | 说明 |
|------|------|
| `/brainstorming` | 创意工作前必用——头脑风暴特性、组件、方法 |
| `/define-goal` | 帮用户定义具体、可衡量的目标 |
| `/ask-questions-if-underspecified` | 实现前澄清模糊的需求 |
| `/let-fate-decide` | 🔮 用塔罗牌给计划注入随机熵 |

### 计划与执行

| 技能 | 说明 |
|------|------|
| `/writing-plans` | 拿到需求后，写多步骤执行计划 |
| `/executing-plans` | 按照书面计划在独立 session 中执行 |
| `/subagent-driven-development` | 用子 agent 并行执行独立任务 |
| `/dispatching-parallel-agents` | 2+ 无共享状态的任务并行调度 |
| `/finishing-a-development-branch` | 实现完成后的收尾：提交、PR、二维码 |

### 开发辅助

| 技能 | 说明 |
|------|------|
| `/test-driven-development` | 红绿重构，先写测试再写实现 |
| `/systematic-debugging` | 遇到 bug 时的结构化调试流程 |
| `/verification-before-completion` | 声称完成前，先系统验证 |
| `/gh-fix-ci` | 调试 GitHub PR Checks 失败 |
| `/gh-address-comments` | 处理当前分支的 PR/Issue 评论 |
| `/using-git-worktrees` | 用 git worktree 隔离特性开发 |

### 代码质量

| 技能 | 说明 |
|------|------|
| `/review` | 审查变更（同 mattpocock） |
| `/receiving-code-review` | 收到审查反馈时使用 |
| `/requesting-code-review` | 请求审查时使用 |
| `/second-opinion` | 用外部 LLM（OpenAI/Gemini）对未提交代码做二次审查 |
| `/sharp-edges` | 识别易出错的 API、危险配置和陷阱设计 |
| `/writing-skills` | 创建/编辑/验证 AI 技能 |

---

## 3. anthropics/skills — Anthropic 官方

**来源**: [github.com/anthropics/skills](https://github.com/anthropics/skills) (官方)

### 前端与设计

| 技能 | 说明 |
|------|------|
| `/frontend-design` | 独特、有意的视觉设计指导 |
| `/web-artifacts-builder` | 创建复杂的多组件 HTML 页面 |
| `/figma-use` | **必用前提** — 调用 Figma MCP 前先用这个 |
| `/figma-implement-design` | Figma 设计稿 → 生产代码，1:1 视觉还原 |
| `/figma-generate-library` | 从代码库构建或更新专业设计系统 |
| `/figma-create-design-system-rules` | 生成自定义设计系统规则 |
| `/brand-guidelines` | 应用 Anthropic 官方品牌色和排版 |
| `/canvas-design` | 用设计哲学创建漂亮的 .png/.pdf 视觉作品 |
| `/algorithmic-art` | 用 p5.js 创建算法艺术 |
| `/theme-factory` | 为幻灯片/文档/页面定制主题风格 |

### 浏览器与测试

| 技能 | 说明 |
|------|------|
| `/playwright` | 浏览器自动化（导航、点击、截图、数据抓取） |
| `/playwright-interactive` | 持久浏览器交互，通过 `js_repl` 快速迭代 |
| `/webapp-testing` | 用 Playwright 测试本地 Web 应用 |

### 文档与 Office

| 技能 | 说明 |
|------|------|
| `/docx` | 创建/读取/编辑 Word 文档 |
| `/xlsx` | 创建/读取/编辑 Excel 电子表格 |
| `/pptx` | 创建/读取/编辑 PowerPoint |
| `/pdf` | 读取/创建/审查 PDF |
| `/jupyter-notebook` | 创建/编辑 Jupyter Notebook |

### MCP 与 API

| 技能 | 说明 |
|------|------|
| `/mcp-builder` | 创建高质量的 MCP Server |
| `/cli-creator` | 从 API 文档/OpenAPI 规范生成 CLI 工具 |
| `/openai-docs` | 查询 OpenAI 产品和 API 用法 |
| `/claude-api` | 查询 Claude API 用法 |

### 部署与基础设施

| 技能 | 说明 |
|------|------|
| `/vercel-deploy` | 部署到 Vercel |
| `/netlify-deploy` | 部署到 Netlify |
| `/cloudflare-deploy` | 部署到 Cloudflare (Workers/Pages) |
| `/render-deploy` | 部署到 Render |
| `/devcontainer-setup` | 创建 Dev Container（Python/Node/Rust/Go + Claude Code） |

### 项目管理

| 技能 | 说明 |
|------|------|
| `/linear` | 管理 Linear 上的 Issues/Projects |
| `/sentry` | 查看 Sentry 错误和性能问题 |
| `/notion-knowledge-capture` | 把对话和决策写到 Notion |
| `/notion-meeting-intelligence` | 用 Notion 上下文准备会议 |
| `/notion-research-documentation` | 跨 Notion 搜索并综合成文档 |
| `/notion-spec-to-implementation` | Notion 规格 → 实现计划 |
| `/internal-comms` | 撰写内部沟通文档 |

### 多媒体

| 技能 | 说明 |
|------|------|
| `/imagegen` | 生成/编辑光栅图像 |
| `/speech` | 文字转语音 |
| `/transcribe` | 音频转文字（支持说话人分离） |
| `/screenshot` | 桌面/系统截图 |
| `/slack-gif-creator` | 创建适合 Slack 的动画 GIF |

### 语言与框架

| 技能 | 说明 |
|------|------|
| `/modern-python` | 现代 Python 项目配置（uv/ruff/ty） |
| `/aspnet-core` | ASP.NET Core Web 应用开发 |
| `/winui-app` | WinUI 3 桌面应用开发 |
| `/chatgpt-apps` | ChatGPT Apps SDK 开发 |
| `/migrate-to-codex` | 迁移配置到 Codex |

---

## 4. trailofbits/skills — 安全审计

**来源**: [github.com/trailofbits/skills](https://github.com/trailofbits/skills) (Trail of Bits 安全公司)

### 代码安全审查

| 技能 | 说明 |
|------|------|
| `/c-review` | C/C++ 安全审查：内存破坏、整数溢出、注入等 |
| `/code-maturity-assessor` | 9 维度代码成熟度评估（Trail of Bits 框架） |
| `/audit-context-building` | 逐行代码分析，建立深层架构上下文 |
| `/audit-prep-assistant` | 用 Trail of Bits 检查清单准备安全审查 |
| `/fp-check` | 系统验证疑似安全 bug，消除误报 |
| `/supply-chain-risk-auditor` | 识别高危依赖（接管/利用风险） |
| `/entry-point-analyzer` | 分析智能合约的 state-changing 入口点 |

### 智能合约安全

| 技能 | 说明 |
|------|------|
| `/algorand-vulnerability-scanner` | Algorand 合约扫描（11 种漏洞） |
| `/cairo-vulnerability-scanner` | Cairo/StarkNet 合约扫描（6 种漏洞） |
| `/cosmos-vulnerability-scanner` | Cosmos SDK / CosmWasm 扫描 |
| `/solana-vulnerability-scanner` | Solana 程序扫描（6 种漏洞） |
| `/substrate-vulnerability-scanner` | Substrate/Polkadot Pallet 扫描 |
| `/ton-vulnerability-scanner` | TON 合约扫描（3 种漏洞） |
| `/token-integration-analyzer` | Token 集成分析 |
| `/spec-to-code-compliance` | 验证代码是否按文档实现 |
| `/mermaid-to-proverif` | Mermaid 协议图 → ProVerif 形式化验证 |

### 工具链

| 技能 | 说明 |
|------|------|
| `/codeql` | CodeQL 查询编写 |
| `/semgrep` | Semgrep 规则编写 |
| `/semgrep-rule-creator` | 创建自定义 Semgrep 规则 |
| `/semgrep-rule-variant-creator` | 把已有 Semgrep 规则移植到其他语言 |
| `/yara-rule-authoring` | YARA 恶意软件检测规则 |
| `/trailmark` | 多语言源码图构建（安全分析用） |
| `/trailmark-structural` | Trailmark 结构化分析 |
| `/sarif-parsing` | SARIF 格式解析 |

### 模糊测试

| 技能 | 说明 |
|------|------|
| `/aflpp` | AFL++ 模糊测试 |
| `/libfuzzer` | libFuzzer 配置/运行 |
| `/cargo-fuzz` | Rust cargo-fuzz |
| `/ossfuzz` | OSS-Fuzz 集成 |
| `/fuzzing-dictionary` | 模糊测试字典生成 |
| `/fuzzing-obstacles` | 模糊测试障碍分析 |

### 密码学与安全最佳实践

| 技能 | 说明 |
|------|------|
| `/constant-time-analysis` | 检测密码学代码中的 timing 侧信道 |
| `/constant-time-testing` | 常量时间测试 |
| `/property-based-testing` | 属性测试指导 |
| `/zeroize-audit` | 检测敏感数据未清零问题 |
| `/insecure-defaults` | 检测 fail-open 不安全默认值 |
| `/wycheproof` | Wycheproof 密码学测试 |
| `/dimensional-analysis` | 安全协议的维度分析 |
| `/differential-review` | 差异代码审查 |
| `/mutation-testing` | 变异测试配置 |

### 威胁建模

| 技能 | 说明 |
|------|------|
| `/security-threat-model` | 基于仓库的威胁建模（信任边界/资产/攻击者/缓解措施） |
| `/agentic-actions-auditor` | 审计 GitHub Actions AI Agent 集成安全 |
| `/firebase-apk-scanner` | 扫描 Android APK 的 Firebase 安全配置 |
| `/secure-workflow-guide` | Trail of Bits 5 步安全开发工作流 |
| `/security-best-practices` | 语言/框架特定安全最佳实践 |
| `/security-ownership-map` | 构建人员→文件安全归属拓扑 |
| `/variant-analysis` | 基于模式的漏洞变体分析 |

---

## 5. 其他技能

| 技能 | 来源 | 说明 |
|------|------|------|
| `/gh-cli` | 通用 | 强制用已验证的 gh CLI 而非 curl |
| `/git-cleanup` | 通用 | 安全清理本地 git 分支和 worktree |
| `/burpsuite-project-parser` | 通用 | 搜索和探索 Burp Suite 项目文件 |
| `/plugin-creator` | 通用 | 创建 Codex 插件目录 |
| `/designing-workflow-skills` | 通用 | 设计工作流技能 |
| `/differential-review` | 通用 | 差异代码审查 |

---

## 快速开始

```bash
# 第一步：启动 superpowers 工作流
/using-superpowers

# 第二步：被 AI 追问明确需求
/grill-me

# 第三步：写执行计划
/writing-plans

# 第四步：TDD 开发
/tdd

# 第五步：代码审查
/review
```

> 所有技能文件位于 `.agents/skills/`，可直接查看 SKILL.md 了解详情。
