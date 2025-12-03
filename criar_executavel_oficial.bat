@echo off
chcp 65001 >nul
echo ===============================================
echo    CRIANDO EXECUTÁVEL - Dashboard KE5Z
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
echo.
streamlit-desktop-app build app.py --name Dashboard_KE5Z_OFICIAL
echo.

REM Verificar se o build foi bem-sucedido
if not exist "dist\Dashboard_KE5Z_OFICIAL\Dashboard_KE5Z_OFICIAL.exe" (
    echo ❌ ERRO: Executável não foi criado!
    echo.
    echo 🔧 Verificando possíveis problemas...
    echo.
    pause
    exit /b 1
)

echo ✅ Executável criado com sucesso!
echo.

REM Passo 3: Copiar dados para _internal
echo 📁 Copiando dados para _internal...
echo.

REM Copiar pastas de dados
REM CRÍTICO: Pasta KE5Z DEVE estar no _internal (dados processados)
if exist "KE5Z" (
    echo    Copiando KE5Z...
    xcopy "KE5Z" "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\" /E /I /Y >nul
    echo    ✅ KE5Z copiado para _internal
) else (
    echo    ⚠️  Pasta KE5Z não encontrada
    echo    ⚠️  AVISO: Pasta KE5Z é OBRIGATÓRIA dentro do _internal
)

if exist "Extracoes" (
    echo    Copiando Extracoes...
    xcopy "Extracoes" "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\" /E /I /Y >nul
    echo    ✅ Extracoes copiado
) else (
    echo    ⚠️  Pasta Extracoes não encontrada
)

REM CRÍTICO: Pasta arquivos deve estar no _internal (mesmo que vazia)
if exist "arquivos" (
    echo    Copiando arquivos...
    xcopy "arquivos" "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\" /E /I /Y >nul
    echo    ✅ arquivos copiado para _internal
) else (
    echo    ⚠️  Pasta arquivos não encontrada - criando vazia no _internal
    if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos"
    echo    ✅ Pasta arquivos criada no _internal (será preenchida pela extração)
)

if exist "pages" (
    echo    Copiando pages...
    xcopy "pages" "dist\Dashboard_KE5Z_OFICIAL\_internal\pages\" /E /I /Y >nul
    echo    ✅ pages copiado
) else (
    echo    ⚠️  Pasta pages não encontrada
)

REM Copiar arquivos de configuração para _internal
if exist "dados_equipe.json" (
    copy "dados_equipe.json" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
    echo    ✅ dados_equipe.json copiado
)

if exist "Dados SAPIENS.xlsx" (
    copy "Dados SAPIENS.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
    echo    ✅ Dados SAPIENS.xlsx copiado
)

if exist "Fornecedores.xlsx" (
    copy "Fornecedores.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
    echo    ✅ Fornecedores.xlsx copiado
)

REM Copiar arquivos Python principais para _internal
if exist "auth_simple.py" (
    copy "auth_simple.py" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
    echo    ✅ auth_simple.py copiado
)

if exist "Extracao.py" (
    copy "Extracao.py" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
    echo    ✅ Extracao.py copiado
)

echo.
echo ✅ Dados copiados para _internal
echo.

REM Passo 4: Copiar arquivos EDITÁVEIS para fora do _internal
echo 📝 Copiando arquivos editáveis...
if exist "usuarios.json" (
    copy "usuarios.json" "dist\Dashboard_KE5Z_OFICIAL\" >nul
    echo    ✅ usuarios.json copiado
) else (
    echo    ⚠️  usuarios.json não encontrado
)

if exist "usuarios_padrao.json" (
    copy "usuarios_padrao.json" "dist\Dashboard_KE5Z_OFICIAL\" >nul
    echo    ✅ usuarios_padrao.json copiado
) else (
    echo    ⚠️  usuarios_padrao.json não encontrado
)

echo.
echo ✅ Arquivos editáveis copiados
echo.

REM Passo 5: Verificação final
echo 🔍 Verificando estrutura final...
echo.

if exist "dist\Dashboard_KE5Z_OFICIAL\Dashboard_KE5Z_OFICIAL.exe" (
    echo ✅ Executável: OK
    for %%A in ("dist\Dashboard_KE5Z_OFICIAL\Dashboard_KE5Z_OFICIAL.exe") do echo    Tamanho: %%~zA bytes
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

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\auth_simple.py" (
    echo ✅ auth_simple.py: OK
) else (
    echo ❌ auth_simple.py: FALTANDO
)

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracao.py" (
    echo ✅ Extracao.py: OK
) else (
    echo ❌ Extracao.py: FALTANDO
)

echo.
echo ===============================================
echo    BUILD CONCLUÍDO!
echo ===============================================
echo.
echo 📁 Localização: dist\Dashboard_KE5Z_OFICIAL\
echo 🚀 Para testar: Execute o arquivo Dashboard_KE5Z_OFICIAL.exe
echo.
echo 💡 Dica: O executável abrirá automaticamente no navegador
echo.
pause

