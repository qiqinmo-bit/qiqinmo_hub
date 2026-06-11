"""
收图夹 - 轮询监听 + OCR + 入库 + 推送

用法:
  python _scripts/watcher.py
  或双击 收图夹_启动.bat

工作方式:
  把截图放进 收图夹/ 文件夹
  每 5 秒检测新文件 -> 自动 OCR -> 入库 -> git push
  按 Ctrl+C 停止
"""

import sys, os, datetime, re, subprocess, shutil, time, hashlib, json, warnings

# Windows GBK 终端兼容
if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 屏蔽 ONNX Runtime 的 Windows 版本警告（不影响功能）
warnings.filterwarnings("ignore", message=".*Unsupported Windows version.*")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATCH_DIR = os.path.join(BASE, "收图夹")
MEMORY_DIR = os.path.join(BASE, "_memory")
COUNTER_FILE = os.path.join(MEMORY_DIR, "counter.txt")
HASH_FILE = os.path.join(MEMORY_DIR, "processed_hashes.json")
os.makedirs(WATCH_DIR, exist_ok=True)
os.makedirs(MEMORY_DIR, exist_ok=True)

DASHBOARD_LOG = os.path.join(MEMORY_DIR, "dashboard_log.jsonl")

def write_log(log_type, msg):
    """写结构化日志供仪表盘读取"""
    try:
        entry = {
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "type": log_type,
            "msg": msg
        }
        with open(DASHBOARD_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except:
        pass

# ── 计数器 + 去重 ───────────────────────────────────

def get_next_serial():
    """获取下一个序号 (001, 002...)，持久化到 counter.txt"""
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
    """计算图片的 MD5 哈希"""
    h = hashlib.md5()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def load_hashes():
    """加载已处理的哈希集合"""
    try:
        with open(HASH_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except:
        return set()

def save_hash(h):
    """保存新哈希"""
    hashes = load_hashes()
    hashes.add(h)
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(hashes), f, ensure_ascii=False)

# ── 工具函数 ────────────────────────────────────────

def log(msg):
    t = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] {msg}", flush=True)

def today():
    return datetime.date.today().isoformat()

def is_image(filename):
    return filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp"))

# ── OCR ────────────────────────────────────────────

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

# ── 入库 ───────────────────────────────────────────

def process_image(image_path):
    fname = os.path.basename(image_path)
    log(f"[处理] {fname}")
    write_log("process", f"处理: {fname}")

    # ── MD5 去重 ──
    img_hash = get_image_hash(image_path)
    existing = load_hashes()
    if img_hash in existing:
        log(f"[跳过] 图片已处理过 (MD5: {img_hash[:12]}...)")
        write_log("skip", f"跳过(重复): {fname}")
        os.remove(image_path)
        log("[清理] 已删除重复图片")
        return

    # OCR
    ocr_text, lines = do_ocr(image_path)
    if ocr_text:
        log(f"[OK] 识别到 {len(lines)} 段文字")
        write_log("info", f"OCR识别: {len(lines)}段文字")
    else:
        log("[!!] 未识别到文字")
        write_log("warn", "未识别到文字")

    # ── 序号命名 ──
    serial = get_next_serial()
    title = f"灵感_{serial}"
    folder_name = f"{today()}_{title}"
    folder = os.path.join(BASE, "01_原始灵感", folder_name)
    os.makedirs(folder, exist_ok=True)

    # 复制截图
    dest_img = os.path.join(folder, fname)
    shutil.copy2(image_path, dest_img)

    # 写 description.md
    desc = [
        "# 原始灵感",
        "",
        f"**日期**: {today()}",
        "**来源**: 收图夹截图",
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
    # 加原文片段方便看
    if ocr_text:
        preview = ocr_text[:200].replace("\n", " ")
        desc.append(f"\n> 原文摘要: {preview}...")

    desc_path = os.path.join(folder, "description.md")
    with open(desc_path, "w", encoding="utf-8") as f:
        f.write("\n".join(desc))

    # 记录哈希
    save_hash(img_hash)

    log(f"[保存] {folder_name}")
    write_log("save", f"入库: {title} ({len(lines)}段)")

    # 更新索引
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    subprocess.run(
        [sys.executable, os.path.join(BASE, "_scripts", "process_inspiration.py"), "--auto"],
        cwd=BASE, capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=env
    )
    log(f"[索引] 已更新")

    # Git push
    subprocess.run(["git", "add", "-A"], cwd=BASE, capture_output=True)
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=BASE, capture_output=True)
    if result.returncode != 0:
        subprocess.run(
            ["git", "commit", "-m", f"收图夹: {title}"],
            cwd=BASE, capture_output=True
        )

    pushed = False
    for port in [7897, 7890, 7891]:
        subprocess.run(["git", "config", "--local", "http.proxy", f"http://127.0.0.1:{port}"], 
                      cwd=BASE, capture_output=True)
        subprocess.run(["git", "config", "--local", "https.proxy", f"http://127.0.0.1:{port}"], 
                      cwd=BASE, capture_output=True)
        push = subprocess.run(["git", "push"], cwd=BASE, capture_output=True, text=True, timeout=30,
                            encoding="utf-8", errors="replace")
        subprocess.run(["git", "config", "--unset", "http.proxy"], cwd=BASE, capture_output=True)
        subprocess.run(["git", "config", "--unset", "https.proxy"], cwd=BASE, capture_output=True)
        if push.returncode == 0:
            log(f"[推送] 成功 (端口 {port})")
            write_log("push", f"推送到GitHub成功")
            pushed = True
            break
    if not pushed:
        log("[!!] 推送失败，稍后手动 git push")
        write_log("err", "Git推送失败")

    # 删除原图
    try:
        os.remove(image_path)
        log("[清理] 原图已删除")
    except:
        pass

    log(f"[完成] {title}")
    write_log("complete", f"完成: {title}")
    print("-" * 40, flush=True)

# ── 主程序 ─────────────────────────────────────────

def main():
    print()
    print("=" * 45)
    print("  [收图夹] 自动监听中 (轮询模式)")
    print("=" * 45)
    print(f"\n  把截图放入: {WATCH_DIR}")
    print(f"\n  每 5 秒检测新文件  |  序号命名  |  MD5 去重")
    print(f"\n  处理流程: OCR > 入库 > 推送 GitHub\n")

    # 清理重复文件名
    processed = set()

    while True:
        try:
            for fname in os.listdir(WATCH_DIR):
                fpath = os.path.join(WATCH_DIR, fname)
                if not os.path.isfile(fpath):
                    continue
                if not is_image(fname):
                    continue
                if fname in processed:
                    continue

                try:
                    size = os.path.getsize(fpath)
                except:
                    continue

                processed.add(fname)
                log(f"[发现] {fname}")
                process_image(fpath)

            time.sleep(5)
        except KeyboardInterrupt:
            log("[停止] 收图夹已停止")
            break
        except Exception as e:
            log(f"[错误] {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
