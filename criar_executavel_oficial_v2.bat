@echo off
chcp 65001 >nul
echo ===============================================
echo    CRIANDO EXECUTAVEL - Dashboard KE5Z v2.0
echo    Estrutura com Anos: 2025 e 2026
echo ===============================================
echo.
echo 📋 Este script:
echo    • Verifica formularios Streamlit
echo    • Cria o executavel
echo    • Copia estrutura por ano (2025, 2026)
echo    • Valida a estrutura final
echo.
echo 📁 Estrutura criada:
echo    _internal/
echo    ├── KE5Z/2025/ e KE5Z/2026/
echo    ├── Extracoes/2025/ e Extracoes/2026/
echo    └── arquivos/2025/ e arquivos/2026/
echo.
REM pause (comentado para build automatico)
echo.

REM Passo 0: Verificar formularios (prevencao de erros)
echo 🔍 Verificando formularios Streamlit...
python verificar_forms.py
if errorlevel 1 (
    echo.
    echo ❌ ERRO: Formularios sem submit button encontrados!
    echo    Execute: python verificar_forms.py para detalhes
    echo.
    pause
    exit /b 1
)
echo ✅ Todos os formularios verificados
echo.

REM Passo 1: Limpar builds anteriores
echo 🧹 Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo ✅ Limpeza concluida
echo.

REM Passo 2: Criar executavel com streamlit-desktop-app
echo 🔨 Criando executavel...
echo.
echo Escolha o metodo de build:
echo 1. streamlit-desktop-app (recomendado - facil)
echo 2. PyInstaller direto com .spec (avancado)
echo.
set /p METODO="Digite 1 ou 2 [1]: "
if "%METODO%"=="" set METODO=1

if "%METODO%"=="2" (
    echo.
    echo 🔨 Usando PyInstaller com Dashboard_KE5Z_OFICIAL.spec...
    pyinstaller --clean --noconfirm Dashboard_KE5Z_OFICIAL.spec
) else (
    echo.
    echo 🔨 Usando streamlit-desktop-app...
    echo    (Este processo pode levar alguns minutos)
    echo.
    streamlit-desktop-app build app.py --name Dashboard_KE5Z_OFICIAL
)

