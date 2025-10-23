@echo off
chcp 65001 >nul
echo ===============================================
echo    CRIANDO EXECUTÁVEL FINAL - Dashboard KE5Z
echo ===============================================
echo.

echo 🧹 Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo ✅ Limpeza concluída

echo.
echo 🔧 Configurando ambiente para PyInstaller...
echo.

REM Configurar variáveis de ambiente para resolver problema do Streamlit
set PYTHONPATH=%CD%
set STREAMLIT_SERVER_HEADLESS=true
set STREAMLIT_SERVER_PORT=8501

echo.
echo 🔨 Criando executável com configurações otimizadas...
echo.

pyinstaller ^
    --onefile ^
    --name Dashboard_KE5Z_FUNCIONAL ^
    --console ^
    --add-data "app_executavel.py;." ^
    --add-data "KE5Z;KE5Z" ^
    --add-data "pages;pages" ^
    --add-data "arquivos;arquivos" ^
    --add-data "usuarios.json;." ^
    --add-data "usuarios_padrao.json;." ^
    --add-data "dados_equipe.json;." ^
    --add-data "Dados SAPIENS.xlsx;." ^
    --add-data "Fornecedores.xlsx;." ^
    --hidden-import streamlit ^
    --hidden-import streamlit.web ^
    --hidden-import streamlit.runtime ^
    --hidden-import streamlit.runtime.scriptrunner ^
    --hidden-import pandas ^
    --hidden-import plotly ^
    --hidden-import altair ^
    --hidden-import pyarrow ^
    --hidden-import numpy ^
    --hidden-import openpyxl ^
    --hidden-import xlsxwriter ^
    --exclude-module tkinter ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    --exclude-module IPython ^
    --exclude-module jupyter ^
    --exclude-module notebook ^
    --exclude-module pytest ^
    --exclude-module sphinx ^
    --exclude-module setuptools ^
    --exclude-module tensorflow ^
    --exclude-module torch ^
    --exclude-module sklearn ^
    --exclude-module seaborn ^
    --exclude-module bokeh ^
    --exclude-module dash ^
    --noconfirm ^
    app_executavel.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERRO durante o build!
    echo.
    echo 🔧 Tentando abordagem alternativa...
    echo.
    
    REM Tentar build mais simples
    pyinstaller ^
        --onefile ^
        --name Dashboard_KE5Z_FUNCIONAL ^
        --console ^
        --hidden-import streamlit ^
        --hidden-import pandas ^
        --hidden-import plotly ^
        --exclude-module tkinter ^
        --exclude-module matplotlib ^
        --noconfirm ^
        app_executavel.py
)

echo.
echo 🔍 Verificando resultado...
if exist "dist\Dashboard_KE5Z_FUNCIONAL.exe" (
    echo ✅ Executável criado com sucesso!
    echo Localização: dist\Dashboard_KE5Z_FUNCIONAL.exe
    echo.
    echo 🚀 Para testar: Execute o arquivo .exe na pasta dist
    echo.
    echo 📋 Copiando arquivos necessários...
    if exist "KE5Z" xcopy KE5Z dist\KE5Z\ /E /I /Y
    if exist "pages" xcopy pages dist\pages\ /E /I /Y
    if exist "arquivos" xcopy arquivos dist\arquivos\ /E /I /Y
    if exist "usuarios.json" copy usuarios.json dist\
    if exist "usuarios_padrao.json" copy usuarios_padrao.json dist\
    if exist "dados_equipe.json" copy dados_equipe.json dist\
    if exist "Dados SAPIENS.xlsx" copy "Dados SAPIENS.xlsx" dist\
    if exist "Fornecedores.xlsx" copy Fornecedores.xlsx dist\
    echo ✅ Arquivos copiados!
) else (
    echo ❌ Executável não encontrado!
    echo.
    echo 🔧 Soluções possíveis:
    echo 1. Verifique se o PyInstaller está instalado
    echo 2. Execute como administrador
    echo 3. Verifique se há antivírus bloqueando
    echo 4. Tente com versão mais antiga do Streamlit
)

echo.
echo ===============================================
echo    BUILD FINALIZADO
echo ===============================================
echo.
pause



