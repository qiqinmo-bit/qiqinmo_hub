# encoding: utf-8
"""
简易 Webhook 接收器 — 让 n8n 能将数据直接写入本地仓库。

用法:
  python _scripts/webhook_server.py

这会启动一个 HTTP 服务（默认 :5678），n8n 的 HTTP Request 节点可以 POST JSON 到:
  POST http://localhost:5678/webhook/inspiration

收到后自动调用 process_inspiration.py 的 n8n 模式处理数据。

可选依赖: Flask 或 uvicorn (FastAPI)
如果都没装，会提示安装。
"""

import sys, os, json, subprocess, tempfile

# Windows GBK 终端兼容
if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(BASE, "_scripts", "process_inspiration.py")


def process_payload(payload: dict) -> dict:
    """将 payload 写入临时文件，调用 process_inspiration.py 处理。"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", encoding="utf-8", delete=False
    ) as f:
        json.dump(payload, f, ensure_ascii=False)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, SCRIPT, "--n8n", tmp_path],
            capture_output=True, text=True, cwd=BASE
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    finally:
        os.unlink(tmp_path)


def run_with_flask():
    from flask import Flask, request, jsonify
    app = Flask(__name__)

    @app.route("/webhook/inspiration", methods=["POST"])
    def webhook():
        payload = request.get_json(silent=True) or {}
        result = process_payload(payload)
        return jsonify(result)

    print("[Webhook] Server started: http://localhost:5677/webhook/inspiration")
    print("[Webhook] Configure this URL in n8n's HTTP Request node (POST)")
    app.run(host="0.0.0.0", port=5677, debug=False)


def run_with_fastapi():
    import uvicorn
    from fastapi import FastAPI, Request
    app = FastAPI()

    @app.post("/webhook/inspiration")
    async def webhook(request: Request):
        payload = await request.json()
        return process_payload(payload)

    print("[Webhook] Server started: http://localhost:5677/webhook/inspiration")
    uvicorn.run(app, host="0.0.0.0", port=5677)


if __name__ == "__main__":
    print("=" * 50)
    print("[Inspiration Workflow] n8n Webhook Receiver")
    print("=" * 50)

    try:
        import flask
        run_with_flask()
    except ImportError:
        try:
            import fastapi
            run_with_fastapi()
        except ImportError:
            print("[Error] Need Flask or FastAPI. Install with:")
            print("   pip install flask")
            print("   # or")
            print("   pip install fastapi uvicorn")
            sys.exit(1)
