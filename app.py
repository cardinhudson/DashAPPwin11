# %%
import streamlit as st
import pandas as pd
import os
import sys
import altair as alt
from io import BytesIO
import base64
import plotly.graph_objects as go
import hashlib
import warnings
from auth_simple import (verificar_autenticacao, exibir_header_usuario,
                         eh_administrador, verificar_status_aprovado,
                         get_usuarios_cloud, adicionar_usuario_simples, criar_hash_senha,
                         get_modo_operacao, is_modo_cloud)
from datetime import datetime

# Suprimir avisos do Streamlit quando executado fora do contexto
import logging
logging.getLogger('streamlit.runtime.scriptrunner_utils.script_run_context').setLevel(logging.ERROR)
logging.getLogger('streamlit.runtime.state.session_state_proxy').setLevel(logging.ERROR)

# Suprimir FutureWarnings do pandas
warnings.filterwarnings('ignore', category=FutureWarning)

# CORREÇÃO CRÍTICA: Garantir diretório de trabalho correto para portabilidade
# Quando o executável é movido para outro local, o diretório de trabalho pode estar errado
def ensure_working_directory():
    """Garante que o diretório de trabalho seja o diretório do executável"""
    if hasattr(sys, '_MEIPASS'):
        # No executável: mudar para o diretório do executável (não do _internal)
        # CORREÇÃO: Usar os.path.abspath() para garantir caminho absoluto correto
        # mesmo quando o executável é movido para outro local
        try:
            exe_path = os.path.abspath(sys.executable)
            exe_dir = os.path.dirname(exe_path)
            if os.path.exists(exe_dir):
                os.chdir(exe_dir)
        except Exception:
            # Fallback: usar diretório atual se houver problema
            pass
        # Limpar variáveis de ambiente que podem causar problemas
        for var in ['VIRTUAL_ENV', 'PYTHONHOME', 'CONDA_DEFAULT_ENV']:
            if var in os.environ:
                del os.environ[var]

# Executar imediatamente ao importar
ensure_working_directory()

# Detectar se está rodando no executável PyInstaller
def get_base_path():
    """Retorna o caminho base correto para LEITURA de dados
    
    Estratégia:
    1. No executável: primeiro tenta _internal (onde dados são copiados)
    2. Se não encontrar, tenta diretório do executável (para portabilidade)
    3. Em desenvolvimento: usa diretório do script
    """
    if hasattr(sys, '_MEIPASS'):
        # Rodando no executável PyInstaller
        # CORREÇÃO CRÍTICA: Tentar múltiplos locais para portabilidade
        
        # 1. Primeiro tentar _internal (onde dados são copiados no build)
        try:
            meipass_path = os.path.abspath(sys._MEIPASS)
            if os.path.exists(meipass_path):
                # Verificar se existe pasta KE5Z em _internal
                ke5z_path = os.path.join(meipass_path, "KE5Z")
                if os.path.exists(ke5z_path):
                    return meipass_path
        except Exception:
            pass
        
        # 2. Fallback: tentar diretório do executável (para quando pasta é movida)
        try:
            exe_path = os.path.abspath(sys.executable)
            exe_dir = os.path.dirname(exe_path)
            if os.path.exists(exe_dir):
                # Verificar se existe pasta KE5Z ou _internal/KE5Z no diretório do executável
                ke5z_path_exe = os.path.join(exe_dir, "KE5Z")
                ke5z_path_internal = os.path.join(exe_dir, "_internal", "KE5Z")
                if os.path.exists(ke5z_path_exe):
                    return exe_dir
                elif os.path.exists(ke5z_path_internal):
                    return os.path.join(exe_dir, "_internal")
        except Exception:
            pass
        
        # 3. Último fallback: usar _MEIPASS mesmo que não exista (pode ser temporário)
        try:
            return os.path.abspath(sys._MEIPASS)
        except Exception:
            return sys._MEIPASS
    else:
        # Rodando em desenvolvimento
        return os.path.dirname(os.path.abspath(__file__))

