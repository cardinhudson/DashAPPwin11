@echo off
chcp 65001 >nul
echo ===============================================
echo    BUILD OTIMIZADO - Dashboard KE5Z
echo    Versão: 3.1 - Otimizado para reduzir warnings
echo ===============================================
echo.

REM Verificar versão do Windows
echo 🔍 Verificando compatibilidade do sistema...
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
echo Sistema: Windows %VERSION%

REM Verificar Python
echo.
echo 🐍 Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: Python não encontrado!
    echo Instale Python 3.8+ e tente novamente.
    pause
    exit /b 1
)

python --version
echo ✅ Python encontrado

REM Verificar dependências
echo.
echo 📦 Verificando dependências...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  PyInstaller não encontrado. Instalando...
    pip install pyinstaller
)

pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Streamlit não encontrado. Instalando...
    pip install streamlit
)

echo ✅ Dependências verificadas

REM Parar processos anteriores
echo.
echo 🛑 Parando processos anteriores...
taskkill /f /im Dashboard_KE5Z_Desktop.exe >nul 2>&1
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im streamlit.exe >nul 2>&1
echo ✅ Processos parados

REM Limpar builds anteriores
echo.
echo 🧹 Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo ✅ Limpeza concluída

REM Verificar arquivos necessários
echo.
echo 📁 Verificando arquivos do projeto...
if not exist "app.py" (
    echo ❌ ERRO: app.py não encontrado!
    pause
    exit /b 1
)

if not exist "Dashboard_KE5Z_Desktop_OTIMIZADO.spec" (
    echo ❌ ERRO: Arquivo .spec otimizado não encontrado!
    pause
    exit /b 1
)

echo ✅ Arquivos verificados

REM Executar build com tratamento de erros
echo.
echo 🔨 Iniciando build otimizado...
echo Usando arquivo: Dashboard_KE5Z_Desktop_OTIMIZADO.spec
echo.

pyinstaller Dashboard_KE5Z_Desktop_OTIMIZADO.spec --noconfirm --clean

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERRO durante o build!
    echo.
    echo 🔧 Soluções possíveis:
    echo 1. Verifique se todos os arquivos estão presentes
    echo 2. Execute como administrador
    echo 3. Feche outros programas Python/Streamlit
    echo 4. Verifique se há antivírus bloqueando
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Build concluído com sucesso!

REM Verificar resultado
echo.
echo 🔍 Verificando resultado...
if exist "dist\Dashboard_KE5Z_Desktop\Dashboard_KE5Z_Desktop.exe" (
    echo ✅ Executável criado com sucesso!
    echo Localização: dist\Dashboard_KE5Z_Desktop\Dashboard_KE5Z_Desktop.exe
) else (
    echo ❌ Executável não encontrado!
    pause
    exit /b 1
)

REM Criar script de teste otimizado
echo.
echo 📝 Criando script de teste otimizado...
echo @echo off > "dist\Dashboard_KE5Z_Desktop\TESTAR_OTIMIZADO.bat"
echo chcp 65001 ^>nul >> "dist\Dashboard_KE5Z_Desktop\TESTAR_OTIMIZADO.bat"
echo echo =============================================== >> "dist\Dashboard_KE5Z_Desktop\TESTAR_OTIMIZADO.bat"
echo echo    TESTANDO DASHBOARD KE5Z - VERSÃO OTIMIZADA >> "dist\Dashboard_KE5Z_Desktop\TESTAR_OTIMIZADO.bat"
echo echo =============================================== >> "dist\Dashboard_KE5Z_Desktop\TESTAR_OTIMIZADO.bat"
echo echo. >> "dist\Dashboard_KE5Z_Desktop\TESTAR_OTIMIZADO.bat"
echo echo 🚀 Iniciando Dashboard KE5Z... >> "dist\Dashboard_KE5Z_Desktop\TESTAR_OTIMIZADO.bat"
echo echo Aguarde alguns segundos... >> "dist\Dashboard_KE5Z_Desktop\TESTAR_OTIMIZADO.bat"
echo echo. >> "dist\Dashboard_KE5Z_Desktop\TESTAR_OTIMIZADO.bat"
echo echo 💡 Se o dashboard não abrir automaticamente, >> "dist\Dashboard_KE5Z_Desktop\TESTAR_OTIMIZADO.bat"
echo echo    acesse: http://localhost:8501 >> "dist\Dashboard_KE5Z_Desktop\TESTAR_OTIMIZADO.bat"
echo echo. >> "dist\Dashboard_KE5Z_Desktop\TESTAR_OTIMIZADO.bat"
echo Dashboard_KE5Z_Desktop.exe >> "dist\Dashboard_KE5Z_Desktop\TESTAR_OTIMIZADO.bat"
echo pause >> "dist\Dashboard_KE5Z_Desktop\TESTAR_OTIMIZADO.bat"

echo ✅ Script de teste otimizado criado

REM Criar script de diagnóstico
echo.
echo 📝 Criando script de diagnóstico...
echo @echo off > "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo chcp 65001 ^>nul >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo echo =============================================== >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo echo    DIAGNÓSTICO - Dashboard KE5Z >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo echo =============================================== >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo echo. >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo echo 🔍 Verificando arquivos... >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo if exist "Dashboard_KE5Z_Desktop.exe" ^( >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo     echo ✅ Executável encontrado >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo ^) else ^( >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo     echo ❌ Executável não encontrado >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo ^) >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo. >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo if exist "_internal" ^( >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo     echo ✅ Pasta _internal encontrada >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo ^) else ^( >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo     echo ❌ Pasta _internal não encontrada >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo ^) >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo. >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo echo 🔍 Verificando portas... >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo netstat -an ^| findstr 8501 >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo. >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo echo 🔍 Verificando processos... >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo tasklist ^| findstr Dashboard >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo. >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"
echo pause >> "dist\Dashboard_KE5Z_Desktop\DIAGNOSTICO.bat"

echo ✅ Script de diagnóstico criado

echo.
echo ===============================================
echo    BUILD OTIMIZADO CONCLUÍDO COM SUCESSO!
echo ===============================================
echo.
echo 📁 Pasta do executável: dist\Dashboard_KE5Z_Desktop\
echo 🚀 Para testar: Execute TESTAR_OTIMIZADO.bat na pasta dist
echo 🔍 Para diagnóstico: Execute DIAGNOSTICO.bat na pasta dist
echo 📋 Para distribuir: Copie toda a pasta dist\Dashboard_KE5Z_Desktop\
echo.
echo 💡 MELHORIAS IMPLEMENTADAS:
echo - Console ativado para ver erros
echo - Otimizações de performance
echo - Exclusões de módulos desnecessários
echo - Scripts de diagnóstico incluídos
echo.
pause