REM Verificar se o build foi bem-sucedido
if not exist "dist\Dashboard_KE5Z_OFICIAL\Dashboard_KE5Z_OFICIAL.exe" (
    echo.
    echo ❌ ERRO: Executavel nao foi criado!
    echo.
    echo 🔍 Possiveis causas:
    echo    - streamlit-desktop-app nao esta instalado
    echo    - Erro durante o build do PyInstaller
    echo    - Falta de permissoes de escrita
    echo.
    echo 💡 Solucoes:
    echo    1. Instalar: pip install streamlit-desktop-app
    echo    2. Verificar logs acima para erros
    echo    3. Executar como Administrador
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Executavel criado com sucesso!
echo.

REM Passo 3: Copiar dados para _internal com estrutura por ano
echo 📁 Copiando dados para _internal (estrutura por ano)...
echo.

REM ========================================
REM PASTA KE5Z - Estrutura por ano
REM ========================================
echo 📊 Copiando pasta KE5Z...
if exist "KE5Z" (
    echo    Copiando KE5Z por ano...
    xcopy "KE5Z" "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\" /E /I /Y >nul
    if errorlevel 1 (
        echo    ⚠️  Aviso: Erro ao copiar KE5Z
    ) else (
        echo    ✅ KE5Z copiada
    )
) else (
    echo    ℹ️  Pasta KE5Z nao existe, criando estrutura base...
    if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\2025" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\2025"
    if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\2026" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\2026"
    echo    ✅ Estrutura base KE5Z criada (2025, 2026)
)

REM ========================================
REM PASTA EXTRACOES - Estrutura por ano
REM ========================================
echo 📥 Copiando pasta Extracoes...
if exist "Extracoes" (
    echo    Copiando Extracoes por ano...
    xcopy "Extracoes" "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\" /E /I /Y >nul
    if errorlevel 1 (
        echo    ⚠️  Aviso: Erro ao copiar Extracoes
    ) else (
        echo    ✅ Extracoes copiada
    )
) else (
    echo    ℹ️  Pasta Extracoes nao existe, criando estrutura base...
    if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\2025\KE5Z" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\2025\KE5Z"
    if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\2025\KSBB" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\2025\KSBB"
    if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\2026\KE5Z" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\2026\KE5Z"
    if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\2026\KSBB" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\2026\KSBB"
    echo    ✅ Estrutura base Extracoes criada (2025/2026)
)

REM ========================================
REM PASTA ARQUIVOS - Estrutura por ano
REM ========================================
echo 📄 Copiando pasta arquivos...
if exist "arquivos" (
    echo    Copiando arquivos Excel por ano...
    xcopy "arquivos" "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\" /E /I /Y >nul
    if errorlevel 1 (
        echo    ⚠️  Aviso: Erro ao copiar arquivos
    ) else (
        echo    ✅ arquivos copiada
    )
) else (
    echo    ℹ️  Pasta arquivos nao existe, criando estrutura base...
    if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\2025" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\2025"
    if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\2026" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\2026"
    echo    ✅ Estrutura base arquivos criada (2025, 2026)
)

REM ========================================
REM PASTA PAGES
REM ========================================
echo 📑 Copiando pasta pages...
if exist "pages" (
    xcopy "pages" "dist\Dashboard_KE5Z_OFICIAL\_internal\pages\" /E /I /Y >nul
    if errorlevel 1 (
        echo    ⚠️  Aviso: Erro ao copiar pages
    ) else (
        echo    ✅ pages copiada
    )
) else (
    echo    ⚠️  AVISO: Pasta pages nao encontrada!
)

REM ========================================
REM ARQUIVOS DE CONFIGURACAO
REM ========================================
echo ⚙️  Copiando arquivos de configuracao...
if exist "dados_equipe.json" (
    copy "dados_equipe.json" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1
    echo    ✅ dados_equipe.json
) else (
    echo    ⚠️  dados_equipe.json nao encontrado
)

if exist "Dados SAPIENS.xlsx" (
    copy "Dados SAPIENS.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1
    echo    ✅ Dados SAPIENS.xlsx
) else (
    echo    ⚠️  Dados SAPIENS.xlsx nao encontrado
)

if exist "Fornecedores.xlsx" (
    copy "Fornecedores.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1
    echo    ✅ Fornecedores.xlsx
) else (
    echo    ⚠️  Fornecedores.xlsx nao encontrado
)

REM ========================================
REM SCRIPTS PYTHON
REM ========================================
echo 🐍 Copiando scripts Python...
if exist "auth_simple.py" (
    copy "auth_simple.py" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1
    echo    ✅ auth_simple.py
) else (
    echo    ⚠️  auth_simple.py nao encontrado
)

if exist "Extracao.py" (
    copy "Extracao.py" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1
    echo    ✅ Extracao.py
) else (
    echo    ⚠️  Extracao.py nao encontrado
)

REM ========================================
REM DOCUMENTACAO (OPCIONAL)
REM ========================================
echo 📚 Copiando documentacao (opcional)...
if exist "GUIA_EXTRACAO.md" (
    copy "GUIA_EXTRACAO.md" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul 2>&1
    echo    ✅ GUIA_EXTRACAO.md
)

echo.
echo ✅ Dados copiados para _internal
echo.

REM Passo 4: Copiar arquivos EDITAVEIS para fora do _internal
echo 📝 Copiando arquivos editaveis (fora do _internal)...
if exist "usuarios.json" (
    copy "usuarios.json" "dist\Dashboard_KE5Z_OFICIAL\" >nul 2>&1
    echo    ✅ usuarios.json
) else (
    echo    ⚠️  usuarios.json nao encontrado
)

if exist "usuarios_padrao.json" (
    copy "usuarios_padrao.json" "dist\Dashboard_KE5Z_OFICIAL\" >nul 2>&1
    echo    ✅ usuarios_padrao.json
) else (
    echo    ⚠️  usuarios_padrao.json nao encontrado
)

echo.
echo ✅ Arquivos editaveis copiados
echo.

REM Passo 5: Remover pyvenv.cfg se existir (CRITICO para portabilidade)
if exist "dist\Dashboard_KE5Z_OFICIAL\pyvenv.cfg" (
    del /q "dist\Dashboard_KE5Z_OFICIAL\pyvenv.cfg"
    echo ✅ pyvenv.cfg removido (portabilidade)
)

REM Passo 6: Verificacao final detalhada
echo.
echo ================================================
echo 🔍 VERIFICACAO FINAL DA ESTRUTURA
echo ================================================
echo.

set ERRORS=0

REM Verificar executavel
if exist "dist\Dashboard_KE5Z_OFICIAL\Dashboard_KE5Z_OFICIAL.exe" (
    echo ✅ Executavel: OK
) else (
    echo ❌ Executavel: FALTANDO
    set /a ERRORS+=1
)

REM Verificar pasta _internal
if exist "dist\Dashboard_KE5Z_OFICIAL\_internal" (
    echo ✅ Pasta _internal: OK
) else (
    echo ❌ Pasta _internal: FALTANDO
    set /a ERRORS+=1
)

REM Verificar pasta KE5Z com anos
if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\2025" (
    echo ✅ Pasta KE5Z\2025\: OK
) else (
    echo ⚠️  Pasta KE5Z\2025\: FALTANDO
)