# Configuração otimizada da página para melhor performance
st.set_page_config(
    page_title="Dashboard KE5Z",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
# CORREÇÃO: Usar hash do arquivo para invalidar cache quando dados são atualizados
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
    
    # CORREÇÃO CRÍTICA: Tentar múltiplos locais para portabilidade
    # Lista de locais possíveis para procurar o arquivo
    locais_possiveis = []
    
    # 1. Local padrão (base_path/KE5Z/) - _internal onde dados são salvos
    locais_possiveis.append(os.path.join(base_path, "KE5Z", nome_arquivo))
    
    # 2. Se estiver no executável, tentar também diretório do executável (para portabilidade)
    if hasattr(sys, '_MEIPASS'):
        try:
            exe_path = os.path.abspath(sys.executable)
            exe_dir = os.path.dirname(exe_path)
            # Tentar exe_dir/KE5Z/ (fallback para portabilidade)
            locais_possiveis.append(os.path.join(exe_dir, "KE5Z", nome_arquivo))
            # Tentar exe_dir/_internal/KE5Z/
            locais_possiveis.append(os.path.join(exe_dir, "_internal", "KE5Z", nome_arquivo))
        except Exception:
            pass
    
    # Procurar arquivo nos locais possíveis (PRIORIDADE: diretório do executável primeiro)
    arquivo_parquet = None
    for local in locais_possiveis:
        if os.path.exists(local):
            arquivo_parquet = local
            break
    
    # Se não encontrou, usar o primeiro local (para mensagem de erro)
    if arquivo_parquet is None:
        arquivo_parquet = locais_possiveis[0]
    
    # CORREÇÃO: Usar caminho completo do arquivo como parte da chave do cache
    # O Streamlit já usa o caminho do arquivo na chave do cache automaticamente
    
    try:
        if not os.path.exists(arquivo_parquet):
            # Se arquivo específico não existe, tentar arquivo completo nos mesmos locais
            if arquivo_tipo != "completo":
                # Tentar encontrar arquivo completo
                arquivo_completo = None
                for base in [base_path]:
                    if hasattr(sys, '_MEIPASS'):
                        try:
                            exe_dir = os.path.dirname(os.path.abspath(sys.executable))
                            for base_alt in [base_path, exe_dir, os.path.join(exe_dir, "_internal")]:
                                caminho_completo = os.path.join(base_alt, "KE5Z", "KE5Z.parquet")
                                if os.path.exists(caminho_completo):
                                    arquivo_completo = caminho_completo
                                    break
                        except Exception:
                            pass
                    if arquivo_completo:
                        break
                    caminho_completo = os.path.join(base, "KE5Z", "KE5Z.parquet")
                    if os.path.exists(caminho_completo):
                        arquivo_completo = caminho_completo
                        break
                
                if arquivo_completo and os.path.exists(arquivo_completo):
                    st.warning(f"⚠️ Arquivo {nome_arquivo} não encontrado, carregando dados completos...")
                    df = pd.read_parquet(arquivo_completo)
                    # Aplicar filtro especial para main_filtered (cloud mode)
                    if arquivo_tipo == "main_filtered" and 'USI' in df.columns:
                        df = df[df['USI'] != 'Others'].copy()
                        st.sidebar.info(f"🔄 Filtro aplicado: {len(df):,} registros (Others removidos)")
                    return df
                else:
                    raise FileNotFoundError(f"Arquivo completo também não encontrado em nenhum local")
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

# OTIMIZAÇÃO: Cachear verificação de arquivos no session_state (persiste entre navegações)
# CORREÇÃO: Buscar arquivos na mesma ordem que load_data_optimized (priorizar diretório do executável)
base_path = get_base_path()

def verificar_arquivo_existe(nome_arquivo):
    """Verifica se arquivo existe nos locais possíveis (mesma ordem de load_data_optimized)"""
    locais_possiveis = []
    
    # 1. Local padrão (base_path/KE5Z/) - _internal onde dados são salvos
    locais_possiveis.append(os.path.join(base_path, "KE5Z", nome_arquivo))
    
    # 2. Se estiver no executável, tentar também diretório do executável (para portabilidade)
    if hasattr(sys, '_MEIPASS'):
        try:
            exe_path = os.path.abspath(sys.executable)
            exe_dir = os.path.dirname(exe_path)
            locais_possiveis.append(os.path.join(exe_dir, "KE5Z", nome_arquivo))
            locais_possiveis.append(os.path.join(exe_dir, "_internal", "KE5Z", nome_arquivo))
        except Exception:
            pass
    
    # Verificar se arquivo existe em algum local
    for local in locais_possiveis:
        if os.path.exists(local):
            return True
    return False

if 'arquivos_status_cache' not in st.session_state:
    arquivos_status = {}
    for tipo, nome in [("completo", "KE5Z.parquet"), ("main", "KE5Z_main.parquet"), ("others", "KE5Z_others.parquet")]:
        arquivos_status[tipo] = verificar_arquivo_existe(nome)
    st.session_state.arquivos_status_cache = arquivos_status
    st.session_state.base_path_cache = base_path
else:
    # Verificar se o base_path mudou ou se arquivos foram atualizados
    # CORREÇÃO: Sempre verificar novamente para detectar novos arquivos
    arquivos_status = {}
    for tipo, nome in [("completo", "KE5Z.parquet"), ("main", "KE5Z_main.parquet"), ("others", "KE5Z_others.parquet")]:
        arquivos_status[tipo] = verificar_arquivo_existe(nome)
    st.session_state.arquivos_status_cache = arquivos_status
    st.session_state.base_path_cache = base_path

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

# Widget de seleção com prioridade para dados completos
def get_default_index():
    """Retorna o índice padrão priorizando dados completos"""
    opcoes_values = [op[1] for op in opcoes_dados]
    
    # Prioridade: completo > main > main_filtered > others
    if "completo" in opcoes_values:
        return opcoes_values.index("completo")
    elif "main" in opcoes_values:
        return opcoes_values.index("main")
    elif "main_filtered" in opcoes_values:
        return opcoes_values.index("main_filtered")
    elif "others" in opcoes_values:
        return opcoes_values.index("others")
    else:
        return 0  # Primeiro disponível

# OTIMIZAÇÃO: Usar session_state para manter seleção e evitar reruns
if 'opcao_dados_selecionada' not in st.session_state:
    st.session_state.opcao_dados_selecionada = opcoes_dados[get_default_index()][1] if opcoes_dados else "completo"

opcao_selecionada = st.sidebar.selectbox(
    "Escolha o conjunto de dados:",
    options=[op[1] for op in opcoes_dados],
    format_func=lambda x: next(op[0] for op in opcoes_dados if op[1] == x),
    index=get_default_index() if st.session_state.opcao_dados_selecionada not in [op[1] for op in opcoes_dados] else [op[1] for op in opcoes_dados].index(st.session_state.opcao_dados_selecionada),
    key="selectbox_dados"
)
st.session_state.opcao_dados_selecionada = opcao_selecionada

# OTIMIZAÇÃO: Mostrar informações apenas se mudou (evitar reruns)
if 'opcao_dados_info_anterior' not in st.session_state or st.session_state.opcao_dados_info_anterior != opcao_selecionada:
    if opcao_selecionada == "main":
        st.sidebar.info("🎯 **Dados Principais** (sem Others)")
    elif opcao_selecionada == "main_filtered":
        st.sidebar.info("🎯 **Dados Filtrados** (Cloud)")
    elif opcao_selecionada == "others":
        st.sidebar.info("🔍 **Apenas Others**")
    else:
        st.sidebar.info("📊 **Dados Completos**")
    st.session_state.opcao_dados_info_anterior = opcao_selecionada

# OTIMIZAÇÃO: Cachear dados no session_state (persiste entre navegações)
cache_key = f"df_total_{opcao_selecionada}"
cache_loaded_key = f"df_total_loaded_{opcao_selecionada}"

# Verificar se precisa carregar (mudou opção ou não existe no cache)
if cache_key not in st.session_state or st.session_state.get('opcao_dados_anterior') != opcao_selecionada:
    # Carregar dados apenas se mudou a opção ou não está em cache
    try:
        with st.spinner("🔄 Carregando dados..."):
            df_total = load_data_optimized(opcao_selecionada)
            # Filtrar USI não nulo antes de cachear
            df_total = df_total[df_total['USI'].notna()].copy()
            st.session_state[cache_key] = df_total
            st.session_state.opcao_dados_anterior = opcao_selecionada
            st.session_state[cache_loaded_key] = True
        
        # Mostrar mensagem apenas na primeira vez ou quando muda
        st.sidebar.success("✅ Dados carregados com sucesso")
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
else:
    # Usar dados do cache (já filtrado)
    df_total = st.session_state[cache_key]
        

# NOTA: df_total já está filtrado no cache acima (USI não nulo)

# Header com informações do usuário e botão de logout
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.title("📊 Dashboard KE5Z")
st.subheader("Perímetro TC")

# Exibir header do usuário
exibir_header_usuario()

st.markdown("---")

# Filtros (COMPACTO)
st.sidebar.markdown("---")
st.sidebar.markdown("**🔍 Filtros**")

# Inicializar session_state para filtros se não existir
if 'filtro_usina' not in st.session_state:
    st.session_state.filtro_usina = ["Todos"]
if 'filtro_periodo' not in st.session_state:
    st.session_state.filtro_periodo = "Todos"
if 'filtro_centro_cst' not in st.session_state:
    st.session_state.filtro_centro_cst = "Todos"
if 'filtro_conta_contabil' not in st.session_state:
    st.session_state.filtro_conta_contabil = []
if 'filtros_principais' not in st.session_state:
    st.session_state.filtros_principais = {}
if 'filtros_avancados' not in st.session_state:
    st.session_state.filtros_avancados = {}

# OTIMIZAÇÃO: Cache de opções de filtros no session_state (persiste entre navegações)
def get_filter_options(df, column_name):
    """Obtém opções de filtro com cache no session_state"""
    # Usar hash do DataFrame para criar chave única
    import hashlib
    df_hash = hashlib.md5(str(df.shape).encode() + str(column_name).encode()).hexdigest()
    cache_key = f"filter_options_{column_name}_{df_hash}"
    
    if cache_key not in st.session_state:
        if column_name in df.columns:
            try:
                opcoes = ["Todos"] + sorted(df[column_name].dropna().astype(str).unique().tolist())
                st.session_state[cache_key] = opcoes
                return opcoes
            except Exception:
                st.session_state[cache_key] = ["Todos"]
                return ["Todos"]
        st.session_state[cache_key] = ["Todos"]
        return ["Todos"]
    else:
        return st.session_state[cache_key]

# Cache para aplicar todos os filtros de uma vez (otimização)
@st.cache_data(ttl=300, max_entries=50)
def aplicar_filtros_otimizado(df_base, filtros_dict):
    """Aplica todos os filtros de uma vez para melhor performance"""
    df = df_base.copy()
    
    # Aplicar filtros sequencialmente
    for coluna, valores in filtros_dict.items():
        if coluna in df.columns and valores:
            if isinstance(valores, list):
                if "Todos" not in valores and valores:
                    df = df[df[coluna].astype(str).isin(valores)]
            elif valores != "Todos":
                df = df[df[coluna].astype(str) == str(valores)]
    
    return df

# OTIMIZAÇÃO: Carregar opções de filtros baseadas no df_total (cache mais eficiente)
usina_opcoes = get_filter_options(df_total, 'USI')
periodo_opcoes_total = get_filter_options(df_total, 'Período')
centro_cst_opcoes_total = get_filter_options(df_total, 'Centro cst') if 'Centro cst' in df_total.columns else ["Todos"]
conta_opcoes_total = get_filter_options(df_total, 'Nº conta')[1:] if 'Nº conta' in df_total.columns else []

# Filtro 1: USINA (com cache otimizado e session_state)
# Manter valores válidos do session_state
usina_valor_atual = st.session_state.filtro_usina
# Filtrar apenas valores que ainda existem nas opções
usina_valor_atual = [v for v in usina_valor_atual if v in usina_opcoes]
# Se não há valores válidos, usar padrão
if not usina_valor_atual:
    usina_valor_atual = ["Todos"]

usina_selecionada = st.sidebar.multiselect(
    "Selecione a USINA:", 
    usina_opcoes, 
    default=usina_valor_atual,
    key="filtro_usina_widget"
)
# Atualizar session_state apenas se mudou
if usina_selecionada != st.session_state.filtro_usina:
    st.session_state.filtro_usina = usina_selecionada if usina_selecionada else ["Todos"]

# Filtro 2: Período (usando opções do df_total para melhor performance)
# Manter valor do session_state se ainda estiver disponível
periodo_valor_atual = st.session_state.filtro_periodo
if periodo_valor_atual not in periodo_opcoes_total:
    periodo_valor_atual = "Todos"

periodo_selecionado = st.sidebar.selectbox(
    "Selecione o Período:", 
    periodo_opcoes_total,
    index=periodo_opcoes_total.index(periodo_valor_atual) if periodo_valor_atual in periodo_opcoes_total else 0,
    key="filtro_periodo_widget"
)
# Atualizar session_state apenas se mudou
if periodo_selecionado != st.session_state.filtro_periodo:
    st.session_state.filtro_periodo = periodo_selecionado

# Filtro 3: Centro cst (usando opções do df_total)
if 'Centro cst' in df_total.columns:
    # Manter valor do session_state se ainda estiver disponível
    centro_cst_valor_atual = st.session_state.filtro_centro_cst
    if centro_cst_valor_atual not in centro_cst_opcoes_total:
        centro_cst_valor_atual = "Todos"
    
    centro_cst_selecionado = st.sidebar.selectbox(
        "Selecione o Centro cst:", 
        centro_cst_opcoes_total,
        index=centro_cst_opcoes_total.index(centro_cst_valor_atual) if centro_cst_valor_atual in centro_cst_opcoes_total else 0,
        key="filtro_centro_cst_widget"
    )
    # Atualizar session_state apenas se mudou
    if centro_cst_selecionado != st.session_state.filtro_centro_cst:
        st.session_state.filtro_centro_cst = centro_cst_selecionado

# Filtro 4: Conta contábil (usando opções do df_total)
if 'Nº conta' in df_total.columns:
    # Manter valores válidos do session_state
    conta_valor_atual = st.session_state.filtro_conta_contabil
    conta_valor_atual = [v for v in conta_valor_atual if v in conta_opcoes_total]
    
    conta_contabil_selecionadas = st.sidebar.multiselect(
        "Selecione a Conta contábil:", 
        conta_opcoes_total,
        default=conta_valor_atual,
        key="filtro_conta_contabil_widget"
    )
    # Atualizar session_state apenas se mudou
    if conta_contabil_selecionadas != st.session_state.filtro_conta_contabil:
        st.session_state.filtro_conta_contabil = conta_contabil_selecionadas

# Filtros principais (com cache otimizado e session_state)
filtros_principais = [
    ("Type 05", "Type 05", "multiselect"),
    ("Type 06", "Type 06", "multiselect"), 
    ("Type 07", "Type 07", "multiselect"),
    ("Fornecedor", "Fornecedor", "multiselect"),
    ("Fornec.", "Fornec.", "multiselect"),
    ("Tipo", "Tipo", "multiselect")
]

for col_name, label, widget_type in filtros_principais:
    if col_name in df_total.columns:
        # Usar opções do df_total (cache mais eficiente)
        opcoes = get_filter_options(df_total, col_name)
        if widget_type == "multiselect":
            # Obter valor atual do session_state
            valor_atual = st.session_state.filtros_principais.get(col_name, ["Todos"])
            # Filtrar apenas valores que ainda existem nas opções
            valor_atual = [v for v in valor_atual if v in opcoes]
            if not valor_atual:
                valor_atual = ["Todos"]
            
            selecionadas = st.sidebar.multiselect(
                f"Selecione o {label}:", 
                opcoes, 
                default=valor_atual,
                key=f"filtro_principal_{col_name}"
            )
            # Atualizar session_state apenas se mudou
            if selecionadas != st.session_state.filtros_principais.get(col_name, ["Todos"]):
                st.session_state.filtros_principais[col_name] = selecionadas if selecionadas else ["Todos"]

# Filtros avançados (usando opções do df_total)
with st.sidebar.expander("🔍 Filtros Avançados"):
    filtros_avancados = [
        ("Oficina", "Oficina", "multiselect"),
        ("Usuário", "Usuário", "multiselect"),
        ("Denominação", "Denominação", "multiselect"),
        ("Dt.lçto.", "Data Lançamento", "multiselect")
    ]
    
    for col_name, label, widget_type in filtros_avancados:
        if col_name in df_total.columns:
            # Usar opções do df_total (cache mais eficiente)
            opcoes = get_filter_options(df_total, col_name)
            # Limitar opções para melhor performance
            if len(opcoes) > 101:  # 100 + "Todos"
                opcoes = opcoes[:101]
                st.caption(f"⚠️ {label}: Limitado a 100 opções para performance")
            
            if widget_type == "multiselect":
                # Obter valor atual do session_state
                valor_atual = st.session_state.filtros_avancados.get(col_name, ["Todos"])
                # Filtrar apenas valores que ainda existem nas opções
                valor_atual = [v for v in valor_atual if v in opcoes]
                if not valor_atual:
                    valor_atual = ["Todos"]
                
                selecionadas = st.multiselect(
                    f"Selecione o {label}:", 
                    opcoes, 
                    default=valor_atual,
                    key=f"filtro_avancado_{col_name}"
                )
                # Atualizar session_state apenas se mudou
                if selecionadas != st.session_state.filtros_avancados.get(col_name, ["Todos"]):
                    st.session_state.filtros_avancados[col_name] = selecionadas if selecionadas else ["Todos"]

# OTIMIZAÇÃO: Aplicar todos os filtros de uma vez (mais eficiente) com cache no session_state
# Criar hash dos filtros para cache
filtros_aplicar = {
    'USI': st.session_state.filtro_usina,
    'Período': st.session_state.filtro_periodo,
    'Centro cst': st.session_state.filtro_centro_cst,
    'Nº conta': st.session_state.filtro_conta_contabil
}

# Adicionar filtros principais
for col_name, _, _ in filtros_principais:
    if col_name in df_total.columns:
        valores = st.session_state.filtros_principais.get(col_name, ["Todos"])
        if valores and "Todos" not in valores:
            filtros_aplicar[col_name] = valores

# Adicionar filtros avançados
for col_name, _, _ in filtros_avancados:
    if col_name in df_total.columns:
        valores = st.session_state.filtros_avancados.get(col_name, ["Todos"])
        if valores and "Todos" not in valores:
            filtros_aplicar[col_name] = valores

# Criar hash dos filtros para usar como chave de cache
filtros_hash = hashlib.md5(str(sorted(filtros_aplicar.items())).encode()).hexdigest()
cache_filtros_key = f"df_filtrado_{opcao_selecionada}_{filtros_hash}"

# Usar cache se disponível, senão calcular
if cache_filtros_key not in st.session_state or st.session_state.get('filtros_hash_anterior') != filtros_hash:
    df_filtrado = aplicar_filtros_otimizado(df_total, filtros_aplicar)
    st.session_state[cache_filtros_key] = df_filtrado
    st.session_state.filtros_hash_anterior = filtros_hash
else:
    df_filtrado = st.session_state[cache_filtros_key]

# Resumo (COMPACTO) - com cache
@st.cache_data(ttl=60, max_entries=100)
def calcular_resumo(df):
    """Calcula resumo com cache para melhor performance"""
    return {
        'linhas': df.shape[0],
        'total': df['Valor'].sum() if 'Valor' in df.columns else 0
    }

resumo = calcular_resumo(df_filtrado)
st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Resumo**")
st.sidebar.write(f"**Linhas:** {resumo['linhas']:,}")
st.sidebar.write(f"**Total:** R$ {resumo['total']:,.2f}")

# Status do Sistema (COMPACTO)
if not is_cloud:  # Só mostrar em modo local para economizar espaço
    st.sidebar.markdown("---")
    st.sidebar.markdown("**💾 Sistema**")
    
    try:
        import sys
        df_size_mb = sys.getsizeof(df_filtrado) / (1024 * 1024)
        st.sidebar.write(f"**Memória:** {df_size_mb:.1f}MB")
        
        if st.sidebar.button("🧹 Limpar Cache", help="Limpar cache e recarregar dados atualizados"):
            st.cache_data.clear()
            # CORREÇÃO: Limpar também cache do session_state para forçar recarregamento
            if 'arquivos_status_cache' in st.session_state:
                del st.session_state['arquivos_status_cache']
            # Limpar caches de dados
            keys_to_delete = [k for k in st.session_state.keys() if k.startswith('df_total_') or k.startswith('cache_filtros_')]
            for k in keys_to_delete:
                del st.session_state[k]
            import gc
            gc.collect()
            st.sidebar.success("✅ Cache limpo! Recarregando dados...")
            st.rerun()
    except Exception:
        pass

# Área administrativa (COMPACTO)
if eh_administrador():
    st.sidebar.markdown("---")
    st.sidebar.markdown("**👑 Admin**")

    # OTIMIZAÇÃO: Cachear dados de usuários
    @st.cache_data(ttl=300, max_entries=1)
    def get_usuarios_info():
        usuarios = get_usuarios_cloud()
        return {
            'total': len(usuarios),
            'aprovados': len([u for u in usuarios.values() if u.get('status') == 'aprovado']),
            'pendentes': len([u for u in usuarios.values() if u.get('status') == 'pendente']),
            'detalhes': usuarios
        }
    
    usuarios_info = get_usuarios_info()
    st.sidebar.write(f"**Usuários:** {usuarios_info['total']} ({usuarios_info['aprovados']} ✅, {usuarios_info['pendentes']} ⏳)")
    
    # Botão para expandir detalhes
    if st.sidebar.button("📋 Ver Usuários", key="btn_ver_usuarios"):
        st.sidebar.markdown("**Cadastrados:**")
        for usuario, dados in usuarios_info['detalhes'].items():
            tipo_icon = "👑" if dados.get('tipo') == 'administrador' else "👥"
            status_icon = "✅" if dados.get('status') == 'aprovado' else "⏳"
            st.sidebar.write(f"{tipo_icon} {status_icon} {usuario}")

# Gráfico de barras para a soma dos valores por 'Período'
@st.cache_data(ttl=900, max_entries=2)
def create_period_chart(df_data):
    """Cria gráfico otimizado"""
    try:
        # Filtrar valores nulos e zeros ANTES de agrupar
        df_filtered = df_data[(df_data['Valor'].notna()) & (df_data['Valor'] != 0) & (df_data['Valor'].abs() >= 0.01)].copy()
        
        if df_filtered.empty:
            return None
        
        chart_data = df_filtered.groupby('Período')['Valor'].sum().reset_index()
        # Filtrar novamente após agrupamento para garantir que não há zeros
        chart_data = chart_data[(chart_data['Valor'].notna()) & (chart_data['Valor'] != 0) & (chart_data['Valor'].abs() >= 0.01)]
        
        if chart_data.empty:
            return None
        
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

# OTIMIZAÇÃO: Lazy loading de gráficos - só criar se necessário
# Criar e exibir gráfico (com cache mais agressivo)
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

# OTIMIZAÇÃO: Lazy loading - gráficos só aparecem se expandidos
with st.expander("📊 Categorias", expanded=True):
    # Gráfico por Type 05
    if 'Type 05' in df_filtrado.columns:
        @st.cache_data(ttl=900, max_entries=2)
        def create_type05_chart(df_data):
            try:
                # Filtrar valores nulos e zeros ANTES de agrupar
                df_filtered = df_data[(df_data['Valor'].notna()) & (df_data['Valor'] != 0) & (df_data['Valor'].abs() >= 0.01)].copy()
                
                if df_filtered.empty:
                    return None
                
                type05_data = df_filtered.groupby('Type 05')['Valor'].sum().reset_index()
                # Filtrar novamente após agrupamento
                type05_data = type05_data[(type05_data['Valor'].notna()) & (type05_data['Valor'] != 0) & (type05_data['Valor'].abs() >= 0.01)]
                type05_data = type05_data.sort_values('Valor', ascending=False)
                
                if type05_data.empty:
                    return None
                
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
            # Adicionar rótulos com valores nas barras
            rotulos_type05 = chart_type05.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Ajuste vertical
                color='black',
                fontSize=11
            ).encode(
                text=alt.Text('Valor:Q', format=',.2f')
            )
            
            # Combinar gráfico com rótulos
            grafico_type05_completo = chart_type05 + rotulos_type05
            st.altair_chart(grafico_type05_completo, use_container_width=True)

    # Gráfico por Type 06
    if 'Type 06' in df_filtrado.columns:
        @st.cache_data(ttl=900, max_entries=2)
        def create_type06_chart(df_data):
            try:
                # Filtrar valores nulos e zeros ANTES de agrupar
                df_filtered = df_data[(df_data['Valor'].notna()) & (df_data['Valor'] != 0) & (df_data['Valor'].abs() >= 0.01)].copy()
                
                if df_filtered.empty:
                    return None
                
                type06_data = df_filtered.groupby('Type 06')['Valor'].sum().reset_index()
                # Filtrar novamente após agrupamento
                type06_data = type06_data[(type06_data['Valor'].notna()) & (type06_data['Valor'] != 0) & (type06_data['Valor'].abs() >= 0.01)]
                type06_data = type06_data.sort_values('Valor', ascending=False)
                
                if type06_data.empty:
                    return None
                
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
            # Adicionar rótulos com valores nas barras
            rotulos_type06 = chart_type06.mark_text(
                align='center',
                baseline='middle',
                dy=-10,  # Ajuste vertical
                color='black',
                fontSize=11
            ).encode(
                text=alt.Text('Valor:Q', format=',.2f')
            )
            
            # Combinar gráfico com rótulos
            grafico_type06_completo = chart_type06 + rotulos_type06
            st.altair_chart(grafico_type06_completo, use_container_width=True)

