@echo off
chcp 65001 >nul
echo ===============================================
echo    BUILD COMPATÍVEL - Dashboard KE5Z
echo    Versão: 2.0 - Compatível com Windows 10/11
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

if not exist "Dashboard_KE5Z_Desktop_ATUALIZADO.spec" (
    echo ❌ ERRO: Arquivo .spec não encontrado!
    pause
    exit /b 1
)

echo ✅ Arquivos verificados

REM Executar build com tratamento de erros
echo.
echo 🔨 Iniciando build...
echo Usando arquivo: Dashboard_KE5Z_Desktop_ATUALIZADO.spec
echo.

pyinstaller Dashboard_KE5Z_Desktop_ATUALIZADO.spec --noconfirm --clean

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

REM Criar script de teste
echo.
echo 📝 Criando script de teste...
echo @echo off > "dist\Dashboard_KE5Z_Desktop\TESTAR.bat"
echo echo Testando Dashboard KE5Z... >> "dist\Dashboard_KE5Z_Desktop\TESTAR.bat"
echo Dashboard_KE5Z_Desktop.exe >> "dist\Dashboard_KE5Z_Desktop\TESTAR.bat"
echo pause >> "dist\Dashboard_KE5Z_Desktop\TESTAR.bat"

echo ✅ Script de teste criado

echo.
echo ===============================================
echo    BUILD CONCLUÍDO COM SUCESSO!
echo ===============================================
echo.
echo 📁 Pasta do executável: dist\Dashboard_KE5Z_Desktop\
echo 🚀 Para testar: Execute TESTAR.bat na pasta dist
echo 📋 Para distribuir: Copie toda a pasta dist\Dashboard_KE5Z_Desktop\
echo.
echo 💡 DICAS:
echo - Se o executável não abrir, execute como administrador
echo - Verifique se o Windows Defender não está bloqueando
echo - Para distribuir, copie toda a pasta, não apenas o .exe
echo.
pause



