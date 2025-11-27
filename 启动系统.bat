@echo off
chcp 65001 >nul
echo ========================================
echo 企业现代制度评价系统 - 启动脚本
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python，请先安装Python 3.7+
    pause
    exit /b 1
)
echo ✅ Python环境正���
echo.

echo [2/3] 检查依赖包...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  缺少依赖包，正在安装...
    pip install flask pandas openpyxl python-docx matplotlib reportlab pillow
) else (
    echo ✅ 依赖包已安装
)
echo.

echo [3/3] 启动Web服务器...
echo.
echo ========================================
echo 系统访问地址：
echo   客户端首页: http://localhost:5000
echo   在线问卷: http://localhost:5000/questionnaire
echo   管理员登录: http://localhost:5000/admin/login
echo.
echo 默认管理员账号:
echo   用户名: admin
echo   密码: admin123
echo ========================================
echo.
echo 按 Ctrl+C 停止服务器
echo.

python app.py

pause
