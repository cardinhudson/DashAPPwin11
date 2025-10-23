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
    <h1 style="color: white; font-size: 3rem; margin: 0;">📦 Guia de Empacotamento</h1>
    <h3 style="color: #f0f0f0; margin: 0;">Dashboard KE5Z Desktop</h3>
    <p style="color: #e0e0e0; font-size: 1.2rem; margin-top: 1rem;">
        Instruções completas para criar executáveis desktop independentes
    </p>
</div>
""", unsafe_allow_html=True)

# Índice
st.markdown("---")
st.subheader("📋 Índice")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🎯 Básico:**
    - [Pré-requisitos](#pré-requisitos)
    - [Estrutura do Projeto](#estrutura-do-projeto)
    - [Configuração de Caminhos](#configuração-de-caminhos)
    """)

with col2:
    st.markdown("""
    **🛠️ Técnico:**
    - [Processo de Empacotamento](#processo-de-empacotamento)
    - [Arquivo .spec Personalizado](#arquivo-spec-personalizado)
    - [Verificação e Testes](#verificação-e-testes)
    """)

with col3:
    st.markdown("""
    **🚀 Avançado:**
    - [Solução de Problemas](#solução-de-problemas)
    - [Distribuição](#distribuição)
    - [Checklist Completo](#checklist-completo)
    """)

# Seção 1: Pré-requisitos
st.markdown("---")
st.header("1. 📋 Pré-requisitos")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🖥️ Sistema Operacional")
    st.markdown("""
    - **Windows 10/11** (64-bit)
    - **Python 3.8+** (apenas para desenvolvimento)
    - **Git** (opcional, para controle de versão)
    - **8GB RAM** mínimo recomendado
    - **2GB espaço livre** para build
    """)

with col2:
    st.subheader("🐍 Dependências Python")
    st.code("""
# Instalar dependências principais
pip install streamlit pandas plotly pyarrow openpyxl

# Instalar ferramenta de empacotamento
pip install streamlit-desktop-app

# Dependências adicionais (se necessário)
pip install altair numpy matplotlib
    """, language="bash")

# Seção 2: Estrutura do Projeto
st.markdown("---")
st.header("2. 📁 Estrutura do Projeto")

st.markdown("""
### 🏗️ Estrutura Recomendada
```
MeuProjeto/
├── app.py                    # Aplicação principal Streamlit
├── auth_simple.py           # Sistema de autenticação
├── Extracao.py              # Script de processamento de dados
├── requirements.txt         # Dependências Python
├── Dashboard_KE5Z_Desktop.spec  # Arquivo de configuração PyInstaller
├── pages/                   # Páginas do Streamlit
│   ├── 1_Dash_Mes.py
│   ├── 2_IUD_Assistant.py
│   └── ...
├── KE5Z/                    # Dados processados
│   ├── KE5Z.parquet
│   └── KE5Z_waterfall.parquet
├── Extracoes/               # Dados brutos
│   ├── KE5Z/
│   └── KSBB/
├── arquivos/                # Arquivos Excel gerados
├── usuarios.json            # Dados de usuários
├── dados_equipe.json        # Configurações
├── Dados SAPIENS.xlsx       # Dados auxiliares
└── Fornecedores.xlsx        # Dados auxiliares
```
""")

# Seção 3: Configuração de Caminhos
st.markdown("---")
st.header("3. 🔧 Configuração de Caminhos")

st.markdown("""
### ⚠️ **CRÍTICO**: Padrão de Caminhos Relativos

**TODOS os caminhos devem ser relativos e usar `sys._MEIPASS` para detectar execução em PyInstaller.**

#### Função Padrão para Caminhos:
```python
import sys
import os

def get_base_path():
    \"\"\"Retorna o caminho base correto para LEITURA de dados\"\"\"
    if hasattr(sys, '_MEIPASS'):
        # Rodando no executável PyInstaller - apontar para _internal
        return sys._MEIPASS
    else:
        # Rodando em desenvolvimento
        return os.path.dirname(os.path.abspath(__file__))

def get_output_path():
    \"\"\"Retorna o caminho correto para ESCRITA de dados\"\"\"
    if hasattr(sys, '_MEIPASS'):
        # No executável: salvar no diretório do executável (fora do _internal)
        return os.path.dirname(sys.executable)
    else:
        # Em desenvolvimento: mesmo diretório
        return os.path.dirname(os.path.abspath(__file__))
```

#### Aplicação em Todas as Páginas:
```python
# Em pages/1_Dash_Mes.py
def load_data_optimized(arquivo_tipo="completo"):
    base_path = get_base_path()
    arquivo_waterfall = os.path.join(base_path, "KE5Z", "KE5Z_waterfall.parquet")
    
    if os.path.exists(arquivo_waterfall):
        return pd.read_parquet(arquivo_waterfall)
    else:
        # Fallback para arquivo principal
        nome_arquivo = arquivos_disponiveis.get(arquivo_tipo, "KE5Z.parquet")
        arquivo_parquet = os.path.join(base_path, "KE5Z", nome_arquivo)
        return pd.read_parquet(arquivo_parquet)
```
""")

