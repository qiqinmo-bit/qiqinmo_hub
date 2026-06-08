# encoding: utf-8
"""
灵感处理核心脚本 — 支持三层架构：

  1. 手动模式 (CLI)         — 原有流程，逐步处理灵感
  2. n8n 驱动模式 (--n8n)   — 接收 n8n webhook JSON，自动入库
  3. GitHub Actions 模式    — push 后自动更新索引 + 图谱

用法:
  python _scripts/process_inspiration.py status          # 查看知识库状态
  python _scripts/process_inspiration.py --n8n payload.json   # n8n webhook 输入
  python _scripts/process_inspiration.py --ocr 图片路径       # OCR + 自动入库
  python _scripts/process_inspiration.py --auto              # GitHub Actions 自动更新
"""

import sys, os, json, datetime, subprocess, re

sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── 工具函数 ────────────────────────────────────────

def today():
    return datetime.date.today().isoformat()

def slug(text):
    """将文本转为适合做文件夹名的格式。"""
    s = text.strip()
    # 替换非法文件名字符
    s = re.sub(r'[\\/:*?"<>|]', '_', s)
    s = s.replace(' ', '_').replace('\n', '_')
    return s[:60]

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

# ── 自动分类 ────────────────────────────────────────

CATEGORY_KEYWORDS = {
    "01_Agent与AI编程": [
        "cursor", "codex", "autogpt", "agent", "copilot", "codeium",
        "ai编程", "代码生成", "自动编程", "agent框架", "multi-agent",
        "llm agent", "function calling", "tool use", "react",
    ],
    "02_模型与API": [
        "gpt", "claude", "gemini", "llama", "qwen", "deepseek",
        "api", "token", "prompt cost", "模型对比", "微调", "fine-tune",
        "embedding", "vector", "RAG", "检索增强",
    ],
    "03_工作流与自动化": [
        "n8n", "zapier", "make.com", "自动化", "workflow", "pipeline",
        "ci/cd", "github actions", "auto", "定时", "爬虫", "crawler",
        "rpa", "浏览器自动化", "playwright", "selenium",
    ],
    "04_提示词工程": [
        "prompt", "提示词", "system prompt", "few-shot", "chain-of-thought",
        "cot", "role-play", "提示工程", "结构化提示", "prompt template",
    ],
    "05_多模态与工具链": [
        "多模态", "multimodal", "vision", "image", "video", "audio",
        "whisper", "stable diffusion", "sora", "tts", "stt",
        "langchain", "llamaindex", "semantic kernel", "dify",
    ],
}

DEFAULT_CATEGORY = "03_工作流与自动化"

def suggest_category(text: str) -> str:
    """根据文本内容自动推荐分类。"""
    text_lower = text.lower()
    scores = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        if score > 0:
            scores[cat] = score
    if scores:
        return max(scores, key=scores.get)
    return DEFAULT_CATEGORY

# ── Step 1: 保存原始灵感 ────────────────────────────

def save_inspiration(screenshot_path=None, title="未命名灵感", source_desc="", ocr_text=""):
    """
    保存原始灵感。
    如果提供了截图路径且未安装 OCR，会尝试调用 ocr_helper。
    """
    date = today()
    folder_name = f"{date}_{slug(title)}"
    folder = os.path.join(BASE, "01_原始灵感", folder_name)
    ensure_dir(folder)

    # 如果有截图路径，复制图片
    if screenshot_path and os.path.exists(screenshot_path):
        import shutil
        fname = os.path.basename(screenshot_path)
        dest = os.path.join(folder, fname)
        if not os.path.exists(dest):
            shutil.copy2(screenshot_path, dest)
            print(f"  📸 图片已复制: {dest}")

    # 组装描述文本
    desc_parts = [
        f"# 原始灵感",
        f"",
        f"**日期**: {date}",
        f"**来源**: {source_desc or '手动输入'}",
        f"**主题**: {title}",
        f"---",
        f"## 描述",
        f"",
    ]
    if ocr_text:
        desc_parts.append(f"> 📝 OCR 提取文字：")
        desc_parts.append(f">")
        for line in ocr_text.strip().split("\n"):
            desc_parts.append(f"> {line}")
        desc_parts.append("")
    if source_desc:
        desc_parts.append(source_desc)

    desc_path = os.path.join(folder, "description.md")
    with open(desc_path, "w", encoding="utf-8") as f:
        f.write("\n".join(desc_parts))

    print(f"  ✅ 灵感已保存: {folder}")
    return folder

