@echo off
chcp 65001 >nul
echo ===============================================
echo    CRIANDO EXECUTAVEL - Dashboard KE5Z
echo ===============================================
echo.

REM Passo 1: Limpar builds anteriores
echo Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo Limpeza concluida
echo.

REM Passo 2: Criar executavel com streamlit-desktop-app
echo Criando executavel...
streamlit-desktop-app build app.py --name Dashboard_KE5Z_OFICIAL
echo.

REM Verificar se o build foi bem-sucedido
if not exist "dist\Dashboard_KE5Z_OFICIAL\Dashboard_KE5Z_OFICIAL.exe" (
    echo ERRO: Executavel nao foi criado!
    pause
    exit /b 1
)

echo Executavel criado com sucesso!
echo.

REM Passo 3: Copiar dados para _internal
echo Copiando dados para _internal...

REM Copiar pastas de dados
REM CRITICO: Pasta KE5Z DEVE estar no _internal (dados processados)
if exist "KE5Z" (
    xcopy "KE5Z" "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\" /E /I /Y >nul
) else (
    REM Criar pasta vazia se nao existir (sera preenchida pela extracao)
    if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z"
)

if exist "Extracoes" (
    xcopy "Extracoes" "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\" /E /I /Y >nul
)

REM CRITICO: Pasta arquivos deve estar no _internal (mesmo que vazia)
if exist "arquivos" (
    xcopy "arquivos" "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\" /E /I /Y >nul
) else (
    REM Criar pasta vazia se nao existir (sera preenchida pela extracao)
    if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos"
)

if exist "pages" (
    xcopy "pages" "dist\Dashboard_KE5Z_OFICIAL\_internal\pages\" /E /I /Y >nul
)

REM Copiar arquivos de configura????o para _internal
copy "dados_equipe.json" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
copy "Dados SAPIENS.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
copy "Fornecedores.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul

REM Copiar arquivos Python principais para _internal
copy "auth_simple.py" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
copy "Extracao.py" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul

REM Copiar documentacao (opcional - para referencia)
if exist "GUIA_EXTRACAO.md" (
    copy "GUIA_EXTRACAO.md" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
)

echo Dados copiados para _internal
echo.

REM Passo 4: Copiar arquivos EDITAVEIS para fora do _internal
echo Copiando arquivos editaveis...
copy "usuarios.json" "dist\Dashboard_KE5Z_OFICIAL\" >nul
copy "usuarios_padrao.json" "dist\Dashboard_KE5Z_OFICIAL\" >nul

echo Arquivos editaveis copiados
echo.

REM Passo 5: Remover pyvenv.cfg se existir (CRITICO para portabilidade)
if exist "dist\Dashboard_KE5Z_OFICIAL\pyvenv.cfg" (
    del /q "dist\Dashboard_KE5Z_OFICIAL\pyvenv.cfg"
)

REM Passo 6: Verifica????o final
echo Verificando estrutura final...
if exist "dist\Dashboard_KE5Z_OFICIAL\Dashboard_KE5Z_OFICIAL.exe" (
    echo Executavel: OK
) else (
    echo Executavel: FALTANDO
)

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z" (
    echo Pasta KE5Z: OK
) else (
    echo Pasta KE5Z: FALTANDO
)

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\pages" (
    echo Pasta pages: OK
) else (
    echo Pasta pages: FALTANDO
)

if exist "dist\Dashboard_KE5Z_OFICIAL\usuarios.json" (
    echo usuarios.json: OK
) else (
    echo usuarios.json: FALTANDO
)

echo.
echo ===============================================
echo    BUILD CONCLUIDO!
echo ===============================================
echo.
echo Localizacao: dist\Dashboard_KE5Z_OFICIAL\
echo Para testar: Execute o arquivo .exe
echo.
pause