# PRIMEIRO: Gráfico por Texto (segunda posição)
if 'Texto' in df_filtrado.columns and 'Type 07' in df_filtrado.columns:
    st.subheader("📝 Análise por Texto")
    
    # Filtros específicos para o gráfico por Texto (incluindo Type 07 como multiselect)
    col_filtro1_texto, col_filtro2_texto, col_filtro3_texto, col_filtro4_texto, col_filtro5_texto = st.columns(5)
    
    with col_filtro1_texto:
        # Filtro Type 05 para o gráfico
        type05_opcoes_grafico_texto = get_filter_options(df_filtrado, 'Type 05')
        type05_grafico_texto = st.selectbox("Type 05 (Texto):", type05_opcoes_grafico_texto, key="type05_grafico_texto")
    
    with col_filtro2_texto:
        # Filtro Type 06 para o gráfico
        type06_opcoes_grafico_texto = get_filter_options(df_filtrado, 'Type 06')
        type06_grafico_texto = st.selectbox("Type 06 (Texto):", type06_opcoes_grafico_texto, key="type06_grafico_texto")
    
    with col_filtro3_texto:
        # Filtro Type 07 para o gráfico (MULTISELECT - agregador)
        type07_opcoes_grafico_texto = get_filter_options(df_filtrado, 'Type 07')
        # Remover "Todos" para multiselect e usar valores padrão
        type07_opcoes_grafico_texto_sem_todos = [op for op in type07_opcoes_grafico_texto if op != "Todos"]
        type07_grafico_texto = st.multiselect(
            "Type 07 (Texto):", 
            type07_opcoes_grafico_texto_sem_todos, 
            default=[],
            key="type07_grafico_texto_multiselect"
        )
    
    with col_filtro4_texto:
        # Filtro Período para o gráfico
        periodo_opcoes_grafico_texto = get_filter_options(df_filtrado, 'Período')
        periodo_grafico_texto = st.selectbox("Período (Texto):", periodo_opcoes_grafico_texto, key="periodo_grafico_texto")
    
    with col_filtro5_texto:
        # Filtro de quantidade (Top N)
        quantidade_opcoes_texto = [10, 15, 20, 30, 50, 100]
        quantidade_grafico_texto = st.selectbox("Top N (Texto):", quantidade_opcoes_texto, index=0, key="quantidade_grafico_texto")
    
    # Aplicar filtros específicos para o gráfico por Texto
    # IMPORTANTE: Começar do df_filtrado (já filtrado pelos filtros principais) e aplicar filtros específicos do gráfico
    df_grafico_texto = df_filtrado.copy()
    
    # Aplicar filtros específicos do gráfico - APENAS os registros que correspondem EXATAMENTE aos filtros
    filtros_aplicados = []
    
    if type05_grafico_texto != "Todos":
        df_grafico_texto = df_grafico_texto[df_grafico_texto['Type 05'].astype(str) == str(type05_grafico_texto)]
        filtros_aplicados.append(f"Type 05: {type05_grafico_texto}")
    
    if type06_grafico_texto != "Todos":
        df_grafico_texto = df_grafico_texto[df_grafico_texto['Type 06'].astype(str) == str(type06_grafico_texto)]
        filtros_aplicados.append(f"Type 06: {type06_grafico_texto}")
    
    # Filtro Type 07 com múltiplos valores (agregador)
    if type07_grafico_texto:  # Se houver seleções
        df_grafico_texto = df_grafico_texto[df_grafico_texto['Type 07'].astype(str).isin(type07_grafico_texto)]
        filtros_aplicados.append(f"Type 07: {', '.join(type07_grafico_texto)}")
    
    if periodo_grafico_texto != "Todos":
        df_grafico_texto = df_grafico_texto[df_grafico_texto['Período'].astype(str) == str(periodo_grafico_texto)]
        filtros_aplicados.append(f"Período: {periodo_grafico_texto}")
    
    # Filtrar valores nulos e zeros ANTES de agrupar por Texto
    df_grafico_texto = df_grafico_texto[(df_grafico_texto['Valor'].notna()) & (df_grafico_texto['Valor'] != 0) & (df_grafico_texto['Valor'].abs() >= 0.01)].copy()
    
    # Mostrar estatísticas dos filtros aplicados
    type07_filtro_texto = ", ".join(type07_grafico_texto) if type07_grafico_texto else "Todos"
    st.caption(f"📊 Dados filtrados: {len(df_grafico_texto):,} registros | Total: R$ {df_grafico_texto['Valor'].sum():,.2f}")
    if filtros_aplicados:
        st.caption(f"🔍 Filtros aplicados: {' | '.join(filtros_aplicados)}")
    
    # Criar gráfico por Texto com os dados filtrados
    @st.cache_data(ttl=900, max_entries=2)
    def create_texto_chart(df_data, quantidade, type05_filtro, type06_filtro, type07_filtro, periodo_filtro):
        try:
            # df_data já está filtrado pelos filtros específicos do gráfico e sem valores nulos/zeros
            if df_data.empty:
                return None
            
            # Agrupar por Texto - apenas textos que correspondem aos filtros selecionados
            texto_data = df_data.groupby('Texto')['Valor'].sum().reset_index()
            
            # Garantir que não há valores nulos ou zeros após agrupamento
            texto_data = texto_data[(texto_data['Valor'].notna()) & (texto_data['Valor'] != 0) & (texto_data['Valor'].abs() >= 0.01)]
            
            # Ordenar e pegar top N
            texto_data = texto_data.sort_values('Valor', ascending=False).head(quantidade)
            
            if texto_data.empty:
                return None
            
            # Formatar lista de Type 07 para o título
            type07_titulo = ", ".join(type07_filtro) if type07_filtro else "Todos"
            
            chart = alt.Chart(texto_data).mark_bar().encode(
                x=alt.X('Texto:N', title='Texto', sort='-y'),
                y=alt.Y('Valor:Q', title='Soma do Valor'),
                color=alt.Color('Valor:Q', title='Valor', scale=alt.Scale(scheme='redyellowgreen', reverse=True)),
                tooltip=['Texto:N', 'Valor:Q']
            ).properties(
                title=f'Top {quantidade} Texto - Filtrado por Type 05: {type05_filtro}, Type 06: {type06_filtro}, Type 07: {type07_titulo}, Período: {periodo_filtro}',
                height=500
            )
            
            return chart
        except Exception as e:
            st.error(f"Erro no gráfico por Texto: {e}")
            return None
    
    chart_texto = create_texto_chart(
        df_grafico_texto, 
        quantidade_grafico_texto,
        type05_grafico_texto,
        type06_grafico_texto,
        type07_grafico_texto,
        periodo_grafico_texto
    )
    if chart_texto:
        # Adicionar rótulos com valores nas barras
        rotulos_texto = chart_texto.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Ajuste vertical
            color='black',
            fontSize=10
        ).encode(
            text=alt.Text('Valor:Q', format=',.2f')
        )
        
        # Combinar gráfico com rótulos
        grafico_texto_completo = chart_texto + rotulos_texto
        st.altair_chart(grafico_texto_completo, use_container_width=True)

