"""
知识提升脚本 — 02_灵感分析 → 03_知识文档 → 04_知识网络

三个模式：
  --status         查看哪些 02 条目待提升
  --entry <folder> 提升指定条目（需要从 stdin 或 --content 传入文档内容）
  --auto           批量提升所有待提升条目（调用 ai_analyzer.py 自动生成）

用法:
  python _scripts/promote_knowledge.py --status
  python _scripts/promote_knowledge.py --entry 2026-06-12_灵感_001 --content "文档内容..."
  python _scripts/promote_knowledge.py --auto
"""

import sys, os, json, datetime, re, subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

def today():
    return datetime.date.today().isoformat()

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def slug(text):
    s = text.strip()
    s = re.sub(r'[\\/:*?"<>|]', '_', s)
    s = s.replace(' ', '_').replace('\n', '_')
    return s[:60]

# ── 模板路径 ───────────────────────────────────────

TEMPLATE_PATH = os.path.join(BASE, "05_模板", "knowledge_doc_template.md")

def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

# ── 读取 analysis.md ──────────────────────────────

def read_analysis(folder_name):
    """读取 02 分析文件，返回解析后的信息。"""
    path = os.path.join(BASE, "02_灵感分析", folder_name, "analysis.md")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # 提取元数据
    cat_match = re.search(r"\*\*建议分类\*\*:\s*(.+)", text)
    kw_match = re.search(r"\*\*关键词\*\*:\s*(.+)", text)
    engine_match = re.search(r"\*\*分析引擎\*\*:\s*(.+)", text)
    source_match = re.search(r"\*\*来源\*\*:\s*(.+)", text)

    category = cat_match.group(1).strip() if cat_match else "03_工作流与自动化"
    keywords = [k.strip() for k in kw_match.group(1).split(",")] if kw_match else []
    engine = engine_match.group(1).strip() if engine_match else "未知"
    source = source_match.group(1).strip() if source_match else ""

    return {
        "folder": folder_name,
        "category": category,
        "keywords": keywords,
        "engine": engine,
        "source": source,
        "text": text
    }

# ── 查找待提升条目 ────────────────────────────────

def find_pending():
    """返回所有待提升的 02 条目列表。"""
    pending = []
    analysis_dir = os.path.join(BASE, "02_灵感分析")
    if not os.path.isdir(analysis_dir):
        return pending

    for dname in sorted(os.listdir(analysis_dir)):
        analysis = read_analysis(dname)
        if not analysis:
            continue
        # 检查是否已有对应 03 文档
        doc_path = get_doc_path(analysis)
        if os.path.exists(doc_path):
            continue
        pending.append(analysis)
    return pending

def find_promoted():
    """返回所有已提升为知识文档的条目路径。"""
    promoted = {}
    analysis_dir = os.path.join(BASE, "02_灵感分析")
    if not os.path.isdir(analysis_dir):
        return promoted
    for dname in sorted(os.listdir(analysis_dir)):
        analysis = read_analysis(dname)
        if not analysis:
            continue
        doc_path = get_doc_path(analysis)
        if os.path.exists(doc_path):
            promoted[dname] = doc_path
    return promoted

# ── 确定目标路径 ──────────────────────────────────

def get_doc_path(analysis):
    """根据分析结果确定知识文档的目标路径。"""
    cat = analysis["category"]
    # 规范化分类
    if not cat.startswith("0"):
        # 尝试匹配已知分类
        known = {
            "Agent与AI编程": "01_Agent与AI编程",
            "模型与API": "02_模型与API",
            "工作流与自动化": "03_工作流与自动化",
            "提示词工程": "04_提示词工程",
            "多模态与工具链": "05_多模态与工具链",
        }
        cat = known.get(cat, cat)
    # 从分析文本中提取有意义的标题
    text = analysis.get("text", "")
    title_match = re.search(r"\*\*主题\*\*:\s*(.+)", text)
    title = title_match.group(1).strip() if title_match else analysis["folder"]
    # 去掉日期前缀
    title_clean = re.sub(r"^\d{4}-\d{2}-\d{2}_", "", title)
    # 用原标题的文件夹名作为 fallback
    fname = slug(title_clean) + ".md"
    return os.path.join(BASE, "03_知识文档", cat, fname)

# ── 从 analysis.md 提取分析结果正文 ───────────────

