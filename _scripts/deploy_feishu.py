# encoding: utf-8
"""
飞书 Bot 一键部署脚本 — 自动完成所有配置。

用法:
  python _scripts/deploy_feishu.py

流程:
  1. 交互式输入飞书 App ID / Secret / Verify Token
  2. 保存到 .env 文件
  3. 安装依赖 (python-dotenv, requests)
  4. 下载隧道工具 (natapp) 用于内网穿透
  5. 启动飞书 Bot + 隧道
  6. 打印公网 URL 供飞书配置
"""

import sys, os, json, subprocess, threading, time, signal, webbrowser

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── 工具函数 ────────────────────────────────────────

def print_step(n, text):
    print(f"\n[{n}/6] {text}")
    print("-" * 40)

def print_ok(text):
    print(f"  ✅ {text}")

def print_info(text):
    print(f"  ℹ️  {text}")

def print_warn(text):
    print(f"  ⚠️  {text}")

def run_cmd(cmd, timeout=120, capture=True):
    """运行命令并返回 (ok, output)。"""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=capture,
                          text=True, timeout=timeout, cwd=BASE)
        ok = r.returncode == 0
        out = (r.stdout or "") + ("\n" + r.stderr if r.stderr else "")
        return ok, out.strip()
    except subprocess.TimeoutExpired:
        return False, "超时"
    except Exception as e:
        return False, str(e)


# ── 步骤实现 ────────────────────────────────────────

def step1_input_config():
    """交互式输入飞书配置。"""
    print("\n📝 请输入飞书应用配置（在 https://open.feishu.cn/ 创建应用后获取）")
    print("   留空则跳过，之后可手动编辑 .env 文件\n")

    app_id = input("  FEISHU_APP_ID (App ID): ").strip()
    app_secret = input("  FEISHU_APP_SECRET (App Secret): ").strip()
    verify_token = input("  FEISHU_VERIFY_TOKEN (验证Token): ").strip()

    if not app_id or not app_secret:
        print_warn("App ID 和 Secret 不能为空，跳过配置")
        return False

    # 保存到 .env
    env_path = os.path.join(BASE, ".env")
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(f"FEISHU_APP_ID={app_id}\n")
        f.write(f"FEISHU_APP_SECRET={app_secret}\n")
        f.write(f"FEISHU_VERIFY_TOKEN={verify_token}\n")
        f.write(f"PORT=5676\n")

    print_ok(f"配置已保存到 {env_path}")
    return True


def step2_install_deps():
    """安装 Python 依赖。"""
    print_info("安装 python-dotenv...")
    ok, out = run_cmd(f"{sys.executable} -m pip install python-dotenv -q")
    if ok:
        print_ok("python-dotenv 安装成功")
    else:
        print_warn(f"安装失败: {out[:100]}")
        print_warn("请手动执行: pip install python-dotenv")

    # Flask 可能也没装
    try:
        import flask
    except ImportError:
        print_info("安装 flask...")
        ok, out = run_cmd(f"{sys.executable} -m pip install flask -q")
        if ok:
            print_ok("flask 安装成功")
        else:
            print_warn("请手动执行: pip install flask")

    # 验证 requests
    try:
        import requests
        print_ok("依赖就绪 (dotenv, flask, requests)")
    except ImportError:
        print_warn("部分依赖未安装，请运行: pip install python-dotenv flask requests")


def step3_download_tunnel():
    """
    下载隧道工具。
    优先用 natapp（国内友好），备选 ngrok。
    """
    # 检查是否已有
    natapp_path = os.path.join(BASE, "_scripts", "natapp.exe")
    ngrok_path = os.path.join(BASE, "_scripts", "ngrok.exe")

    if os.path.exists(natapp_path):
        print_ok("natapp.exe 已存在")
        return "natapp"
    if os.path.exists(ngrok_path):
        print_ok("ngrok.exe 已存在")
        return "ngrok"

    print_info("下载 natapp (内网穿透工具)...")
    import urllib.request
    natapp_url = "https://cdn.natapp.cn/assets/downloads/client/natapp.exe"
    try:
        urllib.request.urlretrieve(natapp_url, natapp_path)
        if os.path.exists(natapp_path):
            print_ok(f"natapp 已下载 ({os.path.getsize(natapp_path)//1024}KB)")
            return "natapp"
    except Exception as e:
        print_warn(f"natapp 下载失败: {e}")

    # 尝试 ngrok
    print_info("尝试下载 ngrok...")
    try:
        ngrok_zip = os.path.join(BASE, "_scripts", "ngrok.zip")
        ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
        urllib.request.urlretrieve(ngrok_url, ngrok_zip)
        import zipfile
        with zipfile.ZipFile(ngrok_zip, "r") as zf:
            zf.extract("ngrok.exe", os.path.join(BASE, "_scripts"))
        os.remove(ngrok_zip)
        if os.path.exists(ngrok_path):
            print_ok(f"ngrok 已下载")
            return "ngrok"
    except Exception as e:
        print_warn(f"ngrok 下载也失败了: {e}")

    return None


