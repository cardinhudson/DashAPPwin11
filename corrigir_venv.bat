@echo off
chcp 65001 >nul
echo ================================================
echo    CORRECAO DO AMBIENTE VIRTUAL
echo ================================================
echo.

echo 🔍 Verificando ambiente virtual...
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Ambiente virtual não encontrado!
    echo.
    echo Criando novo ambiente virtual...
    python -m venv venv
    echo ✅ Ambiente virtual criado
    echo.
)

echo.
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo 📦 Reinstalando Streamlit para corrigir caminhos...
pip install --force-reinstall --no-cache-dir streamlit

echo.
echo ✅ Correção concluída!
echo.
echo Para executar o dashboard, use:
echo   streamlit run app.py
echo.
pause

