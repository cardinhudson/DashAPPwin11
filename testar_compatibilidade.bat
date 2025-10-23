@echo off
chcp 65001 >nul
echo ===============================================
echo    TESTE DE COMPATIBILIDADE - Dashboard KE5Z
echo ===============================================
echo.

echo 🔍 Verificando compatibilidade do sistema...
echo.

REM Verificar versão do Windows
echo 📊 Informações do Sistema:
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
echo Windows: %VERSION%

REM Verificar arquitetura
echo Arquitetura: %PROCESSOR_ARCHITECTURE%

REM Verificar Python
echo.
echo 🐍 Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo Instale Python 3.8+ e tente novamente.
    pause
    exit /b 1
)

python --version
echo ✅ Python OK

REM Verificar dependências críticas
echo.
echo 📦 Verificando dependências críticas...

pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Streamlit não encontrado
    set STREAMLIT_OK=0
) else (
    echo ✅ Streamlit OK
    set STREAMLIT_OK=1
)

pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PyInstaller não encontrado
    set PYINSTALLER_OK=0
) else (
    echo ✅ PyInstaller OK
    set PYINSTALLER_OK=1
)

pip show pandas >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Pandas não encontrado
    set PANDAS_OK=0
) else (
    echo ✅ Pandas OK
    set PANDAS_OK=1
)

REM Verificar arquivos do projeto
echo.
echo 📁 Verificando arquivos do projeto...

if not exist "app.py" (
    echo ❌ app.py não encontrado
    set APP_OK=0
) else (
    echo ✅ app.py OK
    set APP_OK=1
)

if not exist "auth_simple.py" (
    echo ❌ auth_simple.py não encontrado
    set AUTH_OK=0
) else (
    echo ✅ auth_simple.py OK
    set AUTH_OK=1
)

if not exist "Dashboard_KE5Z_Desktop_ATUALIZADO.spec" (
    echo ❌ Arquivo .spec atualizado não encontrado
    set SPEC_OK=0
) else (
    echo ✅ Arquivo .spec atualizado OK
    set SPEC_OK=1
)

REM Verificar pastas de dados
if not exist "KE5Z" (
    echo ❌ Pasta KE5Z não encontrada
    set KE5Z_OK=0
) else (
    echo ✅ Pasta KE5Z OK
    set KE5Z_OK=1
)

if not exist "pages" (
    echo ❌ Pasta pages não encontrada
    set PAGES_OK=0
) else (
    echo ✅ Pasta pages OK
    set PAGES_OK=1
)

REM Testar aplicação Streamlit
echo.
echo 🧪 Testando aplicação Streamlit...
echo Iniciando teste (pressione Ctrl+C para parar)...

timeout /t 3 /nobreak >nul

python -c "import streamlit; print('Streamlit importado com sucesso')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Erro ao importar Streamlit
    set STREAMLIT_TEST_OK=0
) else (
    echo ✅ Streamlit importado com sucesso
    set STREAMLIT_TEST_OK=1
)

python -c "import pandas; print('Pandas importado com sucesso')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Erro ao importar Pandas
    set PANDAS_TEST_OK=0
) else (
    echo ✅ Pandas importado com sucesso
    set PANDAS_TEST_OK=1
)

REM Resumo dos testes
echo.
echo ===============================================
echo    RESUMO DOS TESTES
echo ===============================================

if %STREAMLIT_OK%==1 if %PYINSTALLER_OK%==1 if %PANDAS_OK%==1 if %APP_OK%==1 if %AUTH_OK%==1 if %SPEC_OK%==1 if %KE5Z_OK%==1 if %PAGES_OK%==1 if %STREAMLIT_TEST_OK%==1 if %PANDAS_TEST_OK%==1 (
    echo ✅ TODOS OS TESTES PASSARAM!
    echo.
    echo 🚀 Sistema pronto para build!
    echo Execute: build_compativel.bat
    echo.
    set COMPATIBILIDADE=OK
) else (
    echo ❌ ALGUNS TESTES FALHARAM!
    echo.
    echo 🔧 Soluções necessárias:
    if %STREAMLIT_OK%==0 echo - Instalar Streamlit: pip install streamlit
    if %PYINSTALLER_OK%==0 echo - Instalar PyInstaller: pip install pyinstaller
    if %PANDAS_OK%==0 echo - Instalar Pandas: pip install pandas
    if %APP_OK%==0 echo - Verificar se app.py está presente
    if %AUTH_OK%==0 echo - Verificar se auth_simple.py está presente
    if %SPEC_OK%==0 echo - Usar arquivo .spec atualizado
    if %KE5Z_OK%==0 echo - Verificar pasta KE5Z com dados
    if %PAGES_OK%==0 echo - Verificar pasta pages
    if %STREAMLIT_TEST_OK%==0 echo - Reinstalar Streamlit: pip uninstall streamlit && pip install streamlit
    if %PANDAS_TEST_OK%==0 echo - Reinstalar Pandas: pip uninstall pandas && pip install pandas
    echo.
    set COMPATIBILIDADE=ERRO
)

echo.
echo ===============================================
echo    INFORMAÇÕES ADICIONAIS
echo ===============================================

echo 📊 Versões instaladas:
python --version
pip show streamlit | findstr Version
pip show pyinstaller | findstr Version
pip show pandas | findstr Version

echo.
echo 💡 Dicas para melhorar compatibilidade:
echo 1. Execute como administrador
echo 2. Configure exceções no antivírus
echo 3. Feche outros programas Python/Streamlit
echo 4. Use o arquivo .spec atualizado
echo 5. Execute o script build_compativel.bat

if %COMPATIBILIDADE%==OK (
    echo.
    echo 🎉 SISTEMA COMPATÍVEL!
    echo Pronto para executar o build.
) else (
    echo.
    echo ⚠️  SISTEMA PRECISA DE AJUSTES
    echo Corrija os problemas listados acima.
)

echo.
pause



