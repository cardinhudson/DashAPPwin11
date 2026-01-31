import streamlit as st
import sys
import os
import json
import base64
from datetime import datetime

# Adicionar diretório pai ao path para importar auth_simple
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth_simple import (verificar_autenticacao, exibir_header_usuario,
                         exibir_info_ultima_extracao, exibir_rodape_versao)

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

# Configuração de página removida - apenas app.py deve ter st.set_page_config no modo multi-page
# page_title="Sobre o Projeto - Dashboard KE5Z", page_icon="🎯", layout="wide"

# Verificar autenticação
verificar_autenticacao()

# Navegação simples
st.sidebar.markdown("📋 **NAVEGAÇÃO:** Use abas do navegador")
st.sidebar.markdown("🏠 Dashboard: Aplicação Desktop")
st.sidebar.markdown("---")

# Exibir informação da última extração no topo
exibir_info_ultima_extracao()

# Header
exibir_header_usuario()

# Título principal com estilo
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;">
    <h1 style="color: white; font-size: 3rem; margin: 0;">🎯 Dashboard KE5Z</h1>
    <h3 style="color: #f0f0f0; margin: 0;">Aplicação Desktop Completa v2.04</h3>
    <p style="color: #e0e0e0; font-size: 1.2rem; margin-top: 1rem;">
        Executável independente para análise de dados SAP com extração automática e otimizações avançadas
    </p>
    <p style="color: #d0d0d0; font-size: 1rem; margin-top: 0.5rem;">
        🖥️ Funciona sem Python instalado • ⚡ Performance otimizada • 🔄 Extração automática • 📊 9 páginas completas • 🗂️ Multi-ano
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
    st.metric("💻 Linhas de Código", "4.500+", "Sistema completo")

with col2:
    st.metric("⚡ Otimização", "68%", "Memória reduzida")

with col3:
    st.metric("📊 Páginas", "9", "Funcionalidades completas")

with col4:
    st.metric("🖥️ Versão", "2.04", "Desktop App")

# Objetivos do Projeto - Movidos para o início
st.markdown("---")
st.subheader("🎯 Objetivos do Projeto")

st.markdown("""
**🎯 Objetivos do Projeto:**
- 📈 **Análise avançada de dados financeiros** com visualizações interativas
- ⚡ **Performance otimizada** para grandes volumes (68% redução de memória)
- 🔐 **Sistema de autenticação robusto** com administração de usuários
- 📱 **Interface responsiva** e intuitiva com 9 páginas funcionais
- 🖥️ **Aplicação Desktop independente:** Executável que funciona em qualquer PC Windows 10/11
- 🔄 **Extração automática de dados:** Processamento inteligente de arquivos TXT para Parquet otimizado
- 📊 **Dashboards especializados:** Mensal, Total Accounts, Waterfall Analysis
- 🤖 **Assistente inteligente:** IUD Assistant para análises conversacionais
- 📥 **Extração de dados:** Interface completa para processamento de arquivos
- 👑 **Administração:** Gerenciamento completo de usuários
- 📦 **Transformação inteligente:** Conversão TXT → Parquet (até 10x menor)
- 🚀 **Portabilidade total:** Aplicação completa em uma única pasta, sem Python
- 🗂️ **Suporte Multi-ano:** Análise de dados de múltiplos anos (2025, 2026, etc)
- 📊 **Sistema integrado:** Combina dados de diferentes fontes (KE5Z, KSBB, SAPIENS)
- 💾 **Cache inteligente:** Sistema multi-nível para performance máxima
- 🎨 **Interface otimizada:** Design responsivo com filtros avançados
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
        - **🗂️ Suporte Multi-ano:** Visualize dados de 2025, 2026, etc
        - **📊 Gráficos avançados:** Type 05, Type 06, Type 07 com filtros específicos
        
        ### 📊 Total Accounts (3_Total_accounts.py)
        - **Análise completa** do centro de lucro 02S
        - **100% otimizado** com dados waterfall
        - **Gráficos Type 05 e Type 06** com cores padronizadas
        - **Tabelas dinâmicas** por USI e conta contábil
        - **Interface limpa** sem mensagens de debug
        - **🗂️ Suporte Multi-ano:** Análise comparativa entre anos
        - **📊 Métricas consolidadas** com indicadores visuais
        
        ### 🌊 Waterfall Analysis (4_Waterfall_Analysis.py)
        - **Análise de cascata** entre períodos
        - **Visualização de variações** mês a mês
        - **Identificação de trends** e padrões
        - **100% dados waterfall** para performance máxima
        - **🗂️ Multi-ano:** Selecione múltiplos anos para análise
        - **📊 Comparação entre períodos** com gráficos interativos
        - **💡 Insights automáticos** de variações significativas
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
        - **🗂️ Multi-ano:** Consultas em múltiplos anos
        - **📊 Visualizações dinâmicas** geradas automaticamente
        
        ### 📥 Extração de Dados (6_Extracao_Dados.py)
        - **Interface completa** para processamento de arquivos
        - **Upload de arquivos** TXT, CSV, Excel
        - **Processamento automático** com logs detalhados
        - **Geração de arquivos** Parquet otimizados
        - **Monitoramento** de progresso em tempo real
        - **Validação** de dados e tratamento de erros
        - **🗂️ Estrutura por ano:** Organização automática em pastas anuais
        - **📊 Merge inteligente:** Combina KE5Z, KSBB e SAPIENS
        - **⚡ Otimização automática:** Gera 4 arquivos otimizados
        - **🔄 Filtros de meses:** Selecione quais meses processar
        
        ### 📦 Guia de Empacotamento (8_Guia_Empacotamento.py)
        - **Instruções completas** para criar executáveis
        - **Pré-requisitos** e configuração de ambiente
        - **Processo passo-a-passo** de empacotamento
        - **Solução de problemas** comuns
        - **Checklist completo** de verificação
        - **Dicas avançadas** para distribuição
        - **🖥️ PyInstaller:** Configuração especializada
        - **📦 Estrutura otimizada:** Mínimo de arquivos externos
        
        ### 📖 Guia de Extração (9_Guia_Extracao.py)
        - **Instruções detalhadas** para extração de dados
        - **Pré-requisitos** e configuração
        - **Processo completo** de extração
        - **Troubleshooting** e soluções
        - **Best practices** para melhores resultados
        - **🗂️ Multi-ano:** Como organizar dados por ano
        - **📊 Formatos suportados:** TXT, CSV, Excel
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
        - **💾 Persistência JSON:** Dados salvos localmente
        - **🔒 Proteção do admin:** Usuário principal não pode ser excluído
        
        ### 🔒 Segurança e Autenticação
        - **Hash SHA-256** para senhas
        - **Proteção do admin** principal
        - **Validações completas** de entrada
        - **Sessões persistentes** com logout seguro
        - **Controle de acesso** por página
        - **🌐 Modo de operação:** Cloud ou Completo
        - **👤 Perfis de usuário:** Admin e Usuário comum
        - **✅ Sistema de aprovação:** Controle de novos usuários
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
        ├── 🖥️ Dashboard_KE5Z_OFICIAL.exe (Executável v2.04)
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
        │   ├── 📦 8_Guia_Empacotamento.py (Guia Empacotamento)
        │   └── 📖 9_Guia_Extracao.py (Guia Extração)
        ├── 📂 _internal/ (Arquivos Internos PyInstaller)
        │   ├── 📂 KE5Z/ (Dados por Ano)
        │   │   ├── 📂 2025/
        │   │   │   ├── KE5Z.parquet (Original)
        │   │   │   ├── KE5Z_main.parquet (Otimizado)
        │   │   │   ├── KE5Z_others.parquet (Separado)
        │   │   │   └── KE5Z_waterfall.parquet (68% menor)
        │   │   └── 📂 2026/
        │   │       └── (mesma estrutura...)
        │   └── 📂 Extracoes/ (Dados de Entrada por Ano)
        │       ├── 📂 2025/
        │       │   ├── 📂 KE5Z/ (Arquivos .txt)
        │       │   └── 📂 KSBB/ (Arquivos .txt)
        │       └── 📂 2026/
        │           └── (mesma estrutura...)
        ├── 📂 arquivos/ (Excel Específicos por Ano)
        │   ├── 📂 2025/
        │   └── 📂 2026/
        ├── 📄 Dados SAPIENS.xlsx
        ├── 📄 Fornecedores.xlsx
        ├── 📄 usuarios.json
        └── 📄 versao_projeto.json
        ```
        
        ### 🔧 Tecnologias Utilizadas
        - **Streamlit:** Framework web interativo
        - **Pandas:** Manipulação de dados avançada
        - **Altair & Plotly:** Visualizações interativas
        - **PyArrow:** Performance com Parquet
        - **OpenPyXL:** Exportação Excel
        - **PyInstaller:** Geração de executáveis
        """)

    with st.expander("⚙️ **SCRIPTS DE AUTOMAÇÃO**", expanded=False):
        st.markdown("""
        ### 🚀 Aplicação Desktop
        
        **🖥️ `Dashboard_KE5Z_OFICIAL.exe`** (Executável Principal v2.04)
        ```batch
        # Aplicação desktop independente
        # Não requer instalação de Python
        # Funciona em qualquer PC Windows 10/11
        # Interface web integrada
        # Extração automática de dados
        # Suporte multi-ano completo
        # Sistema de cache avançado
        # Portabilidade total
        ```
        
        **📂 Estrutura Portátil**
        ```batch
        # Pasta completa contém tudo
        # Executável + Dados + Dependências
        # Copiar pasta = Instalar aplicação
        # Zero configuração necessária
        # Estrutura organizada por ano
        # Dados persistentes em JSON
        # Cache em disco para performance
        ```
        
        **📜 `Extração.py`** (Processamento)
        ```python
        # Leitura de múltiplos formatos (TXT, CSV, Excel)
        # Merge inteligente com dados SAPIENS
        # Geração de 4 arquivos otimizados
        # Logs detalhados de progresso
        # Tratamento robusto de erros
        # Organização automática por ano
        # Filtro de meses para processar
        # Estrutura KE5Z/2025/, KE5Z/2026/, etc
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
        - **🗂️ Filtro de ano:** Selecione um ou múltiplos anos
        - **📊 Multi-seleção:** Filtros com múltiplos valores
        - **⚡ Performance:** Cache de opções de filtros
        
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
        - **🗂️ Organização por ano:** Estrutura automática em pastas anuais
        - **📊 Múltiplas fontes:** KE5Z, KSBB, SAPIENS
        - **🔄 Filtro de meses:** Selecione quais meses processar
        - **⚡ Processamento paralelo:** Otimização de performance
        """)

st.markdown("---")

# Seção de NOVIDADES E ATUALIZAÇÕES RECENTES
st.subheader("🆕 Novidades e Atualizações Recentes (v2.04)")