# ── Step 2-3: 创建分析文档 ──────────────────────────

def create_analysis(title, date, source, key_points, tech_stack,
                    steps, opensource_projects, keywords, related_knowledge):
    """创建灵感分析文档。"""
    folder_name = f"{date}_{slug(title)}"
    folder = os.path.join(BASE, "02_灵感分析", folder_name)
    ensure_dir(folder)

    points = "\n".join(f"- {p}" for p in key_points)
    tech = "\n".join(f"- {t}" for t in tech_stack)
    impl_steps = "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
    projects = "\n".join(
        f"| {p[0]} | {p[1]} | {p[2]} | {p[3]} |"
        for p in opensource_projects
    )
    kws = " ".join(f"`{k}`" for k in keywords)
    rel = "\n".join(f"- [[{r}]]" for r in related_knowledge)

    content = f"""# 📝 灵感分析文档

**日期**: {date}
**来源**: {source}
**主题**: {title}

---

## 1️⃣ 核心观点

{points}

## 2️⃣ 技术栈

{tech}

## 3️⃣ 实现步骤

{impl_steps}

## 4️⃣ 开源项目搜索

| 项目 | 功能 | 链接 | 匹配度 |
|------|------|------|--------|
{projects}

## 5️⃣ 关键词

{kws}

## 6️⃣ 关联知识

{rel}
"""
    path = os.path.join(folder, "analysis.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.lstrip("\n"))
    print(f"  ✅ 分析文档已创建: {path}")
    return path

# ── Step 4: 创建知识文档 ────────────────────────────

def create_knowledge_doc(category, title, overview, content_body, keywords, source_ref):
    """创建结构化知识文档。"""
    folder = os.path.join(BASE, "03_知识文档", category)
    ensure_dir(folder)

    safe_title = slug(title).replace("_", "")
    fname = f"{safe_title}.md"
    kws = ", ".join(keywords)

    content = f"""---
创建时间: {today()}
来源灵感: [[{source_ref}]]
关键词: [{kws}]
分类: {category}
---

# 📚 {title}

## 概述

{overview}

## 实现路径

{content_body}

## 关联知识

"""
    path = os.path.join(folder, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.lstrip("\n"))
    print(f"  ✅ 知识文档已创建: {path}")
    return path

# ── Step 5: 更新知识网络 ────────────────────────────

def update_knowledge_graph(keywords, doc_title, doc_path):
    """更新记忆索引 + 知识图谱。"""
    # 5a. 更新 memory_index.json
    idx_path = os.path.join(BASE, "_memory", "memory_index.json")
    with open(idx_path, "r", encoding="utf-8") as f:
        idx = json.load(f)

    # 统一存储相对路径
    rel_path = os.path.relpath(doc_path, BASE) if os.path.isabs(doc_path) else doc_path
    idx["总条目数"] += 1
    entry = {
        "id": f"entry_{idx['总条目数']:03d}",
        "title": doc_title,
        "path": rel_path,
        "date": today(),
        "keywords": keywords
    }
    idx["条目索引"].append(entry)
    for kw in keywords:
        idx["标签云"][kw] = idx["标签云"].get(kw, 0) + 1
    idx["最后更新"] = today()

    # 更新分类统计
    cat_match = re.search(r"03_知识文档/(\d+_.+?)/", doc_path)
    if cat_match:
        cat = cat_match.group(1)
        if cat in idx["分类统计"]:
            idx["分类统计"][cat] += 1

    with open(idx_path, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 记忆索引已更新 (总计 {idx['总条目数']} 篇)")

    # 5b. 更新 graph_data.json
    graph_path = os.path.join(BASE, "04_知识网络", "graph_data.json")
    with open(graph_path, "r", encoding="utf-8") as f:
        g = json.load(f)

    node_id = f"n{len(g['nodes']) + 1:03d}"
    g["nodes"].append({
        "id": node_id,
        "label": doc_title,
        "keywords": keywords,
        "path": rel_path,
        "date": today()
    })

    # 关键词节点之间的关联
    for kw in keywords:
        kw_id = f"kw_{kw}"
        # 如果关键词节点还不存在，创建它
        if not any(n["id"] == kw_id for n in g["nodes"]):
            g["nodes"].append({
                "id": kw_id,
                "label": f"#{kw}",
                "keywords": [kw],
                "path": None,
                "date": today()
            })
        g["edges"].append({
            "from": node_id,
            "to": kw_id,
            "label": kw
        })

    g["last_updated"] = today()
    with open(graph_path, "w", encoding="utf-8") as f:
        # ★ 修复原版 bug: 原来是 json.dump(g, g, ...) 写错了文件句柄
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 知识图谱已更新 ({len(g['nodes'])} 节点, {len(g['edges'])} 关联)")

# ── n8n Webhook 处理 ──────────────────────────────

def process_n8n_payload(payload: dict):
    """
    处理 n8n 发来的 webhook JSON。

    期望格式:
    {
        "source": "bilibili" | "youtube" | "manual",
        "url": "https://...",
        "title": "视频标题或灵感主题",
        "text": "提取的评论/正文内容",
        "tags": ["关键词1", "关键词2"],
        "screenshot_path": "可选截图路径"
    }
    """
    title = payload.get("title", "未命名灵感")
    source = payload.get("source", "n8n")
    text = payload.get("text", "")
    url = payload.get("url", "")
    tags = payload.get("tags", [])
    screenshot = payload.get("screenshot_path")

    source_desc = f"来源: {source}"
    if url:
        source_desc += f"\n链接: {url}"

    # Step 1: 保存原始灵感
    insp_folder = save_inspiration(
        screenshot_path=screenshot,
        title=title,
        source_desc=source_desc,
        ocr_text=text
    )

    # Step 2: 建议分类
    category = suggest_category(title + " " + text)
    print(f"  💡 建议分类: {category}")

    # Step 3: 自动更新记忆索引（标注为待 AI 处理）
    auto_keywords = tags or [source, "待分析"]
    update_knowledge_graph(
        keywords=auto_keywords,
        doc_title=f"[待分析] {title}",
        doc_path=insp_folder
    )

    print(f"\n🎉 n8n 数据已入库！AI 将在下次交互时继续分析。")
    return insp_folder


def process_ocr_auto(image_path: str):
    """OCR 图片后自动入库（等待 AI 分析）。"""
    try:
        from _scripts.ocr_helper import ocr_image, ocr_directory
    except ImportError:
        print("⚠️  ocr_helper 未找到，尝试相对导入...")
        sys.path.insert(0, BASE)
        from _scripts.ocr_helper import ocr_image, ocr_directory

    if os.path.isdir(image_path):
        result = ocr_directory(image_path)
    else:
        result = ocr_image(image_path)

    if not result["success"]:
        print(f"❌ OCR 失败: {result.get('error')}")
        return None

    text = result.get("text", "")
    source = result.get("source", "ocr")

    title = f"OCR_{today()}"
    # 从文字中提取前 20 个字作为主题
    first_line = text.strip().split("\n")[0][:30] if text else "无文字内容"
    if first_line:
        title = first_line

    insp_folder = save_inspiration(
        screenshot_path=image_path if os.path.isfile(image_path) else None,
        title=title,
        source_desc=f"OCR 自动识别 ({source})",
        ocr_text=text
    )

    category = suggest_category(text)
    print(f"  💡 建议分类: {category}")

    raw_keywords = [source, "待分析"]
    update_knowledge_graph(
        keywords=raw_keywords,
        doc_title=f"[待分析] {title}",
        doc_path=insp_folder
    )

    print(f"\n🎉 OCR 完成！请 AI 继续分析。")
    return insp_folder


# ── Git 辅助 ───────────────────────────────────────

def git_commit(message: str):
    """尝试 git add + commit（在 GitHub Actions 中静默失败）。"""
    try:
        subprocess.run(
            ["git", "add", "-A"],
            cwd=BASE, capture_output=True, check=True
        )
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=BASE, capture_output=True
        )
        if result.returncode != 0:
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=BASE, capture_output=True, check=True
            )
            print(f"  📦 Git 已提交: {message}")
        else:
            print("  ℹ️  无变更需要提交")
    except subprocess.CalledProcessError:
        print("  ℹ️  Git 提交跳过（非 git 仓库或 CI 环境）")
    except FileNotFoundError:
        pass  # 没有 git