# SEGUNDO: Gráfico Type 07 com filtros específicos (fora do expander)
if 'Type 07' in df_filtrado.columns:
    st.subheader("🏆 Type 07")
    
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
    
    # Aplicar filtros específicos para o gráfico Type 07
    # IMPORTANTE: Começar do df_filtrado (já filtrado pelos filtros principais) e aplicar filtros específicos do gráfico
    df_grafico = df_filtrado.copy()
    
    # Aplicar filtros específicos do gráfico - APENAS os registros que correspondem EXATAMENTE aos filtros
    filtros_aplicados_type07 = []
    
    if type05_grafico != "Todos":
        df_grafico = df_grafico[df_grafico['Type 05'].astype(str) == str(type05_grafico)]
        filtros_aplicados_type07.append(f"Type 05: {type05_grafico}")
    
    if type06_grafico != "Todos":
        df_grafico = df_grafico[df_grafico['Type 06'].astype(str) == str(type06_grafico)]
        filtros_aplicados_type07.append(f"Type 06: {type06_grafico}")
    
    if periodo_grafico != "Todos":
        df_grafico = df_grafico[df_grafico['Período'].astype(str) == str(periodo_grafico)]
        filtros_aplicados_type07.append(f"Período: {periodo_grafico}")
    
    # Filtrar valores nulos e zeros ANTES de agrupar por Type 07
    df_grafico = df_grafico[(df_grafico['Valor'].notna()) & (df_grafico['Valor'] != 0) & (df_grafico['Valor'].abs() >= 0.01)].copy()
    
    # Mostrar estatísticas dos filtros aplicados
    st.caption(f"📊 Dados filtrados: {len(df_grafico):,} registros | Total: R$ {df_grafico['Valor'].sum():,.2f}")
    if filtros_aplicados_type07:
        st.caption(f"🔍 Filtros aplicados: {' | '.join(filtros_aplicados_type07)}")
    
    # Criar gráfico Type 07 com os dados filtrados
    @st.cache_data(ttl=900, max_entries=2)
    def create_type07_chart(df_data, quantidade):
        try:
            # df_data já está filtrado pelos filtros específicos do gráfico e sem valores nulos/zeros
            if df_data.empty:
                return None
            
            # Agrupar por Type 07 - apenas Type 07 que correspondem aos filtros selecionados
            type07_data = df_data.groupby('Type 07')['Valor'].sum().reset_index()
            
            # Garantir que não há valores nulos ou zeros após agrupamento
            type07_data = type07_data[(type07_data['Valor'].notna()) & (type07_data['Valor'] != 0) & (type07_data['Valor'].abs() >= 0.01)]
            
            # Ordenar e pegar top N
            type07_data = type07_data.sort_values('Valor', ascending=False).head(quantidade)
            
            if type07_data.empty:
                return None
            
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
        # Adicionar rótulos com valores nas barras
        rotulos_type07 = chart_type07.mark_text(
            align='center',
            baseline='middle',
            dy=-10,  # Ajuste vertical
            color='black',
            fontSize=10
        ).encode(
            text=alt.Text('Valor:Q', format=',.2f')
        )
        
        # Combinar gráfico com rótulos
        grafico_type07_completo = chart_type07 + rotulos_type07
        st.altair_chart(grafico_type07_completo, use_container_width=True)
        
        # Mostrar tabela com os dados do gráfico (incluindo Type 05, Type 06 e valores por Período)
        if not df_grafico.empty:
            st.subheader(f"📋 Top {quantidade_grafico}")
            
            # Criar tabela pivot com Type 05, Type 06, Type 07 e valores por Período
            type07_detailed = df_grafico.groupby(['Type 05', 'Type 06', 'Type 07', 'Período'])['Valor'].sum().reset_index()
            # Filtrar valores nulos e zeros
            type07_detailed = type07_detailed[(type07_detailed['Valor'].notna()) & (type07_detailed['Valor'] != 0)]
            
            if not type07_detailed.empty:
                # Pivotar para ter Períodos como colunas (sem fill_value para evitar zeros)
                type07_pivot = type07_detailed.pivot_table(
                    index=['Type 05', 'Type 06', 'Type 07'], 
                    columns='Período', 
                    values='Valor', 
                    aggfunc='sum',
                    observed=True  # Suprimir FutureWarning
                ).reset_index()
                
                # CORREÇÃO CRÍTICA: Converter TODAS as colunas de Período (criadas pelo pivot_table)
                # antes de qualquer fillna. O pivot_table pode criar colunas Categorical.
                valor_cols_type07 = [col for col in type07_pivot.columns if col not in ['Type 05', 'Type 06', 'Type 07']]
                
                # Converter TODAS as colunas de valor, tratando Categorical de forma segura
                for col in valor_cols_type07:
                    try:
                        if pd.api.types.is_categorical_dtype(type07_pivot[col]):
                            # Categorical: converter para string primeiro, depois numérico
                            type07_pivot[col] = pd.to_numeric(type07_pivot[col].astype(str), errors='coerce')
                        elif pd.api.types.is_object_dtype(type07_pivot[col]):
                            # Object: tentar converter diretamente
                            type07_pivot[col] = pd.to_numeric(type07_pivot[col], errors='coerce')
                        else:
                            # Já numérico ou outro tipo: converter para garantir
                            type07_pivot[col] = pd.to_numeric(type07_pivot[col], errors='coerce')
                    except Exception as e:
                        # Em caso de erro, tentar conversão via string
                        try:
                            type07_pivot[col] = pd.to_numeric(type07_pivot[col].astype(str), errors='coerce')
                        except:
                            pass  # Se falhar, deixar como está
                
                # GARANTIR: Preencher NaN APENAS em colunas que são realmente numéricas
                # Verificar novamente após conversão para garantir que não há Categorical
                numeric_cols_type07 = []
                for col in type07_pivot.columns:
                    if col not in ['Type 05', 'Type 06', 'Type 07']:
                        if pd.api.types.is_numeric_dtype(type07_pivot[col]) and not pd.api.types.is_categorical_dtype(type07_pivot[col]):
                            numeric_cols_type07.append(col)
                
                if len(numeric_cols_type07) > 0:
                    type07_pivot[numeric_cols_type07] = type07_pivot[numeric_cols_type07].fillna(0)
                
                # Calcular total por linha
                numeric_cols = type07_pivot.select_dtypes(include=['number']).columns
                type07_pivot['Total'] = type07_pivot[numeric_cols].sum(axis=1)
                
                # Filtrar linhas com total diferente de zero
                type07_pivot = type07_pivot[type07_pivot['Total'] != 0]
                
                # Ordenar por total e pegar top N
                type07_pivot = type07_pivot.sort_values('Total', ascending=False).head(quantidade_grafico)
                
                # Formatar valores monetários (apenas valores diferentes de zero, zeros viram string vazia)
                # Converter colunas numéricas para float antes de formatar (evita erro com Categorical)
                for col in numeric_cols:
                    type07_pivot[col] = pd.to_numeric(type07_pivot[col], errors='coerce')
                    type07_pivot[col] = type07_pivot[col].apply(lambda x: f"R$ {x:,.2f}" if pd.notna(x) and x != 0 else "")
                type07_pivot['Total'] = pd.to_numeric(type07_pivot['Total'], errors='coerce')
                type07_pivot['Total'] = type07_pivot['Total'].apply(lambda x: f"R$ {x:,.2f}" if pd.notna(x) and x != 0 else "")
                
                st.dataframe(type07_pivot, use_container_width=True, hide_index=True)

