@echo off
echo ========================================
echo  Iniciando Dashboard Financeiro
echo ========================================
echo.

REM Obter o diretório do projeto
set PROJECT_DIR=%~dp0

REM Abrir 3 terminais cmd
start "Django Backend" cmd /k "cd /d %PROJECT_DIR%backend && echo ===== DJANGO BACKEND ===== && python manage.py runserver"

timeout /t 2 /nobreak >nul

start "Streamlit Frontend" cmd /k "cd /d %PROJECT_DIR%frontend && echo ===== STREAMLIT FRONTEND ===== && streamlit run Hub.py"

timeout /t 1 /nobreak >nul

start "Terminal Livre" cmd /k "cd /d %PROJECT_DIR% && echo ===== TERMINAL LIVRE ===== && echo Pronto para trabalhar!"

echo.
echo ========================================
echo  3 terminais abertos com sucesso!
echo ========================================
echo.
echo [1] Django Backend (http://localhost:8000)
echo [2] Streamlit Frontend (http://localhost:8501)
echo [3] Terminal Livre (na raiz do projeto)
echo.
pause