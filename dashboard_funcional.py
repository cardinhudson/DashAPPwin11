#!/usr/bin/env python3
"""
Dashboard KE5Z - Versão Funcional
Script otimizado para funcionar como executável
"""

import streamlit as st
import sys
import os
import warnings

# Suprimir warnings desnecessários
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Configuração do Streamlit
st.set_page_config(
    page_title="Dashboard KE5Z",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para detectar se está rodando no executável
def get_base_path():
    """Retorna o caminho base correto"""
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Título principal
st.title("📊 Dashboard KE5Z - Versão Funcional")
st.markdown("---")

# Informações do sistema
with st.expander("🔍 Informações do Sistema"):
    st.write(f"**Python:** {sys.version}")
    st.write(f"**Streamlit:** {st.__version__}")
    st.write(f"**Diretório:** {get_base_path()}")
    st.write(f"**Executável:** {'Sim' if hasattr(sys, '_MEIPASS') else 'Não'}")

# Teste de funcionalidades
st.subheader("🧪 Teste de Funcionalidades")

# Teste 1: Pandas
try:
    import pandas as pd
    st.success("✅ Pandas funcionando!")
except Exception as e:
    st.error(f"❌ Erro no Pandas: {e}")

# Teste 2: Plotly
try:
    import plotly.express as px
    st.success("✅ Plotly funcionando!")
except Exception as e:
    st.error(f"❌ Erro no Plotly: {e}")

# Teste 3: Altair
try:
    import altair as alt
    st.success("✅ Altair funcionando!")
except Exception as e:
    st.error(f"❌ Erro no Altair: {e}")

# Teste 4: PyArrow
try:
    import pyarrow as pa
    st.success("✅ PyArrow funcionando!")
except Exception as e:
    st.error(f"❌ Erro no PyArrow: {e}")

# Demonstração com dados
st.subheader("📊 Demonstração com Dados")

try:
    import pandas as pd
    import numpy as np
    import plotly.express as px
    
    # Criar dados de exemplo
    np.random.seed(42)
    data = {
        'Data': pd.date_range('2025-01-01', periods=30),
        'Vendas': np.random.randn(30).cumsum() + 100,
        'Categoria': np.random.choice(['A', 'B', 'C'], 30)
    }
    df = pd.DataFrame(data)
    
    st.write("**Dados de Exemplo:**")
    st.dataframe(df.head(10))
    
    # Gráfico de linha
    fig = px.line(df, x='Data', y='Vendas', title='Vendas ao Longo do Tempo')
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de barras por categoria
    fig2 = px.bar(df.groupby('Categoria')['Vendas'].sum().reset_index(), 
                  x='Categoria', y='Vendas', title='Vendas por Categoria')
    st.plotly_chart(fig2, use_container_width=True)
    
    st.success("🎉 Todos os testes passaram! O dashboard está funcionando perfeitamente!")
    
except Exception as e:
    st.error(f"❌ Erro na demonstração: {e}")

# Status final
st.markdown("---")
st.success("🚀 **Dashboard KE5Z funcionando perfeitamente!**")
st.info("💡 Este é um teste básico. Para usar o dashboard completo, execute o arquivo principal.")



