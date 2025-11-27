@echo off
chcp 65001 >nul
cls
echo ========================================
echo 专业报告生成工具
echo ========================================
echo.
echo 请选择要生成的报告类型:
echo.
echo 1. 生成专业版企业报告（单个企业）
echo 2. 生成综合分析报告（多个企业）
echo 0. 退出
echo.
echo ========================================
echo.

set /p choice=请输入选项 (0-2):

if "%choice%"=="1" (
    echo.
    echo 正在生成专业版企业报告...
    python test_professional_report.py
) else if "%choice%"=="2" (
    echo.
    echo 正在生成综合分析报告...
    python test_comprehensive_report.py
) else if "%choice%"=="0" (
    echo.
    echo 退出程序
    exit /b 0
) else (
    echo.
    echo 无效选项，请重新运行
    pause
    exit /b 1
)
