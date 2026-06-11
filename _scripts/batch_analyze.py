"""
批量 AI 分析 — 分析所有未处理的灵感

GitHub Actions 调用:
  python _scripts/batch_analyze.py
"""

import os, sys, json, subprocess
from datetime import date

BASE = os.getcwd()
SCRIPT = os.path.join("_scripts", "ai_analyzer.py")

# 查找所有未分析的 description.md
pending = []
for root, dirs, files in os.walk("01_原始灵感"):
    if "description.md" in files:
        folder = os.path.basename(root)
        analysis_path = os.path.join("02_灵感分析", folder, "analysis.md")
        if not os.path.exists(analysis_path):
            pending.append(os.path.join(root, "description.md"))
            print(f"[待分析] {folder}")

if not pending:
    print("[完成] 没有待分析的灵感")
    sys.exit(0)

print(f"[统计] 共 {len(pending)} 篇待分析")

for desc_path in pending:
    folder_name = os.path.basename(os.path.dirname(desc_path))
    target_dir = os.path.join("02_灵感分析", folder_name)
    os.makedirs(target_dir, exist_ok=True)

    print()
    print("=" * 50)
    print(f"[分析] {folder_name}")
    print("=" * 50)

    result = subprocess.run(
        [sys.executable, SCRIPT, "--file", desc_path, "--mode", "quick"],
        capture_output=True, text=True, cwd=BASE,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}
    )

    # ai_analyzer.py 输出 JSON 到 stdout，进度到 stderr
    json_line = result.stdout.strip()

    if not json_line:
        print(f"[跳过] 无法解析 AI 输出")
        if result.stderr:
            print(f"  stderr: {result.stderr.strip()[-200:]}")
        continue

    ai_result = json.loads(json_line)
    if not ai_result.get("success"):
        print(f"[跳过] AI 分析失败")
        continue

    content = ai_result.get("content", "")
    keywords = ai_result.get("keywords", [])
    category = ai_result.get("category", "")
    tier = ai_result.get("tier", "")
    model = ai_result.get("model", "")

    analysis = f"""# 灵感分析

**日期**: {date.today().isoformat()}
**来源**: 01_原始灵感/{folder_name}
**分析引擎**: {tier} ({model})
**建议分类**: {category}
**关键词**: {", ".join(keywords)}

---

## 分析结果

{content}
"""
    path = os.path.join(target_dir, "analysis.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(analysis)

    print(f"[保存] {path}")
    print(f"[分类] {category}")
    print(f"[标签] {', '.join(keywords)}")

print(f"\n[完成] 共分析 {len(pending)} 篇")
