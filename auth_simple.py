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
import glob
from datetime import datetime
from typing import Dict, Any, Optional, List

# Função para determinar diretório base
def get_data_dir():
    """Retorna o diretório onde os arquivos de dados devem ser salvos"""
    if hasattr(sys, '_MEIPASS'):
        # No executável: salvar no diretório do executável (fora do _internal)
        # CORREÇÃO CRÍTICA: Usar os.path.abspath para garantir caminho absoluto correto
        # mesmo quando o executável é movido para outro local
        try:
            # Obter caminho absoluto do executável
            exe_path = os.path.abspath(sys.executable)
            exe_dir = os.path.dirname(exe_path)
            
            # Verificar se o diretório existe e é válido
            if os.path.exists(exe_dir) and os.path.isdir(exe_dir):
                return exe_dir
            else:
                # Se não existe, tentar criar ou usar diretório atual
                try:
                    os.makedirs(exe_dir, exist_ok=True)
                    return exe_dir
                except Exception:
                    # Fallback: usar diretório atual de trabalho
                    return os.path.abspath(os.getcwd())
        except Exception as e:
            # Fallback em caso de erro: usar diretório atual
            return os.path.abspath(os.getcwd())
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
            
            usuario = st.text_input("👤 Usuário:", placeholder="Digite seu usuário", value="admin")
            senha = st.text_input("🔑 Senha:", type="password", placeholder="Digite sua senha", value="admin123")
            
            # Apenas um botão de submit no formulário
            submitted = st.form_submit_button("🚀 Entrar", use_container_width=True, type="primary")
            
            # Processar login quando o formulário for submetido
            if submitted:
                if usuario and senha:
                    if fazer_login(usuario, senha, modo_operacao):
                        st.success("✅ Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha incorretos!")
                else:
                    st.error("❌ Preencha todos os campos!")
    
    # Botão limpar fora do formulário
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Limpar", use_container_width=True):
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
        col1, col2, col3 = st.columns([2.5, 1.2, 0.8])
        
        with col1:
            tipo_icon = "👑" if st.session_state.get('usuario_tipo') == 'administrador' else "👥"
            st.markdown(f"{tipo_icon} **Usuário:** {st.session_state.usuario_nome}")
        
        with col2:
            modo_icon = "☁️" if st.session_state.get('modo_operacao') == 'cloud' else "💻"
            modo_text = "Cloud" if st.session_state.get('modo_operacao') == 'cloud' else "Local"
            st.markdown(f"{modo_icon} **Modo:** {modo_text}")
        
        with col3:
            if st.button("🚪 Sair", use_container_width=True, key="logout_btn"):
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

# ================== FUNÇÕES DE VERSÃO E ÚLTIMA EXTRAÇÃO ==================

VERSION_FILE = os.path.join(DATA_DIR, "versao_projeto.json")
ULTIMA_EXTRACAO_FILE = os.path.join(DATA_DIR, "ultima_extracao.json")
HASH_PAGES_FILE = os.path.join(DATA_DIR, "hash_pages.json")

def carregar_versao() -> Dict[str, Any]:
    """Carrega informações de versão do projeto"""
    try:
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Criar versão inicial
            agora = datetime.now()
            versao_inicial = {
                "versao": "2.0",
                "mes_ano_atualizacao": agora.strftime("%m/%Y"),
                "data_atualizacao": agora.isoformat()
            }
            salvar_versao(versao_inicial)
            return versao_inicial
    except Exception as e:
        # Em caso de erro, retornar versão padrão
        agora = datetime.now()
        return {
            "versao": "2.0",
            "mes_ano_atualizacao": agora.strftime("%m/%Y"),
            "data_atualizacao": agora.isoformat()
        }