# Seção 4: Processo de Empacotamento
st.markdown("---")
st.header("4. 🚀 Processo de Empacotamento")

tab1, tab2 = st.tabs(["Método 1: Streamlit Desktop App", "Método 2: PyInstaller Direto"])

with tab1:
    st.subheader("📦 Streamlit Desktop App (Recomendado)")
    st.code("""
# 1. Navegar para a pasta do projeto
cd C:\\caminho\\para\\seu\\projeto

# 2. Instalar ferramenta
pip install streamlit-desktop-app

# 3. Criar executável
streamlit-desktop-app build app.py --name Dashboard_KE5Z_Desktop
    """, language="bash")
    
    st.info("✅ **Vantagens:** Mais simples, configuração automática")

with tab2:
    st.subheader("🔧 PyInstaller Direto (Avançado)")
    st.code("""
# 1. Instalar PyInstaller
pip install pyinstaller

# 2. Criar executável usando arquivo .spec personalizado
pyinstaller Dashboard_KE5Z_Desktop.spec --noconfirm
    """, language="bash")
    
    st.info("✅ **Vantagens:** Controle total, configuração personalizada")

# Seção 5: Arquivo .spec Personalizado
st.markdown("---")
st.header("5. ⚙️ Arquivo .spec Personalizado")

st.markdown("""
### 📄 Criar Arquivo `Dashboard_KE5Z_Desktop.spec`

```python
# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_all, copy_metadata

# Obter caminho base
base_path = os.path.abspath('.')

# Configuração principal
a = Analysis(
    ['app.py'],
    pathex=[base_path],
    binaries=[],
    datas=[
        # Arquivos Python principais
        (os.path.join(base_path, 'app.py'), '.'),
        (os.path.join(base_path, 'auth_simple.py'), '.'),
        (os.path.join(base_path, 'Extracao.py'), '.'),
        
        # Páginas do Streamlit
        (os.path.join(base_path, 'pages'), 'pages'),
        
        # Dados e pastas
        (os.path.join(base_path, 'KE5Z'), 'KE5Z'),
        (os.path.join(base_path, 'Extracoes'), 'Extracoes'),
        (os.path.join(base_path, 'arquivos'), 'arquivos'),
        
        # Arquivos de configuração
        (os.path.join(base_path, 'usuarios.json'), '.'),
        (os.path.join(base_path, 'usuarios_padrao.json'), '.'),
        (os.path.join(base_path, 'dados_equipe.json'), '.'),
        
        # Arquivos Excel
        (os.path.join(base_path, 'Dados SAPIENS.xlsx'), '.'),
        (os.path.join(base_path, 'Fornecedores.xlsx'), '.')
    ],
    hiddenimports=[
        'altair', 'auth_simple', 'Extracao', 'base64',
        'datetime.datetime', 'gc', 'io.BytesIO', 'os',
        'pandas', 'plotly.graph_objects', 'plotly',
        'streamlit', 'sys'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# Adicionar metadados das bibliotecas
datas = a.datas
binaries = a.binaries
hiddenimports = a.hiddenimports

# Copiar metadados das bibliotecas principais
datas += copy_metadata('streamlit')
datas += copy_metadata('streamlit-desktop-app')
datas += copy_metadata('plotly')
datas += copy_metadata('altair')
datas += copy_metadata('pandas')

# Coletar todas as dependências do Streamlit
tmp_ret = collect_all('streamlit')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# Configuração do executável
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Dashboard_KE5Z_Desktop',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)
```
""")

