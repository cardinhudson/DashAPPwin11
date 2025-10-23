@echo off
chcp 65001 >nul
echo ===============================================
echo    TESTANDO EXECUTÁVEL FINAL
echo ===============================================
echo.

echo 🔍 Verificando se o executável existe...
if exist "dist\app_executavel.exe" (
    echo ✅ Executável encontrado!
    echo.
    echo 🚀 Iniciando teste do executável...
    echo.
    echo ⚠️  ATENÇÃO: O executável pode demorar alguns segundos para iniciar
    echo ⚠️  Aguarde até aparecer a mensagem "You can now view your Streamlit app"
    echo.
    
    cd dist
    echo 📁 Executando de: %CD%
    echo.
    echo 🔧 Iniciando aplicação...
    start app_executavel.exe
    
    echo.
    echo ⏳ Aguardando 10 segundos para inicialização...
    timeout /t 10 /nobreak >nul
    
    echo.
    echo 🔍 Verificando se a aplicação está rodando...
    netstat -an | findstr :8501
    if %errorlevel% equ 0 (
        echo ✅ Dashboard está rodando na porta 8501!
        echo 🌐 Acesse: http://localhost:8501
        echo.
        echo 📋 Para parar a aplicação, feche esta janela ou pressione Ctrl+C
    ) else (
        echo ❌ Dashboard não está rodando na porta 8501
        echo.
        echo 🔧 Verificando processos Python...
        tasklist | findstr python
        if %errorlevel% equ 0 (
            echo ✅ Processo Python encontrado
        ) else (
            echo ❌ Nenhum processo Python encontrado
        )
    )
    
    echo.
    echo 🔍 Verificando se há erros no executável...
    echo Pressione qualquer tecla para verificar logs...
    pause >nul
    
) else (
    echo ❌ Executável não encontrado!
    echo.
    echo 🔧 Verificando pasta dist...
    dir dist
    echo.
    echo 🔧 Verificando se o build foi concluído...
    if exist "build" (
        echo ✅ Pasta build existe
    ) else (
        echo ❌ Pasta build não existe
    )
)

echo.
echo ===============================================
echo    TESTE FINALIZADO
echo ===============================================
echo.
pause



