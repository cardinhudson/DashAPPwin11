"""
Script de diagnóstico para verificar problemas com o Streamlit
"""
import sys
import os

print("=" * 60)
print("DIAGNÓSTICO STREAMLIT - Dashboard KE5Z")
print("=" * 60)

# 1. Verificar Python
print("\n1. Verificando Python...")
print(f"   Versão Python: {sys.version}")

# 2. Verificar Streamlit
print("\n2. Verificando Streamlit...")
try:
    import streamlit as st
    print(f"   ✅ Streamlit instalado: {st.__version__}")
except ImportError as e:
    print(f"   ❌ Streamlit NÃO instalado: {e}")
    sys.exit(1)

# 3. Verificar imports do app.py
print("\n3. Verificando imports do app.py...")
try:
    import pandas as pd
    print("   ✅ pandas OK")
except ImportError as e:
    print(f"   ❌ pandas NÃO instalado: {e}")

try:
    import altair as alt
    print("   ✅ altair OK")
except ImportError as e:
    print(f"   ❌ altair NÃO instalado: {e}")

try:
    from auth_simple import verificar_autenticacao
    print("   ✅ auth_simple OK")
except ImportError as e:
    print(f"   ❌ auth_simple NÃO encontrado: {e}")

# 4. Verificar arquivos de dados
print("\n4. Verificando arquivos de dados...")
base_path = os.path.dirname(os.path.abspath(__file__))
arquivos_necessarios = [
    "KE5Z/KE5Z.parquet",
    "KE5Z/KE5Z_main.parquet",
    "KE5Z/KE5Z_others.parquet"
]

for arquivo in arquivos_necessarios:
    caminho = os.path.join(base_path, arquivo)
    if os.path.exists(caminho):
        tamanho = os.path.getsize(caminho) / (1024 * 1024)
        print(f"   ✅ {arquivo} existe ({tamanho:.2f} MB)")
    else:
        print(f"   ⚠️  {arquivo} NÃO encontrado")

# 5. Verificar app.py
print("\n5. Verificando app.py...")
app_path = os.path.join(base_path, "app.py")
if os.path.exists(app_path):
    print(f"   ✅ app.py existe")
    # Verificar sintaxe
    try:
        with open(app_path, 'r', encoding='utf-8') as f:
            compile(f.read(), app_path, 'exec')
        print("   ✅ Sintaxe do app.py está correta")
    except SyntaxError as e:
        print(f"   ❌ Erro de sintaxe no app.py: {e}")
else:
    print(f"   ❌ app.py NÃO encontrado")

# 6. Verificar porta 8501
print("\n6. Verificando porta 8501...")
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 8501))
sock.close()
if result == 0:
    print("   ⚠️  Porta 8501 está em uso")
else:
    print("   ✅ Porta 8501 está livre")

print("\n" + "=" * 60)
print("DIAGNÓSTICO CONCLUÍDO")
print("=" * 60)
print("\nPara executar o Streamlit, use:")
print("  streamlit run app.py")
print("\nOu use o arquivo batch:")
print("  ABRIR_DASHBOARD.bat")