# Seção 6: Verificação e Testes
st.markdown("---")
st.header("6. ✅ Verificação e Testes")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔍 Verificação de Arquivos")
    st.code("""
# Navegar para pasta do executável
cd dist\\Dashboard_KE5Z_Desktop

# Verificar executável principal
dir *.exe

# Verificar arquivos em _internal
dir _internal\\*.py
dir _internal\\*.xlsx
dir _internal\\KE5Z
dir _internal\\Extracoes
    """, language="bash")

with col2:
    st.subheader("🧪 Teste de Execução")
    st.code("""
# Testar execução
cd dist\\Dashboard_KE5Z_Desktop
Dashboard_KE5Z_Desktop.exe

# Ou usar script de abertura
ABRIR_DASHBOARD.bat
    """, language="bash")

st.subheader("📋 Verificação de Funcionalidades")
st.markdown("""
- ✅ **Executável inicia** sem erros
- ✅ **Sistema de login** funcionando
- ✅ **Todas as páginas** acessíveis
- ✅ **Dados carregando** corretamente
- ✅ **Extração de dados** funcionando
- ✅ **Filtros de dados** funcionando
- ✅ **Download de arquivos** funcionando
- ✅ **Navegação entre páginas** funcionando
""")

# Seção 7: Solução de Problemas
st.markdown("---")
st.header("7. 🔧 Solução de Problemas")

tab1, tab2, tab3 = st.tabs(["Erros Comuns", "Problemas de Caminhos", "Problemas de Performance"])

with tab1:
    st.subheader("❌ Erros Comuns")
    
    st.markdown("""
    **1. ModuleNotFoundError**
    ```
    Problema: Módulos Python não encontrados
    Solução: Adicionar módulo ao hiddenimports no .spec
    hiddenimports=['seu_modulo']
    ```
    
    **2. PermissionError**
    ```
    Problema: Acesso negado durante build
    Solução: Terminar processos Python
    taskkill /f /im python*
    taskkill /f /im streamlit*
    ```
    
    **3. Arquivo não encontrado**
    ```
    Problema: Arquivos de dados não encontrados
    Solução: Verificar se está usando get_base_path() corretamente
    base_path = get_base_path()
    arquivo = os.path.join(base_path, "pasta", "arquivo.parquet")
    ```
    """)

with tab2:
    st.subheader("🗂️ Problemas de Caminhos")
    
    st.markdown("""
    **1. Caminhos Absolutos**
    ```python
    # ❌ ERRADO
    arquivo = "C:\\caminho\\fixo\\arquivo.parquet"
    
    # ✅ CORRETO
    base_path = get_base_path()
    arquivo = os.path.join(base_path, "pasta", "arquivo.parquet")
    ```
    
    **2. Caminhos Relativos Incorretos**
    ```python
    # ❌ ERRADO
    arquivo = os.path.join("KE5Z", "arquivo.parquet")
    
    # ✅ CORRETO
    base_path = get_base_path()
    arquivo = os.path.join(base_path, "KE5Z", "arquivo.parquet")
    ```
    
    **3. Verificação de Existência**
    ```python
    # ✅ SEMPRE verificar se arquivo existe
    if os.path.exists(arquivo):
        df = pd.read_parquet(arquivo)
    else:
        st.error(f"Arquivo não encontrado: {arquivo}")
    ```
    """)

with tab3:
    st.subheader("⚡ Problemas de Performance")
    
    st.markdown("""
    **1. Arquivo Excel Muito Grande**
    ```python
    # Problema: ValueError: This sheet is too large!
    # Solução: Comentar linha que salva Excel completo
    # df_total_excel.to_excel("arquivo_completo.xlsx", index=False)
    ```
    
    **2. Erro de Conversão PyArrow**
    ```python
    # Problema: pyarrow.lib.ArrowInvalid
    # Solução: Converter colunas problemáticas para string
    text_columns = ['coluna1', 'coluna2', 'coluna3']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str)
    ```
    
    **3. Uso Excessivo de Memória**
    ```python
    # Solução: Usar cache inteligente
    @st.cache_data(ttl=3600, max_entries=3, persist="disk")
    def load_data_optimized():
        # Carregamento otimizado
    ```
    """)

# Seção 8: Distribuição
st.markdown("---")
st.header("8. 📦 Distribuição")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Preparação para Distribuição")
    st.code("""
# Criar pasta de distribuição
mkdir Dashboard_KE5Z_Distribuicao

# Copiar pasta do executável
xcopy dist\\Dashboard_KE5Z_Desktop Dashboard_KE5Z_Distribuicao\\ /E /I /Y

# Adicionar arquivos de documentação
echo Para executar, clique duas vezes em Dashboard_KE5Z_Desktop.exe > Dashboard_KE5Z_Distribuicao\\COMO_USAR.txt
    """, language="bash")

