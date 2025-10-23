import streamlit as st
import sys
import os
import json
import base64
from datetime import datetime

# Adicionar diretório pai ao path para importar auth_simple
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth_simple import verificar_autenticacao, exibir_header_usuario

# Função para detectar caminho base correto
def get_base_path():
    """Retorna o caminho base correto para LEITURA de dados"""
    if hasattr(sys, '_MEIPASS'):
        # Rodando no executável PyInstaller - apontar para _internal
        return sys._MEIPASS
    else:
        # Rodando em desenvolvimento
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Funções para persistir dados da equipe
def salvar_dados_equipe(dados):
    """Salva os dados da equipe em arquivo JSON"""
    try:
        base_path = get_base_path()
        dados_path = os.path.join(base_path, 'dados_equipe.json')
        with open(dados_path, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")
        return False

def carregar_dados_equipe():
    """Carrega os dados da equipe do arquivo JSON"""
    try:
        base_path = get_base_path()
        dados_path = os.path.join(base_path, 'dados_equipe.json')
        if os.path.exists(dados_path):
            with open(dados_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Aviso ao carregar dados: {e}")
    
    # Retorna estrutura vazia se não conseguir carregar
    return {
        'hudson': {
            'cargo': '',
            'empresa': '',
            'experiencia': '',
            'linkedin': '',
            'foto': None
        },
        'lauro': {
            'cargo': '',
            'empresa': '',
            'experiencia': '',
            'linkedin': '',
            'foto': None
        }
    }

def salvar_foto_base64(foto_bytes, nome_arquivo):
    """Converte foto para base64 para salvar no JSON"""
    try:
        return base64.b64encode(foto_bytes).decode('utf-8')
    except:
        return None

def carregar_foto_base64(foto_base64):
    """Converte base64 de volta para bytes"""
    try:
        return base64.b64decode(foto_base64)
    except:
        return None

# Configuração da página
st.set_page_config(
    page_title="Sobre o Projeto - Dashboard KE5Z",
    page_icon="🎯",
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

# Título principal com estilo
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;">
    <h1 style="color: white; font-size: 3rem; margin: 0;">🎯 Dashboard KE5Z</h1>
    <h3 style="color: #f0f0f0; margin: 0;">Aplicação Desktop Completa</h3>
    <p style="color: #e0e0e0; font-size: 1.2rem; margin-top: 1rem;">
        Executável independente para análise de dados SAP com extração automática e otimizações avançadas
    </p>
    <p style="color: #d0d0d0; font-size: 1rem; margin-top: 0.5rem;">
        🖥️ Funciona sem Python instalado • ⚡ Performance otimizada • 🔄 Extração automática • 📊 7 páginas completas
    </p>
</div>
""", unsafe_allow_html=True)

# Descrição principal do projeto
st.markdown("""
<div style="text-align: center; padding: 1.5rem; background: rgba(255, 255, 255, 0.05); border-radius: 10px; margin: 1rem 0;">
    <h4 style="color: #333; margin: 0; font-weight: 600;">
        Aplicação Desktop completa com extração automática de dados
    </h4>
    <p style="color: #666; margin: 0.5rem 0; font-size: 1.1rem;">
        Desenvolvido como executável independente para máxima portabilidade e performance
    </p>
</div>
""", unsafe_allow_html=True)

# Métricas principais - Movidas para o início
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💻 Linhas de Código", "4.000+", "Sistema completo")

with col2:
    st.metric("⚡ Otimização", "68%", "Memória reduzida")

with col3:
    st.metric("📊 Páginas", "9", "Funcionalidades completas")

with col4:
    st.metric("🖥️ Aplicação", "Desktop", "Executável independente")

# Objetivos do Projeto - Movidos para o início
st.markdown("---")
st.subheader("🎯 Objetivos do Projeto")

st.markdown("""
**🎯 Objetivos do Projeto:**
- 📈 **Análise avançada de dados financeiros** com visualizações interativas
- ⚡ **Performance otimizada** para grandes volumes (68% redução de memória)
- 🔐 **Sistema de autenticação robusto** com administração de usuários
- 📱 **Interface responsiva** e intuitiva com 7 páginas funcionais
- 🖥️ **Aplicação Desktop independente:** Executável que funciona em qualquer PC Windows 10/11
- 🔄 **Extração automática de dados:** Processamento inteligente de arquivos TXT para Parquet otimizado
- 📊 **Dashboards especializados:** Mensal, Total Accounts, Waterfall Analysis
- 🤖 **Assistente inteligente:** IUD Assistant para análises conversacionais
- 📥 **Extração de dados:** Interface completa para processamento de arquivos
- 👑 **Administração:** Gerenciamento completo de usuários
- 📦 **Transformação inteligente:** Conversão TXT → Parquet (até 10x menor)
- 🚀 **Portabilidade total:** Aplicação completa em uma única pasta, sem Python
""")

# Desafio Principal do Projeto
st.markdown("---")
st.header("⚠️ Desafio Principal & Soluções")

st.markdown("""
<div style="padding: 1.5rem; background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); border-radius: 10px; margin: 1rem 0; color: white;">
    <h4 style="color: white; margin: 0; font-weight: 600;">
        📊 PROBLEMA CRÍTICO: Dados grandes causando instabilidade
    </h4>
    <p style="margin: 0.5rem 0; font-size: 1.1rem;">
        Dados originais com 3+ milhões de registros causavam problemas de performance e estabilidade
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Problemas Identificados")
    st.markdown("""
    - **📁 Arquivo KE5Z.parquet:** 3+ milhões de linhas
    - **💾 Uso de memória:** Excedia limites de processamento
    - **❌ Instabilidade:** Sistema lento e instável
    - **🐌 Downloads grandes:** Causavam timeouts e crashes
    - **🔄 Performance:** Experiência do usuário comprometida
    """)

with col2:
    st.subheader("✅ Soluções Implementadas")
    st.markdown("""
    - **📊 Separação de dados:** main/others/waterfall
    - **⚡ Redução de 68%:** Arquivo waterfall otimizado
    - **🖥️ Aplicação Desktop:** Executável independente
    - **🔄 Extração automática:** Processamento inteligente de dados
    - **💾 Cache otimizado:** TTL e persistência em disco
    - **🎯 Filtros consistentes:** Mesma fonte tabela/Excel
    - **🚀 Portabilidade total:** Funciona em qualquer PC Windows 11
    """)

st.info("🎆 **Resultado Final:** Aplicação Desktop 100% estável com performance otimizada e portabilidade total!")

# Seção da Equipe
st.markdown("---")
st.header("👥 Equipe do Projeto")

# Carregar dados salvos
dados_equipe = carregar_dados_equipe()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔧 Hudson Cardin")
    
    # Upload de foto para Hudson
    foto_hudson = st.file_uploader(
        "📸 Upload da foto do Hudson",
        type=['png', 'jpg', 'jpeg'],
        key="foto_hudson",
        help="Faça upload de uma foto do perfil do Hudson (formato: PNG, JPG, JPEG)"
    )
    
    # Mostrar foto salva ou nova foto
    if foto_hudson is not None:
        st.image(foto_hudson, width=200, caption="Hudson Cardin")
        # Salvar nova foto
        dados_equipe['hudson']['foto'] = salvar_foto_base64(foto_hudson.read(), "hudson.jpg")
    elif dados_equipe['hudson']['foto']:
        # Mostrar foto salva
        foto_bytes = carregar_foto_base64(dados_equipe['hudson']['foto'])
        if foto_bytes:
            st.image(foto_bytes, width=200, caption="Hudson Cardin")
        else:
            st.info("👤 Aguardando upload da foto")
    else:
        st.info("👤 Aguardando upload da foto")
    
    # Campos para informações do Hudson
    st.markdown("**📋 Informações Profissionais:**")
    
    with st.expander("✏️ Editar informações do Hudson", expanded=False):
        with st.form("form_hudson"):
            cargo_hudson = st.text_input(
                "💼 Cargo atual:", 
                value=dados_equipe['hudson']['cargo'],
                placeholder="Ex: Analista de Sistemas", 
                key="cargo_hudson"
            )
            empresa_hudson = st.text_input(
                "🏢 Empresa:", 
                value=dados_equipe['hudson']['empresa'],
                placeholder="Ex: Empresa XYZ", 
                key="empresa_hudson"
            )
            experiencia_hudson = st.text_area(
                "🎯 Experiência:", 
                value=dados_equipe['hudson']['experiencia'],
                placeholder="Descreva a experiência profissional...", 
                key="exp_hudson"
            )
            linkedin_hudson = st.text_input(
                "🔗 LinkedIn:", 
                value=dados_equipe['hudson']['linkedin'],
                placeholder="https://linkedin.com/in/hudson-cardin", 
                key="linkedin_hudson"
            )
            
            if st.form_submit_button("💾 Salvar informações do Hudson", use_container_width=True):
                dados_equipe['hudson']['cargo'] = cargo_hudson
                dados_equipe['hudson']['empresa'] = empresa_hudson
                dados_equipe['hudson']['experiencia'] = experiencia_hudson
                dados_equipe['hudson']['linkedin'] = linkedin_hudson
                
                if salvar_dados_equipe(dados_equipe):
                    st.success("✅ Informações do Hudson salvas com sucesso!")
                    st.rerun()
    
    # Expander para perfil profissional (igual à imagem)
    with st.expander("👨‍💻 Perfil Profissional", expanded=False):
        if dados_equipe['hudson']['cargo'] and dados_equipe['hudson']['empresa']:
            st.write(f"💼 **{dados_equipe['hudson']['cargo']}** na **{dados_equipe['hudson']['empresa']}**")
        elif dados_equipe['hudson']['cargo']:
            st.write(f"💼 **{dados_equipe['hudson']['cargo']}**")
        elif dados_equipe['hudson']['empresa']:
            st.write(f"🏢 **{dados_equipe['hudson']['empresa']}**")
        else:
            st.write("💼 *Cargo não informado*")
        
        if dados_equipe['hudson']['experiencia']:
            st.write(f"🎯 {dados_equipe['hudson']['experiencia']}")
        else:
            st.write("🎯 *Experiência não informada*")
        
        if dados_equipe['hudson']['linkedin']:
            st.markdown(f"🔗 [Perfil no LinkedIn]({dados_equipe['hudson']['linkedin']})")
        else:
            st.write("🔗 *LinkedIn não informado*")

with col2:
    st.subheader("📊 Lauro Paiva Junior")
    
    # Upload de foto para Lauro
    foto_lauro = st.file_uploader(
        "📸 Upload da foto do Lauro",
        type=['png', 'jpg', 'jpeg'],
        key="foto_lauro",
        help="Faça upload de uma foto do perfil do Lauro (formato: PNG, JPG, JPEG)"
    )
    
    # Mostrar foto salva ou nova foto
    if foto_lauro is not None:
        st.image(foto_lauro, width=200, caption="Lauro Paiva Junior")
        # Salvar nova foto
        dados_equipe['lauro']['foto'] = salvar_foto_base64(foto_lauro.read(), "lauro.jpg")
    elif dados_equipe['lauro']['foto']:
        # Mostrar foto salva
        foto_bytes = carregar_foto_base64(dados_equipe['lauro']['foto'])
        if foto_bytes:
            st.image(foto_bytes, width=200, caption="Lauro Paiva Junior")
        else:
            st.info("👤 Aguardando upload da foto")
    else:
        st.info("👤 Aguardando upload da foto")
    
    # Campos para informações do Lauro
    st.markdown("**📋 Informações Profissionais:**")
    
    with st.expander("✏️ Editar informações do Lauro", expanded=False):
        with st.form("form_lauro"):
            cargo_lauro = st.text_input(
                "💼 Cargo atual:", 
                value=dados_equipe['lauro']['cargo'],
                placeholder="Ex: Analista Financeiro", 
                key="cargo_lauro"
            )
            empresa_lauro = st.text_input(
                "🏢 Empresa:", 
                value=dados_equipe['lauro']['empresa'],
                placeholder="Ex: Empresa ABC", 
                key="empresa_lauro"
            )
            experiencia_lauro = st.text_area(
                "🎯 Experiência:", 
                value=dados_equipe['lauro']['experiencia'],
                placeholder="Descreva a experiência profissional...", 
                key="exp_lauro"
            )
            linkedin_lauro = st.text_input(
                "🔗 LinkedIn:", 
                value=dados_equipe['lauro']['linkedin'],
                placeholder="https://linkedin.com/in/lauro-paiva", 
                key="linkedin_lauro"
            )
            
            if st.form_submit_button("💾 Salvar informações do Lauro", use_container_width=True):
                dados_equipe['lauro']['cargo'] = cargo_lauro
                dados_equipe['lauro']['empresa'] = empresa_lauro
                dados_equipe['lauro']['experiencia'] = experiencia_lauro
                dados_equipe['lauro']['linkedin'] = linkedin_lauro
                
                if salvar_dados_equipe(dados_equipe):
                    st.success("✅ Informações do Lauro salvas com sucesso!")
                    st.rerun()
    
    # Expander para perfil profissional (igual à imagem)
    with st.expander("👨‍💼 Perfil Profissional", expanded=False):
        if dados_equipe['lauro']['cargo'] and dados_equipe['lauro']['empresa']:
            st.write(f"💼 **{dados_equipe['lauro']['cargo']}** na **{dados_equipe['lauro']['empresa']}**")
        elif dados_equipe['lauro']['cargo']:
            st.write(f"💼 **{dados_equipe['lauro']['cargo']}**")
        elif dados_equipe['lauro']['empresa']:
            st.write(f"🏢 **{dados_equipe['lauro']['empresa']}**")
        else:
            st.write("💼 *Cargo não informado*")
        
        if dados_equipe['lauro']['experiencia']:
            st.write(f"🎯 {dados_equipe['lauro']['experiencia']}")
        else:
            st.write("🎯 *Experiência não informada*")
        
        if dados_equipe['lauro']['linkedin']:
            st.markdown(f"🔗 [Perfil no LinkedIn]({dados_equipe['lauro']['linkedin']})")
        else:
            st.write("🔗 *LinkedIn não informado*")

# Métricas principais
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Páginas de Análise", 
        value="7",
        delta="Completas"
    )

with col2:
    st.metric(
        label="⚡ Otimização Waterfall", 
        value="68%",
        delta="Menor uso de memória"
    )

with col3:
    # Contar usuários
    try:
        base_path = get_base_path()
        usuarios_path = os.path.join(base_path, 'usuarios.json')
        if os.path.exists(usuarios_path):
            with open(usuarios_path, 'r') as f:
                usuarios = json.load(f)
            total_usuarios = len(usuarios)
        else:
            total_usuarios = 2
    except:
        total_usuarios = 2
    
    st.metric(
        label="👥 Usuários Cadastrados", 
        value=total_usuarios,
        delta="Sistema completo"
    )

with col4:
    # Contar arquivos Python
    base_path = get_base_path()
    arquivos_py = len([f for f in os.listdir(base_path) if f.endswith('.py')])
    
    # Contar arquivos Python na pasta pages
    pages_path = os.path.join(base_path, 'pages')
    if os.path.exists(pages_path):
        arquivos_py += len([f for f in os.listdir(pages_path) if f.endswith('.py')])
    
    st.metric(
        label="🐍 Arquivos Python", 
        value=arquivos_py,
        delta="Linhas de código"
    )

st.markdown("---")

# Seções principais com expanderes
st.subheader("🚀 Funcionalidades Principais")

# Funcionalidades em colunas
col1, col2 = st.columns(2)

with col1:
    with st.expander("📊 **DASHBOARDS INTERATIVOS**", expanded=True):
        st.markdown("""
        ### 📅 Dashboard Mensal (1_Dash_Mes.py)
        - **Análise focada** em um período específico
        - **Filtro de período** simplificado e funcional
        - **Gráficos otimizados** com dados waterfall
        - **Performance superior** para análises detalhadas
        - **Download inteligente** com limites de segurança
        - **🛡️ Proteção Cloud:** 50.000 linhas máximo
        - **💻 Modo Local:** Até 1M+ linhas (limite Excel)
        - **✅ Filtros garantidos** no download Excel
        
        ### 📊 Total Accounts (3_Total_accounts.py)
        - **Análise completa** do centro de lucro 02S
        - **100% otimizado** com dados waterfall
        - **Gráficos Type 05 e Type 06** com cores padronizadas
        - **Tabelas dinâmicas** por USI e conta contábil
        - **Interface limpa** sem mensagens de debug
        
        ### 🌊 Waterfall Analysis (4_Waterfall_Analysis.py)
        - **Análise de cascata** entre períodos
        - **Visualização de variações** mês a mês
        - **Identificação de trends** e padrões
        - **100% dados waterfall** para performance máxima
        """)

    with st.expander("🔍 **ANÁLISES AVANÇADAS**", expanded=False):
        st.markdown("""
        ### 🤖 IUD Assistant (2_IUD_Assistant.py)
        - **Interactive User Dashboard** - Dashboard Interativo do Usuário
        - **Assistente inteligente** para análise de dados
        - **Gráficos automáticos** baseados em consultas
        - **Análise de correlações** e insights
        - **Interface conversacional** para exploração
        - **🤖 Chat inteligente** com processamento local
        - **🌊 Análise Waterfall** configurável
        
        ### 📥 Extração de Dados (6_Extracao_Dados.py)
        - **Interface completa** para processamento de arquivos
        - **Upload de arquivos** TXT, CSV, Excel
        - **Processamento automático** com logs detalhados
        - **Geração de arquivos** Parquet otimizados
        - **Monitoramento** de progresso em tempo real
        - **Validação** de dados e tratamento de erros
        
        ### 📦 Guia de Empacotamento (8_Guia_Empacotamento.py)
        - **Instruções completas** para criar executáveis
        - **Pré-requisitos** e configuração de ambiente
        - **Processo passo-a-passo** de empacotamento
        - **Solução de problemas** comuns
        - **Checklist completo** de verificação
        - **Dicas avançadas** para distribuição
        """)

with col2:
    with st.expander("⚡ **OTIMIZAÇÕES DE PERFORMANCE**", expanded=True):
        st.markdown("""
        ### 🌊 Sistema Waterfall
        - **Arquivo otimizado:** `KE5Z_waterfall.parquet`
        - **68% menor** que arquivo original
        - **Colunas essenciais:** Período, Valor, USI, Types, Fornecedor
        - **Compressão inteligente** com tipos categóricos
        
        ### 📦 Transformação TXT → Parquet
        - **Conversão automática:** Arquivos TXT grandes → Parquet otimizado
        - **Redução de tamanho:** Até **10x menor** que arquivos originais
        - **Performance:** **5-10x mais rápido** para carregar e processar
        - **Exemplos de redução:**
          • Arquivo TXT 500MB → Parquet 50MB (**10x menor**)
          • Arquivo TXT 1GB → Parquet 100MB (**10x menor**)
          • Arquivo TXT 2GB → Parquet 200MB (**10x menor**)
        - **Benefícios:** Menor uso de memória, carregamento instantâneo, compatibilidade total
        
        ### 💾 Gestão de Memória
        - **Cache inteligente** com TTL configurável
        - **Persistência em disco** para dados críticos
        - **Detecção automática** de ambiente (Cloud/Local)
        - **Fallbacks seguros** para compatibilidade
        
        ### 🚀 Modo Cloud vs Completo
        - **Modo Cloud:** Dados otimizados, performance máxima
        - **Modo Completo:** Acesso total, ideal para desenvolvimento
        - **Seleção centralizada** no login
        - **Aplicação automática** em todas as páginas
        
        ### 🛡️ Segurança de Downloads
        - **☁️ Streamlit Cloud:** Limite 50.000 linhas
        - **💻 Modo Local:** Até 1.048.576 linhas (Excel)
        - **Verificação preventiva** antes do download
        - **Bloqueio automático** para proteção do Cloud
        - **Sugestões inteligentes** para otimizar filtros
        - **Dados consistentes** - mesma fonte da tabela
        
        ### ⚠️ Desafio Principal do Projeto
        - **📊 Problema:** Streamlit Cloud derruba o site por uso excessivo de memória
        - **📁 Dados originais:** 3+ milhões de registros causavam erro "Oh no."
        - **🔧 Soluções implementadas:**
          • Separação de arquivos (main/others/waterfall)
          • Limites inteligentes por ambiente
          • Cache otimizado com TTL
          • Compressão de tipos de dados
          • Filtros preventivos
          • Monitoramento de memória
        - **✅ Resultado:** 68% de redução de memória, sistema estável
        """)

    with st.expander("🔐 **SISTEMA DE AUTENTICAÇÃO**", expanded=False):
        st.markdown("""
        ### 👑 Administração de Usuários (5_Admin_Usuarios.py)
        - **Cadastro de usuários** via interface web
        - **Exclusão segura** com confirmação obrigatória
        - **Tipos de usuário:** Administrador e Usuário
        - **Estatísticas** e análise de usuários
        - **Edição de perfis** e permissões
        - **Histórico de atividades** dos usuários
        
        ### 🔒 Segurança
        - **Hash SHA-256** para senhas
        - **Proteção do admin** principal
        - **Validações completas** de entrada
        - **Sessões persistentes** com logout seguro
        - **Controle de acesso** por página
        """)

st.markdown("---")

# Seção técnica
st.subheader("🛠️ Aspectos Técnicos")

col1, col2 = st.columns(2)

with col1:
    with st.expander("📁 **ARQUITETURA DO PROJETO**", expanded=False):
        st.markdown("""
        ### 🏗️ Estrutura de Arquivos
        ```
        📦 Dashboard_KE5Z_Desktop/ (Aplicação Desktop Completa)
        ├── 🖥️ Dashboard_KE5Z_Desktop.exe (Executável)
        ├── 🏠 app.py (Principal)
        ├── 🔐 auth_simple.py (Autenticação)
        ├── 🔄 Extracao.py (Processamento)
        ├── 📂 pages/ (Páginas do Dashboard)
        │   ├── 📅 1_Dash_Mes.py (Dashboard Mensal)
        │   ├── 🤖 2_IUD_Assistant.py (Assistente IA)
        │   ├── 📊 3_Total_accounts.py (Total Accounts)
        │   ├── 🌊 4_Waterfall_Analysis.py (Análise Waterfall)
        │   ├── 👑 5_Admin_Usuarios.py (Admin Usuários)
        │   ├── 📥 6_Extracao_Dados.py (Extração Dados)
        │   ├── ℹ️ 7_Sobre_Projeto.py (Sobre Projeto)
        │   └── 📦 8_Guia_Empacotamento.py (Guia Empacotamento)
        ├── 📂 _internal/ (Arquivos Internos PyInstaller)
        │   ├── 📂 KE5Z/ (Dados Gerados)
        │   │   ├── KE5Z.parquet (Original)
        │   │   ├── KE5Z_main.parquet (Otimizado)
        │   │   ├── KE5Z_others.parquet (Separado)
        │   │   └── KE5Z_waterfall.parquet (68% menor)
        │   └── 📂 Extracoes/ (Dados de Entrada)
        │       ├── KE5Z/ (Arquivos .txt)
        │       └── KSBB/ (Arquivos .txt)
        ├── 📂 arquivos/ (Excel Específicos)
        ├── 📄 Dados SAPIENS.xlsx
        ├── 📄 Fornecedores.xlsx
        └── 📄 usuarios.json
        ```
        
        ### 🔧 Tecnologias Utilizadas
        - **Streamlit:** Framework web interativo
        - **Pandas:** Manipulação de dados avançada
        - **Altair & Plotly:** Visualizações interativas
        - **PyArrow:** Performance com Parquet
        - **OpenPyXL:** Exportação Excel
        """)

    with st.expander("⚙️ **SCRIPTS DE AUTOMAÇÃO**", expanded=False):
        st.markdown("""
        ### 🚀 Aplicação Desktop
        
        **🖥️ `Dashboard_KE5Z.exe`** (Executável Principal)
        ```batch
        # Aplicação desktop independente
        # Não requer instalação de Python
        # Funciona em qualquer PC Windows 11
        # Interface web integrada
        # Extração automática de dados
        ```
        
        **📂 Estrutura Portátil**
        ```batch
        # Pasta "1 - APP" contém tudo
        # Executável + Dados + Dependências
        # Copiar pasta = Instalar aplicação
        # Zero configuração necessária
        ```
        
        **📜 `Extração.py`** (Processamento)
        ```python
        # Leitura de múltiplos formatos (TXT, CSV, Excel)
        # Merge inteligente com dados SAPIENS
        # Geração de 4 arquivos otimizados
        # Logs detalhados de progresso
        # Tratamento robusto de erros
        ```
        """)

with col2:
    with st.expander("🎨 **INTERFACE E UX**", expanded=False):
        st.markdown("""
        ### 🎯 Design Responsivo
        - **Layout wide** para máximo aproveitamento
        - **Sidebar otimizada** com navegação clara
        - **Cores padronizadas** em todos os gráficos
        - **Indicadores visuais** de otimização (⚡)
        
        ### 📱 Experiência do Usuário
        - **Filtros padronizados** em todas as páginas
        - **Cache inteligente** para performance
        - **Feedback visual** em tempo real
        - **Navegação intuitiva** entre páginas
        
        ### 🎨 Elementos Visuais
        - **Gráficos coloridos** com esquema consistente
        - **Tabelas formatadas** com moeda brasileira
        - **Progress bars** para operações longas
        - **Status indicators** para estado do sistema
        """)

    with st.expander("📈 **ANÁLISES DISPONÍVEIS**", expanded=False):
        st.markdown("""
        ### 📊 Tipos de Gráficos
        - **Gráficos de barras** por período e categorias
        - **Análise waterfall** de variações
        - **Gráficos de pizza** para distribuições
        - **Tabelas dinâmicas** com pivot tables
        
        ### 🔍 Filtros e Dimensões
        - **11 filtros principais:** USI, Período, Centro cst, etc.
        - **4 filtros avançados:** Oficina, Usuário, etc.
        - **Filtros específicos Type 07:** Type 05, Type 06, Período, Top N
        - **Filtros em cascata** com dependências
        - **Cache otimizado** para performance
        - **Filtros inteligentes:** Apenas valores diferentes de zero
        
        ### 📥 Exportações
        - **Excel formatado** com múltiplas opções
        - **Dados filtrados** ou completos
        - **Tratamento de limites** do Excel
        - **Nomes inteligentes** de arquivos
        
        ### 🔄 Extração Automática de Dados
        - **Processamento inteligente** de arquivos TXT grandes
        - **Conversão automática** para formato Parquet otimizado
        - **Redução de tamanho** até 10x menor que arquivos originais
        - **Performance superior** para carregamento e processamento
        - **Merge automático** com dados SAPIENS e Fornecedores
        - **Geração de 4 arquivos** otimizados (main, others, waterfall, completo)
        - **Logs detalhados** de progresso e estatísticas
        - **Tratamento robusto** de erros e validações
        """)

st.markdown("---")

# Seção de estatísticas do sistema
st.subheader("📊 Estatísticas do Sistema")

col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("💾 **DADOS E PERFORMANCE**", expanded=True):
        # Verificar arquivos de dados
        arquivos_dados = []
        pasta_ke5z = "KE5Z"
        
        if os.path.exists(pasta_ke5z):
            for arquivo in os.listdir(pasta_ke5z):
                if arquivo.endswith('.parquet'):
                    caminho = os.path.join(pasta_ke5z, arquivo)
                    try:
                        tamanho_mb = os.path.getsize(caminho) / (1024 * 1024)
                        arquivos_dados.append(f"📁 {arquivo}: {tamanho_mb:.1f} MB")
                    except:
                        arquivos_dados.append(f"📁 {arquivo}: Disponível")
        
        if arquivos_dados:
            st.success("✅ **Arquivos de Dados:**")
            for arquivo in arquivos_dados:
                st.write(arquivo)
        else:
            st.info("📭 Execute a extração para gerar dados")

with col2:
    with st.expander("👥 **USUÁRIOS DO SISTEMA**", expanded=True):
        try:
            if os.path.exists('usuarios.json'):
                with open('usuarios.json', 'r') as f:
                    usuarios = json.load(f)
                
                st.success(f"✅ **{len(usuarios)} Usuários Cadastrados:**")
                
                for usuario, dados in usuarios.items():
                    tipo_icon = "👑" if dados.get('tipo') == 'administrador' else "👥"
                    tipo_text = "Admin" if dados.get('tipo') == 'administrador' else "User"
                    st.write(f"{tipo_icon} **{usuario}** ({tipo_text})")
            else:
                st.info("📭 Sistema de usuários em configuração")
        except:
            st.warning("⚠️ Erro ao carregar usuários")

with col3:
    with st.expander("🔧 **TECNOLOGIAS**", expanded=True):
        st.success("✅ **Stack Tecnológico:**")
        
        tecnologias = [
            "🐍 Python 3.11+",
            "🌊 Streamlit (Web Framework)",
            "🐼 Pandas (Análise de Dados)",
            "📊 Altair (Gráficos)",
            "📈 Plotly (Visualizações)",
            "💾 PyArrow (Parquet)",
            "📋 OpenPyXL (Excel)",
            "🔐 Hashlib (Segurança)"
        ]
        
        for tech in tecnologias:
            st.write(tech)

st.markdown("---")

# Seção de complexidade técnica
st.subheader("🏆 Complexidade e Valor Técnico")

with st.expander("💻 **CÓDIGO E DESENVOLVIMENTO**", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📝 Estatísticas de Código
        
        **🎯 Principais Arquivos:**
        - **app.py:** ~730 linhas (Dashboard principal)
        - **Extração.py:** ~610 linhas (Processamento)
        - **auth_simple.py:** ~450 linhas (Autenticação)
        - **Dash_Mes.py:** ~800 linhas (Dashboard mensal)
        - **Total accounts.py:** ~550 linhas (Análise total)
        - **Waterfall_Analysis.py:** ~400 linhas (Análise cascata)
        - **IUD_Assistant.py:** ~500 linhas (Assistente IA)
        
        **📊 Total Estimado:** ~3.500+ linhas de código
        
        **🔧 Funcionalidades Implementadas:**
        - Sistema de cache multi-nível
        - Otimização automática de tipos de dados
        - Detecção de ambiente (Cloud/Local)
        - Tratamento robusto de erros
        - Logging detalhado de operações
        - Análise Type 07 com filtros específicos
        - Filtros inteligentes para valores não-zero
        - Interface limpa sem mensagens de debug
        - Top N dinâmico para análises
        - Tabelas pivot otimizadas
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Inovações Técnicas
        
        **⚡ Otimização Waterfall:**
        ```python
        # Redução de 68% no uso de memória
        df_waterfall = df[colunas_essenciais].copy()
        
        # Otimização automática de tipos
        for col in df.columns:
            if unique_ratio < 0.5:
                df[col] = df[col].astype('category')
        ```
        
        **🔄 Cache Inteligente:**
        ```python
        @st.cache_data(
            ttl=3600,
            max_entries=3,
            persist="disk"
        )
        def load_data_optimized():
            # Carregamento otimizado
        ```
        
        **🎯 Filtros Dinâmicos:**
        ```python
        # Sistema de filtros em cascata
        # Aplicação automática em waterfall
        # Cache de opções para performance
        # Filtros específicos Type 07
        # Top N dinâmico (10, 15, 20, 30, 50, 100)
        ```
        
        **📊 Tabelas Inteligentes:**
        ```python
        # Filtragem automática de valores zero
        # Tabelas pivot otimizadas
        # Formatação monetária brasileira
        # Exportação Excel inteligente
        ```
        """)

with st.expander("📊 **ARQUITETURA DE DADOS**", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🗄️ Estratégia de Dados
        
        **📁 Arquivo Original:**
        - `KE5Z.parquet` (~3M registros)
        - Todas as colunas e dados
        - Uso: Backup e dados completos
        
        **⚡ Arquivos Otimizados:**
        - `KE5Z_main.parquet` (sem Others)
        - `KE5Z_others.parquet` (apenas Others)
        - `KE5Z_waterfall.parquet` (68% menor)
        
        **🎯 Uso Inteligente:**
        - **Gráficos:** Dados waterfall (rápido)
        - **Tabelas:** Dados originais (completo)
        - **Downloads:** Dados filtrados (relevante)
        """)
    
    with col2:
        st.markdown("""
        ### 🔄 Fluxo de Processamento
        
        **1. 📥 Extração:**
        ```
        TXT/CSV → Pandas → Validação → Merge
        ```
        
        **2. 🔧 Otimização:**
        ```
        Dados → Separação → Waterfall → Cache
        ```
        
        **3. 📊 Visualização:**
        ```
        Cache → Filtros → Gráficos → Interface
        ```
        
        **4. 📥 Exportação:**
        ```
        Filtros → Excel → Download → Limpeza
        ```
        """)

with st.expander("🎨 **INTERFACE E DESIGN**", expanded=False):
    st.markdown("""
    ### 🎯 Princípios de Design
    
    **📱 Responsividade:**
    - Layout wide para máximo aproveitamento
    - Colunas adaptáveis para diferentes telas
    - Sidebar otimizada para navegação
    - Componentes escaláveis
    
    **🎨 Consistência Visual:**
    - Esquema de cores padronizado (redyellowgreen)
    - Ícones consistentes em todas as páginas
    - Tipografia uniforme e legível
    - Espaçamento harmonioso
    
    **⚡ Indicadores de Performance:**
    - Símbolo ⚡ para gráficos otimizados
    - Status de carregamento em tempo real
    - Métricas de memória e performance
    - Feedback visual para operações
    
    **🔍 Usabilidade:**
    - Filtros agrupados logicamente
    - Expanderes para organização
    - Tooltips explicativos
    - Navegação intuitiva
    """)

st.markdown("---")

# Seção de reconhecimentos
st.subheader("🏆 Valor e Impacto do Projeto")

col1, col2 = st.columns(2)

with col1:
    with st.expander("💼 **VALOR EMPRESARIAL**", expanded=True):
        st.markdown("""
        ### 📈 Benefícios Quantificáveis
        
        **⚡ Performance:**
        - **68% redução** no uso de memória
        - **3x mais rápido** para carregar gráficos
        - **Compatível** com Streamlit Cloud
        - **Escalável** para milhões de registros
        
        **💰 Economia de Recursos:**
        - Redução de custos de infraestrutura
        - Menor uso de banda e storage
        - Performance otimizada em qualquer ambiente
        - Manutenção simplificada
        
        **👥 Produtividade:**
        - Interface intuitiva para qualquer usuário
        - Análises complexas em poucos cliques
        - Exportações automáticas
        - Sistema de usuários robusto
        """)

with col2:
    with st.expander("🔬 **INOVAÇÃO TÉCNICA**", expanded=True):
        st.markdown("""
        ### 🚀 Soluções Inovadoras
        
        **🧠 Estratégia Híbrida:**
        - Gráficos usam dados otimizados (speed)
        - Tabelas usam dados completos (accuracy)
        - Downloads usam dados filtrados (relevance)
        
        **🔄 Cache Multi-Nível:**
        - Cache de dados por TTL
        - Cache de filtros por performance
        - Persistência em disco
        - Invalidação inteligente
        
        **🎯 Detecção de Ambiente:**
        - Adaptação automática Cloud/Local
        - Fallbacks seguros
        - Otimizações específicas por ambiente
        - Configuração zero para usuário final
        """)

# Footer com informações do sistema
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"🕒 **Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

with col2:
    st.success("✅ **Status:** Sistema Operacional")

with col3:
    st.info("🔧 **Versão:** Otimizada com Waterfall")

# Seção de código-fonte
st.markdown("---")
st.subheader("💻 Código-Fonte Principal")

with st.expander("🔧 **EXTRACAO.PY** - Engine de Processamento de Dados", expanded=False):
    st.markdown("### 📊 Responsável por processar 3+ milhões de registros e gerar 4 arquivos otimizados")
    
    try:
        with open('Extracao.py', 'r', encoding='utf-8') as f:
            codigo_extracao = f.read()
        
        # Mostrar estatísticas do arquivo
        linhas = len(codigo_extracao.split('\n'))
        caracteres = len(codigo_extracao)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📝 Linhas", linhas)
        with col2:
            st.metric("📄 Caracteres", f"{caracteres:,}")
        with col3:
            st.metric("🔧 Complexidade", "Alta")
        
        st.markdown("**🎯 Principais Funcionalidades:**")
        st.markdown("""
        - 📥 Leitura de múltiplos formatos (TXT, CSV, Excel)
        - 🔄 Merge inteligente com dados SAPIENS
        - ⚡ Geração de arquivo waterfall (68% menor)
        - 📊 Separação automática (main/others)
        - 🗂️ Tratamento robusto de erros
        - 📋 Logs detalhados de progresso
        """)
        
        st.code(codigo_extracao, language='python')
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar Extracao.py: {e}")

with st.expander("🏠 **DASHBOARD_MAIN.PY** - Dashboard Principal Interativo", expanded=False):
    st.markdown("### 📊 Interface principal com sistema completo de análise e visualização")
    
    try:
        with open('dashboard_main.py', 'r', encoding='utf-8') as f:
            codigo_dash = f.read()
        
        # Mostrar estatísticas do arquivo
        linhas = len(codigo_dash.split('\n'))
        caracteres = len(codigo_dash)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📝 Linhas", linhas)
        with col2:
            st.metric("📄 Caracteres", f"{caracteres:,}")
        with col3:
            st.metric("🎨 Complexidade", "Muito Alta")
        
        st.markdown("**🎯 Principais Funcionalidades:**")
        st.markdown("""
        - 🎨 Interface responsiva com layout wide
        - 🔍 Sistema de 15 filtros integrados
        - 📊 Gráficos interativos (Altair/Plotly)
        - ⚡ Otimização waterfall para gráficos
        - 📋 Tabelas dinâmicas com formatação
        - 💾 Cache multi-nível para performance
        - 🔄 Detecção automática de ambiente
        - 📥 Exportação Excel avançada
        """)
        
        st.code(codigo_dash, language='python')
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar dashboard_main.py: {e}")

with st.expander("🔐 **AUTH_SIMPLE.PY** - Sistema de Autenticação", expanded=False):
    st.markdown("### 🛡️ Sistema completo de autenticação com administração de usuários")
    
    try:
        with open('auth_simple.py', 'r', encoding='utf-8') as f:
            codigo_auth = f.read()
        
        # Mostrar estatísticas do arquivo
        linhas = len(codigo_auth.split('\n'))
        caracteres = len(codigo_auth)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📝 Linhas", linhas)
        with col2:
            st.metric("📄 Caracteres", f"{caracteres:,}")
        with col3:
            st.metric("🔒 Segurança", "Alta")
        
        st.markdown("**🎯 Principais Funcionalidades:**")
        st.markdown("""
        - 🔐 Hash SHA-256 para senhas
        - 👑 Sistema de níveis (Admin/Usuário)
        - 🌐 Compatibilidade Cloud/Local
        - ⚙️ Seleção de modo centralizada
        - 👥 CRUD completo de usuários
        - 🔒 Validações de segurança
        - 📱 Interface responsiva de login
        - 🔄 Persistência em JSON
        """)
        
        st.code(codigo_auth, language='python')
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar auth_simple.py: {e}")



# Mensagem final
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-top: 2rem;">
    <h3 style="color: white; margin: 0;">🎯 Dashboard KE5Z</h3>
    <p style="color: #f0f0f0; margin: 0.5rem 0;">
        Aplicação Desktop completa de análise financeira com extração automática
    </p>
    <p style="color: #e0e0e0; font-size: 0.9rem; margin: 0;">
        Desenvolvido como executável independente para máxima portabilidade
    </p>
    <p style="color: #d0d0d0; font-size: 0.8rem; margin-top: 1rem;">
        💻 3.500+ linhas de código • ⚡ 68% otimização • 🖥️ Aplicação Desktop • 🔄 Extração automática • 📊 7 páginas completas • 🎯 15+ filtros avançados
    </p>
</div>
""", unsafe_allow_html=True)
