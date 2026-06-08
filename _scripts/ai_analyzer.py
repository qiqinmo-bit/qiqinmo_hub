# encoding: utf-8
"""
AI 分析引擎 — 三档回退策略

在 GitHub Actions 中自动分析灵感内容，按优先级依次尝试：

  1️⃣ GitHub Models (免费)    — 使用 GITHUB_TOKEN，零成本
  2️⃣ DeepSeek (低价)          — 使用 DEEPSEEK_API_KEY
  3️⃣ OpenAI (付费)            — 使用 OPENAI_API_KEY，兜底

用法:
  python _scripts/ai_analyzer.py --prompt "分析这段文字..." [--mode full|quick]
  python _scripts/ai_analyzer.py --file description.md [--mode full|quick]

输出 JSON:
  {
    "success": true,
    "tier": "github_models" | "deepseek" | "openai",
    "model": "gpt-4o-mini" | "deepseek-chat" | "gpt-4o",
    "content": "分析结果文本...",
    "keywords": ["关键词1", "关键词2"],
    "category": "建议分类"
  }
"""

import sys, os, json, re

# ── 模型配置 ────────────────────────────────────────

TIERS = [
    {
        "name": "github_models",
        "label": "GitHub Models (免费)",
        "endpoint": "https://models.inference.ai.azure.com/chat/completions",
        "model": "gpt-4o-mini",
        "api_key": os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"),
        "headers": {
            "Content-Type": "application/json",
        }
    },
    {
        "name": "deepseek",
        "label": "DeepSeek (低价)",
        "endpoint": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-chat",
        "api_key": os.environ.get("DEEPSEEK_API_KEY"),
        "headers": {
            "Content-Type": "application/json",
        }
    },
    {
        "name": "openai",
        "label": "OpenAI (付费兜底)",
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-4o",
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "headers": {
            "Content-Type": "application/json",
        }
    }
]

# ── 分类关键词（同 process_inspiration.py）───────────

CATEGORY_KEYWORDS = {
    "01_Agent与AI编程": ["cursor", "agent", "copilot", "ai编程", "代码生成", "function calling", "tool use"],
    "02_模型与API": ["gpt", "claude", "gemini", "llama", "api", "token", "微调", "embedding", "rag"],
    "03_工作流与自动化": ["n8n", "自动化", "workflow", "github actions", "爬虫", "pipeline"],
    "04_提示词工程": ["prompt", "提示词", "few-shot", "chain-of-thought", "cot"],
    "05_多模态与工具链": ["多模态", "vision", "whisper", "langchain", "dify"],
}

DEFAULT_CATEGORY = "03_工作流与自动化"


def suggest_category(text: str) -> str:
    text_lower = text.lower()
    scores = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        if score > 0:
            scores[cat] = score
    return max(scores, key=scores.get) if scores else DEFAULT_CATEGORY


def extract_keywords(text: str, max_kw: int = 5) -> list:
    """从文本中提取关键词（简单实现，取长词）。"""
    # 去掉标点，按空格/换行切分
    words = re.split(r'[\s,，。.、:：;；!！?？()（）\[\]【】{}]', text)
    # 去重，保留 2-10 个字符的词，按长度排序
    candidates = sorted(
        set(w for w in words if 2 <= len(w) <= 15 and not w.isdigit()),
        key=len, reverse=True
    )
    return candidates[:max_kw] if candidates else ["待分析"]


# ── 调用 API ────────────────────────────────────────

def call_llm(tier: dict, prompt: str, mode: str = "quick") -> dict:
    """调用指定 tier 的 LLM API，返回响应 JSON。"""
    if not tier["api_key"]:
        return {"success": False, "error": f"{tier['name']}: API key 未配置"}

    system_prompt = (
        "你是一个 AI 编程/工具知识分析助手。"
        if mode == "quick"
        else "你是一个资深技术分析师。请详细分析以下灵感内容，输出包含：核心观点、技术栈、实现路径。"
    )

    payload = {
        "model": tier["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"分析以下内容，给出技术要点总结、建议分类和关键词：\n\n{prompt}"}
        ],
        "temperature": 0.3,
        "max_tokens": 1000 if mode == "quick" else 2000,
    }

    headers = {**tier["headers"], "Authorization": f"Bearer {tier['api_key']}"}

    try:
        import urllib.request
        data = json.dumps(payload).encode()
        req = urllib.request.Request(tier["endpoint"], data=data, headers=headers, method="POST")
        resp = urllib.request.urlopen(req, timeout=60)
        result = json.loads(resp.read().decode())
        content = result["choices"][0]["message"]["content"]
        return {"success": True, "content": content}
    except Exception as e:
        return {"success": False, "error": f"{tier['name']}: {e}"}


# ── 主流程：三档回退 ────────────────────────────────

def analyze(prompt: str, mode: str = "quick") -> dict:
    """按优先级依次尝试各 tier，返回第一个成功的结果。"""
    last_error = None
    used_tier = None
    content = None

    for tier in TIERS:
        print(f"  🔄 尝试 {tier['label']} ({tier['model']})...", file=sys.stderr)
        result = call_llm(tier, prompt, mode)
        if result["success"]:
            content = result["content"]
            used_tier = tier
            print(f"  ✅ {tier['label']} 成功", file=sys.stderr)
            break
        else:
            last_error = result["error"]
            print(f"  ⚠️  {result['error']}", file=sys.stderr)

    if content is None:
        # 全部失败，用规则兜底
        print(f"  ⚠️  API 全部失败，使用规则兜底", file=sys.stderr)
        return {
            "success": True,
            "tier": "rule_fallback",
            "model": "none",
            "content": f"[规则分析] {prompt[:200]}...",
            "keywords": extract_keywords(prompt),
            "category": suggest_category(prompt),
            "error": last_error
        }

    # 从 LLM 响应中提取关键词和分类
    keywords = extract_keywords(content)
    category = suggest_category(prompt + "\n" + content)

    return {
        "success": True,
        "tier": used_tier["name"],
        "model": used_tier["model"],
        "content": content,
        "keywords": keywords,
        "category": category
    }


# ── CLI 入口 ────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI 自动分析脚本——三档回退")
    parser.add_argument("--prompt", help="直接提供分析文本")
    parser.add_argument("--file", help="从文件读取分析文本")
    parser.add_argument("--mode", choices=["quick", "full"], default="quick",
                        help="quick=快速摘要(默认), full=详细分析")
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径")
    args = parser.parse_args()

    # 获取输入文本
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            prompt = f.read()
    elif args.prompt:
        prompt = args.prompt
    else:
        # 从 stdin 读取
        prompt = sys.stdin.read()

    if not prompt or not prompt.strip():
        print(json.dumps({"success": False, "error": "未提供分析文本"}))
        sys.exit(1)

    result = analyze(prompt.strip(), mode=args.mode)
    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"结果已保存: {args.output}")
    else:
        print(output)