with st.expander("✨ **PRINCIPAIS MELHORIAS IMPLEMENTADAS**", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🗂️ Suporte Multi-Ano
        - **Estrutura organizada:** Dados separados por ano (2025/, 2026/, etc)
        - **Seleção flexível:** Escolha um ou múltiplos anos para análise
        - **Comparação entre anos:** Análise comparativa de períodos
        - **Organização automática:** Sistema cria pastas por ano
        - **Compatibilidade total:** Todas as páginas suportam multi-ano
        
        ### 📊 Melhorias nos Dashboards
        - **Gráficos aprimorados:** Visualizações mais claras e informativas
        - **Filtros expandidos:** Mais opções de filtragem em todas as páginas
        - **Performance otimizada:** Carregamento mais rápido de dados
        - **Interface refinada:** Design mais limpo e intuitivo
        - **Top N dinâmico:** Selecione 10, 15, 20, 30, 50 ou 100 itens
        
        ### ⚡ Otimizações de Performance
        - **Cache em disco:** Persistência de dados para carregamento rápido
        - **Compressão inteligente:** Tipos de dados otimizados
        - **Carregamento sob demanda:** Dados carregados apenas quando necessário
        - **Memória otimizada:** Redução de 68% no uso de memória
        - **Processamento paralelo:** Múltiplos arquivos processados simultaneamente
        """)
    
    with col2:
        st.markdown("""
        ### 🔄 Extração de Dados Aprimorada
        - **Interface melhorada:** Mais intuitiva e fácil de usar
        - **Filtro de meses:** Selecione quais meses processar
        - **Logs detalhados:** Acompanhe cada etapa do processamento
        - **Validação robusta:** Verificação de dados em múltiplas etapas
        - **Tratamento de erros:** Mensagens claras e soluções sugeridas
        - **Progresso em tempo real:** Barra de progresso e estatísticas
        
        ### 🖥️ Portabilidade e Compatibilidade
        - **Executável otimizado:** Menor tamanho, maior compatibilidade
        - **Detecção inteligente:** Adapta-se ao ambiente automaticamente
        - **Fallbacks seguros:** Funciona mesmo em situações adversas
        - **Modo offline:** Funciona sem conexão de internet
        - **Zero dependências:** Tudo incluído no executável
        
        ### 🔐 Segurança e Usuários
        - **Autenticação aprimorada:** Sistema mais robusto
        - **Gestão de usuários:** Interface completa de administração
        - **Controle de acesso:** Páginas restritas por perfil
        - **Logs de atividade:** Rastreamento de ações dos usuários
        - **Backup automático:** Dados de usuários preservados
        """)

with st.expander("🔧 **CORREÇÕES E AJUSTES**", expanded=False):
    st.markdown("""
    ### 🐛 Bugs Corrigidos
    - ✅ Corrigido problema de carregamento em PCs diferentes
    - ✅ Resolvido erro de cache em modo Cloud
    - ✅ Ajustado formato de datas para compatibilidade
    - ✅ Corrigido filtros em cascata em todas as páginas
    - ✅ Resolvido problema de exportação Excel com dados grandes
    - ✅ Ajustado carregamento de dados waterfall
    - ✅ Corrigido problema de encoding em arquivos TXT
    - ✅ Resolvido erro de memória com datasets grandes
    
    ### 🎨 Melhorias de Interface
    - ✅ Layout mais limpo e organizado
    - ✅ Cores padronizadas em todos os gráficos
    - ✅ Mensagens de erro mais claras
    - ✅ Feedback visual aprimorado
    - ✅ Navegação mais intuitiva
    - ✅ Sidebar otimizada com menos poluição visual
    - ✅ Indicadores de carregamento melhorados
    - ✅ Responsividade aprimorada
    
    ### 📝 Documentação Atualizada
    - ✅ Guia de empacotamento completo
    - ✅ Guia de extração detalhado
    - ✅ Esta página de documentação revisada
    - ✅ Comentários de código melhorados
    - ✅ README.md atualizado
    - ✅ Instruções de instalação simplificadas
    """)

with st.expander("🔮 **PRÓXIMAS FUNCIONALIDADES PLANEJADAS**", expanded=False):
    st.markdown("""
    ### 📅 Em Desenvolvimento
    - 🔄 **Backup automático de dados** com versionamento
    - 📊 **Dashboard de KPIs** com métricas customizáveis
    - 📈 **Previsões e tendências** com machine learning
    - 🔔 **Sistema de notificações** para eventos importantes
    - 📧 **Relatórios automáticos** por email
    - 🎨 **Temas personalizáveis** (claro/escuro)
    - 🌐 **Multi-idioma** (Português, Inglês, Espanhol)
    - 📱 **Versão mobile** responsiva
    
    ### 💡 Ideias Futuras
    - 🤖 **IA integrada** para análises preditivas
    - 📊 **Dashboard customizável** arrastar e soltar
    - 🔗 **Integração com APIs** externas
    - 📦 **Módulos plugáveis** para extensibilidade
    - 🔐 **SSO e LDAP** para autenticação empresarial
    - 📊 **Power BI integration** para relatórios avançados
    - 🌟 **Sistema de favoritos** para análises frequentes
    - 📝 **Anotações e comentários** em gráficos
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
        - **app.py:** ~2.330 linhas (Dashboard principal)
        - **Extração.py:** ~610 linhas (Processamento)
        - **auth_simple.py:** ~450 linhas (Autenticação)
        - **Dash_Mes.py:** ~856 linhas (Dashboard mensal)
        - **Total accounts.py:** ~590 linhas (Análise total)
        - **Waterfall_Analysis.py:** ~602 linhas (Análise cascata)
        - **IUD_Assistant.py:** ~1.004 linhas (Assistente IA)
        - **Admin_Usuarios.py:** ~308 linhas (Admin)
        - **Extracao_Dados.py:** ~828 linhas (Interface extração)
        - **Sobre_Projeto.py:** ~2.886 linhas (Documentação)
        
        **📊 Total Estimado:** ~4.500+ linhas de código
        
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
        - Suporte multi-ano completo
        - Estrutura de pastas por ano
        - Cache persistente em disco
        - Portabilidade total (executável)
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
        - Estrutura por ano (2025/, 2026/, etc)
        
        **⚡ Arquivos Otimizados:**
        - `KE5Z_main.parquet` (sem Others)
        - `KE5Z_others.parquet` (apenas Others)
        - `KE5Z_waterfall.parquet` (68% menor)
        - Separados por ano para organização
        
        **🎯 Uso Inteligente:**
        - **Gráficos:** Dados waterfall (rápido)
        - **Tabelas:** Dados originais (completo)
        - **Downloads:** Dados filtrados (relevante)
        - **Multi-ano:** Seleção de múltiplos anos
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
    
    # Estatísticas do arquivo
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📝 Linhas", "746")
    with col2:
        st.metric("📄 Caracteres", "~25.000")
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
    
    # Código-fonte do Extracao.py (versão completa - 746 linhas)
    codigo_extracao = '''# %%
# SOLUÇÃO DEFINITIVA PARA PROBLEMA PYVENV.CFG
import sys
import os
from pathlib import Path

# Limpar variáveis de ambiente virtual que causam problemas
vars_para_limpar = [
    'VIRTUAL_ENV', 'PYTHONHOME', 'CONDA_DEFAULT_ENV', 
    'PIPENV_ACTIVE', 'POETRY_ACTIVE', 'PYTHONPATH',
    'PYENV_VERSION', 'CONDA_PYTHON_EXE', 'CONDA_EXE'
]

for var in vars_para_limpar:
    if var in os.environ:
        del os.environ[var]

# Garantir que arquivo pyvenv.cfg existe se necessário
pyvenv_path = Path("pyvenv.cfg")
if not pyvenv_path.exists():
    python_exe = sys.executable
    python_home = str(Path(python_exe).parent)
    
    config_content = f"""home = {python_home}
executable = {python_exe}
command = {python_exe} -m venv {os.path.dirname(os.path.abspath(__file__))}
include-system-site-packages = true
version = {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}
prompt = Dash
"""
    try:
        with open(pyvenv_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"Arquivo pyvenv.cfg criado automaticamente")
    except Exception as e:
        print(f"Aviso: Não foi possível criar pyvenv.cfg: {e}")

# Verificar Python ativo
print(f"Python ativo: {sys.executable}")
print(f"Diretorio: {os.getcwd()}")

# Verificação de caminhos para executável (não invasiva)
if hasattr(sys, '_MEIPASS'):
    print(f"Executando no PyInstaller - pasta _internal: {sys._MEIPASS}")
    print(f"Pasta do executável: {os.path.dirname(sys.executable)}")

# ================== CAMINHOS PADRONIZADOS (relativos à pasta principal) ==================
# Pasta raiz do projeto (para ENTRADA - dentro do _internal)
ROOT_DIR = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(os.path.abspath(__file__))

# Pasta raiz para SAÍDA (dentro do _internal para manter consistência)
if hasattr(sys, '_MEIPASS'):
    # No executável: salvar dentro do _internal para manter consistência
    OUTPUT_DIR = sys._MEIPASS
else:
    # Em desenvolvimento: mesmo diretório
    OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Pastas de entrada (dentro do _internal)
DIR_EXTRACOES = os.path.join(ROOT_DIR, "Extracoes")
# Detectar ano mais recente
ano = 2025  # Padrão para dados atuais
if os.path.exists(DIR_EXTRACOES):
    anos = sorted([int(d) for d in os.listdir(DIR_EXTRACOES) if d.isdigit()], reverse=True)
    if anos:
        ano = anos[0]
DIR_KE5Z_IN = os.path.join(DIR_EXTRACOES, str(ano), "KE5Z")
DIR_KSBB_IN = os.path.join(DIR_EXTRACOES, str(ano), "KSBB")

# Arquivos auxiliares de entrada (dentro do _internal)
ARQ_SAPIENS = os.path.join(ROOT_DIR, "Dados SAPIENS.xlsx")
ARQ_FORNECEDORES = os.path.join(ROOT_DIR, "Fornecedores.xlsx")

# Pastas/arquivos de saída (dentro do _internal)
DIR_KE5Z_OUT = os.path.join(OUTPUT_DIR, "KE5Z")
DIR_ARQUIVOS_OUT = os.path.join(OUTPUT_DIR, "arquivos")
# ======================================================================

import pandas as pd

# Obter diretório base (onde está o executável)
if hasattr(sys, '_MEIPASS'):
    # Executando dentro do PyInstaller
    base_dir = sys._MEIPASS
    print(f"Executando dentro do PyInstaller: {base_dir}")
else:
    # Executando normalmente - usar diretório do script atual
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Executando normalmente: {base_dir}")

# Usar pasta local do projeto: Extracoes\KE5Z
pasta = DIR_KE5Z_IN

# Verificar se a pasta local existe
if not os.path.exists(pasta):
    print(f"ERRO: Pasta local {pasta} não encontrada!")
    print(f"Pasta procurada: {os.path.abspath(pasta)}")
    if hasattr(sys, '_MEIPASS'):
        print(f"Pasta _internal: {sys._MEIPASS}")
        print(f"Pasta do executável: {os.path.dirname(sys.executable)}")
    print("Criando pasta local...")
    os.makedirs(pasta, exist_ok=True)
    print(f"Pasta local criada: {os.path.abspath(pasta)}")
    print("Coloque os arquivos .txt na pasta Extracoes/KE5Z/ do projeto")
    exit(1)

print(f"Pasta encontrada: {pasta}")
# Lista para armazenar os DataFrames
dataframes = []

# Iterar sobre todos os arquivos na pasta
arquivos_txt = [f for f in os.listdir(pasta) if f.endswith('.txt')]
print(f"Arquivos .txt encontrados: {len(arquivos_txt)}")

for i, arquivo in enumerate(arquivos_txt, 1):
    caminho_arquivo = os.path.join(pasta, arquivo)
    
    print(f"\n[{i}/{len(arquivos_txt)}] Processando: {arquivo}")
    print(f"Caminho: {caminho_arquivo}")
    
    try:
        # Verificar tamanho do arquivo
        tamanho_mb = os.path.getsize(caminho_arquivo) / (1024 * 1024)
        print(f"Tamanho: {tamanho_mb:.1f} MB")
        
        # Ler o arquivo em um DataFrame com tratamento de erro
        print("Carregando dados...")
        df = pd.read_csv(
            caminho_arquivo, 
            sep='\t', 
            skiprows=9,
            encoding='latin1', 
            engine='c',  # Engine C é mais rápida para arquivos grandes
            low_memory=False  # Evitar warnings de tipos mistos
        )
        print(f"Carregado: {len(df):,} registros, {len(df.columns)} colunas")
        
        # mudar o nome da coluna Doc.ref. pelo seu índice
        if len(df.columns) > 9:
            df.rename(columns={df.columns[9]: 'doc.ref'}, inplace=True)
        
        print(f"Processando dados de {arquivo}...")
        
        # Remover espaços em branco dos nomes das colunas
        df.columns = df.columns.str.strip()
        print("Limpando dados...")
        
        # Filtrar a coluna 'Ano' com valores não nulos e diferentes de 0
        df = df[df['Ano'].notna() & (df['Ano'] != 0)]
        print(f"Após filtro Ano: {len(df):,} registros")
        
        # Substituir ',' por '.' e remover pontos de separação de milhar
        print("Convertendo coluna Em MCont...")
        df['Em MCont.'] = (
            df['Em MCont.']
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )
        # Converter a coluna para float, tratando erros
        df['Em MCont.'] = pd.to_numeric(df['Em MCont.'], errors='coerce')
        # Substituir valores NaN por 0 (ou outro valor padrão, se necessário)
        df['Em MCont.'] = df['Em MCont.'].fillna(0)

        # Substituir ',' por '.' e remover pontos de separação de milhar
        print("Convertendo coluna Qtd...")
        df['Qtd.'] = (
            df['Qtd.']
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )
        # Converter a coluna para float, tratando erros
        df['Qtd.'] = pd.to_numeric(df['Qtd.'], errors='coerce')
        # Substituir valores NaN por 0 (ou outro valor padrão, se necessário)
        df['Qtd.'] = df['Qtd.'].fillna(0)
        
        # Adicionar o DataFrame à lista
        dataframes.append(df)
        print(f"{arquivo} processado com sucesso!")
        
        # Imprimir o valor total da coluna 'Em MCont.'
        total_em_mcont = df['Em MCont.'].sum()
        print(f"Total Em MCont. em {arquivo}: {total_em_mcont:,.2f}")
        
    except Exception as e:
        print(f"Erro ao processar {arquivo}: {str(e)}")
        continue


# Concatenar todos os DataFrames em um único
if dataframes:
    df_total = pd.concat(dataframes, ignore_index=True)
else:
    print("AVISO: Nenhum arquivo .txt encontrado em KE5Z.")
    df_total = pd.DataFrame()


# Remover colunas desnecessárias
colunas_para_remover = [
    'Unnamed: 0',
    'Unnamed: 1',
    'Unnamed: 4',
    'Nº doc.',
    'Elem.PEP',
    'Obj.custo',
    'TD',
    'SocPar',
    'EmpEm.',
    'Empr',
    'TMv',
    'D/C',
    'Imobil.',
    # Colunas restauradas - removidas da lista de remoção:
    # 'Descrição Material',  # RESTAURADA
    # 'Cliente',            # RESTAURADA
    # 'Cen.',              # RESTAURADA  
    # 'Cen.lucro',         # RESTAURADA
    # 'Unnamed: 14',       # RESTAURADA
    # 'Classe objs.',      # RESTAURADA
    # 'Item',              # RESTAURADA
    # 'D',                 # RESTAURADA
]
df_total.drop(columns=colunas_para_remover, inplace=True, errors='ignore')
print(df_total.columns)

# mudar tipo da coluna 'Cliente' e 'Imobil.' para string
df_total['Cliente'] = df_total['Cliente'].astype(str)  # Cliente restaurada

# imprimir a coluna 'Em MCont.'
print(df_total['Em MCont.'])
#
#
#
#
#
# %%
# Modificar o nome da coluna 'Em MCont.' para 'Valor'
df_total.rename(columns={'Em MCont.': 'Valor'}, inplace=True)

# filtrar a coluna Nº conta não vazias e diferentes de 0
df_total = df_total[df_total['Nº conta'].notna() & (df_total['Nº conta'] != 0)]
print(len(df_total))

print(df_total.head(10))  # Exibir as primeiras linhas do DataFrame total


# Usar pasta local do projeto para KSBB: Extracoes\KSBB
pasta_ksbb = DIR_KSBB_IN

# Verificar se a pasta local existe
if not os.path.exists(pasta_ksbb):
    print(f"AVISO: Pasta local {pasta_ksbb} não encontrada!")
    print(f"Pasta procurada: {os.path.abspath(pasta_ksbb)}")
    print("Criando pasta local...")
    os.makedirs(pasta_ksbb, exist_ok=True)
    print(f"Pasta local criada: {os.path.abspath(pasta_ksbb)}")
    print("Coloque os arquivos .txt na pasta Extracoes/KSBB/ do projeto")
    # Não sair do script, apenas pular a parte do KSBB
    pasta_ksbb = None

print(f"Pasta KSBB encontrada: {pasta_ksbb}")
# Lista para armazenar os DataFrames
dataframes_ksbb = []

# Iterar sobre todos os arquivos na pasta (apenas se disponível)
if pasta_ksbb:
    for arquivo in os.listdir(pasta_ksbb):
        caminho_arquivo = os.path.join(pasta_ksbb, arquivo)

        # Verificar se é um arquivo e tem a extensão desejada (.csv)
        if os.path.isfile(caminho_arquivo) and arquivo.endswith('.txt'):
            print(f"Lendo: {arquivo}")

            # Ler o arquivo em um DataFrame
            df_ksbb = pd.read_csv(
                caminho_arquivo,
                sep='\t',
                encoding='latin1',
                engine='python',
                skiprows=3,
                skipfooter=1,
            )

            # remover espaços em branco dos nomes das colunas
            df_ksbb.columns = df_ksbb.columns.str.strip()

            # Filtrar a coluna Material com não vazias e diferentes de 0
            df_ksbb = df_ksbb[
                df_ksbb['Material'].notna() & (df_ksbb['Material'] != 0)
            ]

            # remover as linhas duplicadas pela coluna Material
            df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])

            # Adicionar o DataFrame à lista
            dataframes_ksbb.append(df_ksbb)
else:
    print("Pulando processamento KSBB (pasta não disponível).")


# Concatenar todos os DataFrames em um único e ignorar caso tenha apenas 1
if len(dataframes_ksbb) > 1:
    df_ksbb = pd.concat(dataframes_ksbb, ignore_index=True)
elif len(dataframes_ksbb) == 1:
    df_ksbb = dataframes_ksbb[0]
else:
    df_ksbb = pd.DataFrame()

# remover as linhas duplicadas pela coluna Material
df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])

# merge o df_total com df_ksbb_total pela coluna Material trazendo a coluna de texto breve material do df_ksbb_total
if not df_total.empty and not df_ksbb.empty and 'Material' in df_total.columns:
    df_total = pd.merge(
        df_total,
        df_ksbb[['Material', 'Texto breve material']],
        on='Material',
        how='left',
    )

# renomear a coluna Texto breve material para Descrição Material
df_total = df_total.rename(
    columns={'Texto breve material': 'Descrição Material'}
)

# exibir as 10 primeiras linhas do df_total e as colunas de Material, Descrição Material
if 'Material' in df_total.columns and 'Descrição Material' in df_total.columns:
    print(df_total[['Material', 'Descrição Material']].head(10))

# se a descrição do material nao for nula substituir o valor da coluna Texto pelo valor da Descrição Material
if 'Texto' in df_total.columns and 'Descrição Material' in df_total.columns:
    df_total['Texto'] = df_total.apply(
        lambda row: (
            row['Descrição Material']
            if pd.notnull(row['Descrição Material'])
            else row['Texto']
        ),
        axis=1,
    )

# imprimir os valores totais somarizado por periodo
print(df_total.groupby('Período')['Valor'].sum())
# mudar o tipo de coluna nº conta para string
df_total['Nº conta'] = df_total['Nº conta'].astype(str)

# %%
# Ler o arquivo Excel Dados SAPIENS.xlsx
arquivo_sapiens = ARQ_SAPIENS
df_sapiens = pd.read_excel(arquivo_sapiens, sheet_name='Conta contabil')

# mudar o nome da coluna 'CONTA SAPIENS' para Nº conta
df_sapiens.rename(columns={'CONTA SAPIENS': 'Nº conta'}, inplace=True)
print(df_sapiens.head())
# mudar o tipo da coluna Nº conta para string
df_sapiens['Nº conta'] = df_sapiens['Nº conta'].astype(str)

# Merger o arquivo df_total pela coluna Nº conta com o df_sapiens pela coluna CONTA SAPIENS
df_total = pd.merge(
    df_total,
    df_sapiens[['Nº conta', 'Type 07', 'Type 06', 'Type 05']],
    on='Nº conta',
    how='left',
)

# Ler o arquivo Excel Dados SAPIENS.xlsx e a aba CC
df_CC = pd.read_excel(arquivo_sapiens, sheet_name='CC')

# mudar o nome da coluna CC SAPiens da df_sapiens para Centro cst
df_CC.rename(columns={'CC SAPiens': 'Centro cst'}, inplace=True)

# Merge o df_total com o df_CC pela coluna Centro cst e trazer as colunas Ofincina e USI
df_total = pd.merge(
    df_total,
    df_CC[['Centro cst', 'Oficina', 'USI']],
    on='Centro cst',
    how='left',
)
# Substituir na coluna 'USI' os valores NaN por 'Others'
df_total['USI'] = df_total['USI'].fillna('Others')
# Exibir as 10 primeiras linhas do df_total e as colunas de Nº conta, Type 07, Type 06, Type 05, Centro cst, Oficina e USI
print(
    df_total[
        [
            'Nº conta', 'Type 07', 'Type 06', 'Type 05',
            'Centro cst', 'Oficina', 'USI'
        ]
    ].head(10)
)

# %%
# Limpar e converter tipos de dados antes de salvar parquet
print("Limpando e convertendo tipos de dados...")

# Converter coluna Ano e Período para numérico
for col in ['Ano', 'Período']:
    if col in df_total.columns:
        df_total[col] = pd.to_numeric(df_total[col], errors='coerce')

# Converter colunas numéricas que podem estar como string
numeric_columns = ['Valor', 'Qtd.', 'doc.ref', 'Item']
for col in numeric_columns:
    if col in df_total.columns:
        df_total[col] = pd.to_numeric(df_total[col], errors='coerce')

# Garantir que colunas de texto sejam strings
text_columns = ['Nº conta', 'Centro cst', 'Texto', 'Fornecedor', 'Fornec.', 'Material', 
                'Descrição Material', 'Type 05', 'Type 06', 'Type 07', 'USI', 'Oficina',
                'Doc.compra', 'Usuário', 'Tipo', 'Cliente', 'Dt.lçto.', 'Imobilizado']
for col in text_columns:
    if col in df_total.columns:
        df_total[col] = df_total[col].astype(str)

# Garantir que TODAS as colunas object sejam strings (fallback)
for col in df_total.columns:
    if df_total[col].dtype == 'object':
        df_total[col] = df_total[col].astype(str)

# Substituir valores NaN por None para compatibilidade com PyArrow
df_total = df_total.where(pd.notnull(df_total), None)

# Converter coluna Dt.lçto. para formato DD/MM/AAAA
if 'Dt.lçto.' in df_total.columns:
    print("Convertendo coluna Dt.lçto. para formato DD/MM/AAAA...")
    df_total['Dt.lçto.'] = df_total['Dt.lçto.'].astype(str)
    df_total['Dt.lçto.'] = df_total['Dt.lçto.'].str.replace('.', '/', regex=False)
    print(f"Coluna Dt.lçto. convertida: {df_total['Dt.lçto.'].head(3).tolist()}")

print("Tipos de dados após limpeza:")
print(df_total.dtypes)


# %% Salvar arquivo para extração PBI
# ler arquivo fornecedores e desconsiderar as 3 primeiras linhas
arquivo_fornecedores = ARQ_FORNECEDORES
df_fornecedores = pd.read_excel(arquivo_fornecedores, skiprows=3)
# remover linhas duplicadas pela coluna Fornecedor
df_fornecedores = df_fornecedores.drop_duplicates(subset=['Fornecedor'])
# mudar o nome da coluna Fornecedor para Fornec.
df_fornecedores.rename(columns={'Fornecedor': 'Fornec.'}, inplace=True)

# mudar a coluna fornec. para string
df_fornecedores['Fornec.'] = df_fornecedores['Fornec.'].astype(str)

# merge o df_total com df_fornecedores pela coluna Fornec. retornando a coluna Fornecedor
df_total = pd.merge(
    df_total,
    df_fornecedores[['Fornec.', 'Nome do fornecedor']],
    on='Fornec.',
    how='left',
)
# mudar o nome da coluna Nome do fornecedor para Fornecedor
df_total.rename(columns={'Nome do fornecedor': 'Fornecedor'}, inplace=True)



# Atualizar o nome do fornecedor com as provisoes
# Precimos ler o arquivo Dados SAPIENS.xlsx na pasta do projeto na guia Hist_prov 
# desconsiderar a primeira linha do arquivo
arquivo_hist_prov = os.path.join(base_dir, "Dados SAPIENS.xlsx")
df_hist_prov = pd.read_excel(arquivo_hist_prov, sheet_name='Hist_prov', skiprows=1)
# excluir todas as colunas menos as colunas 'Nome do fornecedor', '20carac'
df_hist_prov = df_hist_prov[['Nome do fornecedor', '20carac']]
# Remover os espaços da coluna '20carac'
df_hist_prov['20carac'] = df_hist_prov['20carac'].str.strip()

# remover linhas duplicadas pela coluna '20carac'
df_hist_prov = df_hist_prov.drop_duplicates(subset=['20carac'])

# criar uma coluna no df_total chamada '20carac' (primeiros 20 caracteres do Fornec.) 
df_total['20carac'] = df_total['Texto'].astype(str).str[:20]
# Remover os espaços da coluna '20carac'
df_total['20carac'] = df_total['20carac'].str.strip()



# merge o df_total com df_hist_prov pela coluna 20carac retornando a coluna 'Nome do fornecedor'
df_total = pd.merge(
    df_total,
    df_hist_prov[['20carac', 'Nome do fornecedor']],
    on='20carac',
    how='left',
)

# Se a coluna 'Nome do fornecedor' não for nula, substituir o valor da coluna Fornecedor pelo valor da coluna 'Nome do fornecedor'
if 'Nome do fornecedor' in df_total.columns and 'Fornecedor' in df_total.columns:
    df_total['Fornecedor'] = df_total.apply(
        lambda row: (
            row['Nome do fornecedor']
            if pd.notnull(row['Nome do fornecedor'])
            else row['Fornecedor']
        ),
        axis=1,
    )


# Colocar as colunas Type 07, Type 06, Type 05 que forem vazias ou nulas como Others
df_total['Type 07'] = df_total['Type 07'].fillna('Others')
df_total['Type 06'] = df_total['Type 06'].fillna('Others')
df_total['Type 05'] = df_total['Type 05'].fillna('Others')


# # gerar um arquivo parquet do df_total atualizado
pasta_parquet = DIR_KE5Z_OUT
os.makedirs(pasta_parquet, exist_ok=True)
print(f"Pasta parquet criada: {pasta_parquet}")

# OTIMIZAÇÃO DE MEMÓRIA: Separar dados por USI
print("\n=== SEPARANDO ARQUIVOS POR USI PARA OTIMIZAÇÃO ===")

# Separar dados Others vs resto
df_others = df_total[df_total['USI'] == 'Others'].copy()
df_main = df_total[df_total['USI'] != 'Others'].copy()

print(f"Total de registros: {len(df_total):,}")
print(f"Registros principais (sem Others): {len(df_main):,}")
print(f"Registros Others: {len(df_others):,}")

# Salvar arquivo principal (sem Others) - para uso no dashboard
caminho_main = os.path.join(pasta_parquet, 'KE5Z_main.parquet')
df_main.to_parquet(caminho_main, index=False)
print(f"Arquivo principal salvo: {caminho_main}")

# Salvar arquivo Others separadamente
if len(df_others) > 0:
    caminho_others = os.path.join(pasta_parquet, 'KE5Z_others.parquet')
    df_others.to_parquet(caminho_others, index=False)
    print(f"Arquivo Others salvo: {caminho_others}")
else:
    print("Nenhum registro Others encontrado")

# Manter arquivo completo para compatibilidade
caminho_saida_atualizado = os.path.join(pasta_parquet, 'KE5Z.parquet')
df_total.to_parquet(caminho_saida_atualizado, index=False)
print(f"Arquivo completo salvo: {caminho_saida_atualizado}")



# CRIAR ARQUIVO WATERFALL OTIMIZADO (72% menor) - ANTES DA RENOMEAÇÃO
print("\n=== CRIANDO ARQUIVO WATERFALL OTIMIZADO ===")

# Definir colunas essenciais para o waterfall (COM Type 07 ORIGINAL!)
colunas_waterfall = [
    'Período',      # OBRIGATÓRIA - Para seleção de meses
    'Valor',        # OBRIGATÓRIA - Para cálculos
    'USI',          # Filtro principal + dimensão
    'Type 05',      # Dimensão de categoria
    'Type 06',      # Dimensão de categoria
    'Type 07',      # Dimensão de categoria (ANTES da renomeação!)
    'Fornecedor',   # Dimensão de categoria + filtro
    'Fornec.',      # Filtro
    'Tipo',         # Filtro
    'Nº conta'      # NOVO: Filtro com EXCELENTE compressão (269 únicos/3M registros = 0.01%)
]

# Verificar quais colunas existem
colunas_existentes = [col for col in colunas_waterfall if col in df_total.columns]
colunas_faltantes = [col for col in colunas_waterfall if col not in df_total.columns]

print(f"Colunas encontradas ({len(colunas_existentes)}): {colunas_existentes}")
if colunas_faltantes:
    print(f"Colunas não encontradas ({len(colunas_faltantes)}): {colunas_faltantes}")

# Filtrar apenas colunas essenciais
if len(colunas_existentes) >= 3:  # Pelo menos Período, Valor, USI
    df_waterfall = df_total[colunas_existentes].copy()
    
    print(f"Dados filtrados: {len(df_waterfall):,} registros, {len(df_waterfall.columns)} colunas")
    
    # Aplicar otimizações de memória
    print("Aplicando otimizações de memória...")
    
    # Converter strings categóricas para category
    for col in df_waterfall.columns:
        if df_waterfall[col].dtype == 'object':
            unique_ratio = df_waterfall[col].nunique(dropna=True) / max(1, len(df_waterfall))
            if unique_ratio < 0.5:  # Se menos de 50% são valores únicos
                df_waterfall[col] = df_waterfall[col].astype('category')
                print(f"  {col}: convertido para category ({unique_ratio:.1%} únicos)")
    
    # Otimizar tipos numéricos
    for col in df_waterfall.select_dtypes(include=['float64']).columns:
        df_waterfall[col] = pd.to_numeric(df_waterfall[col], downcast='float')
        print(f"  {col}: otimizado para float32")
    
    for col in df_waterfall.select_dtypes(include=['int64']).columns:
        df_waterfall[col] = pd.to_numeric(df_waterfall[col], downcast='integer')
        print(f"  {col}: otimizado para int32")
    
    # Remover registros com valores nulos nas colunas críticas
    antes_limpeza = len(df_waterfall)
    df_waterfall = df_waterfall.dropna(subset=['Período', 'Valor'])
    depois_limpeza = len(df_waterfall)
    
    if antes_limpeza != depois_limpeza:
        print(f"Removidos {antes_limpeza - depois_limpeza:,} registros com valores nulos")
    
    # Salvar arquivo otimizado
    arquivo_waterfall = os.path.join(pasta_parquet, "KE5Z_waterfall.parquet")
    df_waterfall.to_parquet(arquivo_waterfall, index=False)
    
    # Calcular redução de tamanho
    try:
        tamanho_original = os.path.getsize(caminho_saida_atualizado) / (1024*1024)
        tamanho_waterfall = os.path.getsize(arquivo_waterfall) / (1024*1024)
        reducao = ((tamanho_original - tamanho_waterfall) / tamanho_original) * 100
        
        print(f"ARQUIVO WATERFALL CRIADO COM SUCESSO!")
        print(f"Arquivo: {arquivo_waterfall}")
        print(f"Registros: {len(df_waterfall):,}")
        print(f"Colunas: {list(df_waterfall.columns)}")
        print(f"Tamanho original: {tamanho_original:.1f} MB")
        print(f"Tamanho otimizado: {tamanho_waterfall:.1f} MB")
        print(f"Redução: {reducao:.1f}%")
        
        # Verificar se Type 07 está presente
        if 'Type 07' in df_waterfall.columns:
            valores_unicos = df_waterfall['Type 07'].nunique()
            print(f"Type 07 incluído com {valores_unicos:,} valores únicos!")
        
    except Exception as e:
        print(f"Erro ao calcular tamanhos: {e}")
        print(f"Arquivo waterfall salvo: {arquivo_waterfall}")
else:
    print("Colunas insuficientes para criar arquivo waterfall")

#
#
# %%
# Salvar arquivos Excel na pasta local do projeto

# organizar a ordem das colunas em Período	Nºconta	Centrocst	doc.ref.	Dt.lçto.	Cen.lucro	 Valor 	QTD	Type 05	Type 06	Account	USI	Oficina	Doc.compra	Texto breve	Fornecedor	Material	DESCRIÇÃO SAPIENS	Usuário	Cofor	Tipo
df_total = df_total[['Período', 'Nº conta', 'Centro cst', 'doc.ref', 'Dt.lçto.', 'Valor', 'Qtd.', 'Type 05', 'Type 06', 'Type 07', 'USI', 'Oficina', 'Doc.compra', 'Texto', 'Fornecedor', 'Material', 'Usuário', 'Fornec.', 'Tipo']]

# mudar os nomes das colunas para Nºconta, Centrocst, Nºdoc.ref., QTD, Texto
df_total.rename(columns={'Texto': 'Texto breve'}, inplace=True)
df_total.rename(columns={'Qtd.': 'QTD'}, inplace=True)
df_total.rename(columns={'Nº conta': 'Nºconta', 'Centro cst': 'Centrocst', 'doc.ref': 'Nºdoc.ref.'}, inplace=True)
# Mudar o nome da coluna Type 07 para Account
df_total.rename(columns={'Type 07': 'Account'}, inplace=True)
# Mudar o nome da coluna 'Periodo' para Mes
df_total.rename(columns={'Período': 'Mes'}, inplace=True)

# Criar uma coluna com os meses minusculos baseados na coluna 'Mes', sendo mes = 1 = janeiro, mes = 2 = fevereiro e assim sucessivamente
# a coluna Mes deve ser string
df_total['Período'] = df_total['Mes'].astype(str)
df_total['Período'] = df_total['Mes'].apply(lambda x: 'janeiro' if x == 1 else 'fevereiro' if x == 2 else 'março' if x == 3 else 'abril' if x == 4 else 'maio' if x == 5 else 'junho' if x == 6 else 'julho' if x == 7 else 'agosto' if x == 8 else 'setembro' if x == 9 else 'outubro' if x == 10 else 'novembro' if x == 11 else 'dezembro')

# Trazer coluna 'mes' para a primeira posição e a coluna 'Período' para a segunda posição do DataFrame
colunas = ['Mes', 'Período'] + [col for col in df_total.columns if col != 'Mes' and col != 'Período']
df_total = df_total[colunas]




# Ler filtro de meses da variável de ambiente (enviada pela página de extração)
meses_env = os.environ.get('MESES_FILTRO', '').strip()
meses_filtrados = None
if meses_env:
    try:
        meses_filtrados = {int(x) for x in meses_env.split(',') if str(x).strip().isdigit()}
        if meses_filtrados:
            print(f"Aplicando filtro de meses (MESES_FILTRO): {sorted(meses_filtrados)}")
    except Exception as e:
        print(f"Aviso: não foi possível interpretar MESES_FILTRO='{meses_env}': {e}")
        meses_filtrados = None

# Se houver filtro, aplicar sobre os DataFrames antes de salvar
if meses_filtrados and 'Mes' in df_total.columns:
    df_total_excel = df_total[df_total['Mes'].isin(meses_filtrados)].copy()
    print(f"Filtro aplicado: {len(df_total_excel):,} linhas após filtrar meses {sorted(meses_filtrados)}")
else:
    df_total_excel = df_total.copy()
    print(f"Sem filtro aplicado: {len(df_total_excel):,} linhas totais")

# Criar pasta 'arquivos' local para salvar os arquivos Excel
pasta_arquivos = DIR_ARQUIVOS_OUT
os.makedirs(pasta_arquivos, exist_ok=True)
print(f"Pasta de arquivos criada: {pasta_arquivos}")

# Salvar arquivo Excel completo primeiro (DESABILITADO - arquivo muito grande para Excel)
# caminho_completo = os.path.join(pasta_arquivos, 'KE5Z_completo.xlsx')
# df_total_excel.to_excel(caminho_completo, index=False)
print(f"Arquivo Excel completo NÃO salvo (dados muito grandes: {len(df_total_excel):,} linhas > limite Excel 1.048.576)")

# Verificar quais USIs existem nos dados
usis_disponiveis = df_total_excel['USI'].unique() if 'USI' in df_total_excel.columns else []
print(f"USIs disponíveis nos dados: {list(usis_disponiveis)}")

# Salvar arquivo Excel com filtro de USI 'Veículos', 'TC Ext' e 'LC' (se existirem)
usis_veiculos = ['Veículos', 'TC Ext', 'LC']
usis_veiculos_existentes = [usi for usi in usis_veiculos if usi in usis_disponiveis]

if usis_veiculos_existentes:
    caminho_veiculos = os.path.join(pasta_arquivos, 'KE5Z_veiculos.xlsx')
    df_veiculos = df_total_excel[df_total_excel['USI'].isin(usis_veiculos_existentes)]
    df_veiculos.to_excel(caminho_veiculos, index=False)
    print(f"Arquivo Excel Veículos salvo: {caminho_veiculos} ({len(df_veiculos)} registros)")
else:
    print("Nenhuma USI de veículos encontrada nos dados")

# Salvar arquivo Excel com filtro de USI 'PWT' (se existir)
if 'PWT' in usis_disponiveis:
    caminho_pwt = os.path.join(pasta_arquivos, 'KE5Z_pwt.xlsx')
    df_pwt = df_total_excel[df_total_excel['USI'] == 'PWT']
    df_pwt.to_excel(caminho_pwt, index=False)
    print(f"Arquivo Excel PWT salvo: {caminho_pwt} ({len(df_pwt)} registros)")
else:
    print("USI PWT não encontrada nos dados")

# Salvar arquivo Excel separado por USI (apenas USIs que NÃO foram agrupadas)
if 'USI' in df_total_excel.columns:
    usis_ja_salvas = set(usis_veiculos_existentes + (['PWT'] if 'PWT' in usis_disponiveis else []))
    for usi in usis_disponiveis:
        if pd.notna(usi) and usi != 'Others' and usi not in usis_ja_salvas:
            # Normalizar nome da USI para evitar duplicação
            nome_arquivo = usi.replace(" ", "_").replace("/", "_").replace("ç", "c").replace("ã", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
            caminho_usi = os.path.join(pasta_arquivos, f'KE5Z_{nome_arquivo}.xlsx')
            df_usi = df_total_excel[df_total_excel['USI'] == usi]
            if len(df_usi) > 0:
                df_usi.to_excel(caminho_usi, index=False)
                print(f"Arquivo Excel {usi} salvo: {caminho_usi} ({len(df_usi)} registros)")

# Mensagem final com link clicável para a pasta de arquivos Excel
pasta_arquivos_absoluta = os.path.abspath(pasta_arquivos)
print("\n" + "="*80)
print("✅ EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
print("="*80)
print(f"📁 Pasta dos arquivos Excel: {pasta_arquivos_absoluta}")
print("🔗 Para abrir a pasta, copie e cole este caminho no Windows Explorer:")
print(f"   {pasta_arquivos_absoluta}")
print("")
print("📊 Arquivos gerados:")
print("   • Arquivos Parquet: pasta KE5Z/")
print("   • Arquivos Excel: pasta arquivos/")
print("")
print("💡 Dica: Pressione Win+R, cole o caminho e pressione Enter para abrir a pasta!")
print("="*80)

# Tentar abrir a pasta automaticamente no Windows
try:
    import subprocess
    if os.name == 'nt':  # Windows
        subprocess.run(['explorer', pasta_arquivos_absoluta], check=False)
        print("🚀 Pasta aberta automaticamente no Windows Explorer!")
    else:
        print("ℹ️  Sistema não-Windows detectado. Abra a pasta manualmente.")
except Exception as e:
    print(f"⚠️  Não foi possível abrir a pasta automaticamente: {e}")
    print(f"   Abra manualmente: {pasta_arquivos_absoluta}")
'''
    
    st.code(codigo_extracao, language='python')

with st.expander("🏠 **APP.PY** - Dashboard Principal Interativo", expanded=False):
    st.markdown("### 📊 Interface principal com sistema completo de análise e visualização")
    
    # Estatísticas do arquivo
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📝 Linhas", "762")
    with col2:
        st.metric("📄 Caracteres", "~30.000")
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
    
    # Código-fonte do app.py (versão completa - 763 linhas)
    codigo_app = '''# %%
import streamlit as st
import pandas as pd
import os
import sys
import altair as alt
from io import BytesIO
import base64
import plotly.graph_objects as go
from auth_simple import (verificar_autenticacao, exibir_header_usuario,
                         eh_administrador, verificar_status_aprovado,
                         get_usuarios_cloud, adicionar_usuario_simples, criar_hash_senha,
                         get_modo_operacao, is_modo_cloud)
from datetime import datetime

# Detectar se está rodando no executável PyInstaller
def get_base_path():
    """Retorna o caminho base correto para LEITURA de dados"""
    if hasattr(sys, '_MEIPASS'):
        # Rodando no executável PyInstaller - apontar para _internal
        return sys._MEIPASS
    else:
        # Rodando em desenvolvimento
        return os.path.dirname(os.path.abspath(__file__))

# Configuração de página removida - apenas app.py deve ter st.set_page_config no modo multi-page
# page_title="Dashboard KE5Z", page_icon="📊", layout="wide"

# Configurações para otimizar conexão e performance
if 'connection_optimized' not in st.session_state:
    # Configurar pandas para usar menos memória
    pd.set_option('display.max_columns', 50)
    pd.set_option('display.max_rows', 1000)
    
    # Marcar como otimizado
    st.session_state.connection_optimized = True

# Verificar autenticação - OBRIGATÓRIO no início de cada página
verificar_autenticacao()

# Verificar se o usuário está aprovado
if 'usuario_nome' in st.session_state and not verificar_status_aprovado(st.session_state.usuario_nome):
    st.warning("⏳ Sua conta ainda está pendente de aprovação. "
               "Aguarde o administrador aprovar seu acesso.")
    st.info("📧 Você receberá uma notificação quando sua conta for "
            "aprovada.")
    st.stop()

# Usar modo selecionado no login (substitui detecção automática)
is_cloud = is_modo_cloud()

# Indicador de navegação no topo
st.sidebar.markdown("📋 **NAVEGAÇÃO:** Menu de páginas acima ⬆️")
st.sidebar.markdown("---")

# Informar sobre modo selecionado (COMPACTO)
modo_atual = get_modo_operacao()
if modo_atual == 'cloud':
    st.sidebar.info("☁️ **Modo Cloud**")
else:
    st.sidebar.info("💻 **Modo Completo**")

# Sistema de cache inteligente para otimização de memória e conexão
@st.cache_data(
    ttl=3600,
    max_entries=3,  # Aumentar para cachear os 3 arquivos
    show_spinner=True,
    persist="disk"
)
def load_data_optimized(arquivo_tipo="completo"):
    """Carrega dados com otimização inteligente de memória
    
    Args:
        arquivo_tipo: "completo", "main" (sem Others), ou "others"
    """
    
    # Definir qual arquivo carregar
    arquivos_disponiveis = {
        "completo": "KE5Z.parquet",
        "main": "KE5Z_main.parquet", 
        "others": "KE5Z_others.parquet",
        "main_filtered": "KE5Z.parquet"  # Usa arquivo completo mas filtra Others
    }
    
    nome_arquivo = arquivos_disponiveis.get(arquivo_tipo, "KE5Z.parquet")
    base_path = get_base_path()
    arquivo_parquet = os.path.join(base_path, "KE5Z", nome_arquivo)
    
    try:
        if not os.path.exists(arquivo_parquet):
            # Se arquivo específico não existe, tentar arquivo completo
            if arquivo_tipo != "completo":
                st.warning(f"⚠️ Arquivo {nome_arquivo} não encontrado, carregando dados completos...")
                # CORREÇÃO: Evitar loop infinito - carregar diretamente o arquivo completo
                arquivo_completo = os.path.join(base_path, "KE5Z", "KE5Z.parquet")
                if os.path.exists(arquivo_completo):
                    df = pd.read_parquet(arquivo_completo)
                    # Aplicar filtro especial para main_filtered (cloud mode)
                    if arquivo_tipo == "main_filtered" and 'USI' in df.columns:
                        df = df[df['USI'] != 'Others'].copy()
                        st.sidebar.info(f"🔄 Filtro aplicado: {len(df):,} registros (Others removidos)")
                    return df
                else:
                    raise FileNotFoundError(f"Arquivo completo também não encontrado: {arquivo_completo}")
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo_parquet}")
        
        # Verificar tamanho do arquivo
        file_size_mb = os.path.getsize(arquivo_parquet) / (1024 * 1024)
        
        # Carregar dados
        df = pd.read_parquet(arquivo_parquet)
        
        # Aplicar filtro especial para main_filtered (cloud mode)
        if arquivo_tipo == "main_filtered" and 'USI' in df.columns:
            # Filtrar para remover Others, simulando arquivo main
            df = df[df['USI'] != 'Others'].copy()
            st.sidebar.info(f"🔄 Filtro aplicado: {len(df):,} registros (Others removidos)")
        
        # Otimizar tipos de dados para economizar memória (sem alterar conteúdo)
        original_memory = df.memory_usage(deep=True).sum() / (1024 * 1024)
        
        for col in df.columns:
            if df[col].dtype == 'object':
                unique_ratio = df[col].nunique() / len(df)
                if unique_ratio < 0.5:  # Menos de 50% valores únicos
                    df[col] = df[col].astype('category')
        
        # Converter floats para tipos menores
        for col in df.select_dtypes(include=['float64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='float')
        
        # Converter ints para tipos menores
        for col in df.select_dtypes(include=['int64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='integer')
        
        # Calcular economia de memória
        optimized_memory = df.memory_usage(deep=True).sum() / (1024 * 1024)
        saved_memory = original_memory - optimized_memory
        
        if saved_memory > 1:  # Economia significativa
            st.sidebar.success(f"💾 Memória economizada: {saved_memory:.1f}MB")
        
        return df
        
    except Exception as e:
        raise e

# Interface para seleção de dados (COMPACTO)
st.sidebar.markdown("---")
st.sidebar.markdown("**🗂️ Dados**")

# Verificar quais arquivos estão disponíveis
base_path = get_base_path()
arquivos_status = {}
for tipo, nome in [("completo", "KE5Z.parquet"), ("main", "KE5Z_main.parquet"), ("others", "KE5Z_others.parquet")]:
    caminho = os.path.join(base_path, "KE5Z", nome)
    arquivos_status[tipo] = os.path.exists(caminho)

# Opções disponíveis baseadas nos arquivos existentes
opcoes_dados = []

# Priorizar arquivos otimizados sempre
if arquivos_status.get("main", False):
    opcoes_dados.append(("📊 Dados Principais (sem Others)", "main"))

# Apenas Others: OCULTAR no modo cloud
if arquivos_status.get("others", False) and not is_cloud:
    opcoes_dados.append(("📋 Apenas Others", "others"))

# Dados completos: APENAS no modo local E quando não há arquivos otimizados
if not is_cloud and arquivos_status.get("completo", False):
    # Se há arquivos otimizados, mostrar completo como opção adicional
    # Se não há arquivos otimizados, será a única opção
    opcoes_dados.append(("📁 Dados Completos", "completo"))

# Tratamento especial para Streamlit Cloud
if is_cloud:
    if not opcoes_dados:  # Não há arquivos otimizados no cloud
        if arquivos_status.get("completo", False):
            # No cloud, usar arquivo completo como "dados principais" temporariamente
            # mas filtrar internamente para remover Others
            opcoes_dados = [("📊 Dados Otimizados (filtrados)", "main_filtered")]
            st.sidebar.warning("⚠️ **Modo Cloud Temporário**\nUsando arquivo completo com filtro interno.\nPara melhor performance, gere arquivos separados localmente.")
        else:
            st.error("❌ **Erro no Streamlit Cloud**: Nenhum arquivo de dados encontrado!")
            st.error("Faça upload dos arquivos parquet para o repositório.")
            st.stop()

# Fallback para modo local sem arquivos otimizados
if not opcoes_dados and not is_cloud:
    if arquivos_status.get("completo", False):
        opcoes_dados = [("📁 Dados Completos", "completo")]
    else:
        st.error("❌ **Erro**: Nenhum arquivo de dados encontrado!")
        st.error("Execute a extração de dados para gerar os arquivos necessários.")
        st.stop()

# Widget de seleção com prioridade para dados principais
def get_default_index():
    """Retorna o índice padrão priorizando dados principais"""
    opcoes_values = [op[1] for op in opcoes_dados]
    
    # Prioridade: main > main_filtered > others > completo
    if "main" in opcoes_values:
        return opcoes_values.index("main")
    elif "main_filtered" in opcoes_values:
        return opcoes_values.index("main_filtered")
    elif "others" in opcoes_values:
        return opcoes_values.index("others")
    else:
        return 0  # Primeiro disponível

opcao_selecionada = st.sidebar.selectbox(
    "Escolha o conjunto de dados:",
    options=[op[1] for op in opcoes_dados],
    format_func=lambda x: next(op[0] for op in opcoes_dados if op[1] == x),
    index=get_default_index()  # Priorizar dados principais
)

# Mostrar informações sobre a seleção (COMPACTO)
if opcao_selecionada == "main":
    st.sidebar.info("🎯 **Dados Principais** (sem Others)")
elif opcao_selecionada == "main_filtered":
    st.sidebar.info("🎯 **Dados Filtrados** (Cloud)")
elif opcao_selecionada == "others":
    st.sidebar.info("🔍 **Apenas Others**")
else:
    st.sidebar.info("📊 **Dados Completos**")

# Carregar dados
try:
    df_total = load_data_optimized(opcao_selecionada)
    st.sidebar.success("✅ Dados carregados com sucesso")
    
    # Log informativo
    if not is_cloud:
        st.sidebar.info(f"📊 {len(df_total)} registros carregados")
        
except FileNotFoundError:
    st.error("❌ Arquivo de dados não encontrado!")
    st.error(f"🔍 Procurando por: `KE5Z/KE5Z.parquet`")
    st.info("💡 **Soluções:**")
    st.info("1. Verifique se o arquivo `KE5Z.parquet` está na pasta `KE5Z/`")
    st.info("2. Execute a extração de dados localmente")
    st.info("3. Faça commit do arquivo no repositório")
    
    if is_cloud:
        st.warning("☁️ **No Streamlit Cloud:** Certifique-se que o arquivo "
                  "foi enviado para o repositório")
    
    st.stop()
    
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {str(e)}")
    st.info("🔧 **Possíveis causas:**")
    st.info("• Arquivo corrompido ou formato inválido")
    st.info("• Problema de permissões")
    st.info("• Arquivo muito grande")
    
    if is_cloud:
        st.info("☁️ **No Cloud:** Verifique se o arquivo tem menos de 100MB")
    
    st.stop()

# Filtrar o df_total com a coluna 'USI' que não seja nula (incluindo 'Others')
df_total = df_total[df_total['USI'].notna()]

# Header com informações do usuário e botão de logout
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.title("📊 Dashboard - Visualização de Dados TC - KE5Z")
st.subheader("Somente os dados com as contas do Perímetro TC")

# Exibir header do usuário
exibir_header_usuario()

st.markdown("---")

# Filtros (COMPACTO)
st.sidebar.markdown("---")
st.sidebar.markdown("**🔍 Filtros**")

# Cache para opções de filtros (otimização de performance)
@st.cache_data(ttl=1800, max_entries=3)
def get_filter_options(df, column_name):
    """Obtém opções de filtro com cache para melhor performance"""
    if column_name in df.columns:
        return ["Todos"] + sorted(df[column_name].dropna().astype(str).unique().tolist())
    return ["Todos"]

# Filtro 1: USINA (com cache otimizado)
usina_opcoes = get_filter_options(df_total, 'USI')
default_usina = ["Veículos"] if "Veículos" in usina_opcoes else ["Todos"]
usina_selecionada = st.sidebar.multiselect("Selecione a USINA:", usina_opcoes, default=default_usina)

# Filtrar o DataFrame com base na USI
if "Todos" in usina_selecionada or not usina_selecionada:
    df_filtrado = df_total.copy()
else:
    df_filtrado = df_total[df_total['USI'].astype(str).isin(usina_selecionada)]

# Filtro 2: Período (com cache otimizado)
periodo_opcoes = get_filter_options(df_filtrado, 'Período')
periodo_selecionado = st.sidebar.selectbox("Selecione o Período:", periodo_opcoes)
if periodo_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Período'].astype(str) == str(periodo_selecionado)]

# Filtro 3: Centro cst (com cache otimizado)
if 'Centro cst' in df_filtrado.columns:
    centro_cst_opcoes = get_filter_options(df_filtrado, 'Centro cst')
    centro_cst_selecionado = st.sidebar.selectbox("Selecione o Centro cst:", centro_cst_opcoes)
    if centro_cst_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Centro cst'].astype(str) == str(centro_cst_selecionado)]

# Filtro 4: Conta contábil (com cache otimizado)
if 'Nº conta' in df_filtrado.columns:
    conta_contabil_opcoes = get_filter_options(df_filtrado, 'Nº conta')[1:]  # Remove "Todos" para multiselect
    conta_contabil_selecionadas = st.sidebar.multiselect("Selecione a Conta contábil:", conta_contabil_opcoes)
    if conta_contabil_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['Nº conta'].astype(str).isin(conta_contabil_selecionadas)]

# Filtros principais (com cache otimizado)
filtros_principais = [
    ("Type 05", "Type 05", "multiselect"),
    ("Type 06", "Type 06", "multiselect"), 
    ("Type 07", "Type 07", "multiselect"),
    ("Fornecedor", "Fornecedor", "multiselect"),
    ("Fornec.", "Fornec.", "multiselect"),
    ("Tipo", "Tipo", "multiselect")
]

for col_name, label, widget_type in filtros_principais:
    if col_name in df_filtrado.columns:
        opcoes = get_filter_options(df_filtrado, col_name)
        if widget_type == "multiselect":
            selecionadas = st.sidebar.multiselect(f"Selecione o {label}:", opcoes, default=["Todos"])
            if selecionadas and "Todos" not in selecionadas:
                df_filtrado = df_filtrado[df_filtrado[col_name].astype(str).isin(selecionadas)]

# Filtros avançados (expansível)
with st.sidebar.expander("🔍 Filtros Avançados"):
    filtros_avancados = [
        ("Oficina", "Oficina", "multiselect"),
        ("Usuário", "Usuário", "multiselect"),
        ("Denominação", "Denominação", "multiselect"),
        ("Dt.lçto.", "Data Lançamento", "multiselect")
    ]
    
    for col_name, label, widget_type in filtros_avancados:
        if col_name in df_filtrado.columns:
            opcoes = get_filter_options(df_filtrado, col_name)
            # Limitar opções para melhor performance
            if len(opcoes) > 101:  # 100 + "Todos"
                opcoes = opcoes[:101]
                st.caption(f"⚠️ {label}: Limitado a 100 opções para performance")
            
            if widget_type == "multiselect":
                selecionadas = st.multiselect(f"Selecione o {label}:", opcoes, default=["Todos"])
                if selecionadas and "Todos" not in selecionadas:
                    df_filtrado = df_filtrado[df_filtrado[col_name].astype(str).isin(selecionadas)]

# Resumo (COMPACTO)
st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Resumo**")
st.sidebar.write(f"**Linhas:** {df_filtrado.shape[0]:,}")
st.sidebar.write(f"**Total:** R$ {df_filtrado['Valor'].sum():,.2f}")

# Status do Sistema (COMPACTO)
if not is_cloud:  # Só mostrar em modo local para economizar espaço
    st.sidebar.markdown("---")
    st.sidebar.markdown("**💾 Sistema**")
    
    try:
        import sys
        df_size_mb = sys.getsizeof(df_filtrado) / (1024 * 1024)
        st.sidebar.write(f"**Memória:** {df_size_mb:.1f}MB")
        
        if st.sidebar.button("🧹 Cache", help="Limpar cache"):
            st.cache_data.clear()
            import gc
            gc.collect()
            st.sidebar.success("✅ Limpo!")
            st.rerun()
    except Exception:
        pass

# Área administrativa (COMPACTO)
if eh_administrador():
    st.sidebar.markdown("---")
    st.sidebar.markdown("**👑 Admin**")

    usuarios = get_usuarios_cloud()
    total_usuarios = len(usuarios)
    usuarios_aprovados = len([u for u in usuarios.values() if u.get('status') == 'aprovado'])
    usuarios_pendentes = len([u for u in usuarios.values() if u.get('status') == 'pendente'])

    st.sidebar.write(f"**Usuários:** {total_usuarios} ({usuarios_aprovados} ✅, {usuarios_pendentes} ⏳)")
    
    # Botão para expandir detalhes
    if st.sidebar.button("📋 Ver Usuários"):
        st.sidebar.markdown("**Cadastrados:**")
        for usuario, dados in usuarios.items():
            tipo_icon = "👑" if dados.get('tipo') == 'administrador' else "👥"
            status_icon = "✅" if dados.get('status') == 'aprovado' else "⏳"
            st.sidebar.write(f"{tipo_icon} {status_icon} {usuario}")

# Gráfico de barras para a soma dos valores por 'Período'
@st.cache_data(ttl=900, max_entries=2)
def create_period_chart(df_data):
    """Cria gráfico otimizado"""
    try:
        chart_data = df_data.groupby('Período')['Valor'].sum().reset_index()
        
        grafico_barras = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Período:N', title='Período'),
            y=alt.Y('Valor:Q', title='Soma do Valor'),
            color=alt.Color('Valor:Q', title='Valor', scale=alt.Scale(scheme='redyellowgreen', reverse=True)),
            tooltip=['Período:N', 'Valor:Q']
        ).properties(
            title='Soma do Valor por Período'
        )
        
        return grafico_barras
    except Exception as e:
        st.error(f"Erro ao criar gráfico: {e}")
        return None

# Criar e exibir gráfico
grafico_barras = create_period_chart(df_filtrado)
if grafico_barras:
    # Adicionar rótulos com valores nas barras
    rotulos = grafico_barras.mark_text(
        align='center',
        baseline='middle',
        dy=-10,  # Ajuste vertical
        color='black',
        fontSize=12
    ).encode(
        text=alt.Text('Valor:Q', format=',.2f')
    )
    
    # Combinar gráfico com rótulos
    grafico_completo = grafico_barras + rotulos
    st.altair_chart(grafico_completo, use_container_width=True)

# Gráficos adicionais por Type
st.subheader("📊 Análise por Categorias")

# Gráfico por Type 05
if 'Type 05' in df_filtrado.columns:
    @st.cache_data(ttl=900, max_entries=2)
    def create_type05_chart(df_data):
        try:
            type05_data = df_data.groupby('Type 05')['Valor'].sum().reset_index()
            type05_data = type05_data.sort_values('Valor', ascending=False)
            
            chart = alt.Chart(type05_data).mark_bar().encode(
                x=alt.X('Type 05:N', title='Type 05', sort='-y'),
                y=alt.Y('Valor:Q', title='Soma do Valor'),
                color=alt.Color('Valor:Q', title='Valor', scale=alt.Scale(scheme='redyellowgreen', reverse=True)),
                tooltip=['Type 05:N', 'Valor:Q']
            ).properties(
                title='Soma do Valor por Type 05',
                height=400
            )
            
            return chart
        except Exception as e:
            st.error(f"Erro no gráfico Type 05: {e}")
            return None
    
    chart_type05 = create_type05_chart(df_filtrado)
    if chart_type05:
        st.altair_chart(chart_type05, use_container_width=True)

# Gráfico por Type 06
if 'Type 06' in df_filtrado.columns:
    @st.cache_data(ttl=900, max_entries=2)
    def create_type06_chart(df_data):
        try:
            type06_data = df_data.groupby('Type 06')['Valor'].sum().reset_index()
            type06_data = type06_data.sort_values('Valor', ascending=False)
            
            chart = alt.Chart(type06_data).mark_bar().encode(
                x=alt.X('Type 06:N', title='Type 06', sort='-y'),
                y=alt.Y('Valor:Q', title='Soma do Valor'),
                color=alt.Color('Valor:Q', title='Valor', scale=alt.Scale(scheme='redyellowgreen', reverse=True)),
                tooltip=['Type 06:N', 'Valor:Q']
            ).properties(
                title='Soma do Valor por Type 06',
                height=400
            )
            
            return chart
        except Exception as e:
            st.error(f"Erro no gráfico Type 06: {e}")
            return None
    
    chart_type06 = create_type06_chart(df_filtrado)
    if chart_type06:
        st.altair_chart(chart_type06, use_container_width=True)

# Gráfico Type 07 com filtros específicos
if 'Type 07' in df_filtrado.columns:
    st.subheader("🏆 Análise Type 07 - Filtros Específicos")
    
    # Filtros específicos para o gráfico Type 07
    col_filtro1, col_filtro2, col_filtro3, col_filtro4 = st.columns(4)
    
    with col_filtro1:
        # Filtro Type 05 para o gráfico
        type05_opcoes_grafico = get_filter_options(df_filtrado, 'Type 05')
        type05_grafico = st.selectbox("Type 05 (Gráfico):", type05_opcoes_grafico, key="type05_grafico")
    
    with col_filtro2:
        # Filtro Type 06 para o gráfico
        type06_opcoes_grafico = get_filter_options(df_filtrado, 'Type 06')
        type06_grafico = st.selectbox("Type 06 (Gráfico):", type06_opcoes_grafico, key="type06_grafico")
    
    with col_filtro3:
        # Filtro Período para o gráfico
        periodo_opcoes_grafico = get_filter_options(df_filtrado, 'Período')
        periodo_grafico = st.selectbox("Período (Gráfico):", periodo_opcoes_grafico, key="periodo_grafico")
    
    with col_filtro4:
        # Filtro de quantidade (Top N)
        quantidade_opcoes = [10, 15, 20, 30, 50, 100]
        quantidade_grafico = st.selectbox("Top N:", quantidade_opcoes, index=0, key="quantidade_grafico")
    
    # Aplicar filtros específicos para o gráfico
    df_grafico = df_filtrado.copy()
    
    if type05_grafico != "Todos":
        df_grafico = df_grafico[df_grafico['Type 05'].astype(str) == str(type05_grafico)]
    
    if type06_grafico != "Todos":
        df_grafico = df_grafico[df_grafico['Type 06'].astype(str) == str(type06_grafico)]
    
    if periodo_grafico != "Todos":
        df_grafico = df_grafico[df_grafico['Período'].astype(str) == str(periodo_grafico)]
    
    # Mostrar estatísticas dos filtros aplicados
    st.caption(f"📊 Dados filtrados: {len(df_grafico):,} registros | Total: R$ {df_grafico['Valor'].sum():,.2f}")
    
    # Criar gráfico Type 07 com os dados filtrados
    @st.cache_data(ttl=900, max_entries=2)
    def create_type07_chart(df_data, quantidade):
        try:
            type07_data = df_data.groupby('Type 07')['Valor'].sum().reset_index()
            type07_data = type07_data.sort_values('Valor', ascending=False).head(quantidade)
            
            chart = alt.Chart(type07_data).mark_bar().encode(
                x=alt.X('Type 07:N', title='Type 07', sort='-y'),
                y=alt.Y('Valor:Q', title='Soma do Valor'),
                color=alt.Color('Valor:Q', title='Valor', scale=alt.Scale(scheme='redyellowgreen', reverse=True)),
                tooltip=['Type 07:N', 'Valor:Q']
            ).properties(
                title=f'Top {quantidade} Type 07 - Filtrado por Type 05: {type05_grafico}, Type 06: {type06_grafico}, Período: {periodo_grafico}',
                height=500
            )
            
            return chart
        except Exception as e:
            st.error(f"Erro no gráfico Type 07: {e}")
            return None
    
    chart_type07 = create_type07_chart(df_grafico, quantidade_grafico)
    if chart_type07:
        st.altair_chart(chart_type07, use_container_width=True)
        
        # Mostrar tabela com os dados do gráfico (incluindo Type 05, Type 06 e valores por Período)
        if not df_grafico.empty:
            st.subheader(f"📋 Dados do Gráfico Type 07 (Top {quantidade_grafico})")
            
            # Criar tabela pivot com Type 05, Type 06, Type 07 e valores por Período
            type07_detailed = df_grafico.groupby(['Type 05', 'Type 06', 'Type 07', 'Período'])['Valor'].sum().reset_index()
            
            # Pivotar para ter Períodos como colunas
            type07_pivot = type07_detailed.pivot_table(
                index=['Type 05', 'Type 06', 'Type 07'], 
                columns='Período', 
                values='Valor', 
                aggfunc='sum', 
                fill_value=0
            ).reset_index()
            
            # Calcular total por linha
            numeric_cols = type07_pivot.select_dtypes(include=['number']).columns
            type07_pivot['Total'] = type07_pivot[numeric_cols].sum(axis=1)
            
            # Ordenar por total e pegar top N
            type07_pivot = type07_pivot.sort_values('Total', ascending=False).head(quantidade_grafico)
            
            # Formatar valores monetários
            for col in numeric_cols:
                type07_pivot[col] = type07_pivot[col].apply(lambda x: f"R$ {x:,.2f}" if x != 0 else "R$ 0,00")
            type07_pivot['Total'] = type07_pivot['Total'].apply(lambda x: f"R$ {x:,.2f}")
            
            st.dataframe(type07_pivot, use_container_width=True, hide_index=True)

# Tabela dinâmica com cores (modificada para mostrar apenas valores diferentes de zero)
df_pivot = df_filtrado.pivot_table(index='USI', columns='Período', values='Valor', aggfunc='sum', margins=True, margins_name='Total', fill_value=0)
st.subheader("Tabela Dinâmica - Soma do Valor por USI e Período (Apenas Valores ≠ 0)")

# Filtrar para mostrar apenas linhas e colunas com valores diferentes de zero
# Remover linhas onde todos os valores (exceto Total) são zero
df_pivot_filtered = df_pivot.loc[(df_pivot != 0).any(axis=1)]

# Remover colunas onde todos os valores (exceto Total) são zero
df_pivot_filtered = df_pivot_filtered.loc[:, (df_pivot_filtered != 0).any(axis=0)]

# Aplicar formatação com cores (verde para positivo, vermelho para negativo)
def colorir_valores(val):
    if isinstance(val, (int, float)):
        if val < 0:
            return 'color: #e74c3c; font-weight: bold;'  # Vermelho para negativo
        elif val > 0:
            return 'color: #27ae60; font-weight: bold;'  # Verde para positivo
    return ''

df_pivot_view = df_pivot_filtered.copy()

# Limites para evitar MessageSizeError
display_limit_pivot = 200 if is_cloud else 1000
max_cells_style = 20_000 if is_cloud else 60_000

# Ordenar por Total (quando existir) e manter a linha "Total" no final
try:
    total_row = df_pivot_view.loc[["Total"]] if "Total" in df_pivot_view.index else None
    df_no_total = df_pivot_view.drop(index="Total", errors="ignore")
    if "Total" in df_no_total.columns:
        df_no_total = df_no_total.sort_values("Total", key=lambda s: s.abs(), ascending=False)
    if len(df_no_total) > display_limit_pivot:
        st.info(
            f"📊 Tabela dinâmica: mostrando {display_limit_pivot:,} de {len(df_no_total):,} USIs (ordem por |Total|)"
        )
        df_no_total = df_no_total.head(display_limit_pivot)
    df_pivot_view = (
        pd.concat([df_no_total, total_row]) if total_row is not None else df_no_total
    )
except Exception:
    if len(df_pivot_view) > display_limit_pivot:
        st.info(
            f"📊 Tabela dinâmica: mostrando {display_limit_pivot:,} de {len(df_pivot_view):,} linhas"
        )
        df_pivot_view = df_pivot_view.head(display_limit_pivot)

aplicar_cores = df_pivot_view.size <= max_cells_style
if not aplicar_cores:
    st.warning(
        "⚠️ Tabela grande: cores desativadas para evitar erro de tamanho (Streamlit MessageSizeError)."
    )

if aplicar_cores:
    styled_pivot = df_pivot_view.style.format('R$ {:,.2f}').map(
        colorir_valores, subset=pd.IndexSlice[:, :]
    )
    st.dataframe(styled_pivot, use_container_width=True)
else:
    try:
        col_cfg = {
            c: st.column_config.NumberColumn(format="R$ %.2f")
            for c in df_pivot_view.columns
            if pd.api.types.is_numeric_dtype(df_pivot_view[c])
        }
        st.dataframe(df_pivot_view, use_container_width=True, column_config=col_cfg)
    except TypeError:
        st.dataframe(df_pivot_view, use_container_width=True)

# Mostrar estatísticas da filtragem
linhas_originais = len(df_pivot)
linhas_filtradas = len(df_pivot_filtered)
colunas_originais = len(df_pivot.columns)
colunas_filtradas = len(df_pivot_filtered.columns)

st.caption(f"📊 Filtragem aplicada: {linhas_originais} → {linhas_filtradas} linhas, {colunas_originais} → {colunas_filtradas} colunas")

# Botão de download da Tabela Dinâmica (logo abaixo da tabela)
if st.button("📥 Baixar Tabela Dinâmica (Excel)", use_container_width=True, key="download_pivot"):
    with st.spinner("Gerando arquivo da tabela dinâmica..."):
        try:
            # Obter pasta Downloads do usuário
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            file_name = "KE5Z_tabela_dinamica_filtrada.xlsx"
            file_path = os.path.join(downloads_path, file_name)
            
            # Salvar arquivo diretamente na pasta Downloads
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df_pivot_filtered.to_excel(writer, index=True, sheet_name='Tabela_Dinamica')
            
            st.success(f"✅ Arquivo salvo com sucesso em: {file_path}")
            st.info(f"📁 Verifique sua pasta Downloads: {downloads_path}")
        except Exception as e:
            st.error(f"❌ Erro ao salvar arquivo: {str(e)}")

# Exibir o DataFrame filtrado (limitado para performance)
st.subheader("Tabela Filtrada")
display_limit = 500 if is_cloud else 2000
if len(df_filtrado) > display_limit:
    st.info(f"📊 Mostrando {display_limit:,} de {len(df_filtrado):,} registros para otimizar performance")
    df_display = df_filtrado.head(display_limit)
else:
    df_display = df_filtrado

st.dataframe(df_display, use_container_width=True)

# Botão de download da Tabela Filtrada (logo abaixo da tabela)
if st.button("📥 Baixar Tabela Filtrada (Excel)", use_container_width=True, key="download_filtered"):
    with st.spinner("Gerando arquivo da tabela filtrada..."):
        try:
            # Obter pasta Downloads do usuário
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            file_name = "KE5Z_tabela_filtrada.xlsx"
            file_path = os.path.join(downloads_path, file_name)
            
            # Salvar arquivo diretamente na pasta Downloads
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df_filtrado.to_excel(writer, index=False, sheet_name='Dados_Filtrados')
            
            st.success(f"✅ Arquivo salvo com sucesso em: {file_path}")
            st.info(f"📁 Verifique sua pasta Downloads: {downloads_path}")
        except Exception as e:
            st.error(f"❌ Erro ao salvar arquivo: {str(e)}")

# Tabela de soma por Types separada por Período (apenas valores ≠ 0)
if all(col in df_filtrado.columns for col in ['Type 05', 'Type 06', 'Type 07', 'Período']):
    st.markdown("---")
    st.subheader("📊 Soma dos Valores por Type 05, Type 06 e Type 07 (Separado por Período)")
    
    # Criar tabela pivot com Type 05, Type 06, Type 07 e valores por Período
    soma_por_type_periodo = df_filtrado.groupby(['Type 05', 'Type 06', 'Type 07', 'Período'])['Valor'].sum().reset_index()
    
    # Pivotar para ter Períodos como colunas
    tabela_pivot_raw = soma_por_type_periodo.pivot_table(
        index=['Type 05', 'Type 06', 'Type 07'], 
        columns='Período', 
        values='Valor', 
        aggfunc='sum', 
        fill_value=0
    ).reset_index()
    # Cópia para exibição formatada
    tabela_pivot = tabela_pivot_raw.copy()
    
    # Calcular total por linha
    numeric_cols = tabela_pivot.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        tabela_pivot['Total'] = tabela_pivot[numeric_cols].sum(axis=1)
        
        # Filtrar apenas linhas com valores diferentes de zero
        tabela_pivot = tabela_pivot[(tabela_pivot[numeric_cols] != 0).any(axis=1)]
        
        # Ordenar por total (decrescente)
        tabela_pivot = tabela_pivot.sort_values('Total', ascending=False)
        
        # Formatar valores monetários
        for col in numeric_cols:
            tabela_pivot[col] = tabela_pivot[col].apply(lambda x: f"R$ {x:,.2f}" if x != 0 else "R$ 0,00")
        tabela_pivot['Total'] = tabela_pivot['Total'].apply(lambda x: f"R$ {x:,.2f}")
        
        st.dataframe(tabela_pivot, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum período encontrado nos dados filtrados.")
    
    # Botão de download nativo da Tabela de Soma por Types (usa dados não formatados)
    with st.spinner("Gerando arquivo da soma por types..."):
        output_types = BytesIO()
        with pd.ExcelWriter(output_types, engine='openpyxl') as writer:
            tabela_pivot_raw.to_excel(writer, index=False, sheet_name='Soma_por_Types')
        output_types.seek(0)

    if st.button("📥 Baixar Soma por Types (Excel)", use_container_width=True, key="download_types"):
        with st.spinner("Gerando arquivo da soma por types..."):
            try:
                # Obter pasta Downloads do usuário
                downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
                file_name = "KE5Z_soma_por_types.xlsx"
                file_path = os.path.join(downloads_path, file_name)
                
                # Salvar arquivo diretamente na pasta Downloads
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    tabela_pivot_raw.to_excel(writer, index=False, sheet_name='Soma_por_Types')
                
                st.success(f"✅ Arquivo salvo com sucesso em: {file_path}")
                st.info(f"📁 Verifique sua pasta Downloads: {downloads_path}")
            except Exception as e:
                st.error(f"❌ Erro ao salvar arquivo: {str(e)}")

# Footer
st.markdown("---")
st.info("💡 Dashboard KE5Z com otimizações de cache e memória")

# Informações de funcionalidades restauradas
col1, col2, col3 = st.columns(3)
with col1:
    st.success("✅ Exportação Excel")
with col2:
    st.success("✅ Gráficos Coloridos")
with col3:
    st.success("✅ Tabelas com Cores")

if is_cloud:
    st.success("☁️ Executando no Streamlit Cloud com otimizações")
else:
    st.success("💻 Executando localmente com performance máxima")'''
    
    st.code(codigo_app, language='python')

with st.expander("🔐 **AUTH_SIMPLE.PY** - Sistema de Autenticação", expanded=False):
    st.markdown("### 🛡️ Sistema completo de autenticação com administração de usuários")
    
    # Estatísticas do arquivo
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📝 Linhas", "273")
    with col2:
        st.metric("📄 Caracteres", "~12.000")
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
    
    # Código-fonte do auth_simple.py (versão completa - 272 linhas)
    codigo_auth = '''# -*- coding: utf-8 -*-
"""
Sistema de Autenticação Simples para Dashboard KE5Z
Sistema completo de autenticação com administração de usuários
"""

import streamlit as st
import json
import hashlib
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional, List

# Função para determinar diretório base
def get_data_dir():
    """Retorna o diretório onde os arquivos de dados devem ser salvos"""
    if hasattr(sys, '_MEIPASS'):
        # No executável: salvar no diretório do executável (fora do _internal)
        return os.path.dirname(sys.executable)
    else:
        # Em desenvolvimento: diretório atual
        return os.path.dirname(os.path.abspath(__file__))

# Configurações do sistema
DATA_DIR = get_data_dir()
USUARIOS_FILE = os.path.join(DATA_DIR, "usuarios.json")
USUARIOS_PADRAO_FILE = os.path.join(DATA_DIR, "usuarios_padrao.json")

def carregar_usuarios() -> Dict[str, Any]:
    """Carrega usuários do arquivo JSON"""
    try:
        # Primeiro, tentar carregar usuarios.json
        if os.path.exists(USUARIOS_FILE):
            with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)
                # Verificar se tem admin, se não, adicionar do padrão
                if "admin" not in usuarios and os.path.exists(USUARIOS_PADRAO_FILE):
                    with open(USUARIOS_PADRAO_FILE, 'r', encoding='utf-8') as f:
                        usuarios_padrao = json.load(f)
                        if "admin" in usuarios_padrao:
                            usuarios["admin"] = usuarios_padrao["admin"]
                            salvar_usuarios(usuarios)
                return usuarios
        
        # Se usuarios.json não existe, tentar carregar do padrão
        if os.path.exists(USUARIOS_PADRAO_FILE):
            with open(USUARIOS_PADRAO_FILE, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)
                # Converter senha para senha_hash se necessário
                for user, data in usuarios.items():
                    if "senha" in data and "senha_hash" not in data:
                        data["senha_hash"] = data.pop("senha")
                # Salvar como usuarios.json
                salvar_usuarios(usuarios)
                return usuarios
        
        # Se nenhum arquivo existe, criar admin padrão
        usuarios_padrao = {
            "admin": {
                "senha_hash": hashlib.sha256("admin123".encode()).hexdigest(),
                "tipo": "administrador",
                "status": "aprovado",
                "data_criacao": datetime.now().isoformat(),
                "aprovado_em": datetime.now().isoformat()
            }
        }
        salvar_usuarios(usuarios_padrao)
        return usuarios_padrao
        
    except Exception as e:
        st.error(f"Erro ao carregar usuários: {e}")
        return {}

def salvar_usuarios(usuarios: Dict[str, Any]) -> bool:
    """Salva usuários no arquivo JSON"""
    try:
        with open(USUARIOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar usuários: {e}")
        return False

def criar_hash_senha(senha: str) -> str:
    """Cria hash SHA-256 da senha"""
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    """Verifica se a senha está correta"""
    return criar_hash_senha(senha) == hash_armazenado

def verificar_autenticacao():
    """Verifica se o usuário está autenticado"""
    if 'autenticado' not in st.session_state or not st.session_state.autenticado:
        mostrar_tela_login()
        st.stop()

def mostrar_tela_login():
    """Exibe a tela de login"""
    st.title("🔐 Login - Dashboard KE5Z")
    st.markdown("---")
    
    with st.form("login_form"):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 📋 Acesso ao Sistema")
            
            # Seleção de modo de operação
            modo_operacao = st.selectbox(
                "🌐 Modo de Operação:",
                ["completo", "cloud"],
                index=0,  # Sempre selecionar "completo" por padrão
                format_func=lambda x: "💻 Completo (Local)" if x == "completo" else "☁️ Cloud (Otimizado)",
                help="Completo: Acesso total aos dados | Cloud: Dados otimizados para melhor performance"
            )
            
            usuario = st.text_input("👤 Usuário:", placeholder="Digite seu usuário")
            senha = st.text_input("🔑 Senha:", type="password", placeholder="Digite sua senha")
            
            col_login, col_limpar = st.columns(2)
            
            with col_login:
                if st.form_submit_button("🚀 Entrar", use_container_width=True, type="primary"):
                    if usuario and senha:
                        if fazer_login(usuario, senha, modo_operacao):
                            st.success("✅ Login realizado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Usuário ou senha incorretos!")
                    else:
                        st.error("❌ Preencha todos os campos!")
            
            with col_limpar:
                if st.form_submit_button("🔄 Limpar", use_container_width=True):
                    st.rerun()
    
    # Informações sobre o sistema
    st.markdown("---")
    st.info("💡 **Sistema de Análise Financeira KE5Z** - Acesso restrito a usuários autorizados")

def fazer_login(usuario: str, senha: str, modo_operacao: str) -> bool:
    """Realiza o login do usuário"""
    usuarios = carregar_usuarios()
    
    if usuario in usuarios:
        if verificar_senha(senha, usuarios[usuario]['senha_hash']):
            # Login bem-sucedido
            st.session_state.autenticado = True
            st.session_state.usuario_nome = usuario
            st.session_state.usuario_tipo = usuarios[usuario].get('tipo', 'usuario')
            st.session_state.modo_operacao = modo_operacao
            return True
    
    return False

def exibir_header_usuario():
    """Exibe o header com informações do usuário"""
    if 'usuario_nome' in st.session_state:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            tipo_icon = "👑" if st.session_state.get('usuario_tipo') == 'administrador' else "👥"
            st.write(f"{tipo_icon} **Usuário:** {st.session_state.usuario_nome}")
        
        with col2:
            modo_icon = "☁️" if st.session_state.get('modo_operacao') == 'cloud' else "💻"
            modo_text = "Cloud" if st.session_state.get('modo_operacao') == 'cloud' else "Completo"
            st.write(f"{modo_icon} **Modo:** {modo_text}")
        
        with col3:
            if st.button("🚪 Logout", use_container_width=True):
                logout()

def logout():
    """Realiza logout do usuário"""
    # Limpar sessão
    for key in ['autenticado', 'usuario_nome', 'usuario_tipo', 'modo_operacao']:
        if key in st.session_state:
            del st.session_state[key]
    
    st.success("✅ Logout realizado com sucesso!")
    st.rerun()

def eh_administrador() -> bool:
    """Verifica se o usuário atual é administrador"""
    return st.session_state.get('usuario_tipo') == 'administrador'

def verificar_status_aprovado(usuario: str) -> bool:
    """Verifica se o usuário está aprovado"""
    usuarios = carregar_usuarios()
    if usuario in usuarios:
        return usuarios[usuario].get('status') == 'aprovado'
    return False

def get_modo_operacao() -> str:
    """Retorna o modo de operação atual"""
    return st.session_state.get('modo_operacao', 'completo')

def is_modo_cloud() -> bool:
    """Verifica se está no modo cloud"""
    return get_modo_operacao() == 'cloud'

def get_usuarios_cloud() -> Dict[str, Any]:
    """Retorna usuários para modo cloud"""
    return carregar_usuarios()

def adicionar_usuario_simples(usuario: str, senha: str, tipo: str) -> tuple[bool, str]:
    """Adiciona um novo usuário"""
    usuarios = carregar_usuarios()
    
    if usuario in usuarios:
        return False, "❌ Usuário já existe!"
    
    if len(senha) < 4:
        return False, "❌ Senha deve ter pelo menos 4 caracteres!"
    
    usuarios[usuario] = {
        "senha_hash": criar_hash_senha(senha),
        "tipo": tipo,
        "status": "aprovado",
        "data_criacao": datetime.now().isoformat(),
        "aprovado_em": datetime.now().isoformat()
    }
    
    if salvar_usuarios(usuarios):
        return True, f"✅ Usuário '{usuario}' criado com sucesso!"
    else:
        return False, "❌ Erro ao salvar usuário!"

def salvar_usuario_json(usuario: str, senha: str, tipo: str) -> tuple[bool, str]:
    """Salva usuário no JSON (alias para compatibilidade)"""
    return adicionar_usuario_simples(usuario, senha, tipo)

def listar_usuarios_json() -> Dict[str, Any]:
    """Lista usuários do JSON (alias para compatibilidade)"""
    return carregar_usuarios()

# Funções de compatibilidade com o código existente
def get_usuarios_cloud() -> Dict[str, Any]:
    """Retorna usuários para modo cloud"""
    return carregar_usuarios()

def adicionar_usuario_simples(usuario: str, senha: str, tipo: str) -> tuple[bool, str]:
    """Adiciona usuário simples"""
    try:
        usuarios = carregar_usuarios()
        
        # Verificar se usuário já existe
        if usuario in usuarios:
            return False, f"Usuário '{usuario}' já existe!"
        
        # Criar hash da senha
        senha_hash = criar_hash_senha(senha)
        
        # Adicionar usuário
        usuarios[usuario] = {
            'senha_hash': senha_hash,
            'tipo': tipo,
            'status': 'pendente',
            'data_criacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_aprovacao': None
        }
        
        # Salvar no arquivo
        salvar_usuarios(usuarios)
        
        return True, f"Usuário '{usuario}' criado com sucesso!"
        
    except Exception as e:
        return False, f"Erro ao criar usuário: {str(e)}"
'''
    
    st.code(codigo_auth, language='python')



# Mensagem final
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-top: 2rem;">
    <h3 style="color: white; margin: 0;">🎯 Dashboard KE5Z v2.04</h3>
    <p style="color: #f0f0f0; margin: 0.5rem 0;">
        Aplicação Desktop completa de análise financeira com extração automática
    </p>
    <p style="color: #e0e0e0; font-size: 0.9rem; margin: 0;">
        Desenvolvido como executável independente para máxima portabilidade
    </p>
    <p style="color: #d0d0d0; font-size: 0.8rem; margin-top: 1rem;">
        💻 4.500+ linhas de código • ⚡ 68% otimização • 🖥️ Aplicação Desktop • 🔄 Extração automática • 📊 9 páginas completas • 🎯 15+ filtros avançados • 🗂️ Multi-ano
    </p>
</div>
""", unsafe_allow_html=True)

# Rodapé com versão
exibir_rodape_versao()
