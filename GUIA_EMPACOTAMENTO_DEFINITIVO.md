# 🚀 GUIA DEFINITIVO DE EMPACOTAMENTO - DASHBOARD KE5Z
## Versão 4.2 - Guia Completo e Unificado para Qualquer IA

---

## 📋 **ÍNDICE COMPLETO**

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

---

## 1. VISÃO GERAL

### 🎯 **OBJETIVO DESTE GUIA**
Este é o guia **DEFINITIVO** e **UNIFICADO** para empacotamento do Dashboard KE5Z. Foi criado para que **QUALQUER IA** possa seguir passo a passo e reproduzir exatamente o mesmo resultado.

### ✅ **O QUE ESTE GUIA GARANTE**
- ✅ Executável standalone funcionando 100%
- ✅ Compatibilidade total com Windows 10/11
- ✅ Todas as funcionalidades preservadas
- ✅ Estrutura de pastas correta (_internal)
- ✅ Sistema de autenticação funcional
- ✅ Processamento de dados operacional
- ✅ Múltiplas páginas com navegação
- ✅ Distribuição simples (1 pasta)

### 🔑 **PRINCÍPIOS FUNDAMENTAIS**

#### **1. Estrutura _internal (CRÍTICO)**
O PyInstaller cria uma estrutura específica:
```
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
```

#### **2. Regra de Ouro: Leitura vs Escrita**
- **LEITURA**: Usar `sys._MEIPASS` (aponta para `_internal/`)
- **ESCRITA**: Usar `os.path.dirname(sys.executable)` (aponta para pasta do .exe)

#### **3. Ferramenta Correta**
- **USAR**: `streamlit-desktop-app` (gerencia _internal automaticamente)
- **NÃO USAR**: PyInstaller direto (requer configuração manual complexa)

---

## 2. PRÉ-REQUISITOS

### 2.1 Sistema Operacional
- **Windows 10/11** (64-bit) - TESTADO E FUNCIONANDO
- **Python 3.8+** (apenas para desenvolvimento)
- **PowerShell** ou **CMD** (para executar scripts)

### 2.2 Dependências Python (Versões Testadas)
```bash
# Instalar todas as dependências de uma vez
pip install streamlit==1.50.0 pandas==2.3.3 plotly==5.17.0 pyarrow==20.0.0 openpyxl==3.1.5 altair==5.5.0 numpy==2.3.3 xlsxwriter==3.2.9 streamlit-desktop-app==0.3.3
```

### 2.3 Verificar Instalação
```bash
# Verificar Python
python --version

# Verificar dependências principais
pip show streamlit
pip show streamlit-desktop-app
pip show pandas
pip show pyarrow
```

---

## 3. ESTRUTURA DO PROJETO

### 3.1 Estrutura Antes do Empacotamento
```
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
```

### 3.2 Arquivos Críticos

#### **app.py** - Aplicação Principal
```python
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
        # Rodando no executável PyInstaller
        # CORREÇÃO CRÍTICA: Tentar múltiplos locais para portabilidade
        
        # 1. Primeiro tentar _internal (onde dados são copiados no build)
        try:
            meipass_path = os.path.abspath(sys._MEIPASS)
            if os.path.exists(meipass_path):
                # Verificar se existe pasta KE5Z em _internal
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
                # Verificar se existe pasta KE5Z ou _internal/KE5Z no diretório do executável
                ke5z_path_exe = os.path.join(exe_dir, "KE5Z")
                ke5z_path_internal = os.path.join(exe_dir, "_internal", "KE5Z")
                if os.path.exists(ke5z_path_exe):
                    return exe_dir
                elif os.path.exists(ke5z_path_internal):
                    return os.path.join(exe_dir, "_internal")
        except Exception:
            pass
        
        # 3. Último fallback: usar _MEIPASS mesmo que não exista (pode ser temporário)
        try:
            return os.path.abspath(sys._MEIPASS)
        except Exception:
            return sys._MEIPASS
    else:
        # Rodando em desenvolvimento
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
```

