# %%
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

styled_pivot = df_pivot_filtered.style.format('R$ {:,.2f}').map(colorir_valores, subset=pd.IndexSlice[:, :])
st.dataframe(styled_pivot, use_container_width=True)

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
    st.success("💻 Executando localmente com performance máxima")