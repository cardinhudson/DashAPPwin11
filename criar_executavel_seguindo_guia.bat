@echo off
chcp 65001 >nul
echo ===============================================
echo    CRIANDO EXECUTAVEL - Dashboard KE5Z
echo    Seguindo Guia de Empacotamento
echo ===============================================
echo.

REM Passo 1: Limpar builds anteriores
echo 🧹 Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo ✅ Limpeza concluída
echo.

REM Passo 2: Criar executável com streamlit-desktop-app
echo 🔨 Criando executável com streamlit-desktop-app...
echo y | streamlit-desktop-app build app.py --name Dashboard_KE5Z_OFICIAL --noconfirm
echo.

REM Verificar se o build foi bem-sucedido
if not exist "dist\Dashboard_KE5Z_OFICIAL\Dashboard_KE5Z_OFICIAL.exe" (
    echo ❌ ERRO: Executável não foi criado!
    pause
    exit /b 1
)

echo ✅ Executável criado com sucesso!
echo.

REM Passo 3: Copiar dados para _internal
echo 📁 Copiando dados para _internal...

REM Copiar pastas de dados
xcopy "KE5Z" "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\" /E /I /Y >nul
xcopy "Extracoes" "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\" /E /I /Y >nul
xcopy "arquivos" "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\" /E /I /Y >nul
xcopy "pages" "dist\Dashboard_KE5Z_OFICIAL\_internal\pages\" /E /I /Y >nul

REM Copiar arquivos de configuração para _internal
copy "dados_equipe.json" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1
copy "Dados SAPIENS.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1
copy "Fornecedores.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1

REM Copiar arquivos Python principais para _internal
copy "auth_simple.py" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1
copy "Extracao.py" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1

echo ✅ Dados copiados para _internal
echo.

REM Passo 4: Copiar arquivos EDITÁVEIS para fora do _internal
echo 📝 Copiando arquivos editáveis...
copy "usuarios.json" "dist\Dashboard_KE5Z_OFICIAL\" >nul 2>&1
copy "usuarios_padrao.json" "dist\Dashboard_KE5Z_OFICIAL\" >nul 2>&1

echo ✅ Arquivos editáveis copiados
echo.

REM Passo 4.5: REMOVER pyvenv.cfg se existir (causa problemas de portabilidade)
echo 🧹 Removendo pyvenv.cfg (não necessário e causa problemas de portabilidade)...
if exist "dist\Dashboard_KE5Z_OFICIAL\pyvenv.cfg" (
    del "dist\Dashboard_KE5Z_OFICIAL\pyvenv.cfg" >nul 2>&1
    echo ✅ pyvenv.cfg removido
) else (
    echo ✅ pyvenv.cfg não existe (OK)
)
echo.

REM Passo 5: Verificação final
echo 🔍 Verificando estrutura final...
if exist "dist\Dashboard_KE5Z_OFICIAL\Dashboard_KE5Z_OFICIAL.exe" (
    echo ✅ Executável: OK
) else (
    echo ❌ Executável: FALTANDO
)

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z" (
    echo ✅ Pasta KE5Z: OK
) else (
    echo ❌ Pasta KE5Z: FALTANDO
)

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\pages" (
    echo ✅ Pasta pages: OK
) else (
    echo ❌ Pasta pages: FALTANDO
)

if exist "dist\Dashboard_KE5Z_OFICIAL\usuarios.json" (
    echo ✅ usuarios.json: OK
) else (
    echo ❌ usuarios.json: FALTANDO
)

echo.
echo ===============================================
echo    BUILD CONCLUIDO!
echo ===============================================
echo.
echo 📁 Localização: dist\Dashboard_KE5Z_OFICIAL\
echo 🚀 Para testar: Execute o arquivo .exe
echo.
pause