def step4_update_feishu_bot():
    """更新 feishu_bot.py 使其支持从 .env 加载配置。"""
    bot_path = os.path.join(BASE, "_scripts", "feishu_bot.py")

    with open(bot_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 如果已经有 dotenv 加载逻辑则跳过
    if "load_dotenv" in content:
        print_ok("feishu_bot.py 已支持 .env")
        return

    # 在文件开头的 import 之后添加 dotenv 加载
    old = ('import sys, os, json, hashlib, base64, hmac, re, datetime')
    new = ('import sys, os, json, hashlib, base64, hmac, re, datetime\n'
           'from dotenv import load_dotenv\n'
           'load_dotenv()  # 从 .env 文件加载配置')

    if old in content:
        content = content.replace(old, new)
        with open(bot_path, "w", encoding="utf-8") as f:
            f.write(content)
        print_ok("feishu_bot.py 已添加 .env 支持")
    else:
        print_info("手动检查 feishu_bot.py 头部是否有 dotenv 加载")


def step5_start_services():
    """启动飞书 Bot + 隧道。"""
    processes = []

    # 5a. 启动 feishu_bot.py
    print_info("启动飞书 Bot (端口 5676)...")
    bot_cmd = f"{sys.executable} {os.path.join(BASE, '_scripts', 'feishu_bot.py')}"
    bot_proc = subprocess.Popen(
        bot_cmd, shell=True, cwd=BASE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace"
    )
    processes.append(("飞书 Bot", bot_proc))
    time.sleep(2)

    # 检查是否启动成功
    import urllib.request
    try:
        resp = urllib.request.urlopen("http://localhost:5676/feishu/health", timeout=3)
        status = json.loads(resp.read().decode())
        print_ok(f"飞书 Bot 运行中 (配置: {status.get('feishu_configured', '?')})")
    except Exception as e:
        print_warn(f"飞书 Bot 启动检查失败: {e}")
        print_info("请手动检查: python _scripts/feishu_bot.py")

    # 5b. 启动隧道
    tunnel_type = "natapp"
    natapp_path = os.path.join(BASE, "_scripts", "natapp.exe")
    ngrok_path = os.path.join(BASE, "_scripts", "ngrok.exe")

    tunnel_url = None

    if os.path.exists(natapp_path):
        print_info("启动 natapp 隧道 (HTTP -> localhost:5676)...")
        # natapp 需要用配置文件指定端口
        config = os.path.join(BASE, "_scripts", "natapp_config.ini")
        with open(config, "w", encoding="utf-8") as f:
            f.write("[default]\n")
            f.write("authtoken=\n")  # 免费版不需要 token
            f.write("clienttoken=\n")
            f.write("log=none\n")
            f.write("loglevel=ERROR\n")
            f.write("server=server.natappfree.cc\n")  # 免费服务器
            f.write("http_proxy=\n")

        natapp_cmd = f"{natapp_path} -config={config} -tcp -localport=5676"
        tunnel_proc = subprocess.Popen(
            natapp_cmd, shell=True, cwd=os.path.join(BASE, "_scripts"),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace"
        )
        processes.append(("natapp 隧道", tunnel_proc))

        # 等几秒获取 URL
        time.sleep(5)
        try:
            out = tunnel_proc.stdout.read(2048) if tunnel_proc.stdout else ""
            for line in out.split("\n"):
                if "http" in line.lower() and "natapp" in line.lower():
                    tunnel_url = line.strip()
        except:
            pass

    elif os.path.exists(ngrok_path):
        print_info("启动 ngrok 隧道...")
        ngrok_cmd = f"{ngrok_path} http 5676 --log=stdout"
        tunnel_proc = subprocess.Popen(
            ngrok_cmd, shell=True, cwd=os.path.join(BASE, "_scripts"),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace"
        )
        processes.append(("ngrok 隧道", tunnel_proc))

        time.sleep(4)
        try:
            import urllib.request
            resp = urllib.request.urlopen("http://localhost:4040/api/tunnels", timeout=3)
            data = json.loads(resp.read().decode())
            for t in data.get("tunnels", []):
                if t.get("public_url", "").startswith("https"):
                    tunnel_url = t["public_url"]
                    break
        except:
            pass

    return processes, tunnel_url


def print_summary(tunnel_url):
    """打印部署完成信息。"""
    print("\n" + "=" * 50)
    print("🎉 部署完成！")
    print("=" * 50)

    if tunnel_url:
        callback_url = f"{tunnel_url}/feishu/webhook"
        print(f"\n📌 飞书回调地址:")
        print(f"   {callback_url}")
        print(f"\n   将此地址填入飞书开放平台:")
        print(f"   应用 → 事件订阅 → 回调地址")
    else:
        print("\n⚠️  未获取到公网地址")
        print("   请手动配置隧道后使用以下地址:")
        print("   http://你的公网IP:5676/feishu/webhook")

    print(f"""
📋 还需要在飞书开放平台完成:
  1. 事件订阅 → 添加事件 → im.message.receive_v1
  2. 权限管理 → 添加 → im:message
  3. 安全设置 → 设置 Verification Token (与 .env 一致)
  4. 发布 → 创建版本 → 上线
  5. 应用 → 添加 Bot 能力

💡 测试方法:
  在飞书给 Bot 发消息，如果收到 "✅ 灵感已收录" 回复就成功了

🔧 管理命令:
  python _scripts/feishu_bot.py     # 单独启动 Bot
  python _scripts/deploy_feishu.py  # 重新部署
""")


def cleanup(processes, signum=None, frame=None):
    """退出时清理子进程。"""
    print("\n\n🛑 正在关闭服务...")
    for name, proc in processes:
        try:
            proc.terminate()
            proc.wait(timeout=3)
            print_ok(f"{name} 已关闭")
        except:
            try:
                proc.kill()
                print_ok(f"{name} 已强制关闭")
            except:
                pass
    sys.exit(0)


# ── 主流程 ────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 飞书 Bot 一键部署")
    print("   日常灵感工作流")
    print("=" * 50)

    # 注册退出信号
    processes = []
    signal.signal(signal.SIGINT, lambda s, f: cleanup(processes))
    signal.signal(signal.SIGTERM, lambda s, f: cleanup(processes))

    # Step 1: 输入配置
    print_step(1, "输入飞书应用配置")
    has_config = os.path.exists(os.path.join(BASE, ".env"))
    if has_config:
        print_info("检测到已有 .env 文件")
        from dotenv import load_dotenv
        load_dotenv(os.path.join(BASE, ".env"))
        if os.environ.get("FEISHU_APP_ID"):
            print_ok(f"已配置: {os.environ['FEISHU_APP_ID']}")
            use_existing = input("使用现有配置? (Y/n): ").strip().lower()
            if use_existing == "n":
                step1_input_config()
        else:
            step1_input_config()
    else:
        step1_input_config()

    # Step 2: 安装依赖
    print_step(2, "安装 Python 依赖")
    step2_install_deps()

    # Step 3: 下载隧道工具
    print_step(3, "下载内网穿透工具")
    tunnel = step3_download_tunnel()
    if tunnel:
        print_ok(f"隧道工具: {tunnel}")
    else:
        print_warn("未自动下载隧道工具")
        print_info("请手动下载 natapp: https://natapp.cn/ 并放到 _scripts/ 目录")
        input("按回车继续...")

    # Step 4: 更新 feishu_bot.py
    print_step(4, "更新 Bot 脚本")
    step4_update_feishu_bot()

    # Step 5: 启动服务
    print_step(5, "启动服务")
    processes, tunnel_url = step5_start_services()

    # Step 6: 打印配置指引
    print_step(6, "配置飞书开放平台")
    print_summary(tunnel_url)

    # 保持运行
    print("\n⏳ 服务运行中，按 Ctrl+C 停止...\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup(processes)