def salvar_versao(dados: Dict[str, Any]) -> bool:
    """Salva informações de versão do projeto"""
    try:
        with open(VERSION_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def incrementar_versao_automatica(versao_atual: str) -> str:
    """Incrementa a versão seguindo a lógica: 2.0 → 2.01 → 2.02 → ... → 2.09 → 2.1 → ... → 2.99 → 3.0
    
    Args:
        versao_atual: Versão atual no formato "X.Y" ou "X.YY"
    
    Returns:
        Nova versão no formato correto
    """
    try:
        versao_num = float(versao_atual)
        parte_inteira = int(versao_num)
        parte_decimal = versao_num - parte_inteira
        
        # Incrementar 0.01
        nova_versao_num = versao_num + 0.01
        
        # Se chegou em X.99 ou mais, arredondar para (X+1).0
        nova_parte_decimal = nova_versao_num - int(nova_versao_num)
        if nova_parte_decimal >= 0.995:  # 0.99 + 0.01 = 1.00, arredondar para próximo inteiro
            nova_versao = f"{int(nova_versao_num) + 1}.0"
        else:
            # Formatar corretamente
            nova_parte_inteira = int(nova_versao_num)
            nova_decimal_valor = int(round(nova_parte_decimal * 100))
            
            if nova_decimal_valor == 0:
                nova_versao = f"{nova_parte_inteira}.0"
            elif nova_decimal_valor < 10:
                # Formato: X.01, X.02, ..., X.09
                nova_versao = f"{nova_parte_inteira}.{nova_decimal_valor:02d}"
            else:
                # Formato: X.1, X.11, X.12, ..., X.99
                # Se termina em 0, remover (X.10 → X.1, mas X.11 → X.11)
                if nova_decimal_valor % 10 == 0:
                    nova_versao = f"{nova_parte_inteira}.{nova_decimal_valor // 10}"
                else:
                    nova_versao = f"{nova_parte_inteira}.{nova_decimal_valor}"
        
        return nova_versao
    except Exception:
        # Em caso de erro, retornar versão incrementada simples
        try:
            versao_num = float(versao_atual)
            nova = versao_num + 0.01
            if nova - int(nova) >= 0.995:
                return f"{int(nova) + 1}.0"
            else:
                decimal = int(round((nova - int(nova)) * 100))
                if decimal == 0:
                    return f"{int(nova)}.0"
                elif decimal < 10:
                    return f"{int(nova)}.{decimal:02d}"
                elif decimal % 10 == 0:
                    return f"{int(nova)}.{decimal // 10}"
                else:
                    return f"{int(nova)}.{decimal}"
        except Exception:
            return "2.0"

def atualizar_versao_projeto() -> bool:
    """Atualiza a versão do projeto automaticamente (incrementa 0.01)
    Segue a lógica: 2.0 → 2.01 → 2.02 → ... → 2.09 → 2.1 → ... → 2.99 → 3.0
    """
    try:
        versao_atual = carregar_versao()
        versao_str = versao_atual.get("versao", "2.0")
        nova_versao_str = incrementar_versao_automatica(versao_str)
        
        agora = datetime.now()
        nova_versao_data = {
            "versao": nova_versao_str,
            "mes_ano_atualizacao": agora.strftime("%m/%Y"),
            "data_atualizacao": agora.isoformat()
        }
        
        return salvar_versao(nova_versao_data)
    except Exception:
        return False

def definir_versao_base(nova_versao_base: str) -> bool:
    """Define uma nova versão base (para modificações grandes)
    Exemplo: definir_versao_base("3.0") recomeça a contagem de 3.0
    
    Args:
        nova_versao_base: Nova versão base (ex: "3.0", "4.0")
    
    Returns:
        True se salvou com sucesso, False caso contrário
    """
    try:
        agora = datetime.now()
        nova_versao_data = {
            "versao": nova_versao_base,
            "mes_ano_atualizacao": agora.strftime("%m/%Y"),
            "data_atualizacao": agora.isoformat()
        }
        
        return salvar_versao(nova_versao_data)
    except Exception:
        return False

def calcular_hash_arquivo(caminho_arquivo: str) -> Optional[str]:
    """Calcula hash MD5 de um arquivo"""
    try:
        if not os.path.exists(caminho_arquivo):
            return None
        hash_md5 = hashlib.md5()
        with open(caminho_arquivo, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        return None

def calcular_hash_pages() -> Dict[str, str]:
    """Calcula hash de todos os arquivos .py na pasta pages/"""
    hash_pages = {}
    try:
        # Determinar caminho da pasta pages
        if hasattr(sys, '_MEIPASS'):
            # No executável: tentar _internal primeiro
            try:
                meipass_path = os.path.abspath(sys._MEIPASS)
                pages_path = os.path.join(meipass_path, "pages")
                if os.path.exists(pages_path):
                    for arquivo in glob.glob(os.path.join(pages_path, "*.py")):
                        hash_arquivo = calcular_hash_arquivo(arquivo)
                        if hash_arquivo:
                            hash_pages[os.path.basename(arquivo)] = hash_arquivo
                    if hash_pages:
                        return hash_pages
            except Exception:
                pass
            
            # Fallback: diretório do executável
            try:
                exe_path = os.path.abspath(sys.executable)
                exe_dir = os.path.dirname(exe_path)
                pages_path_exe = os.path.join(exe_dir, "pages")
                pages_path_internal = os.path.join(exe_dir, "_internal", "pages")
                for pages_path in [pages_path_exe, pages_path_internal]:
                    if os.path.exists(pages_path):
                        for arquivo in glob.glob(os.path.join(pages_path, "*.py")):
                            hash_arquivo = calcular_hash_arquivo(arquivo)
                            if hash_arquivo:
                                hash_pages[os.path.basename(arquivo)] = hash_arquivo
                        if hash_pages:
                            return hash_pages
            except Exception:
                pass
        else:
            # Em desenvolvimento
            script_dir = os.path.dirname(os.path.abspath(__file__))
            pages_path = os.path.join(script_dir, "pages")
            if os.path.exists(pages_path):
                for arquivo in glob.glob(os.path.join(pages_path, "*.py")):
                    hash_arquivo = calcular_hash_arquivo(arquivo)
                    if hash_arquivo:
                        hash_pages[os.path.basename(arquivo)] = hash_arquivo
    except Exception:
        pass
    
    return hash_pages

def carregar_hash_pages_anterior() -> Dict[str, str]:
    """Carrega hash anterior das páginas"""
    try:
        if os.path.exists(HASH_PAGES_FILE):
            with open(HASH_PAGES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def salvar_hash_pages(hash_pages: Dict[str, str]) -> bool:
    """Salva hash atual das páginas"""
    try:
        with open(HASH_PAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(hash_pages, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def verificar_e_atualizar_versao_automatica() -> bool:
    """Verifica se houve mudanças nas páginas e atualiza versão automaticamente
    Retorna True se atualizou a versão, False caso contrário
    """
    try:
        # Calcular hash atual das páginas
        hash_atual = calcular_hash_pages()
        if not hash_atual:
            return False
        
        # Carregar hash anterior
        hash_anterior = carregar_hash_pages_anterior()
        
        # Comparar hashes
        if hash_atual != hash_anterior:
            # Houve mudança, atualizar versão
            if atualizar_versao_projeto():
                # Salvar novo hash
                salvar_hash_pages(hash_atual)
                return True
        
        return False
    except Exception:
        return False

def carregar_ultima_extracao() -> Dict[str, Any]:
    """Carrega data/hora da última extração"""
    try:
        if os.path.exists(ULTIMA_EXTRACAO_FILE):
            with open(ULTIMA_EXTRACAO_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "data_hora": None,
                "data_hora_formatada": "Nunca executada"
            }
    except Exception:
        return {
            "data_hora": None,
            "data_hora_formatada": "Nunca executada"
        }

def salvar_ultima_extracao() -> bool:
    """Salva data/hora da última extração"""
    try:
        agora = datetime.now()
        dados = {
            "data_hora": agora.isoformat(),
            "data_hora_formatada": agora.strftime("%d/%m/%Y %H:%M:%S")
        }
        with open(ULTIMA_EXTRACAO_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def exibir_info_ultima_extracao():
    """Exibe informação da última extração no topo da página
    Baseado na data do último arquivo .txt na pasta Extracoes/KE5Z/
    Usa a mesma lógica do Extracao.py para garantir portabilidade
    """
    try:
        # Função para obter caminho base (IDÊNTICA ao Extracao.py)
        def get_base_path_for_extraction():
            """Retorna caminho base para encontrar pasta Extracoes/KE5Z
            Usa a mesma estratégia do Extracao.py
            """
            if hasattr(sys, '_MEIPASS'):
                # Rodando no executável PyInstaller
                # 1. Primeiro tentar _internal (onde dados são copiados no build)
                try:
                    meipass_path = os.path.abspath(sys._MEIPASS)
                    if os.path.exists(meipass_path):
                        # Verificar se existe pasta Extracoes em _internal
                        extracoes_path = os.path.join(meipass_path, "Extracoes", "KE5Z")
                        if os.path.exists(extracoes_path):
                            return extracoes_path
                except Exception:
                    pass
                
                # 2. Fallback: tentar diretório do executável (para quando pasta é movida)
                try:
                    exe_path = os.path.abspath(sys.executable)
                    exe_dir = os.path.dirname(exe_path)
                    if os.path.exists(exe_dir):
                        # Verificar se existe pasta Extracoes ou _internal/Extracoes no diretório do executável
                        extracoes_path_exe = os.path.join(exe_dir, "Extracoes", "KE5Z")
                        extracoes_path_internal = os.path.join(exe_dir, "_internal", "Extracoes", "KE5Z")
                        if os.path.exists(extracoes_path_exe):
                            return extracoes_path_exe
                        elif os.path.exists(extracoes_path_internal):
                            return extracoes_path_internal
                except Exception:
                    pass
                
                # 3. Último fallback: usar _MEIPASS mesmo que não exista
                try:
                    meipass_path = os.path.abspath(sys._MEIPASS)
                    extracoes_path = os.path.join(meipass_path, "Extracoes", "KE5Z")
                    return extracoes_path
                except Exception:
                    pass
            else:
                # Rodando em desenvolvimento
                script_dir = os.path.dirname(os.path.abspath(__file__))
                return os.path.join(script_dir, "Extracoes", "KE5Z")
            return None
        
        # Buscar último arquivo .txt na pasta KE5Z
        pasta_ke5z = get_base_path_for_extraction()
        data_ultimo_arquivo = None
        nome_ultimo_arquivo = None
        
        # Tentar múltiplas estratégias para encontrar os arquivos
        pastas_para_tentar = []
        
        if pasta_ke5z:
            pastas_para_tentar.append(pasta_ke5z)
        
        # Adicionar outras possíveis localizações
        if hasattr(sys, '_MEIPASS'):
            try:
                meipass_path = os.path.abspath(sys._MEIPASS)
                pastas_para_tentar.append(os.path.join(meipass_path, "Extracoes", "KE5Z"))
            except Exception:
                pass
            
            try:
                exe_path = os.path.abspath(sys.executable)
                exe_dir = os.path.dirname(exe_path)
                pastas_para_tentar.append(os.path.join(exe_dir, "Extracoes", "KE5Z"))
                pastas_para_tentar.append(os.path.join(exe_dir, "_internal", "Extracoes", "KE5Z"))
            except Exception:
                pass
        else:
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                pastas_para_tentar.append(os.path.join(script_dir, "Extracoes", "KE5Z"))
            except Exception:
                pass
        
        # Remover duplicatas e None
        pastas_para_tentar = [p for p in pastas_para_tentar if p and os.path.exists(p)]
        pastas_para_tentar = list(dict.fromkeys(pastas_para_tentar))  # Remove duplicatas
        
        # Tentar cada pasta até encontrar arquivos
        for pasta_teste in pastas_para_tentar:
            try:
                if os.path.exists(pasta_teste):
                    arquivos_txt = [f for f in os.listdir(pasta_teste) if f.endswith('.txt')]
                    if arquivos_txt:
                        # Pegar o arquivo mais recente
                        arquivos_com_data = []
                        for arquivo in arquivos_txt:
                            caminho_arquivo = os.path.join(pasta_teste, arquivo)
                            try:
                                if os.path.isfile(caminho_arquivo):  # Verificar se é arquivo, não pasta
                                    data_modificacao = os.path.getmtime(caminho_arquivo)
                                    arquivos_com_data.append((arquivo, data_modificacao))
                            except Exception:
                                continue
                        
                        if arquivos_com_data:
                            # Ordenar por data de modificação (mais recente primeiro)
                            arquivos_com_data.sort(key=lambda x: x[1], reverse=True)
                            nome_ultimo_arquivo, timestamp = arquivos_com_data[0]
                            data_ultimo_arquivo = datetime.fromtimestamp(timestamp)
                            break  # Encontrou, sair do loop
            except Exception:
                continue
        
        # Se encontrou arquivo, usar sua data; senão, usar data salva
        if data_ultimo_arquivo:
            data_formatada = data_ultimo_arquivo.strftime("%d/%m/%Y %H:%M:%S")
        else:
            # Fallback: usar data salva da última extração executada
            ultima_extracao = carregar_ultima_extracao()
            data_formatada = ultima_extracao.get("data_hora_formatada", "Nunca executada")
        
        st.info(f"🕒 **Última Extração de Dados:** {data_formatada}")
    except Exception:
        # Em caso de erro, não exibir nada (não quebrar a página)
        pass

def exibir_rodape_versao():
    """Exibe rodapé com versão do projeto e responsáveis"""
    try:
        versao_info = carregar_versao()
        versao = versao_info.get("versao", "2.0")
        mes_ano = versao_info.get("mes_ano_atualizacao", datetime.now().strftime("%m/%Y"))
        
        # Carregar dados da equipe para pegar nomes dos responsáveis
        def get_base_path_for_equipe():
            """Retorna caminho base para encontrar dados_equipe.json"""
            if hasattr(sys, '_MEIPASS'):
                try:
                    meipass_path = os.path.abspath(sys._MEIPASS)
                    dados_path = os.path.join(meipass_path, "dados_equipe.json")
                    if os.path.exists(dados_path):
                        return meipass_path
                except Exception:
                    pass
                
                try:
                    exe_path = os.path.abspath(sys.executable)
                    exe_dir = os.path.dirname(exe_path)
                    dados_path_exe = os.path.join(exe_dir, "dados_equipe.json")
                    dados_path_internal = os.path.join(exe_dir, "_internal", "dados_equipe.json")
                    if os.path.exists(dados_path_exe):
                        return exe_dir
                    elif os.path.exists(dados_path_internal):
                        return os.path.join(exe_dir, "_internal")
                except Exception:
                    pass
            else:
                return os.path.dirname(os.path.abspath(__file__))
            return None
        
        # Tentar carregar dados da equipe
        responsaveis = "Hudson Cardin e Lauro Paiva Junior"  # Padrão
        try:
            base_path_equipe = get_base_path_for_equipe()
            if base_path_equipe:
                dados_equipe_path = os.path.join(base_path_equipe, "dados_equipe.json")
                if os.path.exists(dados_equipe_path):
                    with open(dados_equipe_path, 'r', encoding='utf-8') as f:
                        dados_equipe = json.load(f)
                        nomes = []
                        if dados_equipe.get('hudson'):
                            nomes.append("Hudson Cardin")
                        if dados_equipe.get('lauro'):
                            nomes.append("Lauro Paiva Junior")
                        if nomes:
                            responsaveis = " e ".join(nomes)
        except Exception:
            pass
        
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: #f0f0f0; border-radius: 5px; margin-top: 2rem;">
            <p style="color: #666; font-size: 0.9rem; margin: 0;">
                📊 Dashboard KE5Z - Versão {versao} | Atualizado em {mes_ano}
            </p>
            <p style="color: #666; font-size: 0.85rem; margin: 0.3rem 0 0 0;">
                👥 Desenvolvido por: {responsaveis}
            </p>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        pass
