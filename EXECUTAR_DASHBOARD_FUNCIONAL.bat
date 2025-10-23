@echo off
chcp 65001 >nul
echo ===============================================
echo    DASHBOARD KE5Z - EXECUÇÃO FUNCIONAL
echo ===============================================
echo.

echo 🔍 Verificando ambiente...
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Ambiente virtual não encontrado!
    echo Execute primeiro: python -m venv venv
    pause
    exit /b 1
)

echo ✅ Ambiente virtual encontrado

echo.
echo 🐍 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo 📦 Verificando dependências...
python -c "import streamlit; print('✅ Streamlit OK')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Streamlit não encontrado!
    echo Instalando dependências...
    pip install -r requirements.txt
)

echo.
echo 🚀 Iniciando Dashboard KE5Z...
echo.
echo 💡 O dashboard abrirá automaticamente no navegador
echo 💡 Para parar, pressione Ctrl+C nesta janela
echo 💡 Se não abrir automaticamente, acesse: http://localhost:8501
echo.

streamlit run app.py --server.headless true --server.port 8501

echo.
echo 📊 Dashboard finalizado
pause