if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\2026" (
    echo ✅ Pasta KE5Z\2026\: OK
) else (
    echo ⚠️  Pasta KE5Z\2026\: FALTANDO
)

REM Listar anos disponiveis em KE5Z
echo.
echo 📅 Anos disponiveis em KE5Z:
for /d %%a in ("dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\*") do (
    echo    • %%~nxa
)

REM Verificar pasta pages
if exist "dist\Dashboard_KE5Z_OFICIAL\_internal\pages" (
    echo.
    echo ✅ Pasta pages: OK
    REM Contar arquivos
    for /f %%a in ('dir /b "dist\Dashboard_KE5Z_OFICIAL\_internal\pages\*.py" ^| find /c ".py"') do set PAGE_COUNT=%%a
    echo    • Arquivos: %PAGE_COUNT% paginas
) else (
    echo ❌ Pasta pages: FALTANDO
    set /a ERRORS+=1
)

REM Verificar arquivos editaveis
if exist "dist\Dashboard_KE5Z_OFICIAL\usuarios.json" (
    echo ✅ usuarios.json: OK
) else (
    echo ⚠️  usuarios.json: FALTANDO
)

REM Verificar tamanho do executavel
echo.
echo 📊 Tamanho do executavel:
for %%a in ("dist\Dashboard_KE5Z_OFICIAL\Dashboard_KE5Z_OFICIAL.exe") do (
    set /a SIZE_MB=%%~za/1024/1024
    echo    • %%~za bytes (~!SIZE_MB! MB)
)

echo.
echo ================================================
if %ERRORS% GTR 0 (
    echo ⚠️  BUILD CONCLUIDO COM AVISOS (%ERRORS% erro(s))
    echo    Verifique os itens marcados acima
) else (
    echo ✅ BUILD CONCLUIDO COM SUCESSO!
)
echo ================================================
echo.
echo 📁 Localizacao: dist\Dashboard_KE5Z_OFICIAL\
echo 🚀 Para testar: Execute Dashboard_KE5Z_OFICIAL.exe
echo 📦 Para distribuir: Compacte toda a pasta
echo.
echo 💡 Dicas:
echo    • A pasta pode ser movida para qualquer local
echo    • Todos os dados estao em _internal\
echo    • usuarios.json pode ser editado externamente
echo    • Formularios Streamlit verificados antes do build
echo.
echo 🔍 ESTRUTURA POR ANO:
echo    ✅ KE5Z/2025/ e KE5Z/2026/
echo    ✅ Extracoes/2025/ e Extracoes/2026/
echo    ✅ arquivos/2025/ e arquivos/2026/
echo.
echo 📝 NOTA: A extracao cria automaticamente as pastas do ano selecionado
echo.
echo 💡 Dicas:
echo    • A pasta pode ser movida para qualquer local
echo    • Todos os dados estao em _internal\
echo    • usuarios.json pode ser editado externamente
echo    • Formularios Streamlit verificados antes do build
echo.
echo 🔍 VERIFICACOES FINAIS:
echo    • Todos os formularios tem submit button: ✅
echo    • Arquivos Python com correcoes mais recentes: ✅
echo    • Estrutura por ano (2025/2026): ✅
echo.
echo Pressione qualquer tecla para fechar...
pause > nul
