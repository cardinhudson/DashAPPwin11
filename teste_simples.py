import streamlit as st
import sys
import os

# Configuração básica
st.set_page_config(
    page_title="Teste Dashboard KE5Z",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Teste Dashboard KE5Z")
st.write("Se você está vendo esta página, o Streamlit está funcionando!")

# Informações do sistema
st.subheader("Informações do Sistema")
st.write(f"Python: {sys.version}")
st.write(f"Streamlit: {st.__version__}")
st.write(f"Diretório atual: {os.getcwd()}")

# Teste de dados
st.subheader("Teste de Dados")
try:
    import pandas as pd
    import numpy as np
    
    # Criar dados de teste
    df = pd.DataFrame({
        'Data': pd.date_range('2025-01-01', periods=10),
        'Valor': np.random.randn(10).cumsum(),
        'Categoria': ['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A']
    })
    
    st.write("✅ Pandas funcionando!")
    st.dataframe(df)
    
    # Gráfico simples
    st.line_chart(df.set_index('Data')['Valor'])
    
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")

st.success("🎉 Teste concluído com sucesso!")



