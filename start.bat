@echo off
chcp 65001 >nul
cls
echo ========================================
echo Enterprise Report System - Startup
echo ========================================
echo.

echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.7+
    pause
    exit /b 1
)
echo OK: Python installed
echo.

echo [2/3] Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install flask pandas openpyxl python-docx matplotlib reportlab pillow
) else (
    echo OK: Dependencies installed
)
echo.

echo [3/3] Starting web server...
echo.
echo ========================================
echo System URLs:
echo   Client: http://localhost:5000
echo   Questionnaire: http://localhost:5000/questionnaire
echo   Admin: http://localhost:5000/admin/login
echo.
echo Default Admin Account:
echo   Username: admin
echo   Password: admin123
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
