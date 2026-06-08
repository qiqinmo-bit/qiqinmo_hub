# encoding: utf-8
"""
OCR 辅助模块 — 将截图中的文字提取为结构化文本。

支持两种模式：
  1. PaddleOCR（推荐，精度高） — pip install paddleocr
  2. 简易 fallback — 仅返回文件路径提示（当 PaddleOCR 未安装时）

输出 JSON 格式，方便 n8n 和 process_inspiration.py 消费。
"""

import sys, os, json, datetime

# ── 配置 ────────────────────────────────────────────
# 支持的语言，按需增减
LANG_LIST = ["ch", "en"]  # 中文 + 英文

# ── 核心函数 ────────────────────────────────────────

def ocr_image(image_path: str) -> dict:
    """
    对单张图片执行 OCR，返回结构化结果。

    返回:
    {
        "success": true/false,
        "text": "识别的全文...",
        "segments": [
            {"text": "段落1", "confidence": 0.95, "position": [x1,y1,x2,y2]},
            ...
        ],
        "source": "paddleocr" | "fallback",
        "error": "错误信息(仅失败时)"
    }
    """
    # 先尝试 PaddleOCR
    result = _ocr_with_paddle(image_path)
    if result["success"]:
        return result

    # Fallback: 纯文件信息
    return {
        "success": True,
        "text": f"[OCR 未安装] 请手动查看图片: {image_path}",
        "segments": [],
        "source": "fallback",
        "error": None
    }


def ocr_directory(dir_path: str) -> dict:
    """对目录下所有图片执行 OCR，合并结果。"""
    image_exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}
    images = []
    for fname in sorted(os.listdir(dir_path)):
        ext = os.path.splitext(fname)[1].lower()
        if ext in image_exts:
            images.append(os.path.join(dir_path, fname))

    if not images:
        return {"success": True, "text": "", "segments": [], "source": "none"}

    # 有 description.md 时先读已有描述（避免重复 OCR）
    desc_path = os.path.join(dir_path, "description.md")
    if os.path.exists(desc_path):
        with open(desc_path, "r", encoding="utf-8") as f:
            existing = f.read()
        # 如果有用户手动写的描述，OCR 只作为补充
        if "## 描述" in existing and len(existing) > 100:
            existing_text = existing.split("## 描述", 1)[-1].strip()
            return {
                "success": True,
                "text": existing_text,
                "segments": [],
                "source": "existing_description",
                "note": "description.md 已存在，跳过 OCR"
            }

    # 对每张图 OCR 并合并
    all_text = []
    all_segments = []
    source = None
    for img_path in images:
        r = ocr_image(img_path)
        if r["success"]:
            if r["text"]:
                all_text.append(f"--- {os.path.basename(img_path)} ---\n{r['text']}")
            all_segments.extend(r["segments"])
            if r["source"]:
                source = r["source"]

    return {
        "success": True,
        "text": "\n\n".join(all_text),
        "segments": all_segments,
        "source": source or "fallback"
    }


# ── 内部实现 ────────────────────────────────────────

def _ocr_with_paddle(image_path: str) -> dict:
    """尝试用 PaddleOCR 识别。"""
    try:
        from paddleocr import PaddleOCR
    except ImportError:
        return {"success": False, "error": "paddleocr 未安装 (pip install paddleocr)"}

    try:
        ocr = PaddleOCR(use_angle_cls=True, lang=LANG_LIST[0], show_log=False)
        result = ocr.ocr(image_path, cls=True)

        if not result or not result[0]:
            return {"success": True, "text": "", "segments": [], "source": "paddleocr"}

        lines = []
        segments = []
        for line in result[0]:
            box, (text, confidence) = line
            if text and text.strip():
                lines.append(text.strip())
                segments.append({
                    "text": text.strip(),
                    "confidence": round(confidence, 4),
                    "position": [round(p, 1) for point in box for p in point]
                })

        return {
            "success": True,
            "text": "\n".join(lines),
            "segments": segments,
            "source": "paddleocr",
            "error": None
        }
    except Exception as e:
        return {"success": False, "error": f"PaddleOCR 识别失败: {e}"}


# ── CLI 入口 ─────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="截图 OCR 提取工具")
    parser.add_argument("path", help="图片路径或含图片的目录")
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径（默认 stdout）")
    parser.add_argument("--pretty", "-p", action="store_true", help="美化 JSON 输出")
    args = parser.parse_args()

    path = args.path
    if os.path.isdir(path):
        result = ocr_directory(path)
    elif os.path.isfile(path):
        result = ocr_image(path)
    else:
        print(json.dumps({"success": False, "error": f"路径不存在: {path}"}))
        sys.exit(1)

    output = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"OCR 结果已保存: {args.output}")
    else:
        print(output)
