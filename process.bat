@echo off
chcp 65001 >nul
title 🧠 灵感一键处理

echo.
echo  =============================================
echo   🧠  日常灵感工作流 — 一键处理
echo  =============================================
echo.

if "%~1"=="" (
    echo  ❌ 没有文件
    echo  用法: 把截图拖到这个文件上
    echo.
    pause
    exit /b
)

echo  📄 处理: %~nx1
echo.

python _scripts\one_click.py "%~1"

echo.
pause