# Tabela dinâmica com cores (modificada para mostrar apenas valores diferentes de zero)
# OTIMIZAÇÃO: Cache da tabela pivot
@st.cache_data(ttl=300, max_entries=50)
def criar_tabela_pivot(df):
    """Cria tabela pivot com cache para melhor performance"""
    try:
        # Filtrar valores nulos e zeros antes de criar pivot
        df_filtered = df[(df['Valor'].notna()) & (df['Valor'] != 0)].copy()
        
        if df_filtered.empty:
            return None, None
        
        df_pivot = df_filtered.pivot_table(
            index='USI', 
            columns='Período', 
            values='Valor', 
            aggfunc='sum', 
            margins=True, 
            margins_name='Total',
            observed=True  # Suprimir FutureWarning
        )
        # CORREÇÃO CRÍTICA: Converter TODAS as colunas de Período (criadas pelo pivot_table)
        # antes de qualquer fillna. O pivot_table pode criar colunas Categorical.
        valor_cols_pivot = [col for col in df_pivot.columns if col != 'Total']
        
        # Converter TODAS as colunas de valor, tratando Categorical de forma segura
        for col in valor_cols_pivot:
            try:
                if pd.api.types.is_categorical_dtype(df_pivot[col]):
                    # Categorical: converter para string primeiro, depois numérico
                    df_pivot[col] = pd.to_numeric(df_pivot[col].astype(str), errors='coerce')
                elif pd.api.types.is_object_dtype(df_pivot[col]):
                    # Object: tentar converter diretamente
                    df_pivot[col] = pd.to_numeric(df_pivot[col], errors='coerce')
                else:
                    # Já numérico ou outro tipo: converter para garantir
                    df_pivot[col] = pd.to_numeric(df_pivot[col], errors='coerce')
            except Exception as e:
                # Em caso de erro, tentar conversão via string
                try:
                    df_pivot[col] = pd.to_numeric(df_pivot[col].astype(str), errors='coerce')
                except:
                    pass  # Se falhar, deixar como está
        
        # GARANTIR: Preencher NaN APENAS em colunas que são realmente numéricas
        # Verificar novamente após conversão para garantir que não há Categorical
        numeric_cols_pivot = []
        for col in df_pivot.columns:
            if col != 'Total':
                if pd.api.types.is_numeric_dtype(df_pivot[col]) and not pd.api.types.is_categorical_dtype(df_pivot[col]):
                    numeric_cols_pivot.append(col)
        
        if len(numeric_cols_pivot) > 0:
            df_pivot[numeric_cols_pivot] = df_pivot[numeric_cols_pivot].fillna(0)
        
        # Filtrar para mostrar apenas linhas e colunas com valores diferentes de zero
        df_pivot_filtered = df_pivot.loc[(df_pivot != 0).any(axis=1)]
        df_pivot_filtered = df_pivot_filtered.loc[:, (df_pivot_filtered != 0).any(axis=0)]
        return df_pivot, df_pivot_filtered
    except Exception as e:
        return None, None