# ── GitHub Actions 自动模式 ─────────────────────────

def auto_update():
    """
    GitHub Actions 触发模式。
    扫描 01_原始灵感 中最新的未处理条目，更新索引和知识图谱。
    """
    print("=" * 50)
    print("🔄 GitHub Actions 自动更新模式")
    print("=" * 50)

    # 扫描所有灵感目录
    insp_dir = os.path.join(BASE, "01_原始灵感")
    if not os.path.isdir(insp_dir):
        print("  ℹ️  暂无灵感目录")
        return

    entries = []
    for dname in os.listdir(insp_dir):
        dpath = os.path.join(insp_dir, dname)
        desc_path = os.path.join(dpath, "description.md")
        if os.path.isdir(dpath) and os.path.exists(desc_path):
            mtime = os.path.getmtime(desc_path)
            entries.append((mtime, dname, dpath))

    if not entries:
        print("  ℹ️  无待处理条目")
        return

    # 按修改时间排序（最新的最后）
    entries.sort(key=lambda x: x[0])

    # 检查 memory_index 中是否已记录
    idx_path = os.path.join(BASE, "_memory", "memory_index.json")
    with open(idx_path, "r", encoding="utf-8") as f:
        idx = json.load(f)
    known_paths = {e["path"] for e in idx["条目索引"]}

    new_count = 0
    for _, dname, dpath in entries:
        rel_path = os.path.relpath(dpath, BASE)
        if rel_path in known_paths:
            continue

        # 读取 description.md
        with open(os.path.join(dpath, "description.md"), "r", encoding="utf-8") as f:
            desc_text = f.read()

        # 提取主题
        title_match = re.search(r"\*\*主题\*\*:\s*(.+)", desc_text)
        title = title_match.group(1).strip() if title_match else dname

        # 自动分类
        category = suggest_category(desc_text)

        # 提取关键词（从标签和文字中）
        keywords = [category.split("_", 1)[1] if "_" in category else category]
        ocr_match = re.search(r"> 📝 OCR 提取文字", desc_text)
        if ocr_match:
            keywords.append("OCR")
        else:
            keywords.append("手动输入")

        update_knowledge_graph(
            keywords=keywords,
            doc_title=title,
            doc_path=rel_path
        )
        new_count += 1
        print(f"  📄 已处理: {title}")

    if new_count == 0:
        print("  ℹ️  无新条目需要处理")
    else:
        print(f"\n✅ 共处理 {new_count} 条新灵感")


