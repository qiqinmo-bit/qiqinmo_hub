# encoding: utf-8
"""
飞书 Bot 转发器 — 将飞书消息自动转发到灵感工作流。

工作流程:
  用户在飞书给 Bot 发消息
  → 飞书服务器 POST 到本脚本的 /feishu/webhook
  → 提取消息文本
  → 转发到 process_inspiration.py (n8n 格式)

部署:
  python _scripts/feishu_bot.py
  服务启动在 http://0.0.0.0:5676/feishu/webhook

配置(环境变量):
  FEISHU_APP_ID       — 飞书应用的 App ID
  FEISHU_APP_SECRET   — 飞书应用的 App Secret
  FEISHU_VERIFY_TOKEN — 飞书事件订阅的 Verification Token
  (如不配置则只接收不回复)
"""

import sys, os, json, hashlib, base64, hmac, re, datetime

# Windows GBK 兼容
if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "gb2312"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests

# ── 配置 ────────────────────────────────────────────

# 从环境变量读取飞书配置
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
FEISHU_VERIFY_TOKEN = os.environ.get("FEISHU_VERIFY_TOKEN", "")

# 灵感工作流本地的 processor 地址
LOCAL_WEBHOOK = "http://localhost:5677/webhook/inspiration"

# 监听的端口
PORT = int(os.environ.get("PORT", "5676"))

# ── 飞书 API ────────────────────────────────────────

_token_cache = {"token": None, "expire": 0}

def get_tenant_token() -> str:
    """获取飞书 tenant_access_token（自动缓存）。"""
    if _token_cache["token"] and _token_cache["expire"] > datetime.datetime.now().timestamp():
        return _token_cache["token"]

    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        return ""

    try:
        resp = requests.post(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET},
            timeout=10
        )
        data = resp.json()
        if data.get("code") == 0:
            _token_cache["token"] = data["tenant_access_token"]
            _token_cache["expire"] = datetime.datetime.now().timestamp() + data.get("expire", 7200) - 60
            return _token_cache["token"]
        else:
            print(f"[Feishu] 获取 token 失败: {data}")
    except Exception as e:
        print(f"[Feishu] Token 请求异常: {e}")
    return ""


def reply_message(message_id: str, text: str) -> bool:
    """回复飞书消息。"""
    token = get_tenant_token()
    if not token:
        return False

    try:
        resp = requests.post(
            f"https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/reply",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"content": json.dumps({"text": text}, ensure_ascii=False)},
            timeout=10
        )
        data = resp.json()
        if data.get("code") == 0:
            return True
        else:
            print(f"[Feishu] 回复失败: {data.get('msg', '')}")
    except Exception as e:
        print(f"[Feishu] 回复异常: {e}")
    return False


# ── 消息处理 ────────────────────────────────────────

def parse_feishu_message(body: dict) -> dict:
    """
    解析飞书事件回调，提取消息内容。

    支持事件类型:
      - im.message.receive_v1 (事件订阅)
      - url_verification (飞书验证回调)
    """
    # 飞书 URL 验证
    if body.get("type") == "url_verification":
        return {"type": "verify", "challenge": body.get("challenge", "")}

    # 事件回调
    event = body.get("event", {})
    message = event.get("message", {})
    msg_type = message.get("message_type", "")
    content_str = message.get("content", "{}")

    # 只处理文本消息
    if msg_type != "text":
        return {"type": "ignore", "reason": f"不支持的格式: {msg_type}"}

    try:
        content = json.loads(content_str)
    except json.JSONDecodeError:
        return {"type": "ignore", "reason": "content 解析失败"}

    text = content.get("text", "").strip()

    # 去掉 @bot 前缀（飞书文本消息中 @bot 格式如 " @机器人名 "）
    text = re.sub(r'@_?\w+', '', text).strip()

    if not text:
        return {"type": "ignore", "reason": "空消息"}

    # 提取发送者信息
    sender = event.get("sender", {})
    sender_id = sender.get("sender_id", {})

    return {
        "type": "message",
        "text": text,
        "message_id": message.get("message_id", ""),
        "chat_id": event.get("chat_id", ""),
        "sender": {
            "id": sender_id.get("open_id", ""),
            "name": sender_id.get("name", "未知")
        }
    }


