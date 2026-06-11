@echo off
chcp 65001 >nul
title 📊 收图夹仪表盘

echo.
echo  =============================================
echo   📊  收图夹 — 仪表盘
echo  =============================================
echo.
echo  打开浏览器查看: http://localhost:5677
echo  按 Ctrl+C 停止
echo.

python _scripts\web_dashboard.py
pause
