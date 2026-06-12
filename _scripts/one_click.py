"""
一键处理：截图 → OCR → 入库 → git push

用法:
  python _scripts/one_click.py 截图路径
  或 直接把截图拖到 process.bat 上

流程:
  1. OCR 识别截图文字
  2. 创建 description.md (序号命名)
  3. MD5 去重
  4. 更新记忆索引 + 知识图谱
  5. 自动 git push (配 Clash 代理)
"""

import sys, os, json, datetime, re, subprocess, shutil, hashlib, warnings

# 屏蔽 ONNX Runtime 的 Windows 版本警告
warnings.filterwarnings("ignore", message=".*Unsupported Windows version.*")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_DIR = os.path.join(BASE, "_memory")
COUNTER_FILE = os.path.join(MEMORY_DIR, "counter.txt")
HASH_FILE = os.path.join(MEMORY_DIR, "processed_hashes.json")

def log(msg):
    print(f"  {msg}")

def today():
    return datetime.date.today().isoformat()

# ── 计数器 + 去重 ───────────────────────────────────

def get_next_serial():
    try:
        with open(COUNTER_FILE, "r") as f:
            n = int(f.read().strip())
    except:
        n = 0
    n += 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(n))
    return f"{n:03d}"

def get_image_hash(image_path):
    h = hashlib.md5()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def load_hashes():
    try:
        with open(HASH_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except:
        return set()

def save_hash(h):
    hashes = load_hashes()
    hashes.add(h)
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(hashes), f, ensure_ascii=False)

# ── 1. OCR ────────────────────────────────────────

def do_ocr(image_path):
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
    serial = get_next_serial()
    title = f"灵感_{serial}"
    
    folder_name = f"{date}_{title}"
    folder = os.path.join(BASE, "01_原始灵感", folder_name)
    os.makedirs(folder, exist_ok=True)

    # 复制截图
    if image_path and os.path.exists(image_path):
        fname = os.path.basename(image_path)
        dest = os.path.join(folder, fname)
        shutil.copy2(image_path, dest)
        log(f"[复制] 截图已复制")

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
        desc.append("> OCR 提取文字：")
        desc.append(">")
        for l in lines:
            desc.append(f"> {l.split('] ', 1)[-1] if '] ' in l else l}")
        desc.append("")
    if ocr_text:
        preview = ocr_text[:200].replace("\n", " ")
        desc.append(f"\n> 原文摘要: {preview}...")

    with open(os.path.join(folder, "description.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(desc))

    log(f"[保存] {folder_name}")
    return folder, title

# ── 3. 自动更新 ────────────────────────────────────

def auto_update():
    result = subprocess.run(
        [sys.executable, os.path.join(BASE, "_scripts", "process_inspiration.py"), "--auto"],
        cwd=BASE, capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        log(f"[异常] auto 更新:\n{result.stderr}")

# ── 4. Git push ────────────────────────────────────

def git_push():
    PROXY_CACHE = os.path.join(BASE, "_memory", "proxy_port.txt")
    proxy_ports = [7897, 7890, 7891]
    try:
        cached = int(open(PROXY_CACHE, "r").read().strip())
        if cached in proxy_ports:
            proxy_ports = [cached] + [p for p in proxy_ports if p != cached]
    except:
        pass
    port = proxy_ports[0]
    subprocess.run(["git", "config", "--local", "http.proxy", f"http://127.0.0.1:{port}"],
                  cwd=BASE, capture_output=True)
    subprocess.run(["git", "config", "--local", "https.proxy", f"http://127.0.0.1:{port}"],
                  cwd=BASE, capture_output=True)
    test = subprocess.run(
        ["git", "fetch", "--dry-run"],
        cwd=BASE, capture_output=True, text=True, timeout=5
    )
    if test.returncode != 0 and "fatal" in test.stderr.lower():
        for port in proxy_ports[1:]:
            subprocess.run(["git", "config", "--local", "http.proxy", f"http://127.0.0.1:{port}"],
                          cwd=BASE, capture_output=True)
            subprocess.run(["git", "config", "--local", "https.proxy", f"http://127.0.0.1:{port}"],
                          cwd=BASE, capture_output=True)
            test = subprocess.run(
                ["git", "fetch", "--dry-run"],
                cwd=BASE, capture_output=True, text=True, timeout=5
            )
            if test.returncode == 0 or "fatal" not in test.stderr.lower():
                break
            subprocess.run(["git", "config", "--unset", "http.proxy"], cwd=BASE, capture_output=True)
            subprocess.run(["git", "config", "--unset", "https.proxy"], cwd=BASE, capture_output=True)
    log(f"[代理] 端口 {port} 可用")
    try:
        with open(PROXY_CACHE, "w") as f:
            f.write(str(port))
    except:
        pass

    subprocess.run(["git", "add", "-A"], cwd=BASE, capture_output=True)
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=BASE, capture_output=True)
    has_changes = result.returncode != 0

    if has_changes:
        subprocess.run(
            ["git", "commit", "-m", f"一键截图"],
            cwd=BASE, capture_output=True
        )

    push = subprocess.run(
        ["git", "push"],
        cwd=BASE, capture_output=True, text=True, timeout=60
    )
    if push.returncode == 0:
        log("[推送] 成功")
        pull = subprocess.run(
            ["git", "pull", "--rebase", "--autostash"],
            cwd=BASE, capture_output=True, text=True, timeout=30
        )
        if pull.returncode == 0:
            log("[同步] 已拉取云端更新")
        else:
            log(f"[同步] 拉取失败: {pull.stderr[:100]}")
    else:
        log(f"[!!] 推送失败: {push.stderr[:200]}")

    subprocess.run(["git", "config", "--unset", "http.proxy"], cwd=BASE, capture_output=True)
    subprocess.run(["git", "config", "--unset", "https.proxy"], cwd=BASE, capture_output=True)

# ── 入口 ────────────────────────────────────────────

def local_analysis(title, ocr_text):
    import tempfile, json
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".md", encoding="utf-8", delete=False)
    tmp.write(ocr_text)
    tmp.close()
    print("\n  [本地] AI 分析...")
    result = subprocess.run(
        [sys.executable, os.path.join(BASE, "_scripts", "ai_analyzer.py"), "--file", tmp.name, "--mode", "quick"],
        capture_output=True, text=True, cwd=BASE,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}
    )
    os.unlink(tmp.name)
    try:
        ai_result = json.loads(result.stdout.strip())
        if ai_result.get("success"):
            log(f"[AI] {ai_result.get('tier', 'unknown')} \u5206\u6790\u5b8c\u6210")
            subprocess.run([sys.executable, os.path.join(BASE, "_scripts", "promote_knowledge.py"), "--auto"], capture_output=True, cwd=BASE)
            subprocess.run([sys.executable, os.path.join(BASE, "_scripts", "process_inspiration.py"), "--auto"], capture_output=True, cwd=BASE)
            print("  [\u672c\u5730] \u5168\u94fe\u8def\u5b8c\u6210\uff1a\u5206\u6790 \u2192 \u77e5\u8bc6\u6587\u6863 \u2192 \u56fe\u8c31")
        else:
            log("[AI] \u5206\u6790\u5931\u8d25")
    except:
        log("[AI] \u89e3\u6790\u7ed3\u679c\u5931\u8d25")