df_pivot, df_pivot_filtered = criar_tabela_pivot(df_filtrado)
st.subheader("USI x Período")

if df_pivot is None or df_pivot_filtered is None:
    st.error("Erro ao criar tabela dinâmica")
    st.stop()

# Aplicar formatação com cores (verde para positivo, vermelho para negativo)
def colorir_valores(val):
    # Aplicar cor apenas em strings que não estão vazias
    if isinstance(val, str) and val != "":
        # Tentar extrair o valor numérico da string formatada
        try:
            valor_num = float(val.replace("R$", "").replace(",", "").strip())
            if valor_num < 0:
                return 'color: #e74c3c; font-weight: bold;'  # Vermelho para negativo
            elif valor_num > 0:
                return 'color: #27ae60; font-weight: bold;'  # Verde para positivo
        except:
            pass
    return ''

# Formatar valores: mostrar apenas valores diferentes de zero
def formatar_valor(val):
    if isinstance(val, (int, float)):
        if pd.isna(val) or val == 0 or abs(val) < 0.01:  # Considerar valores muito pequenos como zero
            return ""
        return f"R$ {val:,.2f}"
    elif isinstance(val, str):
        # Se já for string, verificar se contém zero
        if val == "R$ 0,00" or val == "R$ 0.00" or val == "0" or val == "":
            return ""
    return val

