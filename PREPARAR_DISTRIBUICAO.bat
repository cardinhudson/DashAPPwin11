@echo off
chcp 65001 >nul
echo ===============================================
echo   PREPARAR DASHBOARD PARA DISTRIBUIÇÃO
echo ===============================================
echo.

echo 🔍 Verificando executável...
if not exist "dist\Dashboard_KE5Z_OFICIAL\Dashboard_KE5Z_OFICIAL.exe" (
    echo ❌ Executável não encontrado!
    echo Execute primeiro: streamlit-desktop-app build
    pause
    exit /b 1
)
echo ✅ Executável encontrado

echo.
echo 🧹 Removendo arquivo pyvenv.cfg (caminhos absolutos)...
if exist "dist\Dashboard_KE5Z_OFICIAL\pyvenv.cfg" (
    del /q "dist\Dashboard_KE5Z_OFICIAL\pyvenv.cfg"
    echo ✅ pyvenv.cfg removido
) else (
    echo ℹ️  pyvenv.cfg já foi removido
)

echo.
echo 📋 Verificando estrutura de arquivos...

set "MISSING_FILES=0"

if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\app.py" (
    echo ❌ Faltando: _internal\app.py
    set "MISSING_FILES=1"
)

if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\auth_simple.py" (
    echo ❌ Faltando: _internal\auth_simple.py
    set "MISSING_FILES=1"
)

if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\dados_equipe.json" (
    echo ❌ Faltando: _internal\dados_equipe.json
    set "MISSING_FILES=1"
)

if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z" (
    echo ❌ Faltando: _internal\KE5Z\
    set "MISSING_FILES=1"
)

if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\pages" (
    echo ❌ Faltando: _internal\pages\
    set "MISSING_FILES=1"
)

if not exist "dist\Dashboard_KE5Z_OFICIAL\usuarios.json" (
    if not exist "dist\Dashboard_KE5Z_OFICIAL\usuarios_padrao.json" (
        echo ❌ Faltando: usuarios.json ou usuarios_padrao.json
        set "MISSING_FILES=1"
    )
)

if "%MISSING_FILES%"=="1" (
    echo.
    echo ❌ Arquivos faltando! Execute o build completo primeiro.
    pause
    exit /b 1
)

echo ✅ Todos os arquivos necessários presentes

echo.
echo 🧪 Testando executável na pasta atual...
cd dist\Dashboard_KE5Z_OFICIAL
start "" Dashboard_KE5Z_OFICIAL.exe
cd ..\..

echo.
echo ⏳ Aguardando 8 segundos para verificar...
timeout /t 8 /nobreak >nul

tasklist | findstr /i "Dashboard_KE5Z_OFICIAL" >nul
if %errorlevel% equ 0 (
    echo ✅ Executável funcionando!
    
    echo.
    echo 🛑 Encerrando teste...
    taskkill /f /im Dashboard_KE5Z_OFICIAL.exe >nul 2>&1
    
    echo.
    echo 📦 Testando portabilidade (cópia para outra pasta)...
    
    if exist "C:\Temp\TesteDashboard_Portabilidade" (
        rmdir /s /q "C:\Temp\TesteDashboard_Portabilidade"
    )
    
    xcopy /E /I /Q dist\Dashboard_KE5Z_OFICIAL C:\Temp\TesteDashboard_Portabilidade >nul
    
    echo ✅ Pasta copiada para C:\Temp\TesteDashboard_Portabilidade
    
    echo.
    echo 🚀 Testando na nova pasta...
    cd /d C:\Temp\TesteDashboard_Portabilidade
    start "" Dashboard_KE5Z_OFICIAL.exe
    
    echo ⏳ Aguardando 8 segundos...
    timeout /t 8 /nobreak >nul
    
    tasklist | findstr /i "Dashboard_KE5Z_OFICIAL" >nul
    if %errorlevel% equ 0 (
        echo.
        echo ✅✅✅ SUCESSO! Executável PORTÁVEL! ✅✅✅
        echo.
        echo 📋 O executável funciona em qualquer pasta/PC!
        echo.
        
        taskkill /f /im Dashboard_KE5Z_OFICIAL.exe >nul 2>&1
    ) else (
        echo ❌ Executável não funcionou na pasta de teste
        cd /d %~dp0
        pause
        exit /b 1
    )
    
    cd /d %~dp0
) else (
    echo ❌ Executável não iniciou corretamente
    pause
    exit /b 1
)

echo.
echo ===============================================
echo   ✅ DASHBOARD PRONTO PARA DISTRIBUIÇÃO!
echo ===============================================
echo.
echo 📦 Pasta pronta: dist\Dashboard_KE5Z_OFICIAL\
echo.
echo 📋 Próximos passos:
echo.
echo 1️⃣  Compactar a pasta:
echo    Compress-Archive -Path dist\Dashboard_KE5Z_OFICIAL -DestinationPath Dashboard_KE5Z.zip
echo.
echo 2️⃣  Ou copiar diretamente:
echo    xcopy /E /I dist\Dashboard_KE5Z_OFICIAL "D:\Destino\Dashboard_KE5Z_OFICIAL"
echo.
echo 3️⃣  No PC destino: executar Dashboard_KE5Z_OFICIAL.exe
echo.
echo 🔑 Login padrão:
echo    Usuário: admin
echo    Senha: admin123
echo.
echo 📖 Documentação completa: INSTRUCOES_DISTRIBUICAO_FINAL.md
echo.
pause





