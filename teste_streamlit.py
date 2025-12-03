"""
Script de teste para verificar se o Streamlit está funcionando
"""
import streamlit as st

st.set_page_config(
    page_title="Teste Streamlit",
    page_icon="📊",
    layout="wide"
)

st.title("✅ Teste Streamlit")
st.success("Se você está vendo esta mensagem, o Streamlit está funcionando corretamente!")

st.info("Agora vamos testar o app.py principal...")

