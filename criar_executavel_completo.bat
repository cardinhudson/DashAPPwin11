@echo off
chcp 65001 >nul
echo ===============================================
echo    CRIANDO EXECUTÁVEL - Dashboard KE5Z
echo    Versão com Extracao.py Atualizado
echo ===============================================
echo.

REM Passo 1: Limpar builds anteriores
echo 🧹 Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo ✅ Limpeza concluída
echo.

REM Passo 2: Criar executável com streamlit-desktop-app
echo 🔨 Criando executável...
streamlit-desktop-app build app.py --name Dashboard_KE5Z_OFICIAL
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
if exist "KE5Z" (
    xcopy "KE5Z" "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\" /E /I /Y >nul
    echo ✅ Pasta KE5Z copiada
)
if exist "Extracoes" (
    xcopy "Extracoes" "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\" /E /I /Y >nul
    echo ✅ Pasta Extracoes copiada
)
if exist "arquivos" (
    xcopy "arquivos" "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\" /E /I /Y >nul
    echo ✅ Pasta arquivos copiada
)
if exist "pages" (
    xcopy "pages" "dist\Dashboard_KE5Z_OFICIAL\_internal\pages\" /E /I /Y >nul
    echo ✅ Pasta pages copiada
)

REM Copiar arquivos de configuração para _internal
if exist "dados_equipe.json" (
    copy "dados_equipe.json" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
    echo ✅ dados_equipe.json copiado
)
if exist "Dados SAPIENS.xlsx" (
    copy "Dados SAPIENS.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
    echo ✅ Dados SAPIENS.xlsx copiado
)
if exist "Fornecedores.xlsx" (
    copy "Fornecedores.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
    echo ✅ Fornecedores.xlsx copiado
)

REM Copiar arquivos Python principais para _internal (INCLUINDO Extracao.py ATUALIZADO)
echo 📝 Copiando arquivos Python atualizados...
if exist "auth_simple.py" (
    copy "auth_simple.py" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
    echo ✅ auth_simple.py copiado
)
if exist "Extracao.py" (
    copy "Extracao.py" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
    echo ✅ Extracao.py ATUALIZADO copiado (com padronização de colunas)
)

echo ✅ Dados copiados para _internal
echo.

REM Passo 4: Copiar arquivos EDITÁVEIS para fora do _internal
echo 📝 Copiando arquivos editáveis...
if exist "usuarios.json" (
    copy "usuarios.json" "dist\Dashboard_KE5Z_OFICIAL\" >nul
    echo ✅ usuarios.json copiado
) else (
    if exist "usuarios_padrao.json" (
        copy "usuarios_padrao.json" "dist\Dashboard_KE5Z_OFICIAL\usuarios.json" >nul
        echo ✅ usuarios.json criado a partir de usuarios_padrao.json
    )
)
if exist "usuarios_padrao.json" (
    copy "usuarios_padrao.json" "dist\Dashboard_KE5Z_OFICIAL\" >nul
    echo ✅ usuarios_padrao.json copiado
)

echo ✅ Arquivos editáveis copiados
echo.

REM Passo 5: Remover pyvenv.cfg se existir (para portabilidade)
echo 🔧 Preparando para distribuição...
if exist "dist\Dashboard_KE5Z_OFICIAL\pyvenv.cfg" (
    del "dist\Dashboard_KE5Z_OFICIAL\pyvenv.cfg" >nul
    echo ✅ pyvenv.cfg removido (portabilidade garantida)
)

REM Passo 6: Criar LEIA-ME.txt se não existir
if not exist "dist\Dashboard_KE5Z_OFICIAL\LEIA-ME.txt" (
    echo Criando LEIA-ME.txt...
    (
        echo DASHBOARD KE5Z - GUIA RÁPIDO
        echo.
        echo Login padrão:
        echo   Usuário: admin
        echo   Senha: admin123
        echo.
        echo Para executar: Clique duas vezes em Dashboard_KE5Z_OFICIAL.exe
        echo.
        echo IMPORTANTE: Não modifique a pasta _internal
    ) > "dist\Dashboard_KE5Z_OFICIAL\LEIA-ME.txt"
    echo ✅ LEIA-ME.txt criado
)
echo.

REM Passo 7: Verificação final
echo 🔍 Verificando estrutura final...
echo.

set VERIFICACAO_OK=1

if exist "dist\Dashboard_KE5Z_OFICIAL\Dashboard_KE5Z_OFICIAL.exe" (
    echo ✅ Executável: OK
) else (
    echo ❌ Executável: FALTANDO
    set VERIFICACAO_OK=0
)

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z" (
    echo ✅ Pasta KE5Z: OK
) else (
    echo ⚠️  Pasta KE5Z: Não encontrada (será criada na primeira execução)
)

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\pages" (
    echo ✅ Pasta pages: OK
) else (
    echo ❌ Pasta pages: FALTANDO
    set VERIFICACAO_OK=0
)

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracao.py" (
    echo ✅ Extracao.py: OK (versão atualizada com padronização)
) else (
    echo ❌ Extracao.py: FALTANDO
    set VERIFICACAO_OK=0
)

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\auth_simple.py" (
    echo ✅ auth_simple.py: OK
) else (
    echo ❌ auth_simple.py: FALTANDO
    set VERIFICACAO_OK=0
)

if exist "dist\Dashboard_KE5Z_OFICIAL\usuarios.json" (
    echo ✅ usuarios.json: OK
) else (
    echo ⚠️  usuarios.json: Não encontrado (será criado na primeira execução)
)

echo.
echo ===============================================
if %VERIFICACAO_OK%==1 (
    echo    ✅ BUILD CONCLUÍDO COM SUCESSO!
) else (
    echo    ⚠️  BUILD CONCLUÍDO COM AVISOS
)
echo ===============================================
echo.
echo 📁 Localização: dist\Dashboard_KE5Z_OFICIAL\
echo 🚀 Para testar: Execute o arquivo Dashboard_KE5Z_OFICIAL.exe
echo.
echo 📋 NOVIDADES NESTA VERSÃO:
echo    • Extracao.py com padronização automática de colunas
echo    • Suporte a múltiplos arquivos (sem limite)
echo    • Processamento robusto de arquivos com estruturas diferentes
echo    • Tratamento de erros melhorado
echo.
pause


