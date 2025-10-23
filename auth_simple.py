# -*- coding: utf-8 -*-
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
