@echo off
echo ===============================================
echo    DASHBOARD KE5Z - INICIANDO APLICACAO
echo ===============================================
echo.
echo Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.8+ e tente novamente.
    pause
    exit /b 1
)

echo.
echo Verificando dependencias...
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

echo.
echo Iniciando Dashboard...
echo A aplicacao abrira automaticamente no navegador.
echo Para parar, pressione Ctrl+C nesta janela.
echo.
echo ===============================================

python -m streamlit run app.py --server.headless true --server.port 8501

pause

