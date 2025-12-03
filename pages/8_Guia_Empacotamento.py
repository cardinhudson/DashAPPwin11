import streamlit as st
import sys
import os
from datetime import datetime

# Adicionar diretório pai ao path para importar auth_simple
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth_simple import verificar_autenticacao, exibir_header_usuario

# Configuração da página
st.set_page_config(
    page_title="Guia de Empacotamento - Dashboard KE5Z",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar autenticação
verificar_autenticacao()

# Navegação simples
st.sidebar.markdown("📋 **NAVEGAÇÃO:** Use abas do navegador")
st.sidebar.markdown("🏠 Dashboard: Aplicação Desktop")
st.sidebar.markdown("---")

# Header
exibir_header_usuario()

# Título principal
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;">
    <h1 style="color: white; font-size: 3rem; margin: 0;">📦 Guia Definitivo de Empacotamento</h1>
    <h3 style="color: #f0f0f0; margin: 0;">Dashboard KE5Z Desktop - Versão 4.1</h3>
    <p style="color: #e0e0e0; font-size: 1.2rem; margin-top: 1rem;">
        Guia Completo e Unificado para Qualquer IA - Com Portabilidade
    </p>
</div>
""", unsafe_allow_html=True)

# Renderizar o conteúdo do guia em seções
st.markdown("# 🚀 GUIA DEFINITIVO DE EMPACOTAMENTO - DASHBOARD KE5Z")
st.markdown("## Versão 4.1 - Guia Completo e Unificado para Qualquer IA - Com Portabilidade")
st.markdown("---")

# Índice
st.markdown("## 📋 **ÍNDICE COMPLETO**")
st.markdown("""
1. [Visão Geral](#1-visão-geral)
2. [Pré-requisitos](#2-pré-requisitos)
3. [Estrutura do Projeto](#3-estrutura-do-projeto)
4. [Configuração de Caminhos](#4-configuração-de-caminhos)
5. [Processo de Empacotamento](#5-processo-de-empacotamento)
6. [Estrutura Final da Pasta dist](#6-estrutura-final-da-pasta-dist)
7. [Verificação e Testes](#7-verificação-e-testes)
8. [Solução de Problemas](#8-solução-de-problemas)
9. [Distribuição](#9-distribuição)
10. [Checklist Completo](#10-checklist-completo)
""")

st.markdown("---")

# Seção 1: Visão Geral
st.markdown("## 1. VISÃO GERAL")
st.markdown("### 🎯 **OBJETIVO DESTE GUIA**")
st.markdown("Este é o guia **DEFINITIVO** e **UNIFICADO** para empacotamento do Dashboard KE5Z. Foi criado para que **QUALQUER IA** possa seguir passo a passo e reproduzir exatamente o mesmo resultado.")

st.markdown("### ✅ **O QUE ESTE GUIA GARANTE**")
st.markdown("""
- ✅ Executável standalone funcionando 100%
- ✅ Compatibilidade total com Windows 10/11
- ✅ Todas as funcionalidades preservadas
- ✅ Estrutura de pastas correta (_internal)
- ✅ Sistema de autenticação funcional
- ✅ Processamento de dados operacional
- ✅ Múltiplas páginas com navegação
- ✅ Distribuição simples (1 pasta)
""")

st.markdown("### 🔑 **PRINCÍPIOS FUNDAMENTAIS**")
st.markdown("#### **1. Estrutura _internal (CRÍTICO)**")
st.markdown("O PyInstaller cria uma estrutura específica:")
st.code("""
dist/
└── Dashboard_KE5Z_OFICIAL/
    ├── Dashboard_KE5Z_OFICIAL.exe          # Executável principal
    ├── usuarios.json                        # Arquivos editáveis (FORA do _internal)
    ├── usuarios_padrao.json                 # Arquivos editáveis (FORA do _internal)
    └── _internal/                           # Pasta com TODOS os arquivos bundled
        ├── app.py                           # Scripts Python
        ├── auth_simple.py
        ├── Extracao.py
        ├── pages/                           # Páginas Streamlit
        │   ├── 1_Dash_Mes.py
        │   ├── 2_IUD_Assistant.py
        │   └── ...
        ├── KE5Z/                            # Dados processados
        │   ├── KE5Z.parquet
        │   ├── KE5Z_waterfall.parquet
        │   └── ...
        ├── Extracoes/                       # Dados brutos
        │   ├── KE5Z/
        │   └── KSBB/
        ├── arquivos/                        # Arquivos gerados
        ├── dados_equipe.json                # Configurações (dentro do _internal)
        ├── Dados SAPIENS.xlsx               # Dados auxiliares
        ├── Fornecedores.xlsx
        └── [Todas as DLLs e dependências Python]
""", language="text")

st.markdown("#### **2. Regra de Ouro: Leitura vs Escrita (ATUALIZADA PARA PORTABILIDADE)**")
st.markdown("""
- **LEITURA**: Usar `get_base_path()` que busca em múltiplos locais:
  - Primeiro tenta `_internal/KE5Z/` (local padrão)
  - Se não encontrar, tenta `exe_dir/KE5Z/` (diretório do executável)
  - Se não encontrar, tenta `exe_dir/_internal/KE5Z/` (fallback)
- **ESCRITA**: Usar `os.path.dirname(os.path.abspath(sys.executable))` (aponta para pasta do .exe)
- **CRÍTICO**: Sempre usar `os.path.abspath()` para garantir portabilidade
""")

st.markdown("#### **3. Ferramenta Correta**")
st.markdown("""
- **USAR**: `streamlit-desktop-app` (gerencia _internal automaticamente)
- **NÃO USAR**: PyInstaller direto (requer configuração manual complexa)
""")

st.markdown("---")

# Seção 2: Pré-requisitos
st.markdown("## 2. PRÉ-REQUISITOS")
st.markdown("### 2.1 Sistema Operacional")
st.markdown("""
- **Windows 10/11** (64-bit) - TESTADO E FUNCIONANDO
- **Python 3.8+** (apenas para desenvolvimento)
- **PowerShell** ou **CMD** (para executar scripts)
""")

st.markdown("### 2.2 Dependências Python (Versões Testadas)")
st.code("""
# Instalar todas as dependências de uma vez
pip install streamlit==1.50.0 pandas==2.3.3 plotly==5.17.0 pyarrow==20.0.0 openpyxl==3.1.5 altair==5.5.0 numpy==2.3.3 xlsxwriter==3.2.9 streamlit-desktop-app==0.3.3
""", language="bash")

st.markdown("### 2.3 Verificar Instalação")
st.code("""
# Verificar Python
python --version

# Verificar dependências principais
pip show streamlit
pip show streamlit-desktop-app
pip show pandas
pip show pyarrow
""", language="bash")

st.markdown("---")

# Seção 3: Estrutura do Projeto
st.markdown("## 3. ESTRUTURA DO PROJETO")
st.markdown("### 3.1 Estrutura Antes do Empacotamento")
st.code("""
DashAPPwin11/                              # Pasta raiz do projeto
├── app.py                                 # ⭐ Aplicação principal Streamlit
├── auth_simple.py                         # ⭐ Sistema de autenticação
├── Extracao.py                            # ⭐ Script de processamento
├── requirements.txt                       # Lista de dependências
├── hook-streamlit.py                      # Hook para PyInstaller
├── pages/                                 # ⭐ Páginas do Streamlit
│   ├── 1_Dash_Mes.py
│   ├── 2_IUD_Assistant.py
│   ├── 3_Total_accounts.py
│   ├── 4_Waterfall_Analysis.py
│   ├── 5_Admin_Usuarios.py
│   ├── 6_Extracao_Dados.py
│   ├── 7_Sobre_Projeto.py
│   └── 8_Guia_Empacotamento.py
├── KE5Z/                                  # ⭐ Dados processados
│   ├── KE5Z.parquet
│   ├── KE5Z_main.parquet
│   ├── KE5Z_others.parquet
│   ├── KE5Z_waterfall.parquet
│   └── KE5Z.xlsx
├── Extracoes/                             # ⭐ Dados brutos
│   ├── KE5Z/
│   │   ├── KE5Z.parquet
│   │   └── KE5Z.xlsx
│   └── KSBB/
├── arquivos/                              # ⭐ Arquivos Excel gerados
│   ├── KE5Z_LC.xlsx
│   ├── KE5Z_pwt.xlsx
│   ├── KE5Z_TC_Ext.xlsx
│   └── KE5Z_veiculos.xlsx
├── usuarios.json                          # ⭐ Dados de usuários (EDITÁVEL)
├── usuarios_padrao.json                   # ⭐ Backup de usuários (EDITÁVEL)
├── dados_equipe.json                      # ⭐ Configurações da equipe
├── Dados SAPIENS.xlsx                     # ⭐ Dados auxiliares
├── Fornecedores.xlsx                      # ⭐ Dados auxiliares
└── criar_executavel_funcional.bat         # Script de build

⭐ = Arquivos/pastas que DEVEM ser incluídos no executável
""", language="text")

st.markdown("### 3.2 Arquivos Críticos")
st.markdown("#### **app.py** - Aplicação Principal (COM PORTABILIDADE)")
st.code('''
import streamlit as st
import pandas as pd
import sys
import os
from auth_simple import verificar_login

# CORREÇÃO CRÍTICA: Garantir diretório de trabalho correto para portabilidade
def ensure_working_directory():
    """Garante que o diretório de trabalho seja o diretório do executável"""
    if hasattr(sys, '_MEIPASS'):
        try:
            exe_path = os.path.abspath(sys.executable)
            exe_dir = os.path.dirname(exe_path)
            if os.path.exists(exe_dir):
                os.chdir(exe_dir)
        except Exception:
            pass
        # Limpar variáveis de ambiente que podem causar problemas
        for var in ['VIRTUAL_ENV', 'PYTHONHOME', 'CONDA_DEFAULT_ENV']:
            if var in os.environ:
                del os.environ[var]

# Executar imediatamente ao importar
ensure_working_directory()

# Função CRÍTICA para caminhos (COM PORTABILIDADE)
def get_base_path():
    """Retorna o caminho base correto para LEITURA de dados
    
    Estratégia de busca para portabilidade:
    1. No executável: primeiro tenta _internal (onde dados são copiados)
    2. Se não encontrar, tenta diretório do executável (para quando pasta é movida)
    3. Em desenvolvimento: usa diretório do script
    """
    if hasattr(sys, '_MEIPASS'):
        # 1. Primeiro tentar _internal (onde dados são copiados no build)
        try:
            meipass_path = os.path.abspath(sys._MEIPASS)
            if os.path.exists(meipass_path):
                ke5z_path = os.path.join(meipass_path, "KE5Z")
                if os.path.exists(ke5z_path):
                    return meipass_path
        except Exception:
            pass
        
        # 2. Fallback: tentar diretório do executável (para quando pasta é movida)
        try:
            exe_path = os.path.abspath(sys.executable)
            exe_dir = os.path.dirname(exe_path)
            if os.path.exists(exe_dir):
                ke5z_path_exe = os.path.join(exe_dir, "KE5Z")
                ke5z_path_internal = os.path.join(exe_dir, "_internal", "KE5Z")
                if os.path.exists(ke5z_path_exe):
                    return exe_dir
                elif os.path.exists(ke5z_path_internal):
                    return os.path.join(exe_dir, "_internal")
        except Exception:
            pass
        
        # 3. Último fallback: usar _MEIPASS mesmo que não exista
        try:
            return os.path.abspath(sys._MEIPASS)
        except Exception:
            return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Configuração da página
st.set_page_config(
    page_title="Dashboard KE5Z",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sistema de autenticação
if not verificar_login():
    st.stop()

# Carregar dados (COM BUSCA EM MÚLTIPLOS LOCAIS)
@st.cache_data
def load_data():
    try:
        base_path = get_base_path()
        
        # CORREÇÃO CRÍTICA: Tentar múltiplos locais para portabilidade
        locais_possiveis = []
        locais_possiveis.append(os.path.join(base_path, "KE5Z", "KE5Z.parquet"))
        
        # Se estiver no executável, tentar também diretório do executável
        if hasattr(sys, '_MEIPASS'):
            try:
                exe_path = os.path.abspath(sys.executable)
                exe_dir = os.path.dirname(exe_path)
                locais_possiveis.append(os.path.join(exe_dir, "KE5Z", "KE5Z.parquet"))
                locais_possiveis.append(os.path.join(exe_dir, "_internal", "KE5Z", "KE5Z.parquet"))
            except Exception:
                pass
        
        # Procurar arquivo nos locais possíveis
        arquivo_parquet = None
        for local in locais_possiveis:
            if os.path.exists(local):
                arquivo_parquet = local
                break
        
        if arquivo_parquet and os.path.exists(arquivo_parquet):
            df = pd.read_parquet(arquivo_parquet)
            return df
        else:
            st.error("❌ Arquivo de dados não encontrado em nenhum local!")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()
''', language="python")

st.markdown("#### **auth_simple.py** - Sistema de Autenticação")
st.code('''
import streamlit as st
import json
import os
import sys

def get_data_dir():
    """Retorna o diretório onde os arquivos EDITÁVEIS devem ser salvos"""
    if hasattr(sys, '_MEIPASS'):
        # No executável: salvar FORA do _internal (diretório do .exe)
        return os.path.dirname(sys.executable)
    else:
        # Em desenvolvimento: diretório atual
        return os.path.dirname(os.path.abspath(__file__))

# Configurações
DATA_DIR = get_data_dir()
USUARIOS_FILE = os.path.join(DATA_DIR, "usuarios.json")
USUARIOS_PADRAO_FILE = os.path.join(DATA_DIR, "usuarios_padrao.json")

def verificar_login():
    """Sistema de autenticação"""
    if 'logado' in st.session_state and st.session_state.logado:
        return True
    
    # Interface de login
    st.title("🔐 Login - Dashboard KE5Z")
    
    with st.form("login_form"):
        usuario = st.text_input("👤 Usuário")
        senha = st.text_input("🔒 Senha", type="password")
        
        if st.form_submit_button("🚀 Entrar"):
            # Lógica de autenticação
            pass
    
    return False
''', language="python")

st.markdown("#### **Extracao.py** - Processamento de Dados")
st.code('''
import pandas as pd
import os
import sys

# Pasta raiz para LEITURA (dentro do _internal)
ROOT_DIR = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(os.path.abspath(__file__))

# Pasta raiz para ESCRITA (fora do _internal)
if hasattr(sys, '_MEIPASS'):
    OUTPUT_DIR = os.path.dirname(sys.executable)
else:
    OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Pastas de entrada (dentro do _internal)
DIR_EXTRACOES = os.path.join(ROOT_DIR, "Extracoes")
DIR_KE5Z_IN = os.path.join(DIR_EXTRACOES, "KE5Z")

# Arquivos auxiliares (dentro do _internal)
ARQ_SAPIENS = os.path.join(ROOT_DIR, "Dados SAPIENS.xlsx")
ARQ_FORNECEDORES = os.path.join(ROOT_DIR, "Fornecedores.xlsx")

# Pastas de saída (fora do _internal)
DIR_KE5Z_OUT = os.path.join(OUTPUT_DIR, "KE5Z")
DIR_ARQUIVOS_OUT = os.path.join(OUTPUT_DIR, "arquivos")

def processar_dados():
    """Função principal de processamento"""
    # Lógica de processamento
    pass
''', language="python")

st.markdown("---")

# Seção 4: Configuração de Caminhos
st.markdown("## 4. CONFIGURAÇÃO DE CAMINHOS")
st.markdown("### 4.1 Padrão de Caminhos (CRÍTICO)")
st.markdown("#### **Função para LEITURA de Dados (COM PORTABILIDADE COMPLETA)**")
st.code('''
import sys
import os

def get_base_path():
    """Retorna o caminho base correto para LEITURA de dados
    
    Estratégia de busca para portabilidade:
    1. No executável: primeiro tenta _internal (onde dados são copiados)
    2. Se não encontrar, tenta diretório do executável (para quando pasta é movida)
    3. Em desenvolvimento: usa diretório do script
    """
    if hasattr(sys, '_MEIPASS'):
        # Rodando no executável PyInstaller
        # CORREÇÃO CRÍTICA: Tentar múltiplos locais para portabilidade
        
        # 1. Primeiro tentar _internal (onde dados são copiados no build)
        try:
            meipass_path = os.path.abspath(sys._MEIPASS)
            if os.path.exists(meipass_path):
                ke5z_path = os.path.join(meipass_path, "KE5Z")
                if os.path.exists(ke5z_path):
                    return meipass_path
        except Exception:
            pass
        
        # 2. Fallback: tentar diretório do executável (para quando pasta é movida)
        try:
            exe_path = os.path.abspath(sys.executable)
            exe_dir = os.path.dirname(exe_path)
            if os.path.exists(exe_dir):
                ke5z_path_exe = os.path.join(exe_dir, "KE5Z")
                ke5z_path_internal = os.path.join(exe_dir, "_internal", "KE5Z")
                if os.path.exists(ke5z_path_exe):
                    return exe_dir
                elif os.path.exists(ke5z_path_internal):
                    return os.path.join(exe_dir, "_internal")
        except Exception:
            pass
        
        # 3. Último fallback: usar _MEIPASS mesmo que não exista
        try:
            return os.path.abspath(sys._MEIPASS)
        except Exception:
            return sys._MEIPASS
    else:
        # Rodando em desenvolvimento
        return os.path.dirname(os.path.abspath(__file__))
''', language="python")

st.markdown("#### **Função para ESCRITA de Dados (CORRIGIDA PARA PORTABILIDADE)**")
st.code('''
def get_output_path():
    """Retorna o caminho correto para ESCRITA de dados"""
    if hasattr(sys, '_MEIPASS'):
        # No executável: salvar no diretório do executável (fora do _internal)
        # CORREÇÃO CRÍTICA: Usar os.path.abspath para garantir caminho absoluto
        # mesmo quando o executável é movido para outro local
        try:
            exe_path = os.path.abspath(sys.executable)
            exe_dir = os.path.dirname(exe_path)
            
            # Verificar se o diretório existe e é válido
            if os.path.exists(exe_dir) and os.path.isdir(exe_dir):
                return exe_dir
            else:
                # Se não existe, tentar criar ou usar diretório atual
                try:
                    os.makedirs(exe_dir, exist_ok=True)
                    return exe_dir
                except Exception:
                    # Fallback: usar diretório atual de trabalho
                    return os.path.abspath(os.getcwd())
        except Exception as e:
            # Fallback em caso de erro: usar diretório atual
            return os.path.abspath(os.getcwd())
    else:
        # Em desenvolvimento: mesmo diretório
        return os.path.dirname(os.path.abspath(__file__))
''', language="python")

st.markdown("#### **Função CRÍTICA: Garantir Diretório de Trabalho Correto**")
st.code('''
def ensure_working_directory():
    """Garante que o diretório de trabalho seja o diretório do executável"""
    if hasattr(sys, '_MEIPASS'):
        # No executável: mudar para o diretório do executável (não do _internal)
        # CORREÇÃO: Usar os.path.abspath() para garantir caminho absoluto correto
        # mesmo quando o executável é movido para outro local
        try:
            exe_path = os.path.abspath(sys.executable)
            exe_dir = os.path.dirname(exe_path)
            if os.path.exists(exe_dir):
                os.chdir(exe_dir)
        except Exception:
            # Fallback: usar diretório atual se houver problema
            pass
        # Limpar variáveis de ambiente que podem causar problemas
        for var in ['VIRTUAL_ENV', 'PYTHONHOME', 'CONDA_DEFAULT_ENV']:
            if var in os.environ:
                del os.environ[var]

# Executar imediatamente ao importar (no início do app.py)
ensure_working_directory()
''', language="python")

st.markdown("### 4.2 Aplicação em Todas as Páginas")
st.markdown("**REGRA**: Todas as páginas do Streamlit devem usar estas funções.")
st.markdown("**Exemplo em pages/1_Dash_Mes.py:**")
st.code('''
import sys
import os
import pandas as pd
import streamlit as st

def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data_optimized():
    base_path = get_base_path()
    arquivo_waterfall = os.path.join(base_path, "KE5Z", "KE5Z_waterfall.parquet")
    
    if os.path.exists(arquivo_waterfall):
        return pd.read_parquet(arquivo_waterfall)
    else:
        arquivo_principal = os.path.join(base_path, "KE5Z", "KE5Z.parquet")
        return pd.read_parquet(arquivo_principal)
''', language="python")

st.markdown("---")

# Seção 5: Processo de Empacotamento
st.markdown("## 5. PROCESSO DE EMPACOTAMENTO")
st.markdown("### 5.1 Método Recomendado: streamlit-desktop-app")
st.markdown("**POR QUE USAR streamlit-desktop-app?**")
st.markdown("""
- ✅ Gerencia automaticamente a estrutura `_internal/`
- ✅ Inclui todas as dependências do Streamlit
- ✅ Configuração simplificada
- ✅ Menos propenso a erros
""")

st.markdown("### 5.2 Script de Build (criar_executavel_funcional.bat)")
st.code('''
@echo off
chcp 65001 >nul
echo ===============================================
echo    CRIANDO EXECUTÁVEL - Dashboard KE5Z
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
if not exist "dist\\Dashboard_KE5Z_OFICIAL\\Dashboard_KE5Z_OFICIAL.exe" (
    echo ❌ ERRO: Executável não foi criado!
    pause
    exit /b 1
)

echo ✅ Executável criado com sucesso!
echo.

REM Passo 3: Copiar dados para _internal
echo 📁 Copiando dados para _internal...

REM Copiar pastas de dados
xcopy "KE5Z" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\KE5Z\\" /E /I /Y >nul
xcopy "Extracoes" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\Extracoes\\" /E /I /Y >nul
xcopy "arquivos" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\arquivos\\" /E /I /Y >nul
xcopy "pages" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\pages\\" /E /I /Y >nul

REM Copiar arquivos de configuração para _internal
copy "dados_equipe.json" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\" >nul
copy "Dados SAPIENS.xlsx" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\" >nul
copy "Fornecedores.xlsx" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\" >nul

REM Copiar arquivos Python principais para _internal
copy "auth_simple.py" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\" >nul
copy "Extracao.py" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\" >nul

echo ✅ Dados copiados para _internal
echo.

REM Passo 4: Copiar arquivos EDITÁVEIS para fora do _internal
echo 📝 Copiando arquivos editáveis...
copy "usuarios.json" "dist\\Dashboard_KE5Z_OFICIAL\\" >nul
copy "usuarios_padrao.json" "dist\\Dashboard_KE5Z_OFICIAL\\" >nul

echo ✅ Arquivos editáveis copiados
echo.

REM Passo 5: Verificação final
echo 🔍 Verificando estrutura final...
if exist "dist\\Dashboard_KE5Z_OFICIAL\\Dashboard_KE5Z_OFICIAL.exe" (
    echo ✅ Executável: OK
) else (
    echo ❌ Executável: FALTANDO
)

if exist "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\KE5Z" (
    echo ✅ Pasta KE5Z: OK
) else (
    echo ❌ Pasta KE5Z: FALTANDO
)

if exist "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\pages" (
    echo ✅ Pasta pages: OK
) else (
    echo ❌ Pasta pages: FALTANDO
)

if exist "dist\\Dashboard_KE5Z_OFICIAL\\usuarios.json" (
    echo ✅ usuarios.json: OK
) else (
    echo ❌ usuarios.json: FALTANDO
)

echo.
echo ===============================================
echo    BUILD CONCLUÍDO!
echo ===============================================
echo.
echo 📁 Localização: dist\\Dashboard_KE5Z_OFICIAL\\
echo 🚀 Para testar: Execute o arquivo .exe
echo.
pause
''', language="batch")

st.markdown("### 5.3 Comandos Passo a Passo")
st.code('''
# 1. Navegar para a pasta do projeto
cd C:\\user\\U235107\\GitHub\\DashAPPwin11

# 2. Verificar se streamlit-desktop-app está instalado
pip show streamlit-desktop-app

# 3. Limpar builds anteriores
rmdir /s /q build
rmdir /s /q dist

# 4. Executar o script de build
criar_executavel_funcional.bat
''', language="bash")

st.markdown("---")

# Seção 6: Estrutura Final
st.markdown("## 6. ESTRUTURA FINAL DA PASTA dist")
st.markdown("### 6.1 Estrutura Completa (CRÍTICO - SEGUIR EXATAMENTE)")
st.markdown("Esta é a estrutura **EXATA** que deve ser criada após o empacotamento:")

st.code("""
dist/
└── Dashboard_KE5Z_OFICIAL/                    # Pasta principal do executável
    │
    ├── Dashboard_KE5Z_OFICIAL.exe             # ⭐ Executável principal (31+ MB)
    ├── usuarios.json                          # ⭐ Arquivo EDITÁVEL (fora do _internal)
    ├── usuarios_padrao.json                   # ⭐ Arquivo EDITÁVEL (fora do _internal)
    ├── pyvenv.cfg                             # Configuração Python (gerado automaticamente)
    │
    └── _internal/                             # ⭐ PASTA CRÍTICA - Todos os arquivos bundled
        │
        ├── ─── ARQUIVOS PYTHON ───
        ├── app.py                             # Aplicação principal
        ├── auth_simple.py                     # Sistema de autenticação
        ├── Extracao.py                        # Script de processamento
        │
        ├── ─── PÁGINAS STREAMLIT ───
        ├── pages/
        │   ├── 1_Dash_Mes.py
        │   ├── 2_IUD_Assistant.py
        │   ├── 3_Total_accounts.py
        │   ├── 4_Waterfall_Analysis.py
        │   ├── 5_Admin_Usuarios.py
        │   ├── 6_Extracao_Dados.py
        │   ├── 7_Sobre_Projeto.py
        │   └── 8_Guia_Empacotamento.py
        │
        ├── ─── DADOS PROCESSADOS ───
        ├── KE5Z/
        │   ├── KE5Z.parquet                   # Arquivo principal (3+ milhões de registros)
        │   ├── KE5Z_main.parquet              # Dados main
        │   ├── KE5Z_others.parquet            # Dados others
        │   ├── KE5Z_waterfall.parquet         # Arquivo otimizado (68% menor)
        │   └── KE5Z.xlsx                      # Backup Excel
        │
        ├── ─── DADOS BRUTOS ───
        ├── Extracoes/
        │   ├── KE5Z/
        │   │   ├── KE5Z.parquet
        │   │   └── KE5Z.xlsx
        │   └── KSBB/
        │       └── (arquivos KSBB se existirem)
        │
        ├── ─── ARQUIVOS GERADOS ───
        ├── arquivos/
        │   ├── KE5Z_LC.xlsx
        │   ├── KE5Z_pwt.xlsx
        │   ├── KE5Z_TC_Ext.xlsx
        │   └── KE5Z_veiculos.xlsx
        │
        ├── ─── CONFIGURAÇÕES E DADOS AUXILIARES ───
        ├── dados_equipe.json                  # Configurações da equipe
        ├── Dados SAPIENS.xlsx                 # Dados auxiliares
        ├── Fornecedores.xlsx                  # Dados de fornecedores
        │
        ├── ─── DEPENDÊNCIAS PYTHON ───
        ├── base_library.zip                   # Biblioteca Python base
        ├── python313.dll                      # DLL Python
        ├── python3.dll
        ├── libcrypto-3.dll
        ├── libssl-3.dll
        ├── libffi-8.dll
        ├── sqlite3.dll
        ├── VCRUNTIME140.dll
        ├── VCRUNTIME140_1.dll
        │
        ├── ─── PACOTES PYTHON ───
        ├── streamlit/                         # Pacote Streamlit completo
        ├── pandas/                            # Pacote Pandas completo
        ├── plotly/                            # Pacote Plotly completo
        ├── pyarrow/                           # Pacote PyArrow completo
        ├── altair/                            # Pacote Altair completo
        ├── numpy/                             # Pacote NumPy completo
        ├── openpyxl/                          # Pacote OpenPyXL completo
        │
        ├── ─── METADADOS (CRÍTICO) ───
        ├── streamlit-1.50.0.dist-info/        # Metadados do Streamlit
        ├── pandas-2.3.3.dist-info/            # Metadados do Pandas
        ├── plotly-5.17.0.dist-info/           # Metadados do Plotly
        ├── pyarrow-20.0.0.dist-info/          # Metadados do PyArrow
        │
        └── [Outros arquivos .pyd, .dll, e dependências...]
""", language="text")

# Continuar com as outras seções...
st.markdown("### 6.2 Verificação da Estrutura")
st.markdown("**Comando para verificar a estrutura:**")
st.code('''
cd dist\\Dashboard_KE5Z_OFICIAL

# Verificar executável
dir *.exe

# Verificar arquivos editáveis (FORA do _internal)
dir *.json

# Verificar pasta _internal
dir _internal

# Verificar dados dentro do _internal
dir _internal\\KE5Z
dir _internal\\Extracoes
dir _internal\\arquivos
dir _internal\\pages

# Verificar arquivos auxiliares
dir _internal\\*.xlsx
dir _internal\\*.json
''', language="bash")

st.markdown("### 6.3 Tamanhos Esperados")
st.markdown("""
| Item | Tamanho Aproximado |
|------|-------------------|
| **Dashboard_KE5Z_OFICIAL.exe** | 31-35 MB |
| **_internal/** (pasta completa) | 400-500 MB |
| **KE5Z.parquet** | 50-100 MB |
| **KE5Z_waterfall.parquet** | 15-30 MB (68% menor) |
| **Dados SAPIENS.xlsx** | 1-5 MB |
| **Total da pasta dist/** | 450-550 MB |
""")

st.markdown("### 6.4 Arquivos Críticos que NÃO Podem Faltar")
st.markdown("#### **No diretório raiz (fora do _internal):**")
st.markdown("""
- ✅ `Dashboard_KE5Z_OFICIAL.exe`
- ✅ `usuarios.json`
- ✅ `usuarios_padrao.json`
""")

st.markdown("#### **Dentro do _internal:**")
st.markdown("""
- ✅ `app.py`
- ✅ `auth_simple.py`
- ✅ `Extracao.py`
- ✅ `pages/` (pasta com 8 arquivos .py)
- ✅ `KE5Z/` (pasta com arquivos .parquet)
- ✅ `Extracoes/` (pasta com dados brutos)
- ✅ `arquivos/` (pasta com arquivos Excel)
- ✅ `dados_equipe.json`
- ✅ `Dados SAPIENS.xlsx`
- ✅ `Fornecedores.xlsx`
- ✅ `streamlit/` (pacote completo)
- ✅ `pandas/` (pacote completo)
- ✅ `streamlit-1.50.0.dist-info/` (metadados)
""")

st.markdown("### 6.5 Regra de Ouro: O que vai onde?")
st.markdown("#### **FORA do _internal (editável pelo usuário):**")
st.code("""
✅ usuarios.json          → Usuário pode editar
✅ usuarios_padrao.json   → Usuário pode editar
""", language="text")

st.markdown("#### **DENTRO do _internal (read-only, bundled):**")
st.code("""
✅ Todos os scripts Python (.py)
✅ Todas as pastas de dados (KE5Z, Extracoes, arquivos, pages)
✅ Todos os arquivos de configuração (dados_equipe.json, *.xlsx)
✅ Todas as dependências Python
✅ Todas as DLLs
""", language="text")

st.markdown("---")

# Seção 7: Verificação e Testes
st.markdown("## 7. VERIFICAÇÃO E TESTES")
st.markdown("### 7.1 Checklist de Verificação Imediata")
st.markdown("Após o build, execute estas verificações:")

st.code('''
# 1. Verificar se o executável foi criado
cd dist\\Dashboard_KE5Z_OFICIAL
dir Dashboard_KE5Z_OFICIAL.exe

# 2. Verificar tamanho do executável (deve ser 31-35 MB)
# Se for muito pequeno (< 10 MB), algo deu errado

# 3. Verificar pasta _internal
dir _internal

# 4. Verificar arquivos Python dentro do _internal
dir _internal\\*.py

# 5. Verificar pastas de dados
dir _internal\\KE5Z
dir _internal\\pages
dir _internal\\Extracoes

# 6. Verificar arquivos editáveis FORA do _internal
dir *.json
''', language="bash")

st.markdown("### 7.2 Teste de Execução")
st.code('''
# Teste 1: Executar o .exe
Dashboard_KE5Z_OFICIAL.exe

# Teste 2: Verificar se abre no navegador
# Deve abrir automaticamente em http://localhost:8501

# Teste 3: Fazer login
# Usar credenciais de teste

# Teste 4: Navegar pelas páginas
# Testar todas as 8 páginas

# Teste 5: Testar funcionalidades
# - Carregar dados
# - Aplicar filtros
# - Gerar gráficos
# - Exportar arquivos
''', language="bash")

st.markdown("### 7.3 Teste em Outro PC")
st.markdown("**IMPORTANTE**: Testar em PC sem Python instalado")
st.code('''
# 1. Copiar TODA a pasta Dashboard_KE5Z_OFICIAL
# 2. Colar em outro PC
# 3. Executar o .exe
# 4. Verificar se funciona 100%
''', language="bash")

st.markdown("---")

# Seção 8: Solução de Problemas
st.markdown("## 8. SOLUÇÃO DE PROBLEMAS")

with st.expander("### 8.1 Problema: Executável não abre"):
    st.markdown("**Sintomas**: Clica no .exe e nada acontece")
    st.markdown("**Soluções**:")
    st.code('''
# 1. Verificar se o Windows Defender está bloqueando
# Ir em: Configurações > Segurança do Windows > Proteção contra vírus

# 2. Executar como administrador
# Clicar com botão direito > Executar como administrador

# 3. Verificar se a porta 8501 está livre
netstat -an | findstr :8501

# 4. Verificar logs de erro
# Executar pelo CMD para ver mensagens de erro
cd dist\\Dashboard_KE5Z_OFICIAL
Dashboard_KE5Z_OFICIAL.exe
''', language="bash")

with st.expander("### 8.2 Problema: Erro 'Arquivo não encontrado'"):
    st.markdown("**Sintomas**: Aplicação abre mas não carrega dados")
    st.markdown("**Soluções**:")
    st.code('''
# 1. Verificar se está usando get_base_path() corretamente
# Em TODOS os arquivos Python

# 2. Verificar se os arquivos estão no _internal
dir _internal\\KE5Z
dir _internal\\Extracoes

# 3. Adicionar debug no código
import sys
import os

base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(os.path.abspath(__file__))
print(f"Base path: {base_path}")
print(f"Arquivos em KE5Z: {os.listdir(os.path.join(base_path, 'KE5Z'))}")
''', language="python")

with st.expander("### 8.3 Problema: Erro 'No package metadata was found for streamlit'"):
    st.markdown("**Sintomas**: Executável abre e fecha imediatamente")
    st.markdown("**Solução**: Usar `streamlit-desktop-app` (já resolve automaticamente)")
    st.markdown("Se o erro persistir:")
    st.code('''
# Reinstalar streamlit-desktop-app
pip uninstall streamlit-desktop-app
pip install streamlit-desktop-app

# Limpar cache
rmdir /s /q build
rmdir /s /q dist

# Rebuild
criar_executavel_funcional.bat
''', language="bash")

with st.expander("### 8.4 Problema: Pastas não foram copiadas para _internal"):
    st.markdown("**Sintomas**: Estrutura do _internal está incompleta")
    st.markdown("**Solução**: Executar comandos manualmente")
    st.code('''
# Navegar para a pasta do projeto
cd C:\\user\\U235107\\GitHub\\DashAPPwin11

# Copiar pastas para _internal
xcopy "KE5Z" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\KE5Z\\" /E /I /Y
xcopy "Extracoes" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\Extracoes\\" /E /I /Y
xcopy "arquivos" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\arquivos\\" /E /I /Y
xcopy "pages" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\pages\\" /E /I /Y

# Copiar arquivos de configuração
copy "dados_equipe.json" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\"
copy "Dados SAPIENS.xlsx" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\"
copy "Fornecedores.xlsx" "dist\\Dashboard_KE5Z_OFICIAL\\_internal\\"

# Copiar arquivos editáveis para fora do _internal
copy "usuarios.json" "dist\\Dashboard_KE5Z_OFICIAL\\"
copy "usuarios_padrao.json" "dist\\Dashboard_KE5Z_OFICIAL\\"
''', language="bash")

with st.expander("### 8.5 Problema: Sistema não funciona quando pasta é movida"):
    st.markdown("**Sintomas**: Executável funciona no PC original, mas não funciona quando pasta é copiada para outro local")
    st.markdown("**Causa**: Caminhos hardcoded ou falta de busca em múltiplos locais")
    st.markdown("**Solução CRÍTICA**:")
    st.code('''
# 1. Garantir que ensure_working_directory() está no início do app.py
def ensure_working_directory():
    """Garante que o diretório de trabalho seja o diretório do executável"""
    if hasattr(sys, '_MEIPASS'):
        try:
            exe_path = os.path.abspath(sys.executable)  # CRÍTICO: usar abspath
            exe_dir = os.path.dirname(exe_path)
            if os.path.exists(exe_dir):
                os.chdir(exe_dir)
        except Exception:
            pass
        # Limpar variáveis de ambiente que podem causar problemas
        for var in ['VIRTUAL_ENV', 'PYTHONHOME', 'CONDA_DEFAULT_ENV']:
            if var in os.environ:
                del os.environ[var]

# Executar imediatamente ao importar
ensure_working_directory()

# 2. Usar get_base_path() que busca em múltiplos locais
def get_base_path():
    """Retorna o caminho base correto para LEITURA de dados
    
    Estratégia de busca para portabilidade:
    1. No executável: primeiro tenta _internal (onde dados são copiados)
    2. Se não encontrar, tenta diretório do executável (para quando pasta é movida)
    3. Em desenvolvimento: usa diretório do script
    """
    if hasattr(sys, '_MEIPASS'):
        # 1. Primeiro tentar _internal (onde dados são copiados no build)
        try:
            meipass_path = os.path.abspath(sys._MEIPASS)  # CRÍTICO
            if os.path.exists(meipass_path):
                ke5z_path = os.path.join(meipass_path, "KE5Z")
                if os.path.exists(ke5z_path):
                    return meipass_path
        except Exception:
            pass
        
        # 2. Fallback: tentar diretório do executável (para quando pasta é movida)
        try:
            exe_path = os.path.abspath(sys.executable)  # CRÍTICO
            exe_dir = os.path.dirname(exe_path)
            if os.path.exists(exe_dir):
                ke5z_path_exe = os.path.join(exe_dir, "KE5Z")
                ke5z_path_internal = os.path.join(exe_dir, "_internal", "KE5Z")
                if os.path.exists(ke5z_path_exe):
                    return exe_dir
                elif os.path.exists(ke5z_path_internal):
                    return os.path.join(exe_dir, "_internal")
        except Exception:
            pass
        
        # 3. Último fallback: usar _MEIPASS mesmo que não exista
        try:
            return os.path.abspath(sys._MEIPASS)
        except Exception:
            return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

# 3. Buscar arquivos em múltiplos locais
def load_data():
    base_path = get_base_path()
    locais_possiveis = []
    locais_possiveis.append(os.path.join(base_path, "KE5Z", "KE5Z.parquet"))
    
    if hasattr(sys, '_MEIPASS'):
        try:
            exe_path = os.path.abspath(sys.executable)
            exe_dir = os.path.dirname(exe_path)
            locais_possiveis.append(os.path.join(exe_dir, "KE5Z", "KE5Z.parquet"))
            locais_possiveis.append(os.path.join(exe_dir, "_internal", "KE5Z", "KE5Z.parquet"))
        except Exception:
            pass
    
    # Procurar arquivo nos locais possíveis
    for local in locais_possiveis:
        if os.path.exists(local):
            return pd.read_parquet(local)
    
    raise FileNotFoundError("Arquivo não encontrado em nenhum local")
''', language="python")
    
    st.markdown("**Regras Obrigatórias para Portabilidade:**")
    st.markdown("""
    1. ✅ **SEMPRE** usar `os.path.abspath()` em `sys.executable` e `sys._MEIPASS`
    2. ✅ **SEMPRE** verificar existência de diretórios antes de usar
    3. ✅ **SEMPRE** ter fallbacks seguros em caso de erro
    4. ✅ **SEMPRE** executar `ensure_working_directory()` no início do app.py
    5. ✅ **SEMPRE** buscar arquivos em múltiplos locais quando no executável
    6. ✅ **NUNCA** usar caminhos relativos sem converter para absolutos
    """)
    
    st.markdown("**Estratégia de Busca de Dados:**")
    st.markdown("""
    O sistema agora busca dados em **3 locais possíveis** (em ordem de prioridade):
    1. `_internal/KE5Z/` (local padrão do build)
    2. `exe_dir/KE5Z/` (diretório do executável - para quando pasta é movida)
    3. `exe_dir/_internal/KE5Z/` (fallback interno)
    """)
    
    st.markdown("**Teste de Portabilidade:**")
    st.code('''
# 1. Criar executável
criar_executavel_oficial.bat

# 2. Copiar pasta para outro local
xcopy "dist\\Dashboard_KE5Z_OFICIAL" "C:\\Teste\\Dashboard_KE5Z_OFICIAL\\" /E /I /Y

# 3. Executar no novo local
cd C:\\Teste\\Dashboard_KE5Z_OFICIAL
Dashboard_KE5Z_OFICIAL.exe

# 4. Verificar se funciona corretamente
# O sistema deve encontrar os dados automaticamente em qualquer um dos 3 locais
''', language="bash")

st.markdown("---")

# Seção 8.5: Problema de Portabilidade (ATUALIZADA)
with st.expander("### 8.5 Problema: Sistema não funciona quando pasta é movida"):
    st.markdown("**Sintomas**: Executável funciona no PC original, mas não funciona quando pasta é copiada para outro local")
    st.markdown("**Causa**: Caminhos hardcoded ou falta de busca em múltiplos locais")
    st.markdown("**Solução CRÍTICA**:")
    st.code('''
# 1. Garantir que ensure_working_directory() está no início do app.py
def ensure_working_directory():
    """Garante que o diretório de trabalho seja o diretório do executável"""
    if hasattr(sys, '_MEIPASS'):
        try:
            exe_path = os.path.abspath(sys.executable)  # CRÍTICO: usar abspath
            exe_dir = os.path.dirname(exe_path)
            if os.path.exists(exe_dir):
                os.chdir(exe_dir)
        except Exception:
            pass
        # Limpar variáveis de ambiente que podem causar problemas
        for var in ['VIRTUAL_ENV', 'PYTHONHOME', 'CONDA_DEFAULT_ENV']:
            if var in os.environ:
                del os.environ[var]

# Executar imediatamente ao importar
ensure_working_directory()

# 2. Usar get_base_path() que busca em múltiplos locais
def get_base_path():
    """Retorna o caminho base correto para LEITURA de dados
    
    Estratégia de busca para portabilidade:
    1. No executável: primeiro tenta _internal (onde dados são copiados)
    2. Se não encontrar, tenta diretório do executável (para quando pasta é movida)
    3. Em desenvolvimento: usa diretório do script
    """
    if hasattr(sys, '_MEIPASS'):
        # 1. Primeiro tentar _internal (onde dados são copiados no build)
        try:
            meipass_path = os.path.abspath(sys._MEIPASS)  # CRÍTICO
            if os.path.exists(meipass_path):
                ke5z_path = os.path.join(meipass_path, "KE5Z")
                if os.path.exists(ke5z_path):
                    return meipass_path
        except Exception:
            pass
        
        # 2. Fallback: tentar diretório do executável (para quando pasta é movida)
        try:
            exe_path = os.path.abspath(sys.executable)  # CRÍTICO
            exe_dir = os.path.dirname(exe_path)
            if os.path.exists(exe_dir):
                ke5z_path_exe = os.path.join(exe_dir, "KE5Z")
                ke5z_path_internal = os.path.join(exe_dir, "_internal", "KE5Z")
                if os.path.exists(ke5z_path_exe):
                    return exe_dir
                elif os.path.exists(ke5z_path_internal):
                    return os.path.join(exe_dir, "_internal")
        except Exception:
            pass
        
        # 3. Último fallback: usar _MEIPASS mesmo que não exista
        try:
            return os.path.abspath(sys._MEIPASS)
        except Exception:
            return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

# 3. Buscar arquivos em múltiplos locais
def load_data():
    base_path = get_base_path()
    locais_possiveis = []
    locais_possiveis.append(os.path.join(base_path, "KE5Z", "KE5Z.parquet"))
    
    if hasattr(sys, '_MEIPASS'):
        try:
            exe_path = os.path.abspath(sys.executable)
            exe_dir = os.path.dirname(exe_path)
            locais_possiveis.append(os.path.join(exe_dir, "KE5Z", "KE5Z.parquet"))
            locais_possiveis.append(os.path.join(exe_dir, "_internal", "KE5Z", "KE5Z.parquet"))
        except Exception:
            pass
    
    # Procurar arquivo nos locais possíveis
    for local in locais_possiveis:
        if os.path.exists(local):
            return pd.read_parquet(local)
    
    raise FileNotFoundError("Arquivo não encontrado em nenhum local")
''', language="python")
    
    st.markdown("**Regras Obrigatórias para Portabilidade:**")
    st.markdown("""
    1. ✅ **SEMPRE** usar `os.path.abspath()` em `sys.executable` e `sys._MEIPASS`
    2. ✅ **SEMPRE** verificar existência de diretórios antes de usar
    3. ✅ **SEMPRE** ter fallbacks seguros em caso de erro
    4. ✅ **SEMPRE** executar `ensure_working_directory()` no início do app.py
    5. ✅ **SEMPRE** buscar arquivos em múltiplos locais quando no executável
    6. ✅ **NUNCA** usar caminhos relativos sem converter para absolutos
    """)
    
    st.markdown("**Estratégia de Busca de Dados:**")
    st.markdown("""
    O sistema agora busca dados em **3 locais possíveis** (em ordem de prioridade):
    1. `_internal/KE5Z/` (local padrão do build)
    2. `exe_dir/KE5Z/` (diretório do executável - para quando pasta é movida)
    3. `exe_dir/_internal/KE5Z/` (fallback interno)
    """)
    
    st.markdown("**Teste de Portabilidade:**")
    st.code('''
# 1. Criar executável
criar_executavel_oficial.bat

# 2. Copiar pasta para outro local
xcopy "dist\Dashboard_KE5Z_OFICIAL" "C:\Teste\Dashboard_KE5Z_OFICIAL\" /E /I /Y

# 3. Executar no novo local
cd C:\Teste\Dashboard_KE5Z_OFICIAL
Dashboard_KE5Z_OFICIAL.exe

# 4. Verificar se funciona corretamente
# O sistema deve encontrar os dados automaticamente em qualquer um dos 3 locais
''', language="bash")

st.markdown("---")

# Seção 9: Distribuição
st.markdown("## 9. DISTRIBUIÇÃO")
st.markdown("### 9.1 Preparar para Distribuição")
st.code('''
# 1. Testar o executável localmente
cd dist\\Dashboard_KE5Z_OFICIAL
Dashboard_KE5Z_OFICIAL.exe

# 2. Criar pasta de distribuição
cd C:\\user\\U235107\\GitHub\\DashAPPwin11
mkdir Dashboard_KE5Z_Distribuicao

# 3. Copiar TODA a pasta
xcopy "dist\\Dashboard_KE5Z_OFICIAL" "Dashboard_KE5Z_Distribuicao\\Dashboard_KE5Z_OFICIAL\\" /E /I /Y

# 4. Criar arquivo de instruções
echo Para executar, clique duas vezes em Dashboard_KE5Z_OFICIAL.exe > Dashboard_KE5Z_Distribuicao\\COMO_USAR.txt
''', language="bash")

st.markdown("### 9.2 Compactar para Distribuição")
st.code('''
# Opção 1: ZIP
# Clicar com botão direito na pasta > Enviar para > Pasta compactada

# Opção 2: PowerShell
Compress-Archive -Path "Dashboard_KE5Z_Distribuicao\\*" -DestinationPath "Dashboard_KE5Z_v4.0.zip"
''', language="bash")

st.markdown("---")

# Seção 10: Checklist
st.markdown("## 10. CHECKLIST COMPLETO")

with st.expander("### ✅ ANTES DO EMPACOTAMENTO"):
    st.markdown("""
    - [ ] Python 3.8+ instalado
    - [ ] streamlit-desktop-app instalado
    - [ ] Todas as dependências instaladas (requirements.txt)
    - [ ] Aplicação Streamlit funcionando (`streamlit run app.py`)
    - [ ] Todos os arquivos Python usando `get_base_path()` e `get_output_path()`
    - [ ] Pastas de dados existem (KE5Z, Extracoes, arquivos, pages)
    - [ ] Arquivos de configuração existem (*.json, *.xlsx)
    - [ ] Sistema de autenticação testado
    - [ ] Todas as páginas carregando sem erros
    """)

with st.expander("### ✅ DURANTE O EMPACOTAMENTO"):
    st.markdown("""
    - [ ] Builds anteriores limpos (build/ e dist/ removidos)
    - [ ] Comando `streamlit-desktop-app build app.py --name Dashboard_KE5Z_OFICIAL` executado
    - [ ] Executável criado em `dist\\Dashboard_KE5Z_OFICIAL\\`
    - [ ] Pasta `_internal` criada automaticamente
    - [ ] Pastas de dados copiadas para `_internal\\`
    - [ ] Arquivos de configuração copiados para `_internal\\`
    - [ ] Arquivos editáveis copiados para fora do `_internal\\`
    """)

with st.expander("### ✅ APÓS O EMPACOTAMENTO"):
    st.markdown("""
    - [ ] Executável principal existe e tem 31-35 MB
    - [ ] Pasta `_internal` existe e tem 400-500 MB
    - [ ] `usuarios.json` está FORA do `_internal`
    - [ ] `usuarios_padrao.json` está FORA do `_internal`
    - [ ] `app.py` está DENTRO do `_internal`
    - [ ] `auth_simple.py` está DENTRO do `_internal`
    - [ ] `Extracao.py` está DENTRO do `_internal`
    - [ ] Pasta `pages/` está DENTRO do `_internal`
    - [ ] Pasta `KE5Z/` está DENTRO do `_internal`
    - [ ] Pasta `Extracoes/` está DENTRO do `_internal`
    - [ ] Pasta `arquivos/` está DENTRO do `_internal`
    - [ ] `dados_equipe.json` está DENTRO do `_internal`
    - [ ] `Dados SAPIENS.xlsx` está DENTRO do `_internal`
    - [ ] `Fornecedores.xlsx` está DENTRO do `_internal`
    """)

with st.expander("### ✅ TESTES"):
    st.markdown("""
    - [ ] Executável inicia sem erros
    - [ ] Navegador abre automaticamente em http://localhost:8501
    - [ ] Sistema de login funcionando
    - [ ] Todas as 8 páginas acessíveis
    - [ ] Dados carregando corretamente
    - [ ] Filtros funcionando
    - [ ] Gráficos renderizando
    - [ ] Exportação de arquivos funcionando
    - [ ] Extração de dados funcionando
    - [ ] Testado em outro PC sem Python
    """)

with st.expander("### ✅ DISTRIBUIÇÃO"):
    st.markdown("""
    - [ ] Pasta de distribuição criada
    - [ ] Arquivo COMO_USAR.txt incluído
    - [ ] Estrutura completa copiada
    - [ ] Arquivo ZIP criado (opcional)
    - [ ] Testado em ambiente limpo
    - [ ] Documentação atualizada
    """)

st.markdown("---")

# Resumo Executivo
st.markdown("## 🎯 RESUMO EXECUTIVO")
st.markdown("### Para Qualquer IA Seguir Este Guia:")

st.markdown("**1. PREPARAÇÃO**")
st.code('''
cd C:\\user\\U235107\\GitHub\\DashAPPwin11
pip install streamlit-desktop-app
''', language="bash")

st.markdown("**2. BUILD**")
st.code('''
criar_executavel_funcional.bat
''', language="bash")

st.markdown("**3. VERIFICAÇÃO**")
st.code('''
cd dist\\Dashboard_KE5Z_OFICIAL
dir *.exe
dir _internal\\KE5Z
dir _internal\\pages
dir *.json
''', language="bash")

st.markdown("**4. TESTE**")
st.code('''
Dashboard_KE5Z_OFICIAL.exe
''', language="bash")

st.markdown("**5. DISTRIBUIÇÃO**")
st.code('''
xcopy "dist\\Dashboard_KE5Z_OFICIAL" "Dashboard_KE5Z_Distribuicao\\" /E /I /Y
''', language="bash")

st.markdown("### Estrutura Final Esperada:")
st.code("""
dist/Dashboard_KE5Z_OFICIAL/
├── Dashboard_KE5Z_OFICIAL.exe (31-35 MB)
├── usuarios.json
├── usuarios_padrao.json
└── _internal/ (400-500 MB)
    ├── app.py
    ├── auth_simple.py
    ├── Extracao.py
    ├── pages/ (8 arquivos)
    ├── KE5Z/ (arquivos parquet)
    ├── Extracoes/
    ├── arquivos/
    ├── dados_equipe.json
    ├── Dados SAPIENS.xlsx
    ├── Fornecedores.xlsx
    └── [Dependências Python]
""", language="text")

st.markdown("### Regras Críticas:")
st.markdown("""
1. **SEMPRE** usar `streamlit-desktop-app` para build
2. **SEMPRE** copiar dados para `_internal/`
3. **SEMPRE** manter `usuarios.json` FORA do `_internal/`
4. **SEMPRE** usar `get_base_path()` para leitura (com busca em múltiplos locais para portabilidade)
5. **SEMPRE** usar `os.path.dirname(os.path.abspath(sys.executable))` para escrita
6. **SEMPRE** chamar `ensure_working_directory()` no início do app.py
7. **SEMPRE** buscar arquivos em múltiplos locais quando no executável (portabilidade)
8. **SEMPRE** usar `os.path.abspath()` em `sys.executable` e `sys._MEIPASS`
""")

st.markdown("---")
st.markdown("**🎉 FIM DO GUIA DEFINITIVO**")
st.markdown("*Este guia foi criado para garantir que qualquer IA possa reproduzir exatamente o mesmo resultado de empacotamento do Dashboard KE5Z.*")
st.markdown("*Versão: 4.1 - Definitivo e Completo com Portabilidade*")
st.markdown("*Data: 25/10/2025*")
st.markdown("*Status: ✅ TESTADO E FUNCIONANDO*")
st.markdown("*Atualização: ✅ Sistema agora funciona quando pasta é movida (portabilidade)*")

# Footer
st.markdown("---")
st.markdown(f"*Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}*")
