@echo off
chcp 65001 >nul
echo ===============================================
echo    CRIANDO EXECUTÁVEL FUNCIONAL
echo ===============================================
echo.

echo 🧹 Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo ✅ Limpeza concluída

echo.
echo 🔨 Criando executável funcional...
echo.

pyinstaller ^
    --onefile ^
    --name Dashboard_KE5Z_Funcional ^
    --console ^
    --add-data "dashboard_funcional.py;." ^
    --hidden-import streamlit ^
    --hidden-import pandas ^
    --hidden-import plotly ^
    --hidden-import altair ^
    --hidden-import pyarrow ^
    --hidden-import numpy ^
    --exclude-module tkinter ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    dashboard_funcional.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERRO durante o build!
    echo.
    echo 🔧 Tentando abordagem alternativa...
    echo.
    
    pyinstaller ^
        --onefile ^
        --name Dashboard_KE5Z_Funcional ^
        --console ^
        dashboard_funcional.py
)

echo.
echo 🔍 Verificando resultado...
if exist "dist\Dashboard_KE5Z_Funcional.exe" (
    echo ✅ Executável criado com sucesso!
    echo Localização: dist\Dashboard_KE5Z_Funcional.exe
    echo.
    echo 🚀 Para testar: Execute o arquivo .exe na pasta dist
) else (
    echo ❌ Executável não encontrado!
    echo.
    echo 🔧 Soluções possíveis:
    echo 1. Verifique se o PyInstaller está instalado
    echo 2. Execute como administrador
    echo 3. Verifique se há antivírus bloqueando
)

echo.
pause