# Aplicar formatação
styled_pivot = df_pivot_filtered.copy()
for col in styled_pivot.columns:
    # Verificar se é coluna numérica (incluindo Categorical que pode ser convertida)
    if pd.api.types.is_numeric_dtype(styled_pivot[col]):
        # Converter para float se for Categorical ou outro tipo numérico
        styled_pivot[col] = pd.to_numeric(styled_pivot[col], errors='coerce')
        styled_pivot[col] = styled_pivot[col].apply(formatar_valor)
    elif styled_pivot[col].dtype == 'object':
        # Verificar se são strings numéricas
        styled_pivot[col] = styled_pivot[col].apply(formatar_valor)
    elif styled_pivot[col].dtype.name == 'category':
        # Converter Categorical para string antes de formatar
        styled_pivot[col] = styled_pivot[col].astype(str)
        styled_pivot[col] = styled_pivot[col].apply(formatar_valor)

# Remover colunas que ficaram completamente vazias após formatação
styled_pivot = styled_pivot.loc[:, (styled_pivot != "").any(axis=0)]
# Remover linhas que ficaram completamente vazias
styled_pivot = styled_pivot.loc[(styled_pivot != "").any(axis=1), :]

styled_pivot = styled_pivot.style.map(colorir_valores, subset=pd.IndexSlice[:, :])
st.dataframe(styled_pivot, use_container_width=True)

