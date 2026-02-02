@echo off
chcp 65001 >nul
echo ===============================================
echo    CRIANDO EXECUTAVEL - Dashboard KE5Z v2.0
echo    Estrutura com Anos: 2025 e 2026
echo ===============================================
echo.

REM Passo 1: Verificar formularios
echo [1/6] Verificando formularios Streamlit...
python verificar_forms.py
if errorlevel 1 (
    echo.
    echo [ERRO] Formularios sem submit button encontrados!
    pause
    exit /b 1
)
echo [OK] Todos os formularios verificados
echo.

REM Passo 2: Limpar builds anteriores
echo [2/6] Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo [OK] Limpeza concluida
echo.

REM Passo 3: Criar executavel
echo [3/6] Criando executavel...
echo.
echo Escolha o metodo de build:
echo 1. streamlit-desktop-app (recomendado)
echo 2. PyInstaller direto com .spec
echo.
set /p METODO="Digite 1 ou 2 [1]: "
if "%METODO%"=="" set METODO=1

if "%METODO%"=="2" (
    echo.
    echo Usando PyInstaller com Dashboard_KE5Z_OFICIAL.spec...
    pyinstaller --clean --noconfirm Dashboard_KE5Z_OFICIAL.spec
) else (
    echo.
    echo Usando streamlit-desktop-app...
    streamlit-desktop-app build app.py --name Dashboard_KE5Z_OFICIAL
)

REM Verificar se o build foi bem-sucedido
if not exist "dist\Dashboard_KE5Z_OFICIAL\Dashboard_KE5Z_OFICIAL.exe" (
    echo.
    echo [ERRO] Executavel nao foi criado!
    echo Verifique os logs acima para erros
    pause
    exit /b 1
)

echo.
echo [OK] Executavel criado com sucesso!
echo.

REM Passo 4: Copiar dados para _internal
echo [4/6] Copiando dados para _internal...
echo.

REM CRIAR ESTRUTURA BASE (sempre criar, independente se pastas existem)
echo Criando estrutura de pastas...
mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\2025" 2>nul
mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\2026" 2>nul
mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\2025\KE5Z" 2>nul
mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\2025\KSBB" 2>nul
mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\2026\KE5Z" 2>nul
mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\2026\KSBB" 2>nul
mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\2025" 2>nul
mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\2026" 2>nul
echo [OK] Estrutura de pastas criada

REM Pasta KE5Z - copiar arquivos Parquet e Excel (NAO copiar .txt)
echo Copiando KE5Z (Parquet e Excel)...
if exist "KE5Z\2025\*.parquet" xcopy "KE5Z\2025\*.parquet" "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\2025\" /I /Y >nul 2>&1
if exist "KE5Z\2025\*.xlsx" xcopy "KE5Z\2025\*.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\2025\" /I /Y >nul 2>&1
if exist "KE5Z\2026\*.parquet" xcopy "KE5Z\2026\*.parquet" "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\2026\" /I /Y >nul 2>&1
if exist "KE5Z\2026\*.xlsx" xcopy "KE5Z\2026\*.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\2026\" /I /Y >nul 2>&1
echo [OK] KE5Z copiada (sem arquivos .txt)

REM Pasta Extracoes - NAO copiar .txt (sao muito grandes, usuario coloca depois)
echo Extracoes: estrutura criada (arquivos .txt devem ser adicionados pelo usuario)
echo [OK] Extracoes pronta (usuario deve colocar arquivos .txt)

REM Pasta arquivos - copiar apenas Excel (ja tem estrutura criada acima)
echo Copiando arquivos Excel...
if exist "arquivos\2025\*.xlsx" xcopy "arquivos\2025\*.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\2025\" /I /Y >nul 2>&1
if exist "arquivos\2026\*.xlsx" xcopy "arquivos\2026\*.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\2026\" /I /Y >nul 2>&1
echo [OK] arquivos Excel copiados

REM Pasta pages
echo Copiando pages...
if exist "pages" (
    xcopy "pages" "dist\Dashboard_KE5Z_OFICIAL\_internal\pages\" /E /I /Y >nul
    echo [OK] pages copiada
) else (
    echo [AVISO] Pasta pages nao encontrada!
)

REM Arquivos de configuracao
echo Copiando arquivos de configuracao...
if exist "dados_equipe.json" copy "dados_equipe.json" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1
if exist "Dados SAPIENS.xlsx" copy "Dados SAPIENS.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1
if exist "Fornecedores.xlsx" copy "Fornecedores.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1
if exist "auth_simple.py" copy "auth_simple.py" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1
if exist "Extracao.py" copy "Extracao.py" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1
echo [OK] Configuracoes copiadas

REM Passo 5: Copiar arquivos editaveis
echo.
echo [5/6] Copiando arquivos editaveis...
if exist "usuarios.json" copy "usuarios.json" "dist\Dashboard_KE5Z_OFICIAL\" >nul 2>&1
if exist "usuarios_padrao.json" copy "usuarios_padrao.json" "dist\Dashboard_KE5Z_OFICIAL\" >nul 2>&1
echo [OK] Arquivos editaveis copiados
echo.

REM Remover pyvenv.cfg
if exist "dist\Dashboard_KE5Z_OFICIAL\pyvenv.cfg" (
    del /q "dist\Dashboard_KE5Z_OFICIAL\pyvenv.cfg"
    echo [OK] pyvenv.cfg removido
)

REM Passo 6: Verificacao final
echo.
echo [6/6] Verificacao final...
echo.

set ERRORS=0

if exist "dist\Dashboard_KE5Z_OFICIAL\Dashboard_KE5Z_OFICIAL.exe" (
    echo [OK] Executavel: OK
) else (
    echo [ERRO] Executavel: FALTANDO
    set /a ERRORS+=1
)

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal" (
    echo [OK] Pasta _internal: OK
) else (
    echo [ERRO] Pasta _internal: FALTANDO
    set /a ERRORS+=1
)

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\2025" (
    echo [OK] Pasta KE5Z\2025: OK
) else (
    echo [AVISO] Pasta KE5Z\2025: FALTANDO
)

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\2026" (
    echo [OK] Pasta KE5Z\2026: OK
) else (
    echo [AVISO] Pasta KE5Z\2026: FALTANDO
)

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\pages" (
    echo [OK] Pasta pages: OK
) else (
    echo [ERRO] Pasta pages: FALTANDO
    set /a ERRORS+=1
)

echo.
echo ================================================
if %ERRORS% GTR 0 (
    echo [AVISO] BUILD CONCLUIDO COM %ERRORS% ERRO(S)
) else (
    echo [OK] BUILD CONCLUIDO COM SUCESSO!
)
echo ================================================
echo.
echo Localizacao: dist\Dashboard_KE5Z_OFICIAL\
echo Para testar: Execute Dashboard_KE5Z_OFICIAL.exe
echo.
echo ESTRUTURA POR ANO:
echo   - KE5Z/2025/ e KE5Z/2026/
echo   - Extracoes/2025/ e Extracoes/2026/
echo   - arquivos/2025/ e arquivos/2026/
echo.
echo NOTA: A extracao cria automaticamente as pastas do ano selecionado
echo.
pause
