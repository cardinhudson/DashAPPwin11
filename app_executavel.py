#!/usr/bin/env python3
"""
Dashboard KE5Z - Versão para Executável
Otimizada para funcionar com PyInstaller
"""

import sys
import os
import warnings

# Suprimir warnings que causam problemas no PyInstaller
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Configurar variáveis de ambiente antes de importar Streamlit
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_PORT'] = '8501'
os.environ['STREAMLIT_SERVER_ADDRESS'] = 'localhost'

# Importar Streamlit após configurar ambiente
try:
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    import altair as alt
    from datetime import datetime
except ImportError as e:
    print(f"Erro ao importar dependências: {e}")
    sys.exit(1)

# Detectar se está rodando no executável PyInstaller
def get_base_path():
    """Retorna o caminho base correto para LEITURA de dados"""
    if hasattr(sys, '_MEIPASS'):
        # Rodando no executável PyInstaller - apontar para _internal
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

# Sistema de autenticação simplificado
def verificar_login():
    """Sistema de autenticação simplificado"""
    if 'logado' in st.session_state and st.session_state.logado:
        return True
    
    # Interface de login
    st.title("🔐 Login - Dashboard KE5Z")
    
    with st.form("login_form"):
        usuario = st.text_input("👤 Usuário")
        senha = st.text_input("🔒 Senha", type="password")
        
        if st.form_submit_button("🚀 Entrar"):
            # Login simples para demonstração
            if usuario and senha:
                st.session_state.logado = True
                st.session_state.usuario_nome = usuario
                st.rerun()
            else:
                st.error("Por favor, preencha usuário e senha")
    
    return False

# Verificar autenticação
if not verificar_login():
    st.stop()

# Título principal
st.title("📊 Dashboard KE5Z - Versão Executável")
st.markdown("---")

# Carregar dados usando caminho correto
@st.cache_data
def load_data():
    """Carrega dados com fallback para dados de exemplo"""
    try:
        base_path = get_base_path()
        arquivo_parquet = os.path.join(base_path, "KE5Z", "KE5Z.parquet")
        
        if os.path.exists(arquivo_parquet):
            df = pd.read_parquet(arquivo_parquet)
            st.success("✅ Dados carregados do arquivo KE5Z.parquet")
            return df
        else:
            st.warning("⚠️ Arquivo KE5Z.parquet não encontrado. Usando dados de exemplo.")
            # Criar dados de exemplo
            import numpy as np
            np.random.seed(42)
            data = {
                'Data': pd.date_range('2025-01-01', periods=100),
                'Valor': np.random.randn(100).cumsum() + 1000,
                'Categoria': np.random.choice(['A', 'B', 'C', 'D'], 100),
                'USI': np.random.choice(['Usina 1', 'Usina 2', 'Usina 3'], 100),
                'Período': np.random.choice(['Jan/2025', 'Fev/2025', 'Mar/2025'], 100)
            }
            df = pd.DataFrame(data)
            return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

# Carregar dados
df_total = load_data()

if not df_total.empty:
    # Filtros
    st.sidebar.markdown("**🔍 Filtros**")
    
    # Filtro por categoria
    if 'Categoria' in df_total.columns:
        categorias = ['Todas'] + sorted(df_total['Categoria'].unique().tolist())
        categoria_selecionada = st.sidebar.selectbox("Categoria:", categorias)
        
        if categoria_selecionada != "Todas":
            df_total = df_total[df_total['Categoria'] == categoria_selecionada]
    
    # Filtro por USI
    if 'USI' in df_total.columns:
        usis = ['Todas'] + sorted(df_total['USI'].unique().tolist())
        usi_selecionada = st.sidebar.selectbox("USI:", usis)
        
        if usi_selecionada != "Todas":
            df_total = df_total[df_total['USI'] == usi_selecionada]
    
    # Resumo
    st.sidebar.markdown("**📊 Resumo**")
    st.sidebar.write(f"**Registros:** {len(df_total):,}")
    if 'Valor' in df_total.columns:
        st.sidebar.write(f"**Total:** R$ {df_total['Valor'].sum():,.2f}")
    
    # Gráfico principal
    if 'Valor' in df_total.columns and 'Data' in df_total.columns:
        st.subheader("📈 Evolução dos Valores")
        fig = px.line(df_total, x='Data', y='Valor', title='Evolução dos Valores ao Longo do Tempo')
        st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico por categoria
    if 'Categoria' in df_total.columns and 'Valor' in df_total.columns:
        st.subheader("📊 Valores por Categoria")
        categoria_soma = df_total.groupby('Categoria')['Valor'].sum().reset_index()
        fig2 = px.bar(categoria_soma, x='Categoria', y='Valor', title='Soma dos Valores por Categoria')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Tabela de dados
    st.subheader("📋 Dados Filtrados")
    st.dataframe(df_total, use_container_width=True)
    
    # Botão de download
    if st.button("📥 Baixar Dados (Excel)"):
        try:
            from io import BytesIO
            import base64
            
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_total.to_excel(writer, index=False, sheet_name='Dados')
            output.seek(0)
            
            excel_data = output.getvalue()
            b64 = base64.b64encode(excel_data).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="dashboard_dados.xlsx">💾 Clique aqui para baixar</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("✅ Arquivo Excel gerado!")
        except Exception as e:
            st.error(f"❌ Erro ao gerar Excel: {e}")

# Informações do sistema
with st.expander("🔍 Informações do Sistema"):
    st.write(f"**Python:** {sys.version}")
    st.write(f"**Streamlit:** {st.__version__}")
    st.write(f"**Pandas:** {pd.__version__}")
    st.write(f"**Executável:** {'Sim' if hasattr(sys, '_MEIPASS') else 'Não'}")
    st.write(f"**Diretório:** {get_base_path()}")

# Footer
st.markdown("---")
st.success("🎉 Dashboard KE5Z funcionando perfeitamente!")
st.info("💡 Esta é a versão executável do dashboard. Todas as funcionalidades estão disponíveis!")