#### **auth_simple.py** - Sistema de Autenticação
```python
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
```

#### **Extracao.py** - Processamento de Dados
```python
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
```

---

## 4. CONFIGURAÇÃO DE CAMINHOS

### 4.1 Padrão de Caminhos (CRÍTICO)

#### **Função para LEITURA de Dados (COM PORTABILIDADE)**
```python
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
```

#### **Função para ESCRITA de Dados**
```python
def get_output_path():
    """Retorna o caminho correto para ESCRITA de dados"""
    if hasattr(sys, '_MEIPASS'):
        # No executável: salvar no diretório do executável (fora do _internal)
        return os.path.dirname(sys.executable)
    else:
        # Em desenvolvimento: mesmo diretório
        return os.path.dirname(os.path.abspath(__file__))
```

### 4.2 Aplicação em Todas as Páginas

**REGRA**: Todas as páginas do Streamlit devem usar estas funções.

**Exemplo em pages/1_Dash_Mes.py:**
```python
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
```

---

## 5. PROCESSO DE EMPACOTAMENTO

### 5.1 Método Recomendado: streamlit-desktop-app

**POR QUE USAR streamlit-desktop-app?**
- ✅ Gerencia automaticamente a estrutura `_internal/`
- ✅ Inclui todas as dependências do Streamlit
- ✅ Configuração simplificada
- ✅ Menos propenso a erros

### 5.2 Script de Build (criar_executavel_funcional.bat)

```batch
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
REM CRÍTICO: Pasta KE5Z DEVE estar no _internal (dados processados)
if exist "KE5Z" (
    xcopy "KE5Z" "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\" /E /I /Y >nul
) else (
    REM Criar pasta vazia se não existir (será preenchida pela extração)
    if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z"
)

if exist "Extracoes" (
    xcopy "Extracoes" "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\" /E /I /Y >nul
)

REM CRÍTICO: Pasta arquivos deve estar no _internal (mesmo que vazia)
if exist "arquivos" (
    xcopy "arquivos" "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\" /E /I /Y >nul
) else (
    REM Criar pasta vazia se não existir (será preenchida pela extração)
    if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos"
)

if exist "pages" (
    xcopy "pages" "dist\Dashboard_KE5Z_OFICIAL\_internal\pages\" /E /I /Y >nul
)

REM Copiar arquivos de configuração para _internal
copy "dados_equipe.json" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
copy "Dados SAPIENS.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
copy "Fornecedores.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul

REM Copiar arquivos Python principais para _internal
copy "auth_simple.py" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul
copy "Extracao.py" "dist\Dashboard_KE5Z_OFICIAL\_internal\" >nul

echo ✅ Dados copiados para _internal
echo.

REM Passo 4: Copiar arquivos EDITÁVEIS para fora do _internal
echo 📝 Copiando arquivos editáveis...
copy "usuarios.json" "dist\Dashboard_KE5Z_OFICIAL\" >nul
copy "usuarios_padrao.json" "dist\Dashboard_KE5Z_OFICIAL\" >nul

echo ✅ Arquivos editáveis copiados
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
echo    BUILD CONCLUÍDO!
echo ===============================================
echo.
echo 📁 Localização: dist\Dashboard_KE5Z_OFICIAL\
echo 🚀 Para testar: Execute o arquivo .exe
echo.
pause
```

### 5.3 Comandos Passo a Passo

```bash
# 1. Navegar para a pasta do projeto
cd C:\user\U235107\GitHub\DashAPPwin11

# 2. Verificar se streamlit-desktop-app está instalado
pip show streamlit-desktop-app

# 3. Limpar builds anteriores
rmdir /s /q build
rmdir /s /q dist

# 4. Executar o script de build
criar_executavel_funcional.bat
```

---

## 6. ESTRUTURA FINAL DA PASTA dist