# Mostrar estatísticas da filtragem
linhas_originais = len(df_pivot)
linhas_filtradas = len(df_pivot_filtered)
colunas_originais = len(df_pivot.columns)
colunas_filtradas = len(df_pivot_filtered.columns)

st.caption(f"📊 Filtragem aplicada: {linhas_originais} → {linhas_filtradas} linhas, {colunas_originais} → {colunas_filtradas} colunas")

# Botão de download da Tabela Dinâmica (logo abaixo da tabela)
if st.button("📥 Baixar Tabela Dinâmica", use_container_width=True, key="download_pivot"):
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
st.subheader("Dados")
# Filtrar valores nulos e zeros na coluna Valor antes de exibir
if 'Valor' in df_filtrado.columns:
    df_display = df_filtrado[(df_filtrado['Valor'].notna()) & (df_filtrado['Valor'] != 0)].copy()
else:
    df_display = df_filtrado.copy()

display_limit = 500 if is_cloud else 2000
if len(df_display) > display_limit:
    st.info(f"📊 Mostrando {display_limit:,} de {len(df_display):,} registros para otimizar performance")
    df_display = df_display.head(display_limit)

st.dataframe(df_display, use_container_width=True)

# Botão de download da Tabela Filtrada (logo abaixo da tabela)
if st.button("📥 Baixar Tabela Filtrada", use_container_width=True, key="download_filtered"):
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
# OTIMIZAÇÃO: Cache da tabela de soma por types
@st.cache_data(ttl=300, max_entries=50)
def criar_tabela_types_periodo(df):
    """Cria tabela de soma por types com cache para melhor performance"""
    try:
        # Filtrar valores nulos e zeros antes de agrupar
        df_filtered = df[(df['Valor'].notna()) & (df['Valor'] != 0)].copy()
        
        if df_filtered.empty:
            return None
        
        soma_por_type_periodo = df_filtered.groupby(['Type 05', 'Type 06', 'Type 07', 'Período'])['Valor'].sum().reset_index()
        # Filtrar novamente após agrupamento para garantir que não há zeros
        soma_por_type_periodo = soma_por_type_periodo[(soma_por_type_periodo['Valor'].notna()) & (soma_por_type_periodo['Valor'] != 0)]
        
        if soma_por_type_periodo.empty:
            return None
        
        tabela_pivot_raw = soma_por_type_periodo.pivot_table(
            index=['Type 05', 'Type 06', 'Type 07'], 
            columns='Período', 
            values='Valor', 
            aggfunc='sum',
            observed=True  # Suprimir FutureWarning
        ).reset_index()
        
        # CORREÇÃO CRÍTICA: Converter TODAS as colunas de Período (criadas pelo pivot_table)
        # antes de qualquer fillna. O pivot_table pode criar colunas Categorical.
        valor_cols_types = [col for col in tabela_pivot_raw.columns if col not in ['Type 05', 'Type 06', 'Type 07']]
        
        # Converter TODAS as colunas de valor, tratando Categorical de forma segura
        for col in valor_cols_types:
            try:
                if pd.api.types.is_categorical_dtype(tabela_pivot_raw[col]):
                    # Categorical: converter para string primeiro, depois numérico
                    tabela_pivot_raw[col] = pd.to_numeric(tabela_pivot_raw[col].astype(str), errors='coerce')
                elif pd.api.types.is_object_dtype(tabela_pivot_raw[col]):
                    # Object: tentar converter diretamente
                    tabela_pivot_raw[col] = pd.to_numeric(tabela_pivot_raw[col], errors='coerce')
                else:
                    # Já numérico ou outro tipo: converter para garantir
                    tabela_pivot_raw[col] = pd.to_numeric(tabela_pivot_raw[col], errors='coerce')
            except Exception as e:
                # Em caso de erro, tentar conversão via string
                try:
                    tabela_pivot_raw[col] = pd.to_numeric(tabela_pivot_raw[col].astype(str), errors='coerce')
                except:
                    pass  # Se falhar, deixar como está
        
        # GARANTIR: Preencher NaN APENAS em colunas que são realmente numéricas
        # Verificar novamente após conversão para garantir que não há Categorical
        numeric_cols_types = []
        for col in tabela_pivot_raw.columns:
            if col not in ['Type 05', 'Type 06', 'Type 07']:
                if pd.api.types.is_numeric_dtype(tabela_pivot_raw[col]) and not pd.api.types.is_categorical_dtype(tabela_pivot_raw[col]):
                    numeric_cols_types.append(col)
        
        if len(numeric_cols_types) > 0:
            tabela_pivot_raw[numeric_cols_types] = tabela_pivot_raw[numeric_cols_types].fillna(0)
        
        return tabela_pivot_raw
    except Exception as e:
        return None

if all(col in df_filtrado.columns for col in ['Type 05', 'Type 06', 'Type 07', 'Período']):
    st.markdown("---")
    st.subheader("📊 Types")
    
    # Criar tabela pivot com cache
    tabela_pivot_raw = criar_tabela_types_periodo(df_filtrado)
    
    if tabela_pivot_raw is None:
        st.error("Erro ao criar tabela de soma por types")
        st.stop()
    # Cópia para exibição formatada
    tabela_pivot = tabela_pivot_raw.copy()
    
    # Calcular total por linha
    numeric_cols = tabela_pivot.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        tabela_pivot['Total'] = tabela_pivot[numeric_cols].sum(axis=1)
        
        # Filtrar apenas linhas com valores diferentes de zero
        tabela_pivot = tabela_pivot[(tabela_pivot[numeric_cols] != 0).any(axis=1)]
        
        # Filtrar linhas com total diferente de zero
        tabela_pivot = tabela_pivot[tabela_pivot['Total'] != 0]
        
        # Ordenar por total (decrescente)
        tabela_pivot = tabela_pivot.sort_values('Total', ascending=False)
        
        # Formatar valores monetários (apenas valores diferentes de zero, zeros viram string vazia)
        # Converter colunas numéricas para float antes de formatar (evita erro com Categorical)
        for col in numeric_cols:
            tabela_pivot[col] = pd.to_numeric(tabela_pivot[col], errors='coerce')
            tabela_pivot[col] = tabela_pivot[col].apply(lambda x: f"R$ {x:,.2f}" if pd.notna(x) and x != 0 else "")
        tabela_pivot['Total'] = pd.to_numeric(tabela_pivot['Total'], errors='coerce')
        tabela_pivot['Total'] = tabela_pivot['Total'].apply(lambda x: f"R$ {x:,.2f}" if pd.notna(x) and x != 0 else "")
        
        st.dataframe(tabela_pivot, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum período encontrado nos dados filtrados.")
    
    # Botão de download nativo da Tabela de Soma por Types (usa dados não formatados)
    with st.spinner("Gerando arquivo da soma por types..."):
        output_types = BytesIO()
        with pd.ExcelWriter(output_types, engine='openpyxl') as writer:
            tabela_pivot_raw.to_excel(writer, index=False, sheet_name='Soma_por_Types')
        output_types.seek(0)

    if st.button("📥 Baixar Soma por Types", use_container_width=True, key="download_types"):
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
    st.success("💻 Executando localmente com performance máxima")