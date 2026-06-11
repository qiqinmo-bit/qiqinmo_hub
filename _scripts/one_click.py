"""
一键处理：截图 → OCR → 入库 → git push

用法:
  python _scripts/one_click.py 截图路径
  或 直接把截图拖到 process.bat 上

流程:
  1. OCR 识别截图文字
  2. 创建 description.md
  3. 更新记忆索引 + 知识图谱
  4. 自动 git push (配 Clash 代理)
"""

import sys, os, json, datetime, re, subprocess, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def log(msg):
    print(f"  {msg}")

def slug(text):
    s = text.strip()
    s = re.sub(r'[\\/:*?"<>|]', '_', s)
    s = s.replace(' ', '_').replace('\n', '_')
    return s[:60]

def today():
    return datetime.date.today().isoformat()

# ── 1. OCR ────────────────────────────────────────

def do_ocr(image_path):
    """用 rapidocr 识别图片文字"""
    from rapidocr_onnxruntime import RapidOCR
    engine = RapidOCR()
    result, elapse = engine(image_path)
    if not result:
        return "", []
    
    texts = []
    lines = []
    for box, text, score in result:
        if text and score > 0.3:
            texts.append(text)
            lines.append(f"[{score:.0%}] {text}")
    return "\n".join(texts), lines

# ── 2. 创建 description.md ────────────────────────

def save_inspiration(image_path, ocr_text, lines):
    date = today()
    # 从 OCR 内容推断标题
    title = "灵感记录"
    if ocr_text:
        # 取第一句有意义的文字做标题
        first = [l for l in ocr_text.split("\n") if len(l) > 4]
        if first:
            title = first[0][:30]
    
    folder_name = f"{date}_{slug(title)}"
    folder = os.path.join(BASE, "01_原始灵感", folder_name)
    os.makedirs(folder, exist_ok=True)

    # 复制截图
    if image_path and os.path.exists(image_path):
        fname = os.path.basename(image_path)
        dest = os.path.join(folder, fname)
        shutil.copy2(image_path, dest)
        log(f"📸 截图已复制")

    # 写 description.md
    desc = [
        "# 原始灵感",
        "",
        f"**日期**: {date}",
        "**来源**: 截图",
        f"**主题**: {title}",
        "---",
        "## 描述",
        "",
    ]
    if lines:
        desc.append("> 📝 OCR 提取文字：")
        desc.append(">")
        for l in lines:
            desc.append(f"> {l.split('] ', 1)[-1] if '] ' in l else l}")
        desc.append("")
    
    with open(os.path.join(folder, "description.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(desc))
    
    log(f"✅ 灵感已保存: {folder_name}")
    return folder, title

# ── 3. 自动更新 ────────────────────────────────────

def auto_update():
    """调用 --auto 更新索引和图谱"""
    result = subprocess.run(
        [sys.executable, os.path.join(BASE, "_scripts", "process_inspiration.py"), "--auto"],
        cwd=BASE, capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        log(f"⚠️ auto 更新异常:\n{result.stderr}")

# ── 4. Git push ────────────────────────────────────

def git_push():
    """配置代理并推送"""
    # 尝试常见 Clash 端口
    proxy_ports = [7897, 7890, 7891]
    proxy_set = False
    for port in proxy_ports:
        test = subprocess.run(
            ["git", "config", "--local", "http.proxy", f"http://127.0.0.1:{port}"],
            cwd=BASE, capture_output=True
        )
        subprocess.run(
            ["git", "config", "--local", "https.proxy", f"http://127.0.0.1:{port}"],
            cwd=BASE, capture_output=True
        )
        # 测试连接
        test = subprocess.run(
            ["git", "fetch", "--dry-run"],
            cwd=BASE, capture_output=True, text=True, timeout=10
        )
        if test.returncode == 0 or "fatal" not in test.stderr.lower():
            proxy_set = True
            log(f"🌐 代理 :{port} 可用")
            break
        else:
            # 清除尝试的代理
            subprocess.run(["git", "config", "--unset", "http.proxy"], cwd=BASE, capture_output=True)
            subprocess.run(["git", "config", "--unset", "https.proxy"], cwd=BASE, capture_output=True)

    # git add + commit + push
    subprocess.run(["git", "add", "-A"], cwd=BASE, capture_output=True)
    
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=BASE, capture_output=True
    )
    if result.returncode == 0:
        log("ℹ️  无变更，跳过提交")
    else:
        subprocess.run(
            ["git", "commit", "-m", f"📸 灵感: 截图自动入库 [skip ci]"],
            cwd=BASE, capture_output=True
        )
        push = subprocess.run(
            ["git", "push"],
            cwd=BASE, capture_output=True, text=True, timeout=60
        )
        if push.returncode == 0:
            log("🚀 已推送到 GitHub")
        else:
            log(f"⚠️ 推送失败: {push.stderr[:200]}")
    
    # 清除代理
    subprocess.run(["git", "config", "--unset", "http.proxy"], cwd=BASE, capture_output=True)
    subprocess.run(["git", "config", "--unset", "https.proxy"], cwd=BASE, capture_output=True)


# ── 入口 ────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("用法: 把截图拖到 process.bat 上")
        print("  或: python _scripts/one_click.py 截图路径")
        sys.exit(1)

    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"❌ 文件不存在: {image_path}")
        sys.exit(1)

    print("\n" + "=" * 45)
    print("  🧠  一键灵感处理")
    print("=" * 45)

    # Step 1: OCR
    print("\n① OCR 识别...")
    ocr_text, lines = do_ocr(image_path)
    if ocr_text:
        log(f"✅ 识别到 {len(lines)} 段文字")
    else:
        log("⚠️ 未识别到文字，将创建空灵感")

    # Step 2: 入库
    print("\n② 写入灵感...")
    folder, title = save_inspiration(image_path, ocr_text, lines)

    # Step 3: 更新索引
    print("\n③ 更新索引...")
    auto_update()

    # Step 4: 推送
    print("\n④ 推送到 GitHub...")
    git_push()

    print("\n" + "=" * 45)
    print("  ✅  全部完成！")
    print("=" * 45)
    print(f"\n📂 灵感位置: 01_原始灵感/{os.path.basename(folder)}")
    print("🌐 GitHub Pages: https://qiqinmo-bit.github.io/qiqinmo_hub/")
    print("\n🔄 GitHub Actions 正在后台自动分析...")

if __name__ == "__main__":
    main()