def extract_content(analysis):
    """从 analysis.md 中提取 '分析结果' 章节。"""
    text = analysis["text"]
    # 找到 "## 分析结果" 之后的内容
    parts = text.split("## 分析结果")
    if len(parts) > 1:
        content = parts[1].strip()
        # 去掉可能的尾部元数据
        content = re.sub(r"\n---.*", "", content, flags=re.DOTALL)
        return content
    return ""

# ── 生成知识文档 ──────────────────────────────────

def generate_knowledge_doc(analysis, custom_content=None):
    """使用模板生成知识文档内容。"""
    template = load_template()
    text = analysis["text"]
    
    # 提取主题
    title_match = re.search(r"\*\*主题\*\*:\s*(.+)", text)
    title_raw = title_match.group(1).strip() if title_match else analysis["folder"]
    title_clean = re.sub(r"^\d{4}-\d{2}-\d{2}_", "", title_raw)
    
    # 摘取正文
    content_body = custom_content or extract_content(analysis)
    
    # 关键词格式化
    kw_list = analysis["keywords"]
    kw_str = ", ".join(kw_list) if kw_list else "待补充"
    
    # 分类
    cat = analysis["category"]
    
    # 填充模板
    doc = template.replace("{{YYYY-MM-DD}}", today())
    doc = doc.replace("{{文档标题}}", title_clean)
    doc = doc.replace("{{分类名}}", cat)
    doc = doc.replace("[关键词1, 关键词2]", kw_str)
    
    # 处理来源链接
    source_link = f"02_灵感分析/{analysis['folder']}"
    doc = doc.replace("02_灵感分析/YYYY-MM-DD_主题", source_link)
    
    # 填充内容占位
    if "{{一句话总结}}" in doc:
        # 取内容前 100 字作为概述
        summary = content_body[:100].replace("\n", " ").strip() + "..."
        doc = doc.replace("{{一句话总结}}", summary)
    
    # 如果模板中有更多占位，尽量填充
    if "{{实现路径}}" in doc or "{{步骤}}" in doc:
        # 把分析结果塞进去
        impl_section = f"\n{content_body}\n"
        doc = doc.replace("{{实现路径}}", impl_section)
    
    # 清理残留的模板占位符
    doc = re.sub(r"\{\{.*?\}\}", "待补充", doc)
    
    return doc, title_clean

# ── 保存知识文档 ──────────────────────────────────

def save_knowledge_doc(analysis, content=None):
    """保存知识文档并更新所有索引。"""
    doc_content, doc_title = generate_knowledge_doc(analysis, content)
    doc_path = get_doc_path(analysis)
    ensure_dir(os.path.dirname(doc_path))
    
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(doc_content)
    
    print(f"  ✅ 知识文档已保存: {os.path.relpath(doc_path, BASE)}")
    
    # 更新 memory_index.json
    update_memory_index(analysis, doc_path, doc_title)
    
    # 更新 knowledge_graph.md
    update_knowledge_graph_md()
    
    # 更新 facts.md
    update_facts_md(analysis, doc_title)
    
    return doc_path

# ── 更新 memory_index.json ───────────────────────