with col2:
    st.subheader("🚀 Script de Abertura")
    st.code("""
@echo off
chcp 65001 >nul
echo ===============================================
echo    DASHBOARD KE5Z - INICIANDO...
echo ===============================================
echo.
echo Aguarde alguns segundos para o aplicativo carregar...
echo.

start "" "Dashboard_KE5Z_Desktop.exe"

echo.
echo Aplicativo iniciado! Aguarde o navegador abrir...
echo.
echo Se o navegador não abrir automaticamente,
echo acesse: http://localhost:8501
echo.
pause
    """, language="batch")

# Seção 9: Checklist Completo
st.markdown("---")
st.header("9. ✅ Checklist Completo")

tab1, tab2, tab3 = st.tabs(["Antes do Empacotamento", "Durante o Empacotamento", "Após o Empacotamento"])

with tab1:
    st.subheader("📋 ANTES DO EMPACOTAMENTO")
    st.markdown("""
    - [ ] Aplicação Streamlit funcionando corretamente
    - [ ] Todos os caminhos usando `get_base_path()` e `get_output_path()`
    - [ ] Dependências listadas em `requirements.txt`
    - [ ] Arquivos de dados organizados e acessíveis
    - [ ] Scripts auxiliares funcionando independentemente
    - [ ] Sistema de autenticação testado
    - [ ] Todas as páginas carregando sem erros
    - [ ] Arquivo `.spec` criado com configuração correta
    """)

with tab2:
    st.subheader("🔧 DURANTE O EMPACOTAMENTO")
    st.markdown("""
    - [ ] Comando `pyinstaller` executado sem erros
    - [ ] Pasta `dist/` criada com sucesso
    - [ ] Executável gerado sem erros críticos
    - [ ] Todos os arquivos incluídos em `_internal/`
    - [ ] Processo de build completado sem interrupções
    - [ ] Logs de build sem erros fatais
    """)

with tab3:
    st.subheader("🎯 APÓS O EMPACOTAMENTO")
    st.markdown("""
    - [ ] Executável principal presente e executável
    - [ ] Arquivos Python em `_internal/`
    - [ ] Dados auxiliares em `_internal/`
    - [ ] Pastas de dados em `_internal/`
    - [ ] Arquivos de configuração na raiz (acessíveis)
    - [ ] Script de abertura criado
    - [ ] Teste em PC sem Python instalado
    - [ ] Verificação de portabilidade
    - [ ] Documentação criada
    - [ ] Instruções claras para usuário
    """)

# Seção 10: Dicas Importantes
st.markdown("---")
st.header("10. 💡 Dicas Importantes")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Caminhos Relativos")
    st.markdown("""
    - **SEMPRE** use `get_base_path()` para leitura de dados
    - **SEMPRE** use `get_output_path()` para escrita de dados
    - **NUNCA** use caminhos absolutos hardcoded
    - Teste em diferentes locais do sistema
    """)

with col2:
    st.subheader("📦 Arquivos de Dados")
    st.markdown("""
    - Mantenha dados de entrada em `_internal/` (read-only)
    - Salve dados de saída no diretório do executável (writable)
    - Use duplicação estratégica quando necessário
    - Verifique permissões de escrita
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-top: 2rem;">
    <h3 style="color: white; margin: 0;">📦 Guia de Empacotamento</h3>
    <p style="color: #f0f0f0; margin: 0.5rem 0;">
        Instruções completas para criar executáveis desktop independentes
    </p>
    <p style="color: #e0e0e0; font-size: 0.9rem; margin: 0;">
        🖥️ Funciona sem Python • ⚡ Performance otimizada • 🔄 Extração automática • 📊 8 páginas completas
    </p>
    <p style="color: #d0d0d0; font-size: 0.8rem; margin-top: 1rem;">
        💻 4.000+ linhas de código • ⚡ 68% otimização • 🖥️ Aplicação Desktop • 🔄 Extração automática • 📊 8 páginas completas • 🎯 Guia completo de empacotamento
    </p>
</div>
""", unsafe_allow_html=True)

# Informações do sistema
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"🕒 **Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

with col2:
    st.success("✅ **Status:** Guia Atualizado")

with col3:
    st.info("🔧 **Versão:** Baseado no Projeto Real")
