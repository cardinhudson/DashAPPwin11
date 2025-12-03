@echo off
chcp 65001 >nul
echo ================================================
echo    DASHBOARD KE5Z - ABRINDO COM CORRECOES
echo ================================================
echo.

echo 🔍 Verificando porta 8501...
netstat -ano | findstr :8501 >nul
if %errorlevel% equ 0 (
    echo ⚠️  Porta 8501 está em uso!
    echo.
    echo 🔧 Tentando liberar a porta...
    echo.
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501 ^| findstr LISTENING') do (
        echo Encerrando processo PID: %%a...
        taskkill /F /PID %%a >nul 2>&1
        if !errorlevel! equ 0 (
            echo ✅ Processo %%a encerrado
        ) else (
            echo ⚠️  Não foi possível encerrar processo %%a (pode precisar de permissões de admin)
        )
    )
    timeout /t 2 >nul
    echo.
    echo ✅ Tentando iniciar Streamlit...
    echo.
)

echo 🚀 Iniciando Dashboard KE5Z...
echo.
echo 💡 O dashboard abrirá automaticamente no navegador
echo 💡 Para parar, pressione Ctrl+C nesta janela
echo 💡 Se não abrir automaticamente, acesse: http://localhost:8501
echo.

streamlit run app.py --server.headless true --server.port 8501

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Erro ao iniciar na porta 8501. Tentando porta alternativa...
    streamlit run app.py --server.headless true --server.port 8502
)

echo.
echo 📊 Dashboard finalizado
pause