def update_memory_index(analysis, doc_path, doc_title):
    """将新知识文档添加到 memory_index.json。"""
    idx_path = os.path.join(BASE, "_memory", "memory_index.json")
    with open(idx_path, "r", encoding="utf-8") as f:
        idx = json.load(f)
    
    # 检查是否已存在
    rel_path = os.path.relpath(doc_path, BASE)
    for entry in idx["条目索引"]:
        if entry["path"] == rel_path:
            print(f"  ℹ️  索引中已存在: {doc_title}")
            return
    
    cat = analysis["category"]
    idx["总条目数"] += 1
    entry = {
        "id": f"entry_{idx['总条目数']:03d}",
        "title": doc_title,
        "path": rel_path,
        "date": today(),
        "keywords": analysis["keywords"],
        "source": f"02_灵感分析/{analysis['folder']}"
    }
    idx["条目索引"].append(entry)
    
    for kw in analysis["keywords"]:
        idx["标签云"][kw] = idx["标签云"].get(kw, 0) + 1
    idx["最后更新"] = today()
    
    # 更新分类统计
    cat_short = cat.split("_", 1)[1] if "_" in cat else cat
    full_cat = None
    for c in idx["分类统计"]:
        if cat_short in c or cat in c:
            full_cat = c
            break
    if full_cat and full_cat in idx["分类统计"]:
        idx["分类统计"][full_cat] += 1
    
    with open(idx_path, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 记忆索引已更新")

# ── 更新 knowledge_graph.md（Mermaid 图谱）───────

def update_knowledge_graph_md():
    """基于 memory_index.json 和 graph_data.json 重写 knowledge_graph.md。"""
    idx_path = os.path.join(BASE, "_memory", "memory_index.json")
    graph_path = os.path.join(BASE, "04_知识网络", "graph_data.json")
    md_path = os.path.join(BASE, "04_知识网络", "knowledge_graph.md")
    
    with open(idx_path, "r", encoding="utf-8") as f:
        idx = json.load(f)
    
    with open(graph_path, "r", encoding="utf-8") as f:
        g = json.load(f)
    
    # 收集知识文档（03）条目
    doc_entries = [e for e in idx["条目索引"] if e["path"].startswith("03_知识文档")]
    # 收集原始灵感条目
    insp_entries = [e for e in idx["条目索引"] if e["path"].startswith("01_原始灵感")]
    
    # 按分类分组
    nodes_by_cat = {}
    for e in doc_entries:
        cat = "其他"
        for c in ["01_Agent与AI编程", "02_模型与API", "03_工作流与自动化", "04_提示词工程", "05_多模态与工具链"]:
            if c in e.get("path", ""):
                cat = c
                break
        if cat not in nodes_by_cat:
            nodes_by_cat[cat] = []
        nodes_by_cat[cat].append(e["title"])
    
    # 收集出现在 graph_data.json 中的内容灵感
    graph_nodes = g.get("nodes", [])
    
    lines = []
    lines.append("# 🕸️ 知识网络")
    lines.append("")
    lines.append("> 可视化展示所有灵感与知识之间的连接关系。")
    lines.append("")
    lines.append("## 知识地图")
    lines.append("")
    lines.append("```mermaid")
    lines.append("mindmap")
    lines.append("  root((🧠 我的 AI 知识库))")
    
    cat_order = ["01_Agent与AI编程", "02_模型与API", "03_工作流与自动化", "04_提示词工程", "05_多模态与工具链"]
    doc_count = 0
    for cat in cat_order:
        items = nodes_by_cat.get(cat, [])
        lines.append(f"    {cat}")
        if items:
            for title in items:
                lines.append(f"      {title}")
                doc_count += 1
        else:
            lines.append(f"      [等待灵感输入]")
    
    lines.append("```")
    lines.append("")
    
    # 关联图谱 - 只对有连接的知识节点生成
    doc_nodes = [n for n in graph_nodes if "03_知识文档" in n.get("path", "")]
    insp_nodes = [n for n in graph_nodes if "01_原始灵感" in n.get("path", "")]
    
    if doc_nodes or (doc_entries and insp_entries):
        lines.append("## 关联图谱")
        lines.append("")
        lines.append("```mermaid")
        lines.append("graph LR")
        
        # 知识文档节点
        seen_docs = set()
        for i, entry in enumerate(doc_entries):
            nid = f"n{i+1}"
            label = entry["title"][:20]
            lines.append(f"    {nid}[{label}]")
            seen_docs.add(entry["title"])
        
        # 关联：知识文档 ← 灵感源
        for i, entry in enumerate(doc_entries):
            nid = f"n{i+1}"
            source = entry.get("source", "")
            # 找到对应的灵感节点
            for si, se in enumerate(insp_entries):
                if source and source.split("/")[-1] in se.get("path", ""):
                    sid = f"s{si+1}"
                    if sid not in [l.split("[")[0].strip() for l in lines if l.strip().startswith("s")]:
                        lines.append(f"    {sid}[{se['title'][:20]}]")
                    lines.append(f"    {nid} -->|来源于| {sid}")
        
        lines.append("```")
    
    lines.append("")
    lines.append(f"---")
    lines.append(f"")
    total = len(doc_entries)
    lines.append(f"*📅 初始化于 2026-06-09 | 共 {total} 个知识节点 | 最后更新: {today()}*")
    
    md_content = "\n".join(lines)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"  ✅ 知识图谱已更新: 04_知识网络/knowledge_graph.md")

# ── 更新 facts.md ─────────────────────────────────