# ── 状态查看 ───────────────────────────────────────

def print_status():
    """打印知识库统计。"""
    idx_path = os.path.join(BASE, "_memory", "memory_index.json")
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8") as f:
            idx = json.load(f)
        print("\n📊 知识库状态")
        print("=" * 40)
        print(f"  总知识条目: {idx['总条目数']}")
        for cat, count in idx["分类统计"].items():
            bar = "█" * count + "░" * max(0, 10 - count)
            print(f"  {cat}: {count} 篇 {bar}")
        print(f"  标签数: {len(idx['标签云'])}")
        print(f"  最后更新: {idx.get('最后更新', '未知')}")

        if idx["条目索引"]:
            print(f"\n  最近条目:")
            for entry in idx["条目索引"][-5:]:
                print(f"    - {entry['title']} ({entry['date']})")
    else:
        print("📭 知识库为空")

# ── CLI 入口 ───────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="日常灵感工作流 — 处理脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python _scripts/process_inspiration.py status              # 查看状态
  python _scripts/process_inspiration.py --n8n payload.json  # 从 n8n webhook 导入
  python _scripts/process_inspiration.py --ocr 图片.png      # OCR + 自动入库
  python _scripts/process_inspiration.py --auto              # GitHub Actions 自动更新
        """
    )

    # 互斥模式
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("status", nargs="?", const=True, help="查看知识库状态")
    mode.add_argument("--n8n", metavar="payload.json", help="从 n8n webhook JSON 文件导入")
    mode.add_argument("--ocr", metavar="图片路径", help="对截图执行 OCR 并入库")
    mode.add_argument("--auto", action="store_true", help="GitHub Actions 自动更新模式")

    args = parser.parse_args()

    # 计算实际模式
    if args.status or (len(sys.argv) == 2 and sys.argv[1] == "status"):
        print_status()
    elif args.n8n:
        if os.path.exists(args.n8n):
            with open(args.n8n, "r", encoding="utf-8") as f:
                payload = json.load(f)
            process_n8n_payload(payload)
        else:
            print(f"❌ 文件不存在: {args.n8n}")
            sys.exit(1)
    elif args.ocr:
        if os.path.exists(args.ocr):
            process_ocr_auto(args.ocr)
        else:
            print(f"❌ 路径不存在: {args.ocr}")
            sys.exit(1)
    elif args.auto:
        auto_update()
        git_commit("chore: auto-update knowledge index & graph [skip ci]")
    else:
        # 无参数时显示帮助
        parser.print_help()
