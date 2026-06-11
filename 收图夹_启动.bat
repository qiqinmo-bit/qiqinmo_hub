@echo off
chcp 65001 >nul
title 📸 收图夹 — 自动监听

echo.
echo  =============================================
echo   📸  收图夹 — 自动截图处理
echo  =============================================
echo.
echo  把截图或照片放进「收图夹」文件夹
echo  会自动 OCR → 入库 → 推送到 GitHub
echo.
echo  按 Ctrl+C 停止监听
echo.

python _scripts\watcher.py

pause