def update_facts_md(analysis, doc_title):
    """向 facts.md 追加新知识文档的记录。"""
    facts_path = os.path.join(BASE, "_memory", "facts.md")
    
    # 检查是否已有相关记录防止重复
    if os.path.exists(facts_path):
        with open(facts_path, "r", encoding="utf-8") as f:
            existing = f.read()
        if doc_title in existing:
            print(f"  ℹ️  facts.md 已记录: {doc_title}")
            return
    
    cat = analysis["category"]
    kw = ", ".join(analysis["keywords"])
    
    addition = f"""
### {doc_title}

| 项目 | 内容 |
|------|------|
| **日期** | {today()} |
| **分类** | {cat} |
| **关键词** | {kw} |
| **来源灵感** | [{analysis['folder']}](02_灵感分析/{analysis['folder']}) |
| **知识文档** | 03_知识文档/{cat}/{slug(doc_title)}.md |

"""
    with open(facts_path, "a", encoding="utf-8") as f:
        f.write(addition)
    print(f"  ✅ facts.md 已更新")

# ── 状态查看 ──────────────────────────────────────

def print_status():
    pending = find_pending()
    promoted = find_promoted()
    
    print("\n📊 知识提升状态")
    print("=" * 50)
    print(f"  02_灵感分析 条目: {len(pending) + len(promoted)}")
    print(f"  已提升为知识文档: {len(promoted)}")
    print(f"  待提升: {len(pending)}")
    
    if pending:
        print(f"\n  待提升条目:")
        for p in pending:
            print(f"    - {p['folder']} → {p['category']}")
    
    if promoted:
        print(f"\n  已提升条目:")
        for name, path in promoted.items():
            print(f"    - {name} → {os.path.relpath(path, BASE)}")

# ── 自动模式 ──────────────────────────────────────

def auto_promote():
    """调用 ai_analyzer.py 批量生成知识文档。"""
    pending = find_pending()
    if not pending:
        print("  ℹ️  没有待提升的条目")
        return
    
    ai_script = os.path.join(BASE, "_scripts", "ai_analyzer.py")
    if not os.path.exists(ai_script):
        print("  ⚠️  ai_analyzer.py 不存在，尝试用本地 AI 生成")
        return auto_promote_local(pending)
    
    for p in pending:
        print(f"\n{'=' * 50}")
        print(f"  📄 处理: {p['folder']}")
        print(f"{'=' * 50}")
        
        result = subprocess.run(
            [sys.executable, ai_script, "--mode", "full"],
            input=p["text"],
            capture_output=True, text=True, cwd=BASE,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"}
        )
        
        json_line = result.stdout.strip()
        if not json_line:
            print(f"  ⚠️  AI 分析无输出，跳过")
            continue
        
        try:
            ai_result = json.loads(json_line)
            if ai_result.get("success") and ai_result.get("content"):
                save_knowledge_doc(p, custom_content=ai_result["content"])
            else:
                save_knowledge_doc(p)
        except json.JSONDecodeError:
            save_knowledge_doc(p)
    
    print(f"\n✅ 批量提升完成")

def auto_promote_local(pending):
    """无 AI API 时，直接基于 analysis.md 内容生成文档。"""
    for p in pending:
        print(f"\n  📄 {p['folder']}")
        save_knowledge_doc(p)

# ── CLI 入口 ──────────────────────────────────────

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="知识提升脚本")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--status", action="store_true", help="查看待提升状态")
    group.add_argument("--entry", help="提升指定条目（folder name）")
    group.add_argument("--content", help="文档内容（配合 --entry 使用）")
    group.add_argument("--auto", action="store_true", help="批量自动提升")
    
    args = parser.parse_args()
    
    if args.status:
        print_status()
    elif args.entry:
        analysis = read_analysis(args.entry)
        if not analysis:
            print(f"❌ 未找到: {args.entry}")
            sys.exit(1)
        doc_path = get_doc_path(analysis)
        if os.path.exists(doc_path):
            print(f"  ⚠️  知识文档已存在: {os.path.relpath(doc_path, BASE)}")
            sys.exit(0)
        save_knowledge_doc(analysis, custom_content=args.content)
        print(f"\n✅ 提升完成: {os.path.relpath(doc_path, BASE)}")
    elif args.auto:
        auto_promote()
    else:
        print_status()

