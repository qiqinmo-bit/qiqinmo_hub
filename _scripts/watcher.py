"""
收图夹 - 自动监听 + OCR + 入库 + 推送

用法:
  python _scripts/watcher.py
  或双击 收图夹_启动.bat

工作方式:
  把截图放进 收图夹/ 文件夹
  -> 自动 OCR -> 入库 -> git push
"""

import sys, os, datetime, re, subprocess, shutil, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Windows GBK 终端兼容
if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATCH_DIR = os.path.join(BASE, "收图夹")
os.makedirs(WATCH_DIR, exist_ok=True)

# ── 工具函数 ────────────────────────────────────────

def log(msg):
    t = datetime.datetime.now().strftime("%H:%M:%S")
    # 过滤 GBK 不兼容字符
    safe = msg.encode("gbk", errors="replace").decode("gbk", errors="replace")
    print(f"[{t}] {safe}")

def slug(text):
    s = text.strip()
    s = re.sub(r'[\\/:*?"<>|]', '_', s)
    s = s.replace(' ', '_').replace('\n', '_')
    return s[:60]

def today():
    return datetime.date.today().isoformat()

def is_image(filename):
    return filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp"))

def file_stable(path, wait=3, check_interval=0.5):
    """等待文件写入完成（大小稳定）"""
    try:
        size = -1
        for _ in range(int(wait / check_interval)):
            time.sleep(check_interval)
            if os.path.getsize(path) == size:
                return True
            size = os.path.getsize(path)
        return True
    except:
        return False

# ── OCR ────────────────────────────────────────────

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

# ── 入库 ───────────────────────────────────────────

def process_image(image_path):
    fname = os.path.basename(image_path)
    log(f"[处理] {fname}")

    # OCR
    ocr_text, lines = do_ocr(image_path)
    if ocr_text:
        log(f"[OK] 识别到 {len(lines)} 段文字")
    else:
        log("[!!] 未识别到文字")

    # 提取标题
    title = "灵感记录"
    if ocr_text:
        first = [l for l in ocr_text.split("\n") if len(l) > 4]
        if first:
            title = first[0][:30]

    # 创建灵感目录
    folder_name = f"{today()}_{slug(title)}"
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

    desc_path = os.path.join(folder, "description.md")
    with open(desc_path, "w", encoding="utf-8") as f:
        f.write("\n".join(desc))

    log(f"[保存] {folder_name}")

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
            ["git", "commit", "-m", f"收图夹: {title} [skip ci]"],
            cwd=BASE, capture_output=True
        )

    # 尝试代理推送
    pushed = False
    for port in [7897, 7890, 7891]:
        subprocess.run(["git", "config", "--local", "http.proxy", f"http://127.0.0.1:{port}"], 
                      cwd=BASE, capture_output=True)
        subprocess.run(["git", "config", "--local", "https.proxy", f"http://127.0.0.1:{port}"], 
                      cwd=BASE, capture_output=True)
        push = subprocess.run(["git", "push"], cwd=BASE, capture_output=True, text=True, timeout=30)
        subprocess.run(["git", "config", "--unset", "http.proxy"], cwd=BASE, capture_output=True)
        subprocess.run(["git", "config", "--unset", "https.proxy"], cwd=BASE, capture_output=True)
        if push.returncode == 0:
            log(f"[推送] 成功 (端口 {port})")
            pushed = True
            break
    if not pushed:
        log("[!!] 推送失败，稍后手动 git push")

    # 删除原图
    try:
        os.remove(image_path)
        log("[清理] 原图已删除")
    except:
        pass

    log(f"[完成] {title}")
    print("-" * 40)

# ── 文件监听器 ──────────────────────────────────────

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if not is_image(event.src_path):
            return
        time.sleep(1)
        try:
            process_image(event.src_path)
        except Exception as e:
            log(f"[错误] {e}")

    def on_modified(self, event):
        if event.is_directory:
            return
        if not is_image(event.src_path):
            return
        if not file_stable(event.src_path):
            return
        try:
            process_image(event.src_path)
        except Exception as e:
            log(f"[错误] {e}")

# ── 主程序 ─────────────────────────────────────────

def main():
    print()
    print("=" * 45)
    print("  [收图夹] 自动监听中")
    print("=" * 45)
    print(f"\n  把截图放入: {WATCH_DIR}")
    print(f"\n  处理后自动: OCR > 入库 > 推送 GitHub")
    print(f"\n  按 Ctrl+C 停止\n")

    # 先处理已有的文件
    for fname in os.listdir(WATCH_DIR):
        fpath = os.path.join(WATCH_DIR, fname)
        if os.path.isfile(fpath) and is_image(fname):
            log(f"[待处理] {fname}")
            process_image(fpath)

    # 启动监听
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        log("[停止] 收图夹已停止")
    observer.join()

if __name__ == "__main__":
    main()
