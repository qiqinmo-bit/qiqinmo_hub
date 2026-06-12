"""
Web 仪表盘 — 收图夹实时可视化

用法:
  python _scripts/web_dashboard.py

打开浏览器: http://localhost:5677

功能:
  - 实时日志推送 (SSE)
  - 今日处理统计
  - 知识库状态
"""

import sys, os, json, time, datetime
from flask import Flask, render_template, Response, jsonify

# Windows GBK 兼容
if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE, "_memory", "dashboard_log.jsonl")
COUNTER_FILE = os.path.join(BASE, "_memory", "counter.txt")

app = Flask(__name__, template_folder=os.path.join(BASE, "templates"))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# ── 工具函数 ────────────────────────────────────────

def read_logs(tail=50):
    """读取最近的 N 条日志"""
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [json.loads(l) for l in lines[-tail:]]
    except:
        return []

def get_today_count():
    """获取今日处理数"""
    today = datetime.date.today().isoformat()
    logs = read_logs(500)
    return sum(1 for l in logs if l.get("time", "").startswith(today) and l.get("type") in ("complete", "skip"))

def get_total_entries():
    """获取总知识条目数"""
    idx_path = os.path.join(BASE, "_memory", "memory_index.json")
    try:
        with open(idx_path, "r", encoding="utf-8") as f:
            idx = json.load(f)
        return idx.get("总条目数", 0)
    except:
        return 0

def get_current_step():
    """从最新日志判断当前进度步骤 (0-6)"""
    logs = read_logs(20)
    if not logs:
        return 0
    # 定义步骤映射
    steps = {
        "process": 1,
        "skip": 6,
    }
    # 从最新到最老遍历，找最高步骤
    step = 0
    for log in reversed(logs):
        t = log.get("type", "")
        msg = log.get("msg", "")
        if t == "complete" or t == "skip":
            return 6
        if t == "push":
            step = max(step, 5)
        elif "索引" in msg and t != "":
            step = max(step, 4)
        elif t == "save":
            step = max(step, 3)
        elif t == "info" and "OCR" in msg:
            step = max(step, 2)
        elif t == "process":
            step = max(step, 1)
    return step

STALL_TIMEOUT = 45  # 秒，超过此时间无新日志判定为卡住

def get_stalled_info():
    """检测是否处理超时。返回 (is_stalled, step_stuck, seconds_since_last)"""
    step = get_current_step()
    # 空闲(0)或已完成(6)不算卡住
    if step == 0 or step == 6:
        return False, step, 0
    logs = read_logs(1)
    if not logs:
        return False, step, 0
    try:
        t = logs[0].get("time", "")
        last_time = datetime.datetime.strptime(t, "%H:%M:%S")
        now = datetime.datetime.now()
        diff = (now - last_time).total_seconds()
        if diff > STALL_TIMEOUT:
            return True, step, int(diff)
    except:
        pass
    return False, step, 0

def get_watcher_status():
    """检查 watcher 是否在运行"""
    # 看最后一条日志的时间
    logs = read_logs(1)
    if logs:
        last = logs[0]
        t = last.get("time", "")
        try:
            last_time = datetime.datetime.strptime(t, "%H:%M:%S")
            now = datetime.datetime.now()
            diff = (now - last_time).total_seconds()
            if diff < 30:
                return "running"
        except:
            pass
    return "stopped"

# ── GitHub Actions 状态缓存 ──────────────────────────

GH_OWNER = "qiqinmo-bit"
GH_REPO = "qiqinmo_hub"
GH_CACHE_FILE = os.path.join(BASE, "_memory", "gh_status_cache.json")

def fetch_gh_status():
    """尝试从 GitHub API 获取最近工作流状态，失败则返回缓存"""
    # 先检查缓存
    cache = {}
    if os.path.exists(GH_CACHE_FILE):
        try:
            with open(GH_CACHE_FILE, "r") as f:
                cache = json.load(f)
        except:
            pass

    cache_age = 0
    if cache.get("time"):
        try:
            t = datetime.datetime.fromisoformat(cache["time"])
            cache_age = (datetime.datetime.now() - t).total_seconds()
        except:
            pass

    # 缓存 5 分钟内有效，避免频繁请求被限流
    if cache_age < 300 and cache.get("workflows"):
        return cache

    # 尝试请求 GitHub API
    try:
        import urllib.request
        url = f"https://api.github.com/repos/{GH_OWNER}/{GH_REPO}/actions/runs?per_page=5"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.load(r)

        workflows = {}
        for run in data.get("workflow_runs", []):
            name = run["name"]
            if name not in workflows:
                workflows[name] = {
                    "status": run["status"],
                    "conclusion": run.get("conclusion"),
                    "updated": run["updated_at"][:19],
                    "url": run["html_url"]
                }

        result = {
            "time": datetime.datetime.now().isoformat(),
            "workflows": workflows
        }
        with open(GH_CACHE_FILE, "w") as f:
            json.dump(result, f, ensure_ascii=False)
        return result
    except Exception as e:
        # 失败返回缓存（如果有）
        if cache.get("workflows"):
            cache["offline"] = True
            return cache
        return {"time": datetime.datetime.now().isoformat(), "workflows": {}, "offline": True}

@app.route("/api/gh-status")
def api_gh_status():
    return jsonify(fetch_gh_status())

# ── 路由 ────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/progress")
def api_progress():
    return jsonify({"step": get_current_step(), "max": 6})

@app.route("/api/status")
def api_status():
    return jsonify({
        "watcher": get_watcher_status(),
        "today": get_today_count(),
        "total_entries": get_total_entries(),
        "step": get_current_step(),
        "stalled": get_stalled_info()[0],
        "stalled_step": get_stalled_info()[1],
        "stalled_seconds": get_stalled_info()[2],
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route("/api/logs")
def api_logs():
    tail = request.args.get("tail", 50, type=int)
    return jsonify(read_logs(tail))

# SSE 实时推送
@app.route("/stream")
def stream():
    last_count = 0
    def event_stream():
        nonlocal last_count
        while True:
            logs = read_logs(10)
            current_count = len(logs)
            if current_count != last_count:
                last_count = current_count
                yield f"data: {json.dumps(logs, ensure_ascii=False)}\n\n"
            time.sleep(2)
    return Response(event_stream(), mimetype="text/event-stream", 
                    headers={"Cache-Control": "no-cache", "Connection": "keep-alive"})

# ── 启动 ────────────────────────────────────────────

if __name__ == "__main__":
    # 修复 Flask 的 request 导入
    from flask import request

    # 屏蔽 Werkzeug 开发服务器警告和请求日志
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    import warnings
    warnings.filterwarnings('ignore', message='.*development server.*')

    print()
    print("=" * 45)
    print("  [仪表盘] 收图夹实时监控")
    print("=" * 45)
    print(f"\n  打开浏览器: http://localhost:5677")
    print(f"\n  按 Ctrl+C 停止\n")
    app.run(host="0.0.0.0", port=5677, debug=False, threaded=True)