def forward_to_workflow(text: str) -> dict:
    """将消息转发到灵感工作流的 webhook。"""
    title = text.strip().split("\n")[0][:40]  # 取第一行/前40字做标题
    payload = {
        "source": "feishu",
        "title": title,
        "text": text,
        "tags": ["飞书", "灵感"],
        "screenshot_path": None
    }
    try:
        resp = requests.post(LOCAL_WEBHOOK, json=payload, timeout=10)
        result = resp.json() if resp.ok else {"error": f"HTTP {resp.status_code}"}
        return {"success": resp.ok, "result": result}
    except requests.exceptions.ConnectionError:
        return {"success": False, "result": {"error": f"无法连接 {LOCAL_WEBHOOK} — webhook 服务未运行?"}}
    except Exception as e:
        return {"success": False, "result": {"error": str(e)}}


# ── Flask 服务 ──────────────────────────────────────

def create_app():
    from flask import Flask, request, jsonify

    app = Flask(__name__)

    @app.route("/feishu/webhook", methods=["POST"])
    def feishu_webhook():
        body = request.get_json(silent=True) or {}
        print(f"[Feishu] 收到消息: {json.dumps(body, ensure_ascii=False)[:200]}")

        # 1. 验证飞书事件订阅的 Verification Token
        token = body.get("token", "")
        if FEISHU_VERIFY_TOKEN and token != FEISHU_VERIFY_TOKEN:
            print(f"[Feishu] Token 不匹配 (期望: {FEISHU_VERIFY_TOKEN}, 收到: {token})")
            return jsonify({"error": "token mismatch"}), 403

        # 2. 解析消息
        parsed = parse_feishu_message(body)

        # 3. 飞书 URL 验证 - 直接返回 challenge
        if parsed["type"] == "verify":
            print("[Feishu] URL 验证通过")
            return jsonify({"challenge": parsed["challenge"]})

        # 4. 非文本消息忽略
        if parsed["type"] == "ignore":
            print(f"[Feishu] 忽略: {parsed.get('reason', '')}")
            return jsonify({"status": "ignored", "reason": parsed.get("reason", "")})

        # 5. ⭐ 转发到灵感工作流
        text = parsed["text"]
        print(f"[Feishu] 处理消息: {text[:60]}...")
        fwd_result = forward_to_workflow(text)

        # 6. 回复用户（可选）
        if fwd_result["success"] and parsed.get("message_id"):
            msg = f"✅ 灵感已收录！标题: {text[:30]}..."
            if LOCAL_WEBHOOK:
                msg += "\n分析中...请稍候"
            reply_message(parsed["message_id"], msg)

        # 7. 返回给飞书
        if fwd_result["success"]:
            return jsonify({"status": "ok"})
        else:
            print(f"[Feishu] 转发失败: {fwd_result['result']}")
            # 失败也返回 200 给飞书，避免飞书重试轰炸
            return jsonify({"status": "forward_failed", "detail": str(fwd_result["result"])})

    @app.route("/feishu/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok",
            "feishu_configured": bool(FEISHU_APP_ID and FEISHU_APP_SECRET),
            "webhook": LOCAL_WEBHOOK
        })

    return app


# ── CLI 入口 ────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("🔌 飞书 Bot 转发器 — 日常灵感工作流")
    print("=" * 50)
    print(f"  监听端口: {PORT}")
    print(f"  回调地址: http://你的IP:{PORT}/feishu/webhook")
    print(f"  转发目标: {LOCAL_WEBHOOK}")
    print(f"  飞书配置:", "✅ 已配置" if FEISHU_APP_ID else "⚠️  未配置 (仅接收不回复)")
    print()
    print("📋 步骤:")
    print("  1. 在 https://open.feishu.cn/ 创建应用")
    print("  2. 开启「事件订阅」→ 添加事件 im.message.receive_v1")
    print("  3. 回调地址填: http://你的IP:{PORT}/feishu/webhook")
    print("  4. 在「权限管理」添加 im:message 权限并发布")
    print("  5. 设置环境变量:")
    print("     FEISHU_APP_ID / FEISHU_APP_SECRET / FEISHU_VERIFY_TOKEN")
    print("=" * 50)

    app = create_app()

    # 如果用 nginx/caddy 反代，可关掉 debug
    app.run(host="0.0.0.0", port=PORT, debug=False)