### 6.1 Estrutura Completa (CRÍTICO - SEGUIR EXATAMENTE)

Esta é a estrutura **EXATA** que deve ser criada após o empacotamento:

```
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
```

### 6.2 Verificação da Estrutura

**Comando para verificar a estrutura:**
```bash
cd dist\Dashboard_KE5Z_OFICIAL

# Verificar executável
dir *.exe

# Verificar arquivos editáveis (FORA do _internal)
dir *.json

# Verificar pasta _internal
dir _internal

# Verificar dados dentro do _internal
dir _internal\KE5Z
dir _internal\Extracoes
dir _internal\arquivos
dir _internal\pages

# Verificar arquivos auxiliares
dir _internal\*.xlsx
dir _internal\*.json
```

### 6.3 Tamanhos Esperados

| Item | Tamanho Aproximado |
|------|-------------------|
| **Dashboard_KE5Z_OFICIAL.exe** | 31-35 MB |
| **_internal/** (pasta completa) | 400-500 MB |
| **KE5Z.parquet** | 50-100 MB |
| **KE5Z_waterfall.parquet** | 15-30 MB (68% menor) |
| **Dados SAPIENS.xlsx** | 1-5 MB |
| **Total da pasta dist/** | 450-550 MB |

### 6.4 Arquivos Críticos que NÃO Podem Faltar

#### **No diretório raiz (fora do _internal):**
- ✅ `Dashboard_KE5Z_OFICIAL.exe`
- ✅ `usuarios.json`
- ✅ `usuarios_padrao.json`

#### **Dentro do _internal:**
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

### 6.5 Regra de Ouro: O que vai onde?

#### **FORA do _internal (editável pelo usuário):**
```
✅ usuarios.json          → Usuário pode editar
✅ usuarios_padrao.json   → Usuário pode editar
```

#### **DENTRO do _internal (read-only, bundled):**
```
✅ Todos os scripts Python (.py)
✅ Todas as pastas de dados (KE5Z, Extracoes, arquivos, pages)
✅ Todos os arquivos de configuração (dados_equipe.json, *.xlsx)
✅ Todas as dependências Python
✅ Todas as DLLs
```

---

## 7. VERIFICAÇÃO E TESTES

### 7.1 Checklist de Verificação Imediata

Após o build, execute estas verificações:

```bash
# 1. Verificar se o executável foi criado
cd dist\Dashboard_KE5Z_OFICIAL
dir Dashboard_KE5Z_OFICIAL.exe

# 2. Verificar tamanho do executável (deve ser 31-35 MB)
# Se for muito pequeno (< 10 MB), algo deu errado

# 3. Verificar pasta _internal
dir _internal

# 4. Verificar arquivos Python dentro do _internal
dir _internal\*.py

# 5. Verificar pastas de dados
dir _internal\KE5Z
dir _internal\pages
dir _internal\Extracoes

# 6. Verificar arquivos editáveis FORA do _internal
dir *.json
```

### 7.2 Teste de Execução

```bash
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
```

### 7.3 Teste em Outro PC

**IMPORTANTE**: Testar em PC sem Python instalado

```bash
# 1. Copiar TODA a pasta Dashboard_KE5Z_OFICIAL
# 2. Colar em outro PC
# 3. Executar o .exe
# 4. Verificar se funciona 100%
```

---

## 8. SOLUÇÃO DE PROBLEMAS

### 8.1 Problema: Executável não abre

**Sintomas**: Clica no .exe e nada acontece

**Soluções**:
```bash
# 1. Verificar se o Windows Defender está bloqueando
# Ir em: Configurações > Segurança do Windows > Proteção contra vírus

# 2. Executar como administrador
# Clicar com botão direito > Executar como administrador

# 3. Verificar se a porta 8501 está livre
netstat -an | findstr :8501

# 4. Verificar logs de erro
# Executar pelo CMD para ver mensagens de erro
cd dist\Dashboard_KE5Z_OFICIAL
Dashboard_KE5Z_OFICIAL.exe
```

### 8.2 Problema: Erro "Arquivo não encontrado"

**Sintomas**: Aplicação abre mas não carrega dados

**Soluções**:
```python
# 1. Verificar se está usando get_base_path() corretamente
# Em TODOS os arquivos Python (com busca em múltiplos locais)

# 2. Verificar se os arquivos estão no _internal
dir _internal\KE5Z
dir _internal\Extracoes

# 3. Se a pasta foi movida, verificar estrutura:
# - Se dados estão em exe_dir/KE5Z/
# - Se dados estão em exe_dir/_internal/KE5Z/
# - Se dados estão em _MEIPASS/KE5Z/

# 4. Adicionar debug no código
import sys
import os

def get_base_path():
    """Versão com debug"""
    if hasattr(sys, '_MEIPASS'):
        meipass_path = os.path.abspath(sys._MEIPASS)
        print(f"_MEIPASS: {meipass_path}")
        if os.path.exists(meipass_path):
            ke5z_path = os.path.join(meipass_path, "KE5Z")
            print(f"KE5Z em _MEIPASS: {os.path.exists(ke5z_path)}")
            if os.path.exists(ke5z_path):
                return meipass_path
        
        exe_path = os.path.abspath(sys.executable)
        exe_dir = os.path.dirname(exe_path)
        print(f"Exe dir: {exe_dir}")
        ke5z_path_exe = os.path.join(exe_dir, "KE5Z")
        ke5z_path_internal = os.path.join(exe_dir, "_internal", "KE5Z")
        print(f"KE5Z em exe_dir: {os.path.exists(ke5z_path_exe)}")
        print(f"KE5Z em exe_dir/_internal: {os.path.exists(ke5z_path_internal)}")
        
        if os.path.exists(ke5z_path_exe):
            return exe_dir
        elif os.path.exists(ke5z_path_internal):
            return os.path.join(exe_dir, "_internal")
    
    return os.path.dirname(os.path.abspath(__file__))

base_path = get_base_path()
print(f"Base path final: {base_path}")
print(f"Arquivos em KE5Z: {os.listdir(os.path.join(base_path, 'KE5Z'))}")
```

### 8.2.1 Problema: Sistema não funciona quando pasta é movida

**Sintomas**: Executável funciona no PC original, mas não funciona quando pasta é copiada para outro local

**Causa**: Caminhos hardcoded ou falta de busca em múltiplos locais

**Solução**: Usar função `get_base_path()` atualizada que busca em múltiplos locais:
1. `_internal/KE5Z/` (local padrão do build)
2. `exe_dir/KE5Z/` (diretório do executável)
3. `exe_dir/_internal/KE5Z/` (fallback interno)

**Verificação**:
```python
# Garantir que ensure_working_directory() está sendo chamada
# Garantir que get_base_path() tenta múltiplos locais
# Garantir que load_data() busca em múltiplos locais
```

### 8.3 Problema: Erro "No package metadata was found for streamlit"

**Sintomas**: Executável abre e fecha imediatamente

**Solução**: Usar `streamlit-desktop-app` (já resolve automaticamente)

Se o erro persistir:
```bash
# Reinstalar streamlit-desktop-app
pip uninstall streamlit-desktop-app
pip install streamlit-desktop-app

# Limpar cache
rmdir /s /q build
rmdir /s /q dist

# Rebuild
criar_executavel_funcional.bat
```

### 8.4 Problema: Pastas não foram copiadas para _internal

**Sintomas**: Estrutura do _internal está incompleta

**Solução Automática**: O script `criar_executavel_oficial.bat` agora cria automaticamente as pastas `KE5Z/` e `arquivos/` dentro do `_internal` se elas não existirem no diretório fonte. Isso garante que a estrutura esteja sempre completa.

**Solução Manual (se necessário)**: Executar comandos manualmente
```bash
# Navegar para a pasta do projeto
cd C:\user\U235107\GitHub\DashAPPwin11

# Copiar pastas para _internal
xcopy "KE5Z" "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z\" /E /I /Y
xcopy "Extracoes" "dist\Dashboard_KE5Z_OFICIAL\_internal\Extracoes\" /E /I /Y
xcopy "arquivos" "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos\" /E /I /Y
xcopy "pages" "dist\Dashboard_KE5Z_OFICIAL\_internal\pages\" /E /I /Y

# Se as pastas não existirem, criar vazias (CRÍTICO)
if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\KE5Z"
if not exist "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos" mkdir "dist\Dashboard_KE5Z_OFICIAL\_internal\arquivos"

# Copiar arquivos de configuração
copy "dados_equipe.json" "dist\Dashboard_KE5Z_OFICIAL\_internal\"
copy "Dados SAPIENS.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\"
copy "Fornecedores.xlsx" "dist\Dashboard_KE5Z_OFICIAL\_internal\"

# Copiar arquivos editáveis para fora do _internal
copy "usuarios.json" "dist\Dashboard_KE5Z_OFICIAL\"
copy "usuarios_padrao.json" "dist\Dashboard_KE5Z_OFICIAL\"
```

**Nota Importante**: As pastas `KE5Z/` e `arquivos/` são **OBRIGATÓRIAS** dentro do `_internal`, mesmo que vazias. Elas serão preenchidas quando a extração for executada.

### 8.5 Problema: Erro ao processar dados

**Sintomas**: Extração de dados não funciona

**Solução**: Verificar caminhos de entrada e saída
```python
# Em Extracao.py, verificar:

# Para LEITURA (dentro do _internal)
ROOT_DIR = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(os.path.abspath(__file__))

# Para ESCRITA (dentro do _internal - dados salvos no mesmo local onde são lidos)
OUTPUT_DIR = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(os.path.abspath(__file__))
```

### 8.5.1 Problema: Erro "read_csv() got an unexpected keyword argument 'warn_bad_lines'"

**Sintomas**: Durante a extração, aparece erro: `read_csv() got an unexpected keyword argument 'warn_bad_lines'. Did you mean 'on_bad_lines'?`

**Causa**: O pandas descontinuou o parâmetro `warn_bad_lines` nas versões mais recentes. Este parâmetro foi removido e substituído apenas por `on_bad_lines`.

**Solução**: Remover todas as ocorrências de `warn_bad_lines=True` do arquivo `Extracao.py`:

**ANTES (ERRADO):**
```python
df = pd.read_csv(
    arquivo,
    sep='\t',
    encoding='latin1',
    engine='python',
    on_bad_lines='skip',
    warn_bad_lines=True   # ❌ ERRO: Este parâmetro foi descontinuado
)
```

**DEPOIS (CORRETO):**
```python
df = pd.read_csv(
    arquivo,
    sep='\t',
    encoding='latin1',
    engine='python',
    on_bad_lines='skip'  # ✅ CORRETO: Apenas este parâmetro é necessário
)
```

**Verificação**: Garantir que não há mais ocorrências de `warn_bad_lines` no código:
```bash
# Verificar se há ocorrências restantes
grep -n "warn_bad_lines" Extracao.py

# Se retornar resultados, remover manualmente todas as linhas com warn_bad_lines=True
```

**Nota**: O parâmetro `on_bad_lines='skip'` já faz o trabalho de pular linhas mal formatadas e não precisa de `warn_bad_lines` para avisar sobre isso.

### 8.6 Problema: "No module named 'auth_simple'"

**Sintomas**: Executável abre mas dá erro de módulo não encontrado

**Causa**: Arquivos Python principais não foram copiados para `_internal`

**Solução**:
```batch
REM Verificar se todos os arquivos Python estão presentes
dir /b dist\Dashboard_KE5Z_OFICIAL\_internal\*.py

REM Se faltar algum, copiar:
copy auth_simple.py dist\Dashboard_KE5Z_OFICIAL\_internal\
copy Extracao.py dist\Dashboard_KE5Z_OFICIAL\_internal\
```

### 8.7 Problema: "deu erro ao entrar no app"

**Sintomas**: Executável não inicia ou fecha imediatamente

**Causa**: Arquivos essenciais faltando no `_internal`

**Solução**:
```batch
REM Verificar estrutura completa
dir /b dist\Dashboard_KE5Z_OFICIAL\_internal\

REM Copiar arquivos que podem estar faltando:
copy dados_equipe.json dist\Dashboard_KE5Z_OFICIAL\_internal\
copy auth_simple.py dist\Dashboard_KE5Z_OFICIAL\_internal\
copy Extracao.py dist\Dashboard_KE5Z_OFICIAL\_internal\
```

---

## 9. DISTRIBUIÇÃO

### 9.1 Preparar para Distribuição

```bash
# 1. Testar o executável localmente
cd dist\Dashboard_KE5Z_OFICIAL
Dashboard_KE5Z_OFICIAL.exe

# 2. Criar pasta de distribuição
cd C:\user\U235107\GitHub\DashAPPwin11
mkdir Dashboard_KE5Z_Distribuicao

# 3. Copiar TODA a pasta
xcopy "dist\Dashboard_KE5Z_OFICIAL" "Dashboard_KE5Z_Distribuicao\Dashboard_KE5Z_OFICIAL\" /E /I /Y

# 4. Criar arquivo de instruções
echo Para executar, clique duas vezes em Dashboard_KE5Z_OFICIAL.exe > Dashboard_KE5Z_Distribuicao\COMO_USAR.txt
```

### 9.2 Arquivo COMO_USAR.txt

```text
===============================================
    DASHBOARD KE5Z - VERSÃO DESKTOP
===============================================

🎉 BEM-VINDO!

===============================================
    COMO USAR:
===============================================

1. EXECUTAR O DASHBOARD:
   - Clique duas vezes no arquivo: Dashboard_KE5Z_OFICIAL.exe
   - Aguarde alguns segundos para o aplicativo carregar
   - O dashboard abrirá automaticamente no seu navegador

2. ACESSO:
   - O dashboard abrirá em: http://localhost:8501
   - Use as credenciais fornecidas para fazer login

3. FUNCIONALIDADES:
   ✅ Dashboard principal com métricas
   ✅ Análise de dados por mês
   ✅ Waterfall analysis
   ✅ Extração e processamento de dados
   ✅ Exportação de relatórios
   ✅ Sistema de usuários

===============================================
    REQUISITOS:
===============================================

✅ Windows 10/11 (64-bit)
✅ Navegador web (Chrome, Firefox, Edge)
❌ NÃO precisa de Python instalado

===============================================
    SOLUÇÃO DE PROBLEMAS:
===============================================

❌ Se o executável não abrir:
   - Execute como administrador
   - Verifique se o Windows Defender não está bloqueando

❌ Se o navegador não abrir automaticamente:
   - Acesse manualmente: http://localhost:8501

❌ Se aparecer erro de arquivo não encontrado:
   - NÃO mova arquivos individuais
   - Mantenha TODA a estrutura de pastas intacta

===============================================
    SUPORTE:
===============================================

Para suporte, entre em contato com a equipe de desenvolvimento.

Versão: 4.0
Data: 25/10/2025
Status: ✅ FUNCIONANDO
```

### 9.3 Compactar para Distribuição

```bash
# Opção 1: ZIP
# Clicar com botão direito na pasta > Enviar para > Pasta compactada

# Opção 2: PowerShell
Compress-Archive -Path "Dashboard_KE5Z_Distribuicao\*" -DestinationPath "Dashboard_KE5Z_v4.0.zip"
```

---

## 10. CHECKLIST COMPLETO

### ✅ ANTES DO EMPACOTAMENTO

- [ ] Python 3.8+ instalado
- [ ] streamlit-desktop-app instalado
- [ ] Todas as dependências instaladas (requirements.txt)
- [ ] Aplicação Streamlit funcionando (`streamlit run app.py`)
- [ ] Todos os arquivos Python usando `get_base_path()` e `get_output_path()`
- [ ] Pastas de dados existem (KE5Z, Extracoes, arquivos, pages)
- [ ] Arquivos de configuração existem (*.json, *.xlsx)
- [ ] Sistema de autenticação testado
- [ ] Todas as páginas carregando sem erros

### ✅ DURANTE O EMPACOTAMENTO

- [ ] Builds anteriores limpos (build/ e dist/ removidos)
- [ ] Comando `streamlit-desktop-app build app.py --name Dashboard_KE5Z_OFICIAL` executado
- [ ] Executável criado em `dist\Dashboard_KE5Z_OFICIAL\`
- [ ] Pasta `_internal` criada automaticamente
- [ ] Pastas de dados copiadas para `_internal\`
- [ ] Arquivos de configuração copiados para `_internal\`
- [ ] Arquivos editáveis copiados para fora do `_internal\`

### ✅ APÓS O EMPACOTAMENTO

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

### ✅ TESTES

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

### ✅ DISTRIBUIÇÃO

- [ ] Pasta de distribuição criada
- [ ] Arquivo COMO_USAR.txt incluído
- [ ] Estrutura completa copiada
- [ ] Arquivo ZIP criado (opcional)
- [ ] Testado em ambiente limpo
- [ ] Documentação atualizada

---

## 🎯 RESUMO EXECUTIVO

### Para Qualquer IA Seguir Este Guia:

**1. PREPARAÇÃO**
```bash
cd C:\user\U235107\GitHub\DashAPPwin11
pip install streamlit-desktop-app
```

**2. BUILD**
```bash
criar_executavel_funcional.bat
```

**3. VERIFICAÇÃO**
```bash
cd dist\Dashboard_KE5Z_OFICIAL
dir *.exe
dir _internal\KE5Z
dir _internal\pages
dir *.json
```

**4. TESTE**
```bash
Dashboard_KE5Z_OFICIAL.exe
```

**5. DISTRIBUIÇÃO**
```bash
xcopy "dist\Dashboard_KE5Z_OFICIAL" "Dashboard_KE5Z_Distribuicao\" /E /I /Y
```

### Estrutura Final Esperada:
```
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
```

### Regras Críticas:
1. **SEMPRE** usar `streamlit-desktop-app` para build
2. **SEMPRE** copiar dados para `_internal/`
3. **SEMPRE** manter `usuarios.json` FORA do `_internal/`
4. **SEMPRE** usar `get_base_path()` para leitura (com busca em múltiplos locais para portabilidade)
5. **SEMPRE** usar `os.path.dirname(sys.executable)` para escrita
6. **SEMPRE** chamar `ensure_working_directory()` no início do app.py
7. **SEMPRE** buscar arquivos em múltiplos locais quando no executável (portabilidade)

---

**🎉 FIM DO GUIA DEFINITIVO**

*Este guia foi criado para garantir que qualquer IA possa reproduzir exatamente o mesmo resultado de empacotamento do Dashboard KE5Z.*

*Versão: 4.2 - Definitivo e Completo com Portabilidade e Correções de Extração*  
*Data: 03/12/2025*  
*Status: ✅ TESTADO E FUNCIONANDO*  
*Atualizações:*
- ✅ Sistema funciona quando pasta é movida (portabilidade)
- ✅ Correção do erro `warn_bad_lines` no pandas (removido parâmetro descontinuado)
- ✅ Criação automática das pastas `KE5Z/` e `arquivos/` no build se não existirem
- ✅ Dados de extração salvos dentro do `_internal` (mesmo local onde são lidos)

---