def main():
    if len(sys.argv) < 2:
        print("用法: 把截图拖到 process.bat 上")
        print("  或: python _scripts/one_click.py 截图路径 [--full]")
        sys.exit(1)

    image_path = sys.argv[1]
    full_mode = "--full" in sys.argv
    if not os.path.exists(image_path):
        print(f"[!!] 文件不存在: {image_path}")
        sys.exit(1)

    # MD5 去重
    img_hash = get_image_hash(image_path)
    existing = load_hashes()
    if img_hash in existing:
        print(f"\n[跳过] 图片已处理过 (MD5: {img_hash[:12]}...)")
        return

    print("\n" + "=" * 45)
    print("  一键灵感处理")
    print("=" * 45)

    print("\n1. OCR 识别...")
    ocr_text, lines = do_ocr(image_path)
    if ocr_text:
        log(f"[OK] 识别到 {len(lines)} 段文字")
    else:
        log("[!!] 未识别到文字")

    print("\n2. 写入灵感...")
    folder, title = save_inspiration(image_path, ocr_text, lines)
    save_hash(img_hash)

    print("\n3. 更新索引...")
    auto_update()

    print("\n3.5 归档截图...")
    archive_dir = os.path.join(BASE, "_archive")
    os.makedirs(archive_dir, exist_ok=True)
    src_img = image_path
    dest_img = os.path.join(archive_dir, os.path.basename(src_img))
    try:
        import shutil
        if not os.path.exists(dest_img):
            shutil.move(src_img, dest_img)
        else:
            os.remove(src_img)
        log("[归档] 原图已移至 _archive/")
    except Exception as e:
        log(f"[归档] 失败: {e}")

    print("\n4. 推送到 GitHub...")
    git_push()

    print("\n" + "=" * 45)
    print("  全部完成！")
    print("=" * 45)
    print(f"\n  灵感: 01_原始灵感/{os.path.basename(folder)}")
    print("  GitHub Actions 后台自动分析中...\n")

if __name__ == "__main__":
    main()


